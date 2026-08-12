# Contribuer à BudgetRadar

Ce projet est développé en simulant un workflow d'équipe à 3 rôles, même si un seul compte Git/GitHub est utilisé pour tous les commits. La séparation des responsabilités se lit dans les noms de branches, le contenu des Pull Requests et les commentaires de revue — pas dans l'identité des commits.

## Les 3 rôles

- **Lead / Architecture** : structure du projet, CI/CD, Docker, schéma de base de données, documentation, cohérence globale.
- **Data / Backend** : API FastAPI, modèles PostgreSQL, logique métier (calcul des écarts budgétaires), migrations.
- **Frontend** : interface React, intégration avec l'API, dashboard et visualisations.

## Convention de branches

```
feature/<role>-<description-courte>
fix/<role>-<description-courte>
```

Exemples : `feature/lead-project-scaffold`, `feature/backend-budget-crud`, `feature/frontend-dashboard-ui`.

## Convention de commits

[Conventional Commits](https://www.conventionalcommits.org/) : `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, avec un scope optionnel (`feat(backend): ...`, `feat(frontend): ...`).

## Flux de Pull Request

1. Créer une branche depuis `main` selon la convention ci-dessus.
2. Développer, committer, pousser la branche sur `origin`.
3. Ouvrir une Pull Request sur GitHub en remplissant le template fourni.
4. La description doit préciser le rôle porteur de la PR et les points d'attention pour la revue (ex : contrat d'API pour le Frontend, contraintes de schéma pour le Backend).
5. Vérifier que la CI (lint + tests) est verte.
6. Ajouter au moins un commentaire de revue croisée avant de merger (squash merge recommandé).

## Développement local

```bash
docker compose up
```

Backend : tests avec `pytest` (voir `backend/README` implicite via `pyproject.toml`), lint avec `ruff check .`.
Frontend : tests avec `npm run test`, lint avec `npm run lint`.
