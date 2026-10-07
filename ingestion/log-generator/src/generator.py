#!/usr/bin/env python3
"""Générateur de trafic réseau simulé (NetFlow-like) pour SENTINEL.

Modes :
  normal  — trafic de fond réaliste
  attack  — attaque continue (type configurable ou aléatoire)
  mixed   — calme puis attaque toutes les 5 min (idéal pour tester la détection)

Chaque événement porte un champ `label` = vérité terrain pour l'évaluation ML.
Fallback stdout si Kafka n'est pas joignable.
"""

import json
import os
import random
import signal
import sys
import time
from datetime import datetime, timezone

# ── Configuration ─────────────────────────────
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("TOPIC", "netflow")
MODE = os.getenv("MODE", "normal")           # normal | attack | mixed
ATTACK_TYPE = os.getenv("ATTACK_TYPE", "")   # port_scan | brute_force | syn_flood | (vide = aléatoire)
RATE = int(os.getenv("RATE", "20"))          # événements/sec en mode normal

INTERNAL_NET = "10.0.1."
EXTERNAL_IPS = [
    "185.220.101.4", "45.148.10.88", "91.240.118.172", "103.75.201.4",
    "198.51.100.23", "203.0.113.77", "192.0.2.44", "45.155.205.34",
]
COMMON_PORTS = [80, 443, 53, 22, 25, 110, 143, 993, 995, 8080, 8443]

ATTACKERS = ["185.220.101.4", "45.148.10.88", "103.75.201.4"]  # IPs "malveillantes" connues

running = True

def handle_sigterm(signum, frame):
    global running
    running = False

signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)


# ── Producteurs d'événements ──────────────────

def make_normal_event():
    """Trafic de fond : communications internes <-> externes plausibles."""
    src_internal = random.random() < 0.7
    if src_internal:
        src_ip = INTERNAL_NET + str(random.randint(2, 254))
        dst_ip = random.choice(EXTERNAL_IPS)
    else:
        src_ip = random.choice(EXTERNAL_IPS)
        dst_ip = INTERNAL_NET + str(random.randint(2, 254))
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": random.randint(1024, 65535),
        "dst_port": random.choice(COMMON_PORTS),
        "protocol": random.choice(["TCP", "UDP", "TCP", "TCP"]),  # TCP dominant
        "bytes": random.randint(60, 1500),
        "packets": random.randint(1, 20),
        "duration_ms": random.randint(1, 5000),
        "flags": random.choice(["SYN", "ACK", "SYN,ACK", "FIN,ACK", "PSH,ACK"]),
        "label": "normal",
    }


def make_port_scan(attacker_ip):
    """Scan de ports : une IP externe balaie rapidement les ports d'une cible."""
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "src_ip": attacker_ip,
        "dst_ip": INTERNAL_NET + str(random.randint(2, 254)),
        "src_port": random.randint(1024, 65535),
        "dst_port": random.randint(1, 1024),          # ports bas = signature de scan
        "protocol": "TCP",
        "bytes": random.randint(40, 80),               # paquets SYN nus
        "packets": 1,
        "duration_ms": random.randint(0, 5),
        "flags": "SYN",
        "label": "port_scan",
    }


def make_brute_force(attacker_ip):
    """Brute force SSH : tentatives répétées sur le port 22 d'une cible fixe."""
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "src_ip": attacker_ip,
        "dst_ip": INTERNAL_NET + "22",                 # serveur SSH fixe
        "src_port": random.randint(1024, 65535),
        "dst_port": 22,
        "protocol": "TCP",
        "bytes": random.randint(60, 200),
        "packets": random.randint(1, 3),
        "duration_ms": random.randint(10, 200),
        "flags": random.choice(["SYN", "RST", "ACK"]),
        "label": "brute_force",
    }


def make_syn_flood(attacker_ip):
    """SYN flood : volume massif de SYN vers une cible, sans réponse."""
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "src_ip": attacker_ip,
        "dst_ip": INTERNAL_NET + str(random.randint(2, 254)),
        "src_port": random.randint(1024, 65535),
        "dst_port": random.choice([80, 443]),
        "protocol": "TCP",
        "bytes": 60,
        "packets": 1,
        "duration_ms": 0,
        "flags": "SYN",
        "label": "syn_flood",
    }


ATTACK_GENERATORS = {
    "port_scan": make_port_scan,
    "brute_force": make_brute_force,
    "syn_flood": make_syn_flood,
}


# ── Moteur principal ──────────────────────────

def get_kafka_producer():
    """Retourne un producteur Kafka, ou None si indisponible (fallback stdout)."""
    try:
        from kafka import KafkaProducer
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            acks="all",
            retries=3,
        )
        print(f"[generator] Connecté à Kafka ({KAFKA_BOOTSTRAP}), topic '{TOPIC}'", flush=True)
        return producer
    except Exception as e:
        print(f"[generator] Kafka indisponible ({e}) → fallback stdout", flush=True)
        return None


def emit(producer, event):
    if producer:
        producer.send(TOPIC, value=event)
    else:
        print(json.dumps(event), flush=True)


def run():
    producer = get_kafka_producer()
    print(f"[generator] Mode={MODE} rate={RATE}/s attack_type='{ATTACK_TYPE}'", flush=True)

    attack_active = False
    attack_end = 0.0
    next_mixed_attack = time.time() + random.randint(120, 300)  # première attaque dans 2-5 min

    while running:
        now = time.time()

        # ── Mode mixed : déclenchement périodique d'une attaque de 60 s
        if MODE == "mixed":
            if not attack_active and now >= next_mixed_attack:
                attack_active = True
                attack_end = now + 60
                chosen = ATTACK_TYPE or random.choice(list(ATTACK_GENERATORS))
                print(f"[generator] ⚠️  ATTAQUE '{chosen}' déclenchée (60 s)", flush=True)
            if attack_active and now >= attack_end:
                attack_active = False
                next_mixed_attack = now + random.randint(240, 360)  # prochaine dans 4-6 min
                print(f"[generator] ✅ Trafic revenu à la normale", flush=True)

        # ── Mode attack : attaque en continu
        if MODE == "attack":
            attack_active = True

        # ── Émission
        if attack_active:
            gen_fn = ATTACK_GENERATORS.get(
                ATTACK_TYPE, random.choice(list(ATTACK_GENERATORS.values()))
            ) if ATTACK_TYPE else random.choice(list(ATTACK_GENERATORS.values()))
            attacker = random.choice(ATTACKERS)
            for _ in range(RATE * 5):       # rafale : 5x le débit normal
                emit(producer, gen_fn(attacker))
                time.sleep(0.2 / RATE)
        else:
            for _ in range(RATE):
                emit(producer, make_normal_event())
                time.sleep(1.0 / RATE)

    if producer:
        producer.flush()
        producer.close()
    print("[generator] Arrêt propre.", flush=True)


if __name__ == "__main__":
    run()
