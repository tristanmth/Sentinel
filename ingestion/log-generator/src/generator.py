#!/usr/bin/env python3
"""Générateur de trafic réseau simulé (NetFlow-like) pour SENTINEL — v2.

Nouveautés v2 :
  - Topic `auth` pour les événements d'authentification (SSH, FTP, login)
  - Attaque brute_force = trafic réseau (netflow) + échecs d'auth (auth) en parallèle
  - Séparation propre : réseau → netflow, auth → auth

Modes :
  normal  — trafic de fond réaliste
  attack  — attaque continue (type configurable ou aléatoire)
  mixed   — calme puis attaque toutes les 5 min

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
TOPIC_NETFLOW = os.getenv("TOPIC_NETFLOW", "netflow")
TOPIC_AUTH = os.getenv("TOPIC_AUTH", "auth")
MODE = os.getenv("MODE", "normal")           # normal | attack | mixed
ATTACK_TYPE = os.getenv("ATTACK_TYPE", "")   # port_scan | brute_force | syn_flood | (vide = aléatoire)
RATE = int(os.getenv("RATE", "20"))          # événements/sec en mode normal

INTERNAL_NET = "10.0.1."
EXTERNAL_IPS = [
    "185.220.101.4", "45.148.10.88", "91.240.118.172", "103.75.201.4",
    "198.51.100.23", "203.0.113.77", "192.0.2.44", "45.155.205.34",
]
COMMON_PORTS = [80, 443, 53, 22, 25, 110, 143, 993, 995, 8080, 8443]
ATTACKERS = ["185.220.101.4", "45.148.10.88", "103.75.201.4"]

running = True

def handle_sigterm(signum, frame):
    global running
    running = False

signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)


# ── Producteurs d'événements réseau (topic: netflow) ──

def make_normal_netflow():
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
        "protocol": random.choice(["TCP", "UDP", "TCP", "TCP"]),
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
        "dst_port": random.randint(1, 1024),
        "protocol": "TCP",
        "bytes": random.randint(40, 80),
        "packets": 1,
        "duration_ms": random.randint(0, 5),
        "flags": "SYN",
        "label": "port_scan",
    }


def make_brute_force_netflow(attacker_ip):
    """Brute force SSH : tentatives répétées sur le port 22."""
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "src_ip": attacker_ip,
        "dst_ip": INTERNAL_NET + "22",
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


# ── Producteurs d'événements auth (topic: auth) ──

def make_normal_auth():
    """Authentification réussie ou échec isolé (bruit de fond)."""
    users = ["admin", "root", "ubuntu", "deploy", "backup"]
    src_internal = random.random() < 0.8
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "src_ip": INTERNAL_NET + str(random.randint(2, 254)) if src_internal else random.choice(EXTERNAL_IPS),
        "dst_ip": INTERNAL_NET + "22",
        "service": "ssh",
        "user": random.choice(users),
        "status": "success" if random.random() < 0.9 else "failed",
        "label": "normal",
    }


def make_brute_force_auth(attacker_ip):
    """Brute force SSH : rafale d'échecs d'authentification."""
    users = ["root", "admin", "ubuntu", "test", "user", "oracle", "postgres"]
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "src_ip": attacker_ip,
        "dst_ip": INTERNAL_NET + "22",
        "service": "ssh",
        "user": random.choice(users),
        "status": "failed",
        "label": "brute_force",
    }


# ── Registres d'attaques ──────────────────────

NETFLOW_ATTACKS = {
    "port_scan": make_port_scan,
    "brute_force": make_brute_force_netflow,
    "syn_flood": make_syn_flood,
}

AUTH_ATTACKS = {
    "brute_force": make_brute_force_auth,
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
        print(f"[generator] Connecté à Kafka ({KAFKA_BOOTSTRAP})", flush=True)
        return producer
    except Exception as e:
        print(f"[generator] Kafka indisponible ({e}) → fallback stdout", flush=True)
        return None


def emit(producer, topic, event):
    """Envoie un événement vers un topic spécifique."""
    if producer:
        producer.send(topic, value=event)
    else:
        print(f"[{topic}] {json.dumps(event)}", flush=True)


def run():
    producer = get_kafka_producer()
    print(f"[generator] Mode={MODE} rate={RATE}/s attack_type='{ATTACK_TYPE}'", flush=True)
    print(f"[generator] Topics: {TOPIC_NETFLOW}, {TOPIC_AUTH}", flush=True)

    attack_active = False
    attack_end = 0.0
    next_mixed_attack = time.time() + random.randint(120, 300)

    while running:
        now = time.time()

        # ── Mode mixed : déclenchement périodique d'une attaque de 60 s
        if MODE == "mixed":
            if not attack_active and now >= next_mixed_attack:
                attack_active = True
                attack_end = now + 60
                chosen = ATTACK_TYPE or random.choice(list(NETFLOW_ATTACKS))
                print(f"[generator] ⚠️  ATTAQUE '{chosen}' déclenchée (60 s)", flush=True)
            if attack_active and now >= attack_end:
                attack_active = False
                next_mixed_attack = now + random.randint(240, 360)
                print(f"[generator] ✅ Trafic revenu à la normale", flush=True)

        # ── Mode attack : attaque en continu
        if MODE == "attack":
            attack_active = True

        # ── Émission
        if attack_active:
            chosen = ATTACK_TYPE or random.choice(list(NETFLOW_ATTACKS))
            attacker = random.choice(ATTACKERS)

            # 1. Événements réseau (netflow)
            netflow_fn = NETFLOW_ATTACKS[chosen]
            for _ in range(RATE * 3):
                emit(producer, TOPIC_NETFLOW, netflow_fn(attacker))
                time.sleep(0.2 / RATE)

            # 2. Événements auth (si l'attaque en produit)
            if chosen in AUTH_ATTACKS:
                auth_fn = AUTH_ATTACKS[chosen]
                for _ in range(RATE * 2):  # auth plus dense pendant brute force
                    emit(producer, TOPIC_AUTH, auth_fn(attacker))
                    time.sleep(0.3 / RATE)
        else:
            # Trafic normal : netflow + auth de fond
            for _ in range(RATE):
                emit(producer, TOPIC_NETFLOW, make_normal_netflow())
                time.sleep(0.8 / RATE)
            for _ in range(RATE // 5):  # auth moins fréquent
                emit(producer, TOPIC_AUTH, make_normal_auth())
                time.sleep(4 / RATE)

    if producer:
        producer.flush()
        producer.close()
    print("[generator] Arrêt propre.", flush=True)


if __name__ == "__main__":
    run()
