#!/bin/bash
# create-topics.sh — Crée les topics Kafka nécessaires à SENTINEL

set -e

KAFKA="docker exec sentinel-kafka /opt/kafka/bin"

echo "Creation des topics SENTINEL..."

$KAFKA/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic netflow --partitions 3 --replication-factor 1 --if-not-exists
$KAFKA/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic auth --partitions 3 --replication-factor 1 --if-not-exists
$KAFKA/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic alerts-raw --partitions 3 --replication-factor 1 --if-not-exists

echo -e "\nTopics crees. Verification :"
$KAFKA/kafka-topics.sh --bootstrap-server localhost:9092 --list
