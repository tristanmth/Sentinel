# make.ps1 — Équivalent PowerShell du Makefile SENTINEL
# Usage : .\make.ps1 <cible>
#         .\make.ps1           → affiche l'aide

param([string]$target = "help")

function Show-Help {
    Write-Host @"
SENTINEL — Commandes disponibles
─────────────────────────────────
  up            Démarre Kafka + Kafka UI
  down          Arrête tout
  logs          Logs du générateur (si lancé via compose)
  normal        Trafic normal (20 év/s)
  attack        Attaque continue (type aléatoire, 50 év/s)
  attack-scan   Attaque : scan de ports
  attack-brute  Attaque : brute force SSH
  attack-ddos   Attaque : SYN flood
  mixed         Mode mixte : calme puis attaque toutes les 5 min
  consume       Console consumer Kafka
  topics        Liste les topics
  clean         Reset complet (supprime les volumes)
─────────────────────────────────
Exemple : .\make.ps1 up
"@
}

function Run-Generator([string]$mode, [string]$attackType = "", [int]$rate = 20) {
    $env:TOPIC = "netflow"
    $env:MODE = $mode
    $env:RATE = "$rate"
    if ($attackType) { $env:ATTACK_TYPE = $attackType } else { Remove-Item Env:ATTACK_TYPE -ErrorAction SilentlyContinue }
    python ingestion/log-generator/src/generator.py
}

switch ($target) {
    "help"        { Show-Help }
    "up"          { docker compose up -d; Write-Host "Kafka UI → http://localhost:8080" }
    "down"        { docker compose down }
    "logs"        { docker compose logs -f log-generator }
    "normal"      { Run-Generator "normal" "" 20 }
    "attack"      { Run-Generator "attack" "" 50 }
    "attack-scan" { Run-Generator "attack" "port_scan" 50 }
    "attack-brute"{ Run-Generator "attack" "brute_force" 50 }
    "attack-ddos" { Run-Generator "attack" "syn_flood" 50 }
    "mixed"       { Run-Generator "mixed" "" 20 }
    "consume"     { docker exec sentinel-kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic netflow --from-beginning }
    "topics"      { docker exec sentinel-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list }
    "clean"       { docker compose down -v }
    default       { Write-Host "Cible inconnue : $target"; Show-Help }
}
