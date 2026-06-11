# Standards de code et d'expérimentation ML

## Objectif

Ce document définit les règles techniques du projet P5.

L'objectif est de garantir un code lisible, testable, maintenable et déployable.

## Standards de code

Le code doit respecter les principes suivants :

- fonctions courtes et compréhensibles ;
- noms explicites ;
- séparation claire entre API, logique métier, modèle ML et base de données ;
- aucune donnée sensible dans le code ;
- aucune clé API dans le dépôt Git ;
- tests associés aux fonctionnalités critiques.

## Organisation du code

Le dossier app contient le code FastAPI.

Le dossier tests contient les tests Pytest.

Le dossier db contient les scripts SQL.

Le dossier models contient les modèles exportés.

Le dossier docs contient la documentation technique.

## Standards ML

Pour chaque modèle utilisé en production, il faut documenter :

- la source des données ;
- les variables utilisées ;
- le preprocessing ;
- la métrique principale ;
- les limites du modèle ;
- le format d'entrée attendu ;
- le format de sortie retourné par l'API.

## Expérimentations

Les expérimentations doivent être reproductibles.

Chaque expérimentation importante doit préciser :

- la version du dataset ;
- la version du code ;
- les paramètres du modèle ;
- les métriques obtenues ;
- la date de l'expérimentation.

## Déploiement

Le modèle ne doit être exposé que via une API testée.

Avant déploiement :

- les tests doivent réussir ;
- le modèle doit être chargeable ;
- l'endpoint de prédiction doit être documenté ;
- les erreurs doivent être gérées proprement.
