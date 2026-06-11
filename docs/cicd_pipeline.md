# Pipeline CI/CD

## Objectif

Ce document décrit la stratégie d'intégration continue et de déploiement continu du projet P5.

Le pipeline permet de :

- lancer automatiquement les tests ;
- vérifier la qualité minimale du code avant fusion ;
- produire un rapport de couverture ;
- déployer automatiquement l'application sur Hugging Face Spaces depuis la branche main.

## Environnements

### Développement

Les branches feature correspondent à l'environnement de développement.

Exemples :

- feature/ci-cd
- feature/fastapi-api
- feature/model-loading
- feature/tests

Les tests sont lancés automatiquement à chaque push.

### Test

La branche develop sert d'environnement d'intégration.

Les fonctionnalités terminées sont fusionnées dans develop après validation.

### Production

La branche main représente la version stable.

Tout push sur main déclenche le déploiement vers Hugging Face Spaces.

## GitHub Actions

Le fichier de workflow principal est :

.github/workflows/ci-cd.yml

Il contient deux jobs :

- test : installation des dépendances, lancement de Pytest et rapport de couverture ;
- deploy : synchronisation du dépôt vers Hugging Face Spaces.

## Secrets et variables

Le déploiement utilise :

- HF_TOKEN : secret GitHub contenant le token Hugging Face ;
- HF_SPACE_ID : variable GitHub contenant l'identifiant du Space Hugging Face.

Exemple de valeur pour HF_SPACE_ID :

VincentDesmouceaux/p5-ml-api-futurisys

## Règles de fusion

Avant de fusionner dans main :

- les tests doivent passer ;
- le code doit être relu ;
- la branche doit être à jour ;
- le déploiement ne doit être déclenché que depuis main.

## Vigilance

Le pipeline doit rester rapide.

Si l'exécution dépasse 10 minutes, il faudra analyser :

- le poids des dépendances ;
- le chargement du modèle ;
- la taille des données ;
- la complexité des tests.
