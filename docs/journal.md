# Journal de bord - SENTINEL

> Rituels : mise à jour chaque vendredi. 5 lignes :
> **fait / bloqué / appris / décision / priorité suivante**
> Ce journal servira de matière première pour le mémoire (chapitres réalisation & bilan).

---

## Semaine 1 - 05 → 09 octobre 2026

**Objectif de la semaine :** repo structuré, générateur de logs v1, Kafka opérationnel.

- ✅ Fait : Kafka 4.0.1 (KRaft) + UI opérationnels. Générateur de trafic avec 3 modes (normal/attack/mixed) et 3 attaques (port_scan, brute_force, syn_flood). Champ `label` = vérité terrain. Commandes PowerShell (`make.ps1`). CI GitHub Actions (lint, test, build). Docs : cahier des charges, 3 ADR, guide datasets.
- 🚧 Bloqué : `make` non reconnu sous Windows → résolu avec `make.ps1`.
- 🧠 Appris : Kafka KRaft (sans Zookeeper), format NetFlow-like JSON, importance du champ `label` pour l'évaluation ML.
- ⚖️ Décision : Kafka (durabilité), Isolation Forest non supervisé (évite domain shift), GitHub Actions (repo public).
- ➡️ Priorité S2 : topics structurés (`auth`, `alerts-raw`), premier consumer Spark, tests unitaires.
- 📸 Preuve : capture Kafka UI + console consumer (voir `docs/WEEK1_RECAP.md`).

---

## Semaine 2 - 12 → 16 octobre 2026

- ✅ Fait : Topics Kafka structurés créés (netflow, auth, alerts-raw) via scripts/create-topics.ps1. Générateur v2 opérationnel : émet vers netflow (trafic réseau) ET auth (événements SSH/login) selon le type d'événement. Attaque brute_force visible dans les deux topics simultanément. make.ps1 enrichi (consume-netflow, consume-auth).
- 🚧 Bloqué / retard : Aucun bloquage. Légère avance sur le planning (topics créés en début de semaine).
- 🧠 Appris : Séparation des responsabilités entre topics (netflow = réseau, auth = authentification). Pattern producteur multi-topics. Rôle de chaque source de données : générateur pour la baseline non supervisée, CIC-IDS2017 pour la classification supervisée en S5.
- ⚖️ Décision prise : Garder le générateur maison comme source principale jusqu'à S4. CIC-IDS2017 réservé à l'entraînement supervisé (S5).
- ➡️ Priorité S3 :Premier consumer Spark Structured Streaming : lecture Kafka, fenêtres glissantes (5 min / 1 h), agrégations par IP (nb connexions, bytes, ratio SYN, entropie ports). Stockage Parquet sur MinIO.
- 📸 Preuve (capture, lien commit) :

---

## Semaine 3 - 19 → 23 octobre 2026

- ✅ Fait :Préparation du pipeline Spark Structured Streaming : lecture des événements Kafka (netflow et auth), calcul de 7 features réseau et 3 features d'authentification, puis écriture prévue au format Parquet sur un stockage S3 local. Préparation de l'architecture Docker avec Spark Master/Worker et LocalStack pour remplacer MinIO. Ajout prévu de commandes PowerShell pour soumettre le job Spark et vérifier les données stockées.
- 🚧 Bloqué / retard :Erreur de récupération de l'image Docker minio/minio. Remplacement envisagé par LocalStack, compatible avec le stockage S3 local. Le bon fonctionnement du pipeline complet reste à tester.
- 🧠 Appris :Fonctionnement de Spark Structured Streaming avec Kafka. Importance des features agrégées pour l'analyse comportementale du trafic réseau. Découverte de LocalStack comme solution de stockage S3 local et du format Parquet pour conserver les données structurées.
- ⚖️ Décision prise :Remplacer MinIO par LocalStack pour éviter le problème de récupération de l'image Docker. Conserver Kafka comme source des événements, Spark pour le traitement en continu et S3 pour le stockage des features.
- ➡️ Priorité S4 :Finaliser et tester le pipeline de bout en bout : génération des événements, lecture Kafka par Spark, calcul des features et écriture Parquet dans LocalStack. Vérifier les données produites et préparer leur exploitation par Isolation Forest pour la détection d'anomalies.
- 📸 Preuve (capture, lien commit) :

---

## Semaine 4 - 26 → 30 octobre 2026

- ✅ Fait :
- 🚧 Bloqué / retard :
- 🧠 Appris :
- ⚖️ Décision prise :
- ➡️ Priorité S5 :
- 📸 Preuve (capture, lien commit) :

---

## Semaine 5 - 02 → 06 novembre 2026

- ✅ Fait :
- 🚧 Bloqué / retard :
- 🧠 Appris :
- ⚖️ Décision prise :
- ➡️ Priorité S6 :
- 📸 Preuve (capture, lien commit) :

---

## Semaine 6 - 09 → 13 novembre 2026

- ✅ Fait :
- 🚧 Bloqué / retard :
- 🧠 Appris :
- ⚖️ Décision prise :
- ➡️ Priorité S7 :
- 📸 Preuve (capture, lien commit) :

---

## Semaine 7 - 16 → 20 novembre 2026

- ✅ Fait :
- 🚧 Bloqué / retard :
- 🧠 Appris :
- ⚖️ Décision prise :
- ➡️ Priorité S8 :
- 📸 Preuve (capture, lien commit) :

---

## Semaine 8 - 23 → 27 novembre 2026

- ✅ Fait :
- 🚧 Bloqué / retard :
- 🧠 Appris :
- ⚖️ Décision prise :
- ➡️ Priorité S9 :
- 📸 Preuve (capture, lien commit) :

---

## Semaine 9 - 30 novembre → 04 décembre 2026

- ✅ Fait :
- 🚧 Bloqué / retard :
- 🧠 Appris :
- ⚖️ Décision prise :
- ➡️ Priorité S10 :
- 📸 Preuve (capture, lien commit) :

---

## Semaine 10 - 07 → 11 décembre 2026

- ✅ Fait :
- 🚧 Bloqué / retard :
- 🧠 Appris :
- ⚖️ Décision prise :
- ➡️ Priorité S11 :
- 📸 Preuve (capture, lien commit) :

---

## Semaine 11 - 14 → 18 décembre 2026

- ✅ Fait :
- 🚧 Bloqué / retard :
- 🧠 Appris :
- ⚖️ Décision prise :
- ➡️ Priorité S12 :
- 📸 Preuve (capture, lien commit) :

---

## Semaine 12 - 21 → 25 décembre 2026

- ✅ Fait :
- 🚧 Bloqué / retard :
- 🧠 Appris :
- ⚖️ Décision prise :
- ➡️ Priorité S13 :
- 📸 Preuve (capture, lien commit) :

---

## Semaine 13 - 28 décembre 2026 → 01 janvier 2027

- ✅ Fait :
- 🚧 Bloqué / retard :
- 🧠 Appris :
- ⚖️ Décision prise :
- ➡️ Priorité S14 :
- 📸 Preuve (capture, lien commit) :

---

## Semaine 14 - 04 → 08 janvier 2027

- ✅ Fait :
- 🚧 Bloqué / retard :
- 🧠 Appris :
- ⚖️ Décision prise :
- ➡️ Priorité S15 :
- 📸 Preuve (capture, lien commit) :

---

## Semaine 15 - 11 → 15 janvier 2027

- ✅ Fait :
- 🚧 Bloqué / retard :
- 🧠 Appris :
- ⚖️ Décision prise :
- ➡️ Priorité S16 :
- 📸 Preuve (capture, lien commit) :

---

## Semaine 16 - 18 → 22 janvier 2027

- ✅ Fait :
- 🚧 Bloqué / retard :
- 🧠 Appris :
- ⚖️ Décision prise :
- 📸 Preuve (capture, lien commit) :

---


## Bilan des checkpoints

| Checkpoint | Échéance | Statut | Commentaire |
|------------|----------|--------|-------------|
| 1 - Détection E2E | fin S4 | ⬜ | |
| 2 - Pipeline MLOps complet | fin S8 | ⬜ | |
| 3 - Scénario agents E2E | fin S13 | ⬜ | |
