# Base de données PostgreSQL

## Objectif

Cette étape met en place une base PostgreSQL locale pour stocker le dataset complet du projet et assurer la traçabilité complète des échanges entre l'API FastAPI et le modèle de machine learning.

Toutes les interactions avec le modèle doivent passer par la base de données :

1. les inputs envoyés au modèle sont enregistrés dans une table dédiée ;
2. les outputs générés par le modèle sont enregistrés dans une table dédiée ;
3. chaque output est relié à l'input qui l'a produit grâce à une clé étrangère.

Cette architecture permet de conserver un historique complet des prédictions, de vérifier les données utilisées par le modèle et de garantir la cohérence entre les requêtes API et les réponses du modèle.

## Choix techniques

La base de données utilisée est PostgreSQL.

Pour cette étape, l'utilisation de PostgreSQL reste locale afin de simplifier l'installation, les tests et la démonstration.

La création de la base et des tables est réalisée avec des scripts SQL.

L'interaction applicative entre FastAPI et PostgreSQL sera ensuite gérée avec un connecteur Python, idéalement SQLAlchemy, afin d'enregistrer automatiquement les inputs et outputs de chaque prédiction.

## Base et schema

Nom de la base :

p5_ml_api

Nom du schema PostgreSQL :

ml_api

## Scripts SQL

Les scripts SQL sont stockés dans le dossier :

db/sql/

Les scripts sont :

01_create_database.sql : création de la base PostgreSQL p5_ml_api
02_create_tables.sql : création du schema et des tables
03_load_dataset.sql : chargement du dataset CSV dans PostgreSQL
04_check_database.sql : vérification du contenu de la base

## Tables

### ml_api.employees_dataset

Cette table contient le dataset complet d'attrition des collaborateurs.

Elle contient les variables explicatives du modèle ainsi que la variable cible left_company.

Colonnes principales :

- employee_id : identifiant technique
- satisfaction_level : niveau de satisfaction
- last_evaluation : dernière évaluation
- number_project : nombre de projets
- average_monthly_hours : heures moyennes mensuelles
- time_spend_company : ancienneté dans l'entreprise
- work_accident : accident du travail
- left_company : variable cible indiquant le départ
- promotion_last_5years : promotion récente
- department : département
- salary : niveau de salaire
- created_at : date d'insertion

### ml_api.prediction_requests

Cette table enregistre les inputs envoyés à l'endpoint /predict.

Chaque appel à l'API devra créer une ligne dans cette table avant ou pendant l'appel au modèle.

Elle contient :

- request_id : identifiant de la requête
- created_at : date de la requête
- source : origine de la requête
- toutes les variables envoyées au modèle
- raw_payload : payload JSON brut envoyé à l'API

### ml_api.prediction_responses

Cette table enregistre les outputs générés par le modèle.

Chaque réponse est reliée à une requête via request_id.

Elle contient :

- response_id : identifiant de la réponse
- request_id : clé étrangère vers prediction_requests
- created_at : date de la réponse
- prediction : classe prédite, 0 ou 1
- prediction_label : libellé métier, stay ou leave
- probability_leave : probabilité estimée de départ
- model_name : nom du modèle utilisé
- model_version : version du modèle utilisé
- raw_output : réponse JSON brute

## Schéma relationnel simplifié

employees_dataset
- employee_id PK

prediction_requests
- request_id PK

prediction_responses
- response_id PK
- request_id FK vers prediction_requests.request_id

Relation principale :

prediction_requests 1 --- 1 prediction_responses

Cela signifie qu'une requête de prédiction génère une réponse de prédiction.

## Ordre d'exécution des scripts SQL

1. Créer la base :

psql postgres -f db/sql/01_create_database.sql

2. Créer les tables :

psql p5_ml_api -f db/sql/02_create_tables.sql

3. Charger le dataset :

psql p5_ml_api -f db/sql/03_load_dataset.sql

4. Vérifier le contenu :

psql p5_ml_api -f db/sql/04_check_database.sql

## Dataset attendu

Le script de chargement attend le fichier suivant :

data/employee_attrition.csv

Ce fichier n'est pas versionné dans Git car les fichiers CSV sont ignorés par le .gitignore.

Le dataset doit contenir les colonnes suivantes :

- satisfaction_level
- last_evaluation
- number_project
- average_monthly_hours
- time_spend_company
- work_accident
- left_company
- promotion_last_5years
- department
- salary

## Traçabilité complète

Le flux attendu est le suivant :

1. L'utilisateur appelle l'endpoint /predict.
2. L'API valide les données avec Pydantic.
3. L'API enregistre l'input dans prediction_requests.
4. Le modèle génère une prédiction.
5. L'API enregistre l'output dans prediction_responses.
6. L'API retourne la prédiction à l'utilisateur.

Ainsi, toutes les interactions avec le modèle sont historisées dans PostgreSQL.

## Sécurité

Les informations de connexion à la base ne doivent pas être écrites directement dans le code.

Elles seront stockées dans un fichier .env ignoré par Git.

Exemple :

DATABASE_URL=postgresql://localhost:5432/p5_ml_api

Points de vigilance :

- ne pas versionner les identifiants de connexion ;
- ne pas versionner le dataset complet s'il contient des données sensibles ;
- garantir la cohérence entre les inputs enregistrés et les outputs générés ;
- utiliser des transactions lors de l'enregistrement des prédictions ;
- vérifier que chaque prédiction possède bien un request_id.

## Résultat attendu

À la fin de l'étape, le projet doit contenir :

- un schéma PostgreSQL documenté ;
- des scripts SQL de création de base et de tables ;
- un script SQL de chargement du dataset ;
- des tables dédiées à la traçabilité des inputs et outputs ;
- une documentation claire de l'architecture base de données ;
- une base prête à être connectée à l'API FastAPI.

## Schéma relationnel

Le schéma relationnel de la base est disponible dans le fichier suivant :

docs/database_schema.mmd

Ce schéma montre les trois tables principales :

- employees_dataset : stockage du dataset complet ;
- prediction_requests : stockage des inputs envoyés au modèle ;
- prediction_responses : stockage des outputs générés par le modèle.

La table prediction_requests est reliée au dataset via employee_id lorsque l'input correspond à un collaborateur existant.

La table prediction_responses est reliée à prediction_requests via request_id.

Cette structure garantit la traçabilité complète entre une requête API, les données envoyées au modèle et la prédiction retournée.

## Connexion Python avec SQLAlchemy

L'application utilise SQLAlchemy pour se connecter à PostgreSQL.

La connexion est centralisée dans :

app/database.py

L'enregistrement des inputs et outputs est centralisé dans :

app/services/prediction_log_service.py

Le endpoint POST /predict suit maintenant ce flux :

1. réception de l'input API ;
2. enregistrement de l'input dans prediction_requests ;
3. appel du modèle de machine learning ;
4. enregistrement de l'output dans prediction_responses ;
5. retour de la prédiction à l'utilisateur.

Ainsi, toutes les interactions avec le modèle passent bien par la base de données.

## Variables d'environnement

Le fichier .env contient la connexion locale à PostgreSQL.

Il n'est pas versionné afin d'éviter de publier des informations sensibles.

Un fichier .env.example est fourni pour documenter la variable attendue :

DATABASE_URL=postgresql://localhost:5432/p5_ml_api

## Script de traçabilité

Le fichier suivant permet de vérifier les dernières prédictions enregistrées :

db/sql/05_trace_predictions.sql

Il joint les tables prediction_requests et prediction_responses afin de retrouver, pour chaque prédiction :

- l'input envoyé ;
- l'output retourné ;
- la date de création ;
- le modèle utilisé ;
- la version du modèle.
