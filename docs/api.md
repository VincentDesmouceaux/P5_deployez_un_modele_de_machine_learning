# Documentation de l'API

## Objectif

Cette API expose un service de prédiction d'attrition des collaborateurs.

Elle est développée avec FastAPI et utilise Pydantic pour valider les données entrantes.

## Endpoints

### GET /health

Vérifie que l'API est disponible.

Réponse attendue :

{
  "status": "ok",
  "service": "p5-ml-api",
  "version": "0.3.0"
}

### GET /model-info

Retourne les informations principales sur le modèle exposé.

Informations retournées :

- nom du modèle ;
- version du modèle ;
- type du modèle ;
- cible prédite ;
- variables attendues.

### POST /predict

Retourne une prédiction d'attrition à partir des caractéristiques d'un collaborateur.

Exemple de payload :

{
  "satisfaction_level": 0.38,
  "last_evaluation": 0.86,
  "number_project": 6,
  "average_monthly_hours": 260,
  "time_spend_company": 4,
  "work_accident": false,
  "promotion_last_5years": false,
  "department": "technical",
  "salary": "low"
}

Exemple de réponse :

{
  "prediction": 1,
  "prediction_label": "leave",
  "probability_leave": 0.72,
  "model_name": "attrition-baseline-api",
  "model_version": "0.3.0"
}

## Validation des données

Les données sont validées avec Pydantic.

Exemples de règles :

- satisfaction_level doit être compris entre 0 et 1 ;
- last_evaluation doit être compris entre 0 et 1 ;
- number_project doit être compris entre 1 et 10 ;
- average_monthly_hours doit être compris entre 50 et 350 ;
- salary doit être low, medium ou high ;
- department doit appartenir à la liste des départements autorisés.

En cas de donnée invalide, l'API retourne une erreur HTTP 422.
