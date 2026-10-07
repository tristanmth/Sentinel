# 📖 Explications techniques — Semaine 1

---

## 1. Le Makefile / make.ps1 : c'est quoi exactement ?

### Le concept

Un **Makefile** est un fichier qui définit des **raccourcis de commandes**. Au lieu de taper des commandes longues et complexes, tu tapes `make <nom>` et tout s'exécute.

**Analogie** : c'est comme des favoris dans ton navigateur, mais pour les commandes terminal.

### Exemple concret

Sans Makefile, pour lancer le générateur en mode attaque, tu devrais taper :

```powershell
$env:TOPIC="netflow"; $env:MODE="attack"; $env:ATTACK_TYPE="port_scan"; $env:RATE="50"; python ingestion/log-generator/src/generator.py
```

Avec le Makefile / make.ps1 :

```powershell
.\make.ps1 attack-scan
```

**Résultat identique**, mais :
- ✅ Moins de fautes de frappe
- ✅ Mémorisation des paramètres exacts
- ✅ Documentation vivante (les noms sont explicites)

### Pourquoi `make.ps1` et pas `Makefile` ?

| Outil | Plateforme | Syntaxe |
|-------|------------|---------|
| `make` | Linux, Mac, Windows (avec GnuWin32) | Fichier `Makefile` |
| `make.ps1` | Windows natif (PowerShell) | Script PowerShell |

Ton `make.ps1` **reproduit exactement** les mêmes commandes que le Makefile original, mais en syntaxe PowerShell.

### Structure d'une commande dans make.ps1

```powershell
"attack-scan" { Run-Generator "attack" "port_scan" 50 }
#  ↑ nom        ↑ appelle la fonction  ↑ mode  ↑ type    ↑ débit
```

Quand tu tapes `.\make.ps1 attack-scan`, PowerShell :
1. Lit le paramètre `attack-scan`
2. Appelle `Run-Generator` avec les bons arguments
3. `Run-Generator` définit les variables d'environnement
4. Lance `python generator.py`

---

## 2. Le flux Kafka : que vois-tu exactement ?

### Le voyage d'un événement

```
[generator.py] → [Kafka] → [console-consumer]
     ↑              ↑            ↑
  produit        stocke       affiche
```

### Étape 1 : Le générateur produit

`generator.py` crée des objets JSON comme celui-ci :

```json
{
  "timestamp": "2026-10-07T12:34:56.789Z",
  "src_ip": "10.0.1.42",
  "dst_ip": "185.220.101.4",
  "src_port": 52344,
  "dst_port": 443,
  "protocol": "TCP",
  "bytes": 1200,
  "packets": 8,
  "duration_ms": 245,
  "flags": "SYN,ACK",
  "label": "normal"
}
```

**Ce que ça représente** : la machine `10.0.1.42` a ouvert une connexion HTTPS vers `185.220.101.4` (un serveur web externe). Elle a envoyé 1200 bytes en 8 paquets, sur 245 ms.

### Étape 2 : Kafka stocke

Kafka reçoit ce JSON et l'ajoute à la **fin** du topic `netflow`. C'est une **file d'attente persistante** :
- Les messages restent stockés (même si tu éteins le consumer)
- Ils sont **ordonnés** (chaque message a un numéro : offset 0, 1, 2...)
- Tu peux **relire** depuis le début (`--from-beginning`)

### Étape 3 : Le consumer affiche

`kafka-console-consumer.sh` lit les messages et les affiche. C'est un **outil de debug** — en production, ce sera Spark à la place.

### Les 3 modes du générateur

| Mode | Ce que tu vois | Usage |
|------|----------------|-------|
| `normal` | Événements `label: "normal"` réguliers (20/sec) | Baseline pour entraîner l'Isolation Forest |
| `attack` | Rafale d'événements `label: "port_scan"` (50/sec) | Tester la détection |
| `mixed` | Alternance calme/attaque toutes les 5 min | Simuler la réalité |

### Les 3 types d'attaque

| Attaque | Signature dans les logs | Exemple réel |
|---------|------------------------|--------------|
| `port_scan` | Même IP source, `dst_port` qui varie (1, 2, 3...), `flags: "SYN"` | nmap, masscan |
| `brute_force` | Même IP → même cible, `dst_port: 22`, répétitions rapides | hydra, patator |
| `syn_flood` | Volume massif de SYN, `duration_ms: 0`, pas de réponse | hping3, LOIC |

---

## 3. Pourquoi ce format JSON ?

### NetFlow vs notre format

**NetFlow** (Cisco) est le standard industriel pour exporter des métadonnées de trafic :
- IP source/destination
- Ports source/destination
- Protocole (TCP/UDP/ICMP)
- Octets, paquets, durée
- Flags TCP

Notre JSON est une **simplification pédagogique** de NetFlow. Les vrais équipements exportent en binaire, mais le concept est identique.

### Pourquoi c'est utile pour le ML

En semaine 3-4, Spark va agréger ces événements par fenêtre de temps :

```
Fenêtre 12:00 → 12:05 :
- IP 185.220.101.4 a contacté 847 ports différents
- Tous en SYN, sans réponse
- Durée moyenne : 2 ms
→ FEATURES : [847, 0, 2ms, ...] → Isolation Forest dit : ANOMALIE !
```

---

## 4. Le champ `label` : pourquoi c'est crucial

### Le problème du ML en cybersécurité

En production, tu ne sais pas si un événement est normal ou une attaque. C'est **le modèle qui doit le décider**.

Mais pour **évaluer** si ton modèle marche, tu as besoin de connaître la vérité. C'est le **label**.

### Comment on l'utilise

| Phase | Usage du label |
|-------|----------------|
| Entraînement Isolation Forest (S4) | On entraîne **sans** label (non supervisé) |
| Évaluation (S4) | On compare les prédictions du modèle aux labels réels |
| Entraînement XGBoost (S5) | On entraîne **avec** les labels (supervisé) |

### Exemple d'évaluation

```
Modèle prédit : [anomalie, anomalie, normal, normal, anomalie]
Labels réels :  [normal,    anomalie, normal, normal, normal   ]
                  ↑ FP       ↑ TP                ↑ FN

Précision = TP / (TP + FP) = 1 / 2 = 50%
Rappel    = TP / (TP + FN) = 1 / 2 = 50%
```

Sans labels, impossible de calculer ces métriques.

---

## 5. Kafka UI : http://localhost:8080

### Ce que tu peux voir

| Onglet | Contenu |
|--------|---------|
| **Topics** | Liste des topics, nombre de messages, taille |
| **Consumers** | Groupes de consommateurs, retard (lag) |
| **Brokers** | État du cluster Kafka |

### À surveiller en semaine 1

- Topic `netflow` : le nombre de messages doit augmenter en continu
- Si tu vois `0 messages` → le générateur n'envoie pas
