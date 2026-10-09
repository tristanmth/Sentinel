#!/bin/bash
# submit.sh — Lance le job Spark Structured Streaming
# Usage : ./submit.sh [local|cluster]

MODE=${1:-local}

if [ "$MODE" = "local" ]; then
    echo "Lancement en mode local..."
    spark-submit \
        --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
        --master local[*] \
        src/streaming_kafka.py
else
    echo "Lancement sur cluster Spark..."
    spark-submit \
        --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
        --master spark://spark-master:7077 \
        --deploy-mode cluster \
        src/streaming_kafka.py
fi
