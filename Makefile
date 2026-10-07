# ── SENTINEL — Commandes de développement ──────────────
.PHONY: up down logs normal attack mixed consume topics clean

up:              ## Démarre Kafka + Kafka UI
	docker compose up -d
	@echo "Kafka UI → http://localhost:8080"

down:            ## Arrête tout
	docker compose down

logs:            ## Logs du générateur (si lancé via compose)
	docker compose logs -f log-generator

normal:          ## Trafic normal (depuis l'hôte, nécessite kafka-python)
	TOPIC=netflow MODE=normal RATE=20 python ingestion/log-generator/src/generator.py

attack:          ## Attaque continue (type aléatoire)
	TOPIC=netflow MODE=attack RATE=50 python ingestion/log-generator/src/generator.py

attack-scan:     ## Attaque : scan de ports
	TOPIC=netflow MODE=attack ATTACK_TYPE=port_scan RATE=50 python ingestion/log-generator/src/generator.py

attack-brute:    ## Attaque : brute force SSH
	TOPIC=netflow MODE=attack ATTACK_TYPE=brute_force RATE=50 python ingestion/log-generator/src/generator.py

attack-ddos:     ## Attaque : SYN flood
	TOPIC=netflow MODE=attack ATTACK_TYPE=syn_flood RATE=50 python ingestion/log-generator/src/generator.py

mixed:           ## Mode mixte : calme puis attaque toutes les 5 min
	TOPIC=netflow MODE=mixed RATE=20 python ingestion/log-generator/src/generator.py

consume:         ## Console consumer (nécessite un client Kafka local)
	docker exec sentinel-kafka /opt/kafka/bin/kafka-console-consumer.sh \
		--bootstrap-server localhost:9092 --topic netflow --from-beginning

topics:          ## Liste des topics
	docker exec sentinel-kafka /opt/kafka/bin/kafka-topics.sh \
		--bootstrap-server localhost:9092 --list

clean:           ## Reset complet (supprime les volumes)
	docker compose down -v
