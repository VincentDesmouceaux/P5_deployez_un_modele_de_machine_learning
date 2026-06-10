# Workflow Git du projet

## Objectif

Ce document décrit l'organisation Git utilisée pour le projet P5.

L'objectif est de garantir :

- un historique de commits clair ;
- une séparation propre des fonctionnalités ;
- une meilleure traçabilité du développement ;
- une collaboration plus fluide.

## Branches principales

### main

La branche main contient uniquement les versions stables du projet.

Elle correspond au code prêt à être présenté ou déployé.

### develop

La branche develop sert de branche d'intégration.

Les fonctionnalités terminées sont fusionnées dans develop avant d'être intégrées dans main.

## Branches de fonctionnalités

Chaque nouvelle fonctionnalité doit être développée dans une branche dédiée.

Convention de nommage :

- feature/nom-de-la-fonctionnalite
- fix/nom-de-la-correction

Exemples :

- feature/project-setup
- feature/fastapi-api
- feature/model-loading
- feature/tests
- feature/database
- feature/ci-cd
- fix/api-validation-error

## Convention de commits

Les messages de commit doivent être courts, clairs et descriptifs.

Exemples :

- Initialise project structure
- Add Git workflow documentation
- Add FastAPI health endpoint
- Add model loading service
- Add prediction endpoint tests
- Configure GitHub Actions workflow

## Versioning

Les versions stables sont marquées avec des tags Git.

Exemple :

git tag -a v0.1.0 -m "Initialisation du projet"

## Gestion des conflits

En cas de conflit Git :

1. identifier les fichiers en conflit avec git status ;
2. ouvrir les fichiers concernés dans l'éditeur de code ;
3. choisir la bonne version du code ;
4. supprimer les marqueurs de conflit ;
5. ajouter les fichiers corrigés avec git add ;
6. finaliser avec un commit.

## Bonnes pratiques

- Ne pas travailler directement sur main.
- Créer une branche feature pour chaque nouvelle fonctionnalité.
- Faire des commits réguliers et explicites.
- Fusionner les branches terminées dans develop.
- Fusionner develop dans main uniquement pour les versions stables.
- Ajouter un tag Git à chaque version importante.
