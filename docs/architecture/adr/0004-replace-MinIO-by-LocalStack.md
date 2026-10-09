# ADR-0001 : Remplacement de MinIO par LocalStack pour le stockage S3 local

* **Statut :** accepté
* **Date :** 2026-10-23

## Contexte

Dans le cadre de la semaine 3 du projet Sentinel, le pipeline Spark Structured Streaming doit lire les événements depuis Kafka, calculer des features réseau et d'authentification, puis stocker les résultats au format Parquet dans un stockage compatible S3.

Le démarrage de Docker Compose a échoué lors de la récupération de l'image `minio/minio`, avec l'erreur `pull access denied`. Il est donc nécessaire d'envisager une alternative pour poursuivre le développement du pipeline localement.

## Décision

Remplacer MinIO par LocalStack pour fournir un stockage S3 local destiné aux fichiers Parquet générés par Spark.

## Alternatives envisagées

* **Option A — Conserver MinIO :** solution adaptée au stockage objet et disposant d'une console web ; contre : problème de récupération de l'image Docker dans l'environnement actuel.
* **Option B — Utiliser LocalStack :** permet d'émuler l'API S3 localement et de poursuivre les tests ; contre : configuration spécifique de l'endpoint S3 et absence de console web MinIO équivalente par défaut.

## Conséquences

* **Positives :**

  * Poursuite du développement sans dépendre de MinIO.
  * Stockage local des fichiers Parquet via une API compatible S3.
  * Intégration possible avec Spark Structured Streaming et Docker Compose.

* **Négatives / dette :**

  * Configuration spécifique de l'endpoint S3 et des identifiants de test.
  * Installation ou configuration d'AWS CLI pour créer et vérifier le bucket.
  * Tests d'intégration nécessaires pour confirmer l'écriture effective des fichiers Parquet.
  * Réévaluation possible du choix du stockage avant le déploiement final.

## Références

* [Documentation LocalStack — S3](https://docs.localstack.cloud/aws/services/s3/)
* [Documentation Apache Spark — Structured Streaming](https://spark.apache.org/docs/3.5.0/structured-streaming-programming-guide.html)
* [Documentation Apache Spark — Configuration Hadoop AWS](https://hadoop.apache.org/docs/current/hadoop-aws/tools/hadoop-aws/index.html)
* `docker-compose.yml`
* `streaming/spark-jobs/src/streaming_kafka.py`
* `scripts/create-bucket.ps1`
* `docs/WEEK3.md`
