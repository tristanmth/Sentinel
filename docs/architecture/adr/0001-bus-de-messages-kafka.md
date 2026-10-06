# ADR-0001 : Kafka comme bus de messages temps réel

- **Statut :** accepté
- **Date :** 2026-10-06

## Contexte
La plateforme doit ingérer un flux continu d'événements réseau et les distribuer à plusieurs consommateurs (Spark, alertes, journalisation) avec durabilité et reprise sur incident. Les alertes doivent survivre à une indisponibilité temporaire des agents LLM (coûteux et non critiques).

## Décision
Utiliser **Apache Kafka** (mode KRaft, 1 broker en dev) comme backbone d'événements. Topics : `netflow`, `alerts-raw`, `alerts-prioritized`, `responses`.

## Alternatives envisagées
- **Redpanda** — même API, plus léger (pas de JVM). Non retenu pour l'instant afin d'apprendre l'outil standard de l'industrie ; reste un fallback documenté si les ressources locales posent problème.
- **RabbitMQ** — excellent pour les files de tâches, mais modèle push et rétention limitée : inadapté au replay de flux et à la reprise après incident.

## Conséquences
- Positives : durabilité, reprise, découverte progressive des volumes (partitions), écosystème mature (Connect, Schema Registry possibles plus tard).
- Négatives : empreinte mémoire/JVM en local → mitigé par 1 broker et ressources limitées dans docker-compose.
