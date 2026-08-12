# BudgetRadar

Dashboard de contrôle de gestion : suivi des lignes budgétaires et des écarts prévu/réalisé.

## Stack

- **Backend** : Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL
- **Frontend** : React, TypeScript, Vite, Recharts
- **Infra locale** : Docker Compose

## Démarrage rapide

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
docker compose up
```

- Backend : http://localhost:8000 (docs interactives sur `/docs`)
- Frontend : http://localhost:5173

## Structure du projet

```
backend/    API FastAPI, modèles, migrations Alembic, tests
frontend/   Application React (Vite + TypeScript)
```

## Contribuer

Le workflow de développement (branches, commits, revues, CI) est documenté dans [CONTRIBUTING.md](./CONTRIBUTING.md).

## Périmètre fonctionnel (MVP)

- Saisie de lignes budgétaires (catégorie, montant prévu, montant réalisé, période)
- Calcul automatique des écarts (valeur et pourcentage)
- Dashboard de synthèse avec graphique des écarts par catégorie

## Licence

BudgetRadar — Copyright (C) 2026 Princesse ZANOU

Ce programme est un logiciel libre : vous pouvez le redistribuer et/ou le
modifier selon les termes de la GNU Affero General Public License publiée
par la Free Software Foundation, version 3 de la licence, ou (à votre
choix) toute version ultérieure. Voir [LICENSE](./LICENSE) pour le texte
complet.

L'AGPL impose que toute personne faisant tourner une version modifiée de
ce logiciel comme service réseau (SaaS) mette également son code source
à disposition des utilisateurs de ce service.
