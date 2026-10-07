# Semaine 1 — Fondations (05 → 09 octobre 2026)

## Objectif
Repo structuré + générateur de logs v1 + Kafka opérationnel. **Rien d'autre.**

## Setup

```bash
# 1. Cloner / initialiser le repo
git init && git add . && git commit -m "chore: structure initiale + générateur v1"

# 2. Lancer Kafka
docker compose up -d

# 3. Installer le générateur (une fois)
pip install kafka-python

# 4. Vérifier
make topics          # doit afficher "netflow" après le premier lancement
```

## Scénario de validation

Terminal 1 — trafic normal :
```bash
make normal
```

Terminal 2 — attaque (au bout de ~30 s) :
```bash
make attack-scan
```

Terminal 3 — observer :
```bash
make consume
```

**Critère de réussite** : tu vois défiler des `label: "normal"` puis une rafale de `label: "port_scan"` depuis la même IP. Dans Kafka UI (http://localhost:8080), le topic `netflow` grossit.

## Definition of Done

- [ ] `make up` fonctionne, Kafka UI accessible
- [ ] `make normal` + `make attack-scan` + `make consume` fonctionnent
- [ ] La CI passe (3 jobs verts) sur le premier push
- [ ] Capture d'écran Kafka UI ajoutée dans `docs/journal.md`
- [ ] Journal S1 rempli (5 lignes : fait / bloqué / appris / décision / priorité)

## Pièges connus

| Symptôme | Cause | Fix |
|----------|-------|-----|
| `No module named 'kafka'` | kafka-python pas installé | `pip install kafka-python` |
| Consumer vide | Topic inexistant → le créer : `docker exec sentinel-kafka kafka-topics.sh --bootstrap-server localhost:9092 --create --topic netflow --partitions 1 --replication-factor 1` | ou lancer `make normal` d'abord |
| `Connection refused` | Kafka pas prêt | attendre 10 s après `docker compose up -d` |

## Lien dataset (pour S5, à garder sous le coude)

**CIC-IDS2017** : https://www.unb.ca/cic/datasets/ids-2017.html
→ Télécharger `MachineLearningCSV/MachineLearningCVE/` (les CSV, ~2 GB décompressés)
Alternative légère pour prototyper : **NSL-KDD** : https://www.unb.ca/cic/datasets/nsl.html
