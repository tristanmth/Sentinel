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

- ✅ Fait :
- 🚧 Bloqué / retard :
- 🧠 Appris :
- ⚖️ Décision prise :
- ➡️ Priorité S3 :
- 📸 Preuve (capture, lien commit) :

---

## Semaine 3 - 19 → 23 octobre 2026

- ✅ Fait :
- 🚧 Bloqué / retard :
- 🧠 Appris :
- ⚖️ Décision prise :
- ➡️ Priorité S4 :
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
