# P5 - Déployez un modèle de Machine Learning

## Contexte du projet

Ce projet est réalisé dans le cadre du parcours Data Scientist Machine Learning.

L'objectif est de déployer un modèle de machine learning issu du projet 4 : Classifiez automatiquement des informations.

Le client fictif, Futurisys, souhaite rendre un modèle de machine learning opérationnel et accessible via une API performante.

## Objectifs

Le projet vise à :

- créer une API avec FastAPI pour exposer le modèle ;
- écrire des tests unitaires et fonctionnels avec Pytest ;
- utiliser Git pour gérer les versions du code ;
- connecter le projet à une base PostgreSQL ;
- préparer un pipeline CI/CD ;
- documenter l'installation, l'utilisation, le déploiement et la sécurisation de l'application.

## Structure du projet

- app/ : code source de l'application FastAPI
- models/ : modèles de machine learning exportés
- data/ : exemples de données
- db/sql/ : scripts SQL PostgreSQL
- tests/ : tests unitaires et fonctionnels
- docs/ : documentation technique
- .github/workflows/ : configuration CI/CD GitHub Actions
- requirements.txt : dépendances Python
- .gitignore : fichiers ignorés par Git
- README.md : documentation principale du projet

## Installation locale

Créer un environnement virtuel :

python3 -m venv .venv

Activer l'environnement virtuel :

source .venv/bin/activate

Installer les dépendances :

pip install -r requirements.txt

## Workflow Git

Le projet utilise une organisation simple :

- main : version stable du projet ;
- develop : branche d'intégration ;
- feature/... : branches dédiées aux fonctionnalités ;
- fix/... : branches dédiées aux corrections.

Exemples de branches :

- feature/project-setup
- feature/fastapi-api
- feature/model-loading
- feature/tests
- feature/database
- feature/ci-cd

## Versioning

Les versions stables seront marquées avec des tags Git.

Exemple :

git tag -a v0.1.0 -m "Initialisation du projet"

## État du projet

Projet en cours de développement.
