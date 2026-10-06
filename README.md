# 🛡️ SENTINEL

**Plateforme de détection et d'investigation de cyberattaques en temps réel, assistée par agents IA.**

Projet personnel de fin d'études - Data Engineering (big data, MLOps, IA agentique, cloud, cybersécurité).

## Le concept en 30 secondes

Un pipeline temps réel ingère du trafic réseau simulé (Kafka + Spark Structured Streaming), détecte les anomalies par machine learning, surveille et réentraîne ses modèles de façon industrialisée (MLflow, Airflow, Evidently), puis délègue l'investigation des alertes à des **agents IA** qui produisent des rapports d'analyse avant validation humaine.

```
Trafic simulé → Kafka → Spark Streaming → Détection ML → Alertes groupées
                                                              ↓
Dashboard ← Validation humaine ← Rapport ← Agents IA (LangGraph)
```

## Quickstart

```bash
docker compose up -d     # démarre Kafka + UI + générateur
make normal              # trafic normal
make attack              # lance une attaque simulée (2e terminal)
make consume             # voir les événements (3e terminal)
```

Interface Kafka : http://localhost:8080

## Stack

`Kafka` · `Spark Structured Streaming` · `Delta Lake / MinIO` · `Isolation Forest / XGBoost` · `MLflow` · `Airflow` · `Evidently` · `LangGraph` · `Grafana` · `Kubernetes` · `Terraform` · `GitHub Actions`

## Structure du repo

| Dossier | Rôle |
|---------|------|
| `ingestion/` | Générateur de logs réseau + mode attaque |
| `streaming/` | Jobs Spark Structured Streaming |
| `alerting/` | Groupement d'alertes + rate limiting |
| `ml/` | Entraînement, inférence, monitoring de drift |
| `agents/` | Agents IA (enquêteur, enrichisseur, rapporteur) |
| `serving/` | Dashboard + API de validation humaine |
| `orchestration/` | DAGs Airflow |
| `infra/` | Terraform, Helm, Dockerfiles |
| `docs/` | Cahier des charges, ADR, journal, datasets |

## Roadmap

- [x] Phase 1 — Fondations (Kafka, Spark, stockage, détection v1)
- [ ] Phase 2 — ML & MLOps (MLflow, Airflow, drift monitoring)
- [ ] Phase 3 — Agents IA (investigation automatisée)
- [ ] Phase 4 — Industrialisation (K8s, Terraform, sécurisation)

## Documentation

- 📋 [Cahier des charges](docs/cahier-des-charges.md)
- 🗂️ [Décisions d'architecture (ADR)](docs/architecture/adr/)
- 📓 [Journal de bord hebdomadaire](docs/journal.md)
- 📊 [Notes sur les jeux de données](docs/datasets.md)


---

<div align="center">

Fait avec ❤️ par Tristan Mathon - SENTINEL

</div>
