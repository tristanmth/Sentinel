# Semaine 3 — Spark Structured Streaming (19 → 23 octobre 2026)

## Objectif
Job Spark lit Kafka en temps réel, calcule des features par fenêtre glissante (5 min), écrit en Parquet sur S3 (LocalStack).

## ⚠️ Changement important : MinIO → LocalStack

L'image `minio/minio` nécessite désormais un login Docker. **Remplacée par LocalStack** (S3 compatible, sans login).

## Architecture S3

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐     ┌─────────────┐
│  Générateur │────▶│    Kafka     │────▶│  Spark Streaming │────▶│ LocalStack  │
│  (Python)   │     │ netflow/auth │     │  Features 5min  │     │  S3 Parquet │
└─────────────┘     └──────────────┘     └─────────────────┘     └─────────────┘
                                                │
                                                ▼
                                        ┌──────────────┐
                                        │   Console    │
                                        │   (debug)    │
                                        └──────────────┘
```

## Setup

```powershell
# 1. Démarrer tous les services
.\make.ps1 up

# 2. Vérifier (5 conteneurs)
docker ps
# sentinel-kafka, sentinel-kafka-ui, sentinel-localstack, sentinel-spark-master, sentinel-spark-worker

# 3. Créer le bucket S3
.\make.ps1 create-bucket
# Si aws cli manquant : pip install awscli

# 4. Générateur (terminal 1)
.\make.ps1 mixed

# 5. Spark (terminal 2)
.\make.ps1 spark-submit

# 6. Voir les features
.\make.ps1 spark-logs
```

## Features calculées

### Topic `netflow` (par IP source, fenêtre 5 min)

| Feature | Description | Détection |
|---------|-------------|-----------|
| `conn_count` | Nombre de connexions | Volume anormal |
| `unique_dst_ips` | IPs destination distinctes | Scan horizontal |
| `unique_dst_ports` | Ports destination distincts | Scan vertical |
| `total_bytes` | Volume total | Exfiltration / DDoS |
| `avg_duration_ms` | Durée moyenne | SYN flood = très courte |
| `syn_ratio` | Proportion flags SYN | Scan / flood |
| `port_diversity` | Diversité ports / connexions | Scan = haute diversité |

### Topic `auth` (par IP source, fenêtre 5 min)

| Feature | Description | Détection |
|---------|-------------|-----------|
| `auth_attempts` | Tentatives auth | Volume anormal |
| `failed_attempts` | Échecs auth | Brute force |
| `unique_users` | Utilisateurs distincts | Password spraying |

## Definition of Done

- [ ] `docker-compose.yml` mis à jour (LocalStack + Spark)
- [ ] `.\make.ps1 up` démarre 5 conteneurs sans erreur
- [ ] Bucket `sentinel-data` créé (`.\make.ps1 create-bucket`)
- [ ] `.\make.ps1 spark-submit` tourne sans erreur
- [ ] Logs Spark montrent des features
- [ ] Fichiers Parquet visibles (`.\make.ps1 s3-ls`)
- [ ] Journal S3 rempli

## Exemple sortie Spark

```
| src_ip       | conn_count | unique_dst_ports | syn_ratio | avg_duration_ms |
|--------------|------------|------------------|-----------|-----------------|
| 185.220.101.4| 847        | 847              | 1.0       | 2.3             |  ← PORT SCAN !
| 10.0.1.42    | 23         | 4                | 0.12      | 1200.5          |  ← normal
```

## Pièges connus

| Symptôme | Cause | Fix |
|----------|-------|-----|
| `pull access denied for minio/minio` | MinIO nécessite login | **Utilise LocalStack** (ce fix) |
| `aws cli not found` | AWS CLI pas installé | `pip install awscli` |
| `Connection refused: localstack:4566` | LocalStack pas prêt | Attendre 5 s, relancer |
| `Bucket does not exist` | Bucket non créé | `.\make.ps1 create-bucket` |
| Pas de données | Générateur pas lancé | `.\make.ps1 mixed` |

