# Cahier des charges — Projet SENTINEL

**Plateforme de détection et d'investigation de cyberattaques en temps réel, assistée par agents IA**

| | |
|---|---|
| **Projet** | Projet personnel de fin d'études — Data Engineering |
| **Auteur** | Mathon Tristan |
| **Date de début** | 05 octobre 2026 |
| **Date de soutenance** | Fin janvier 2027 |
| **Durée** | 16 semaines |
| **Version** | 1.0 |

---

## 1. Contexte et problématique

### 1.1 Contexte
Les centres de sécurité (SOC) sont submergés d'alertes : une grande entreprise peut générer des **milliers d'alertes par jour**, dont une majorité de faux positifs. Les analystes passent l'essentiel de leur temps sur des tâches répétitives : collecter le contexte d'une alerte, vérifier la réputation d'une IP, chercher des CVE associées, rédiger un rapport.

### 1.2 Problématique
> **Comment construire une plateforme data temps réel capable de détecter des cyberattaques, d'industrialiser le cycle de vie de ses modèles de détection, et d'automatiser l'investigation des alertes grâce à des agents IA, tout en maîtrisant les coûts et la dérive des modèles ?**

### 1.3 Pourquoi ce projet ?
Il croise l'ensemble des enseignements suivis : **big data** (Kafka, Spark), **machine learning et MLOps** (entraînement, versioning, monitoring de dérive), **IA agentique** (agents autonomes d'investigation), **cloud** (conteneurisation, Kubernetes, IaC), **transition data** (migration legacy → plateforme moderne) et **cybersécurité** (cas d'usage métier, sécurisation du pipeline lui-même).

---

## 2. Objectifs

### 2.1 Objectif général
Concevoir, implémenter et industrialiser une plateforme complète allant de la génération de trafic réseau simulé jusqu'au rapport d'investigation automatisé, déployée de manière reproductible.

### 2.2 Objectifs fonctionnels

| ID | Objectif | Priorité |
|----|----------|----------|
| OF1 | Ingérer un flux continu d'événements réseau (NetFlow-like) via un bus de messages temps réel | Must |
| OF2 | Calculer des features de détection en streaming (agrégations par fenêtres glissantes) | Must |
| OF3 | Détecter les anomalies par apprentissage non supervisé sur la baseline du système | Must |
| OF4 | Classifier le type d'attaque (scan, brute force, DDoS) par apprentissage supervisé | Must |
| OF5 | Versionner, déployer et surveiller les modèles (MLOps : tracking, registry, drift detection) | Must |
| OF6 | Regrouper et prioriser les alertes avant investigation (dédoublonnage, scoring) | Must |
| OF7 | Investiguer automatiquement les alertes via des agents IA (contexte, enrichment externe, rapport) | Must |
| OF8 | Soumettre les actions de remédiation à validation humaine avant exécution (human-in-the-loop) | Should |
| OF9 | Visualiser le trafic, les alertes et l'activité des agents sur un dashboard | Must |
| OF10 | Déployer l'ensemble de façon reproductible (IaC, CI/CD, Kubernetes) | Should |

### 2.3 Objectifs non fonctionnels

| ID | Objectif | Cible mesurable |
|----|----------|-----------------|
| ONF1 | Latence de détection | Alerte émise < 5 min après le début d'une attaque |
| ONF2 | Taux de faux positifs | < 20 % sur trafic normal simulé |
| ONF3 | Maîtrise des coûts LLM | < 0,10 € par investigation |
| ONF4 | Résilience | Pipeline fonctionnel avec 1 composant tué (pod) |
| ONF5 | Régularité du développement | ≥ 5 commits/semaine en moyenne |
| ONF6 | Reproductibilité | `terraform apply` + un script unique déploient toute la plateforme |
| ONF7 | Qualité de code | CI avec lint + tests unitaires sur chaque PR |

---

## 3. Périmètre

### 3.1 Inclus
- Pipeline complet : génération de trafic → ingestion → traitement streaming → détection → investigation agentique → rapport
- Gestion industrialisée du cycle de vie ML (entraînement, registry, drift, réentraînement)
- Dashboards d'observabilité (infrastructure, métriques ML, coûts agents)
- Infrastructure as Code et CI/CD
- Sécurisation du pipeline lui-même (chiffrement, secrets)

### 3.2 Exclus (hors périmètre volontaire)
- Déploiement sur un réseau de production réel (trafic simulé uniquement)
- Remédiation automatique sans validation humaine (décision sécurité volontaire)
- Détection sur trafic chiffré (inspection de contenu TLS)
- Entraînement de LLM custom (utilisation d'API ou de modèles open source locaux)

### 3.3 Hypothèses
- Le trafic généré, bien que synthétique, présente des caractéristiques réalistes (volumes, patterns d'attaque connus)
- L'écart entre dataset public (CIC-IDS2017) et trafic simulé est traité comme un sujet à part entière (drift)

---

## 4. Description fonctionnelle (use cases)

| Acteur | Cas d'usage |
|--------|-------------|
| Analyste SOC (utilisateur) | Consulter le dashboard, recevoir un rapport d'investigation, valider/contredire une action de blocage |
| Système (agents) | Détecter, grouper, investiguer, rédiger, recommander |
| Data engineer (moi) | Réentraîner, déployer, monitorer, faire évoluer la plateforme |

**Scénario principal :**
1. Trafic normal circule (générateur en mode `mixed`)
2. Une attaque simulée démarre (scan de ports puis brute force)
3. Spark détecte l'anomalie en < 5 min et publie une alerte
4. Les alertes sont groupées et soumises aux agents
5. Les agents produisent un rapport : nature de l'attaque, IP source, réputation, historique, recommandation
6. L'analyste valide → l'IP est bloquée → le trafic s'interrompt sur les graphiques en temps réel

---

## 5. Architecture technique (vue d'ensemble)

```
[Générateur de trafic] → Kafka → [Spark Structured Streaming] → [Stockage Delta/MinIO]
                                                          ↘ [Modèles ML (IF + XGBoost)]
                                                                  ↓
                                        [Groupement d'alertes + rate limiting]
                                                                  ↓
                        [Agents IA : Enquêteur → Enrichisseur → Rapporteur] (LangGraph)
                                                                  ↓
                              [Dashboard + Slack] ← validation humaine → [Blocage via Kafka]
```

**Stack retenue :** Kafka (Redpanda possible en local) · Spark Structured Streaming · Delta Lake/MinIO · scikit-learn (Isolation Forest) · XGBoost · MLflow · Airflow · Evidently · LangGraph + API LLM · Grafana/Prometheus · Docker, Kubernetes (K3s), Terraform · GitHub Actions · Streamlit (dashboard)

*(Chaque choix majeur sera justifié par un ADR, voir `docs/architecture/adr/`)*

---

## 6. Données

| Source | Rôle | Nature |
|--------|------|--------|
| Générateur maison | Flux temps réel principal | Événements NetFlow-like JSON, étiquetés (`label`) |
| CIC-IDS2017 | Entraînement supervisé | ~80 features réseau labellisées (7 attaques) |
| NSL-KDD | Prototypage rapide | Version nettoyée de KDD'99 |
| AbuseIPDB / NVD API | Enrichissement agents | Réputation IP, CVE |

---

## 7. Méthodologie et organisation

- **Approche :** itérative par phases de 4 semaines, avec **3 checkpoints go/no-go** (fin S4 : détection E2E ; fin S8 : MLOps complet ; fin S13 : scénario agents E2E)
- **Rituels hebdomadaires :** planning lundi (3 tâches max) · commit quotidien · revue vendredi avec journal de bord
- **Gestion de configuration :** Git + GitHub Actions, branches par fonctionnalité, PR revues par le tuteur si souhaité
- **Suivi :** GitHub Projects (kanban) + journal hebdo dans `docs/journal.md`

## 8. Planning prévisionnel

| Phase | Semaines | Contenu |
|-------|----------|---------|
| 1 — Fondations | S1-S4 (oct) | Kafka, générateur, Spark streaming, stockage, Isolation Forest v1 |
| 2 — ML & MLOps | S5-S8 (nov) | EDA, modèles supervisés, MLflow, Airflow, drift |
| 3 — Agents IA | S9-S12 (déc) | Agents, orchestration LangGraph, boucle fermée |
| 4 — Industrialisation | S13-S16 (jan) | K8s, Terraform, sécurisation, mémoire, soutenance |

*(Échéancier détaillé semaine par semaine : voir `SENTINEL_Plan_Projet.md`)*

## 9. Risques et mitigation

| Risque | Probabilité | Mitigation |
|--------|-------------|------------|
| Kafka/Spark trop lourds en local | Élevée | 1 broker / partitions réduites, ou Redpanda |
| Dérive de planning (fêtes S11-S12) | Élevée | Phase allégée planifiée + marge S13 |
| Coûts API LLM lors d'attaques simulées | Moyenne | Groupement d'alertes + rate limiting (budget intégré au design) |
| Drift dataset vs trafic simulé | Certain (volontaire) | Détecteur non supervisé sur baseline propre + Evidently + réentraînement |
| API LLM indisponible le jour J | Faible | Fallback modèle local (Ollama) + vidéo de démo pré-enregistrée |

## 10. Critères de réussite

1. Le scénario de démo complet fonctionne de bout en bout (détection → rapport → blocage)
2. Les 3 checkpoints sont validés
3. Les KPIs ONF1-ONF4 sont mesurés et présentés (graphes Grafana à l'appui)
4. Le mémoire documente l'ensemble, y compris les échecs et apprentissages
5. Le repo est public, propre, et constitue un portfolio crédible pour un poste de data engineer


