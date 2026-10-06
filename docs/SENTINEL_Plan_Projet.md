# SENTINEL : Livrables, Échéancier & Plan d'Action

## Plateforme de détection et d'investigation SOC automatisée

**Projet personnel de fin d'études | Data Engineering | Durée : 16 semaines**
*Démarrage : lundi 5 octobre 2026 → Soutenance : fin janvier 2027*

---

# PARTIE 1 : LES LIVRABLES À RENDRE

## A. Livrables techniques (le cœur du projet)

| # | Livrable | Description |
| --- | --- | --- | --- |
| A1 | **Repo GitHub structuré** | Code source complet, commits propres et réguliers, branches par fonctionnalité, tags par version |
| A2 | **Pipeline d'ingestion temps réel** | Générateur de logs/attaques → Kafka → Spark Structured Streaming → stockage (Delta Lake / MinIO) |
| A3 | **Détecteur d'anomalies ML** | Isolation Forest (non supervisé, baseline propre) + classifieur supervisé (CIC-IDS2017) intégré au streaming |
| A4 | **Pipeline MLOps complet** | MLflow (tracking + registry), DAG Airflow d'entraînement, détection de drift (Evidently), réentraînement déclenché | 
| A5 | **Système multi-agents IA** | 3 agents (Enquêteur, Enrichisseur, Rapporteur) orchestrés via LangGraph, avec groupement d'alertes + rate limiting |
| A6 | **Infrastructure as Code** | Terraform (cloud ou K3s local) + Docker Compose, Kubernetes/Helm pour le déploiement |
| A7 | **CI/CD** | GitHub Actions : tests, lint, build images, déploiement automatique |
| A8 | **Observabilité** | Dashboards Grafana (infra + métriques ML + coûts LLM), Prometheus, alerting |

## B. Livrables documentaires

| # | Livrable | Description |
| --- | --- | --- | --- |
| B1 | **Cahier des charges** (10-15 pages) | Contexte, objectifs, périmètre fonctionnel, stack technique, contraintes |
| B2 | **Notebooks d'exploration (EDA)** | Analyse du dataset CIC-IDS2017, statistiques, visualisations, choix de features |
| B3 | **Dossier d'architecture** | Schémas d'architecture (composants, flux de données, séquences agents), ADR (Architecture Decision Records) |
| B4 | **Rapport de modélisation** | Baselines, métriques, comparaison modèles, gestion du drift, limites |
| B5 | **Rapport final / mémoire** (30-50 pages) | Tout le projet : contexte, conception, réalisation, résultats, bilan, perspectives |
| B6 | **Documentation technique** | README par service, guide d'installation, guide de contribution |

## C. Livrables de soutenance

| # | Livrable | Description |
| --- | --- | --- |
| C1 | **Support de présentation** (15-20 slides) | Problème → architecture → démo → résultats → bilan |
| C2 | **Démo live OU vidéo 3 min** | Scénario narratif : attaque simulée → détection → agents → rapport → blocage. La vidéo est le plan B si la démo live plante |
| C3 | **Poster / one-pager** (optionnel) | Résumé visuel du projet pour le portfolio |

---

# PARTIE 2 : ÉCHÉANCIER (16 semaines)

| Semaine | Dates (2026-2027) | Objectif principal | Livrable associé |
| --- | --- | --- | --- |
| **S1** | 05-09 oct | Setup environnement : Git, Docker, CI basique. Repo structuré. Générateur de logs v1 | A1, B1 |
| **S2** | 12-16 oct | Kafka opérationnel, premier topic, console de consommation. Cahier des charges finalisé | A2, B1 |
| **S3** | 19-23 oct | Spark Structured Streaming : lecture Kafka, fenêtres glissantes, agrégations | A2 |
| **S4** | 26-30 oct | Stockage Parquet/Delta sur MinIO. Isolation Forest v1 en batch. 🏁 **Checkpoint 1 : détection E2E** | A2, A3 |
| **S5** | 02-06 nov | EDA CIC-IDS2017, feature engineering, classifieur supervisé baseline | B2, A3 |
| **S6** | 09-13 nov | MLflow : tracking + registry. Chargement du modèle dans le pipeline streaming | A4 |
| **S7** | 16-20 nov | Airflow : DAG d'entraînement périodique. Tests et validation | A4 |
| **S8** | 23-27 nov | Evidently : monitoring drift → alertes Grafana. 🏁 **Checkpoint 2 : pipeline MLOps complet** | A4, B4 |
| **S9** | 30 nov-04 déc | Agent Enquêteur v1 (alerte → requêtes logs → résumé) | A5 |
| **S10** | 07-11 déc | Agent Enrichisseur (AbuseIPDB, CVE NVD, géoloc) + groupement d'alertes | A5 |
| **S11** | 14-18 déc | Orchestration LangGraph : chaîne Enquêteur → Enrichisseur → Rapporteur. Slack + rapport markdown | A5 |
| **S12** | 21 déc-01 jan | 🎄 **Période légère** : boucle fermée (validation humaine → blocage), documentation, rattrapage éventuel | A5, B6 |
| **S13** | 04-08 jan | Migration Kubernetes (K3s/EKS) + Terraform. 🏁 **Checkpoint 3 : scénario E2E complet** | A6 |
| **S14** | 11-15 jan | Sécurisation du pipeline (TLS Kafka, secrets, authn), tests E2E, chaos léger. Début rapport final | A6, B5 |
| **S15** | 18-22 jan | Optimisations (watermarking, backpressure), polish dashboards, **vidéo démo** | B5, C2 |
| **S16** | 25-29 jan | Finalisation mémoire, répétitions soutenance, **soutenance** 🎓 | B5, C1 |

### 🏁 Les 3 checkpoints non négociables

- **Checkpoint 1 (fin S4)** : une attaque simulée est détectée de bout en bout en moins de 5 minutes
- **Checkpoint 2 (fin S8)** : MLflow montre des expériences, un modèle en production, et un dashboard de drift
- **Checkpoint 3 (fin S13)** : le scénario complet agents + blocage fonctionne

> Règle d'or : si un checkpoint est raté, tu ne passes pas à la phase suivante sans arbitrage. Mieux vaut un périmètre réduit qui marche qu'un périmètre large qui brille par l'absence en soutenance.

---

# PARTIE 3 : PLAN D'ACTION

## Phase 1 : FONDATIONS (S1-S4)

**Objectif :** des données qui circulent de bout en bout.

- [ ] S1 : Repo Git + structure (`/ingestion`, `/streaming`, `/ml`, `/agents`, `/infra`, `/docs`) + CI lint
- [ ] S1 : Générateur Python de logs réseau (NetFlow-like) + mode "attaque" activable
- [ ] S2 : Kafka en Docker Compose, topics : `netflow`, `auth`, `alerts-raw`
- [ ] S3 : Job Spark : lecture Kafka, fenêtres 5 min / 1 h, agrégations par IP
- [ ] S3 : Features streaming : nb connexions, bytes, durée, ratio SYN, entropie ports
- [ ] S4 : Isolation Forest batch sur historique + seuillage scores
- [ ] S4 : Publication alertes dans Kafka → vérification console

- ✅ **Definition of Done Phase 1** : attaque simulée → alerte visible en < 5 min, données stockées, tests unitaires sur le générateur et les features

## Phase 2 : MACHINE LEARNING & MLOPS (S5-S8)

**Objectif :** un modèle industrialisé, pas un notebook orphelin.

- [ ] S5 : EDA CIC-IDS2017 (notebooks) + baseline RandomForest/XGBoost
- [ ] S6 : MLflow tracking (params, métriques, artifacts) + model registry (staging → production)
- [ ] S6 : Chargement du modèle registry dans Spark Streaming
- [ ] S7 : DAG Airflow : entraînement nocturne + réentraînement déclenché
- [ ] S8 : Evidently : data drift + performance drift → métriques Prometheus → Grafana

- ✅ **Definition of Done Phase 2** : dashboard Grafana montrant précision du modèle et drift ; le réentraînement se déclenche sans intervention humaine

## Phase 3 : AGENTS IA (S9-S12)

**Objectif :** l'investigation automatisée qui te démarque.

- [ ] S9 : Agent Enquêteur : prompt + outil text-to-SQL sur tes tables de logs
- [ ] S10 : Agent Enrichisseur : outils AbuseIPDB, NVD (CVE), géoloc IP
- [ ] S10 : **Groupement d'alertes** : agrégation par IP source / type sur fenêtre 15 min
- [ ] S11 : Orchestration LangGraph + rate limiting (max 5 investigations/min)
- [ ] S11 : Agent Rapporteur : rapport markdown + notification Slack
- [ ] S12 : Boucle fermée : approbation humaine dashboard → publication règle Kafka → blocage effectif

- ✅ **Definition of Done Phase 3** : 1 attaque simulée → 1 rapport d'agent complet reçu sur Slack, avec coût LLM < 0,10€ par investigation

## Phase 4 : INDUSTRIALISATION & SOUTENANCE (S13-S16)

**Objectif :** du solide, du propre, du présentable.

- [ ] S13 : Terraform + Kubernetes, Helm charts, déploiement reproductible
- [ ] S14 : Sécurisation : TLS Kafka, Vault pour les clés API, RBAC minimal
- [ ] S14 : Tests E2E + chaos léger (kill d'un pod mid-demo)
- [ ] S15 : Optimisations : watermarking, gestion backpressure
- [ ] S15 : **Vidéo démo 3 min** (plan B de la soutenance) + slides
- [ ] S16 : Mémoire final, répétitions, soutenance

- ✅ **Definition of Done Phase 4** : `terraform apply` + script unique déploie tout ; la démo fonctionne même si un composant tombe

## Rituels hebdomadaires (30 min, non négociables)

| Rituel | Quand | Quoi |
| --- | --- | --- |
| Planning | Lundi matin | Choisir 3 tâches max pour la semaine, écrites dans GitHub Projects |
| Commit quotidien | Chaque jour | Au moins 1 commit/jour, même petit |
| Revue | Vendredi | Démo à soi-même de ce qui marche, mise à jour du journal de bord (`/docs/journal.md`) |
| Checkpoint | Fin de phase | Démo en conditions réelles, décision go/no-go |

## Gestion des risques

| Risque | Probabilité | Mitigation |
| --- | --- | --- |
| Kafka/Spark trop lourds en local | Élevée | Docker Compose calibré (1 broker, 1 partition suffisent), ou Redpanda |
| Surcharge en S9-S12 (agents complexes) | Moyenne | Agent Enquêteur minimal d'abord, enrichir ensuite |
| Dérive du planning pendant les fêtes | Élevée | S12 volontairement légère, marge intégrée en S13 |
| Coûts cloud | Moyenne | Local/K3s d'abord, crédits étudiants (AWS/GCP) si besoin en S13-S14 |
| API LLM indisponible le jour J | Faible | Fallback Ollama local testé en S11, vidéo pré-enregistrée |

## KPIs de réussite du projet

- Latence détection : alerte émise en **< 5 min** après début d'attaque
- Faux positifs : **< 20%** sur trafic normal simulé
- Coût par investigation agent : **< 0,10€**
- Résilience : pipeline fonctionnel avec **1 pod tué** pendant la démo
- Couverture : **100% des checkpoints** validés
- Régularité Git : **≥ 5 commits/semaine** en moyenne
