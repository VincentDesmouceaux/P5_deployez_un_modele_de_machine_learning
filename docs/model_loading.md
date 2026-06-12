# Chargement du modèle de machine learning

## Objectif

Cette étape remplace le modèle de référence provisoire par un modèle Random Forest réellement entraîné sur le dataset central du projet P4.

Le modèle est exporté au format joblib afin d'être chargé directement par l'API FastAPI.

## Fichiers générés

- models/attrition_random_forest.joblib
- models/model_metadata.json

## Script d'entraînement

Le script suivant entraîne et exporte le modèle :

- scripts/train_export_model.py

Il réalise les étapes suivantes :

1. chargement du dataset central ;
2. séparation des variables explicatives et de la cible ;
3. préparation des variables numériques et catégorielles ;
4. entraînement d'un RandomForestClassifier ;
5. calcul des métriques de test ;
6. export du pipeline complet ;
7. export des métadonnées du modèle.

## Résultats du modèle

Le modèle entraîné est un Random Forest.

Métriques obtenues sur le jeu de test :

- accuracy : 0.8367
- precision : 0.4865
- recall : 0.3830
- f1-score : 0.4286
- roc_auc : 0.7975

## Chargement dans l'API

Le service FastAPI charge le modèle exporté depuis le dossier models.

Le modèle reçoit les données d'entrée, génère une prédiction, puis retourne :

- la classe prédite ;
- le libellé métier ;
- la probabilité estimée de départ ;
- le nom du modèle ;
- la version du modèle.

## Traçabilité

Chaque appel à /predict suit ce flux :

1. l'input API est enregistré dans PostgreSQL ;
2. le modèle génère une prédiction ;
3. l'output du modèle est enregistré dans PostgreSQL ;
4. la réponse est retournée à l'utilisateur.

Cette logique garantit la traçabilité complète entre l'API, le modèle et la base de données.
