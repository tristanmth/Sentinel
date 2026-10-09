# make.ps1 — Équivalent PowerShell du Makefile SENTINEL
# Usage : .\make.ps1 <cible>
#         .\make.ps1           → affiche l'aide

param([string]$target = "help")

function Show-Help {
    Write-Host @"
SENTINEL — Commandes disponibles
─────────────────────────────────
  up               Démarre Kafka + Kafka UI + LocalStack + Spark
  down             Arrête tout
  logs             Logs du générateur
  normal           Trafic normal (20 év/s)
  attack           Attaque continue (type aléatoire, 50 év/s)
  attack-scan      Attaque : scan de ports
  attack-brute     Attaque : brute force SSH
  attack-ddos      Attaque : SYN flood
  mixed            Mode mixte : calme puis attaque toutes les 5 min
  consume          Console consumer (netflow par défaut)
  consume-netflow  Console consumer topic netflow
  consume-auth     Console consumer topic auth
  topics           Liste les topics
  create-bucket    Crée le bucket S3 'sentinel-data' dans LocalStack
  spark-submit     Lance le job Spark Structured Streaming
  spark-logs       Logs du master Spark
  s3-ls            Liste les fichiers S3
  clean            Reset complet (supprime les volumes)
─────────────────────────────────
Exemple : .\make.ps1 up
"@
}

function Run-Generator([string]$mode, [string]$attackType = "", [int]$rate = 20) {
    $env:TOPIC_NETFLOW = "netflow"
    $env:TOPIC_AUTH = "auth"
    $env:MODE = $mode
    $env:RATE = "$rate"
    if ($attackType) { $env:ATTACK_TYPE = $attackType } else { Remove-Item Env:ATTACK_TYPE -ErrorAction SilentlyContinue }
    python ingestion/log-generator/src/generator.py
}

function Consume-Topic([string]$topic) {
    docker exec sentinel-kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic $topic --from-beginning
}

function Submit-Spark {
    Write-Host "Lancement du job Spark..."
    docker exec sentinel-spark-master /opt/spark/bin/spark-submit `
        --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 `
        --master spark://spark-master:7077 `
        /app/src/streaming_kafka.py
}

function S3-Ls {
    Write-Host "Liste des buckets S3 :"
    aws s3 ls --endpoint-url=http://localhost:4566 --region us-east-1 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "aws cli non configuré. Installation : pip install awscli"
    }
}

switch ($target) {
    "help"           { Show-Help }
    "up"             { docker compose up -d; Write-Host "Kafka UI → http://localhost:8080"; Write-Host "Spark Master → http://localhost:8081"; Write-Host "LocalStack S3 → http://localhost:4566" }
    "down"           { docker compose down }
    "logs"           { docker compose logs -f log-generator }
    "normal"         { Run-Generator "normal" "" 20 }
    "attack"         { Run-Generator "attack" "" 50 }
    "attack-scan"    { Run-Generator "attack" "port_scan" 50 }
    "attack-brute"   { Run-Generator "attack" "brute_force" 50 }
    "attack-ddos"    { Run-Generator "attack" "syn_flood" 50 }
    "mixed"          { Run-Generator "mixed" "" 20 }
    "consume"        { Consume-Topic "netflow" }
    "consume-netflow"{ Consume-Topic "netflow" }
    "consume-auth"   { Consume-Topic "auth" }
    "topics"         { docker exec sentinel-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list }
    "create-bucket"  { .\scripts\create-bucket.ps1 }
    "spark-submit"   { Submit-Spark }
    "spark-logs"     { docker logs -f sentinel-spark-master }
    "s3-ls"          { S3-Ls }
    "clean"          { docker compose down -v }
    default          { Write-Host "Cible inconnue : $target"; Show-Help }
}
