# ADR-0002 : Isolation Forest non supervisé pour la détection de base

- **Statut :** accepté
- **Date :** 2026-10-06

## Contexte
Le dataset public CIC-IDS2017 (2017) diffère structurellement du trafic simulé en 2026 (volumes, ports, chiffrement). Un modèle supervisé entraîné dessous subirait du **domain shift** : faux positifs massifs ou détection nulle.

## Décision
Deux modèles complémentaires :
1. **Isolation Forest**, non supervisé, entraîné sur la baseline `normal` du générateur → détection d'anomalies adaptée à notre environnement.
2. **Classifieur supervisé** (XGBoost) entraîné sur CIC-IDS2017 → typage de l'attaque une fois l'anomalie détectée.

Le drift entre les deux distributions est surveillé en continu (Evidently) — c'est un **sujet de démonstration** du projet, pas un bug.

## Alternatives envisagées
- **Autoencodeur (deep learning)** — plus puissant mais plus lourd à entraîner/monitorer ; reporté en perspective.
- **Un seul modèle supervisé** — rejeté : fragile face au domain shift.
- **Règles statiques (seuils)** — rejetées : pas d'apprentissage, référence conservée uniquement comme baseline comparative.

## Conséquences
- Positives : détection robuste à l'environnement, sujet riche pour la soutenance (gestion de la dérive).
- Négatives : l'Isolation Forest ne donne pas le *type* d'attaque → justifie le second modèle supervisé.
