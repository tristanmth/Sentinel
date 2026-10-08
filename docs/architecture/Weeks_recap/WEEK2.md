# Semaine 2 — Topics Kafka structurés (12 → 16 octobre 2026)

## Objectif
Topics `netflow`, `auth`, `alerts-raw` créés. Générateur v2 émet vers les bons topics. Cahier des charges finalisé.

## Setup

```powershell
# 1. Créer les topics (une fois)
.\scripts\create-topics.ps1

# 2. Vérifier
.\make.ps1 topics
# Doit afficher : alerts-raw, auth, netflow

# 3. Lancer le générateur v2
.\make.ps1 mixed

# 4. Observer les deux flux (2 terminaux)
.\make.ps1 consume-netflow    # trafic réseau
.\make.ps1 consume-auth       # événements d'auth
```

## Nouveautés du générateur v2

| Type d'événement | Topic | Exemple |
|------------------|-------|---------|
| Connexion TCP/UDP | `netflow` | `{"src_ip": "10.0.1.42", "dst_port": 443, ...}` |
| Login SSH/FTP | `auth` | `{"user": "root", "status": "failed", ...}` |
| Alerte ML (S4) | `alerts-raw` | *(pas encore utilisé)* |

**Attaque brute_force** = les deux topics en parallèle :
- `netflow` : connexions SSH répétées (port 22)
- `auth` : échecs de login ("failed")

## Definition of Done

- [ ] `.\scripts\create-topics.ps1` exécuté, 3 topics visibles
- [ ] `.\make.ps1 mixed` fonctionne, événements dans `netflow` ET `auth`
- [ ] Attaque brute_force visible dans les deux topics simultanément
- [ ] Cahier des charges
- [ ] Journal S2 rempli (5 lignes)

## Pièges connus

| Symptôme | Cause | Fix |
|----------|-------|-----|
| Topic existe déjà | Normal | `--if-not-exists` gère ça |
| Pas d'événements dans `auth` | Mode `normal` émet peu d'auth | Attendre une attaque `brute_force` ou augmenter `RATE` |
| Consumer vide | Mauvais topic | Vérifier avec `.\make.ps1 topics` |
