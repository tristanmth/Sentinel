# 📋 Récapitulatif Semaine 1 — 05 → 09 octobre 2026

**Statut : ✅ TERMINÉE** | Date de clôture : 07 octobre 2026

---

## 🎯 Objectif de la semaine

> Repo structuré + générateur de logs v1 + Kafka opérationnel. **Rien d'autre.**

---

## ✅ Ce qui a été livré

| Élément | Fichier / Emplacement | Statut |
|---------|----------------------|--------|
| Structure du repo | `sentinel/` (12 dossiers) | ✅ |
| Docker Compose (Kafka + UI) | `docker-compose.yml` | ✅ |
| Générateur de trafic | `ingestion/log-generator/src/generator.py` | ✅ |
| Commandes PowerShell | `make.ps1` | ✅ |
| CI GitHub Actions | `.github/workflows/ci.yml` | ✅ |
| Cahier des charges | `docs/cahier-des-charges.md` | ✅ |
| ADR (3 décisions) | `docs/architecture/adr/` | ✅ |
| Journal de bord | `docs/journal.md` | ✅ |
| Guide datasets | `data/README.md` | ✅ |
| .gitignore + .env.example | Racine | ✅ |

---

## 🔧 Ce qui fonctionne (validé le 07/10)

Terminal 1 - trafic normal :
```powershell
.\make.ps1 up           # Kafka + UI démarrent
.\make.ps1 normal       # Flux continu de trafic normal vers Kafka
```

Terminal 2 - attaque (au bout de ~30 s) :
```powershell
.\make.ps1 attack-scan  # Rafale d'événements "port_scan"
```

Terminal 3 - observer :
```powershell
.\make.ps1 consume      # Visualisation des événements en temps réel
```

**Preuve de fonctionnement** : capture d'écran Kafka UI montrant le topic `netflow` en croissance + console consumer affichant les JSON.

---

## 🧠 Ce qu'on a appris

1. **Kafka KRaft** : mode sans Zookeeper, plus simple pour le dev local
2. **NetFlow-like** : format JSON simplifié des flux réseau (IP source/dest, ports, protocole, bytes...)
3. **Vérité terrain** : le champ `label` dans chaque événement permettra d'évaluer les faux positifs en S4
4. **PowerShell vs Make** : `make.ps1` reproduit le Makefile pour Windows

---

## ⚖️ Décisions prises (ADR)

| ADR | Décision | Pourquoi |
|-----|----------|----------|
| 0001 | Kafka comme bus de messages | Durabilité, reprise, standard industrie |
| 0002 | Isolation Forest non supervisé | Évite le domain shift CIC-IDS2017 vs trafic simulé |
| 0003 | GitHub Actions | Repo public = minutes illimitées + visibilité |

---

## 🚧 Bloquages rencontrés

| Problème | Solution |
|----------|----------|
| `make` non reconnu sur Windows | Création de `make.ps1` équivalent |

---

## Lien dataset

**CIC-IDS2017** : https://www.unb.ca/cic/datasets/ids-2017.html
→ Télécharger `MachineLearningCSV/MachineLearningCVE/`
Alternative légère pour prototyper : **NSL-KDD** : https://www.unb.ca/cic/datasets/nsl.html

---

## ➡️ Priorité Semaine 2

1. **Topics Kafka structurés** : `netflow`, `auth`, `alerts-raw`
2. **Premier consumer Spark** : lecture Kafka, fenêtres glissantes
3. **Tests unitaires** sur le générateur (CI)

---

*Document généré le 07/10/2026*
