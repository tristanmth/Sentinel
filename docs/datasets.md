# Notes sur les jeux de données

## 1. Générateur maison (source principale)

- Événements NetFlow-like au format JSON, publiés vers Kafka en continu
- Chaque événement porte un champ **`label`** = vérité terrain (`normal`, `port_scan`, `brute_force`, `syn_flood`)
- Modes : `normal` / `attack` / `mixed` (calme puis attaque périodique)
- **Utilité :** démo live temps réel + évaluation chiffrée des faux positifs
- ⚠️ Le drift entre ce trafic et CIC-IDS2017 est **volontaire**, c'est un sujet du projet (voir ADR-0002)

## 2. CIC-IDS2017

- Référence académique, trafic réel labellisé : BENIGN + 7 familles d'attaques (DoS, DDoS, brute force, port scan, botnet, web, infiltration)
- ~80 features par flux réseau (durée, bytes, flags, paquets...)
- Téléchargement : https://www.unb.ca/cic/datasets/ids-2017.html
- ⚠️ Caves connus : trafic daté de 2017, volumes plus faibles qu'aujourd'hui, biais de capture → **ne pas l'utiliser seul pour la détection en production**, mais parfait pour le classifieur supervisé

## 3. NSL-KDD

- Version nettoyée de KDD'99, petit (~148k lignes), bon pour **prototyper vite** la semaine 5
- Limite : daté, features anciennes

## 4. Sources d'enrichissement (agents)

| Source | Donnée | Accès |
|--------|--------|-------|
| AbuseIPDB | Réputation / score IP | API key (gratuit, rate limité) |
| NVD (NIST) | CVE associées à un service | API publique |
| ip-api / ipinfo | Géolocalisation IP | Gratuit (quota) |

## Stratégie d'usage

| Besoin | Source |
|--------|--------|
| Baseline non supervisée (Isolation Forest) | Générateur, mode `normal` uniquement |
| Classifieur supervisé (type d'attaque) | CIC-IDS2017 (NSL-KDD pour le prototypage) |
| Évaluation falsifiable | Générateur, grâce au champ `label` |
| Enrichissement des rapports | AbuseIPDB + NVD |
