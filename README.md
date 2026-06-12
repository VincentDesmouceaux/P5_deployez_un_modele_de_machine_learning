## 🏗️ Architecture API, modèle ML et base de données

Ce projet expose un modèle de machine learning de prédiction d’attrition via une API **FastAPI**.

L’objectif est de proposer une architecture complète permettant :

* d’exposer un modèle de prédiction via une API REST ;
* de charger un modèle ML exporté au format `joblib` ;
* de stocker le dataset complet dans une base PostgreSQL locale ;
* de tracer systématiquement les inputs et outputs de chaque prédiction.

---

## 🧠 Modèle de machine learning

Le modèle utilisé est un **RandomForestClassifier** entraîné sur le dataset central du projet P4.

Il permet de prédire si un collaborateur est susceptible de quitter l’entreprise.

### Fichiers associés

* `scripts/train_export_model.py` : script d’entraînement et d’export du modèle ;
* `models/attrition_random_forest.joblib` : pipeline complet exporté ;
* `models/model_metadata.json` : métadonnées du modèle.

### Métriques obtenues sur le jeu de test

| Métrique  |  Score |
| --------- | -----: |
| Accuracy  | 0.8367 |
| Precision | 0.4865 |
| Recall    | 0.3830 |
| F1-score  | 0.4286 |
| ROC AUC   | 0.7975 |

---

## ⚡ API FastAPI

L’API expose les endpoints suivants :

| Endpoint      | Méthode | Description                                                                |
| ------------- | ------- | -------------------------------------------------------------------------- |
| `/health`     | GET     | Vérifie que l’API fonctionne                                               |
| `/model-info` | GET     | Retourne les informations du modèle chargé                                 |
| `/predict`    | POST    | Envoie les données d’un collaborateur au modèle et retourne une prédiction |

### Documentation interactive locale

```text
http://127.0.0.1:8000/docs
```

### Lancement local de l’API

```bash
python -m uvicorn app.main:app --reload
```

---

## 🐘 Base de données PostgreSQL

La base PostgreSQL est utilisée localement pour stocker le dataset complet et tracer les échanges entre l’API et le modèle.

Le schéma utilisé est :

```text
ml_api
```

### Scripts SQL

| Script                            | Rôle                                           |
| --------------------------------- | ---------------------------------------------- |
| `db/sql/01_create_database.sql`   | Création de la base PostgreSQL                 |
| `db/sql/02_create_tables.sql`     | Création du schéma et des tables               |
| `db/sql/03_load_dataset.sql`      | Insertion du dataset complet                   |
| `db/sql/04_check_database.sql`    | Vérification du contenu de la base             |
| `db/sql/05_trace_predictions.sql` | Vérification de la traçabilité des prédictions |

### Schéma de la base

* `docs/database_schema.mmd`

### Documentation détaillée

* `docs/database.md`
* `docs/model_loading.md`

---

## 🗂️ Tables principales

La base contient trois tables principales.

| Table                         | Description                                    |
| ----------------------------- | ---------------------------------------------- |
| `ml_api.employees_dataset`    | Contient le dataset complet des collaborateurs |
| `ml_api.prediction_requests`  | Stocke les inputs envoyés au modèle            |
| `ml_api.prediction_responses` | Stocke les outputs générés par le modèle       |

---

## 🔍 Traçabilité des prédictions

Chaque appel à `POST /predict` suit le flux suivant :

1. l’input envoyé à l’API est enregistré dans `prediction_requests` ;
2. le modèle de machine learning est appelé ;
3. l’output du modèle est enregistré dans `prediction_responses` ;
4. la réponse est retournée à l’utilisateur.

Cette logique garantit une traçabilité complète entre :

```text
API FastAPI → PostgreSQL → Modèle ML → PostgreSQL → Réponse API
```

### Exemple de vérification SQL

```bash
psql p5_ml_api -f db/sql/05_trace_predictions.sql
```

Exemple de résultat obtenu :

```text
request_id | prediction | prediction_label | probability_leave | model_name              | model_version
-----------|------------|------------------|-------------------|-------------------------|---------------
3          | 1          | leave            | 0.89550           | attrition-random-forest | 0.5.0
2          | 0          | stay             | 0.40030           | attrition-random-forest | 0.5.0
```

---

## ✅ Tests

Les tests sont exécutés avec :

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Résultat validé :

```text
6 passed
coverage 90%
```

---

## 🚀 Versions du projet

| Version             | Contenu                         |
| ------------------- | ------------------------------- |
| `v0.1.0` / `v0.1.1` | Structure initiale du projet    |
| `v0.2.0`            | Pipeline CI/CD                  |
| `v0.3.0`            | API FastAPI                     |
| `v0.4.0` / `v0.4.1` | PostgreSQL et traçabilité       |
| `v0.5.0`            | Chargement du modèle ML exporté |
