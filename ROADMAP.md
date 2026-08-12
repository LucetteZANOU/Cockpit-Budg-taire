# BudgetRadar — Cadrage produit

Ce document fixe le cap du projet. Il n'est pas rouvert à chaque conversation —
une idée qui sort d'une discussion va dans la section « Idées futures », pas
directement dans le code.

## 1. Pour qui

**Le RAF (Responsable Administratif et Financier) d'un projet ou d'une ONG
financé(e) par un bailleur international, au Bénin.**

Pas un contrôleur de gestion en poste dédié (rare et coûteux, réservé aux
grandes entreprises) — quelqu'un qui porte le suivi budgétaire *en plus* du
reste, dans une petite équipe sans budget IT.

## 2. Le problème précis

Le bailleur exige un suivi budget prévu/réalisé et une explication des
écarts, de façon récurrente et contractuelle. Le RAF le fait à la main dans
Excel : pas d'historique fiable, pas de structure garantissant que les
chiffres remontés d'un mois sur l'autre restent cohérents, risque d'erreur
élevé au moment de consolider avant un rapport bailleur.

BudgetRadar remplace ce fichier Excel par un outil structuré, sans imposer la
lourdeur (et le coût) d'un ERP ou d'une suite FP&A.

## 3. Périmètre V1 (verrouillé)

Ce qui est déjà construit ou en cours (PR1–PR3) et qui définit le V1 :

- Référentiel **centres de coût** (= lignes budgétaires bailleur / activités)
- Saisie de lignes budgétaires : centre de coût, exercice, période mensuelle
- Trois montants par ligne : **prévu**, **réestimé** (optionnel), **réalisé**
- Calcul automatique des écarts (valeur + %) — prévu/réalisé et prévu/réestimé
- Dashboard : tableau des lignes + graphique des écarts par centre de coût
- Mono-utilisateur, pas d'authentification (usage type "fichier partagé en
  confiance", comme l'Excel qu'il remplace)

### Explicitement hors scope pour l'instant (→ idées futures)

- Authentification / multi-utilisateur / rôles
- Workflow de validation d'exercice (brouillon → validé → clôturé)
- Export de rapport formaté pour bailleur (PDF/Excel)
- Multi-devises
- Plusieurs projets/bailleurs dans une même instance
- Import Excel en masse
- Alertes automatiques sur dépassement
- Historique d'audit (qui a modifié quoi, quand)

## 4. Après V1 — dans l'ordre

1. **Export bailleur** (PDF/Excel) — c'est l'obligation contractuelle
   concrète du RAF ; la première vraie valeur ajoutée au-delà du socle.
2. **Authentification basique** (mot de passe d'équipe, pas de RBAC complexe)
   — nécessaire dès qu'on déploie pour un usage partagé réel.
3. **Workflow de validation d'exercice** (brouillon/validé/clôturé) — pour
   formaliser le cycle annuel documenté en amont du projet.

## Idées futures (non planifiées)

- Multi-projets / multi-bailleurs
- Import Excel en masse
- Alertes automatiques
- Historique d'audit
- Cible PME (DAF) en plus de la cible ONG/bailleur
