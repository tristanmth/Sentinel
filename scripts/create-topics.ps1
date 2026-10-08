# create-topics.ps1 — Crée les topics Kafka nécessaires à SENTINEL
# Usage : .\scripts\create-topics.ps1

Write-Host "Création des topics SENTINEL..."

# Topic principal : trafic réseau
& docker exec sentinel-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic netflow --partitions 3 --replication-factor 1 --if-not-exists

# Topic authentification : logs SSH, FTP, login
& docker exec sentinel-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic auth --partitions 3 --replication-factor 1 --if-not-exists

# Topic alertes brutes : sortie du détecteur ML (S4)
& docker exec sentinel-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic alerts-raw --partitions 3 --replication-factor 1 --if-not-exists

Write-Host "`nTopics créés. Vérification :"
& docker exec sentinel-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
