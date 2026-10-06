# ADR-0003 : GitHub Actions pour la CI/CD

- **Statut :** accepté
- **Date :** 2026-10-06

## Contexte
Un pipeline CI/CD est requis (tests, lint, build d'images). Expérience préalable de l'auteur sur GitLab CI ; le choix entre GitHub Actions et GitLab CI n'était pas évident.

## Décision
**GitHub Actions**, le repo étant public (minutes illimitées, visibilité portfolio).

## Alternatives envisagées
- **GitLab CI** — syntaxe un peu plus simple, tout intégré ; non retenu ici car repo déjà hébergé sur GitHub et objectif de visibilité professionnelle.
- Aucune CI — évidemment rejeté (exigence ONF7).

## Conséquences
- Positives : gratuit en illimité (repo public), écosystème d'actions très large, profil GitHub = vitrine.
- Négatives : YAML parfois verbeux ; acceptable.
