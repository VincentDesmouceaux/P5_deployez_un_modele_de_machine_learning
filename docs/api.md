# ⚡ Documentation API — P5 ML API Futurisys

## Objectif

Cette documentation décrit l’API REST du projet **P5 — Déployez un modèle de Machine Learning**.

L’API permet :

* de vérifier l’état du service ;
* de consulter les métadonnées du modèle chargé ;
* d’envoyer un profil collaborateur au modèle de machine learning ;
* de récupérer une prédiction d’attrition ;
* de retourner une probabilité estimée de départ ;
* de tracer les inputs et outputs de prédiction dans PostgreSQL en environnement local.

L’API est développée avec **FastAPI**.
La documentation interactive est générée automatiquement avec **Swagger/OpenAPI**.

---

## 1. URLs disponibles

### URL locale

Après lancement local de l’API :

```bash
python -m uvicorn app.main:app --reload
```

L’API est disponible ici :

```text
http://127.0.0.1:8000
```

Documentation Swagger locale :

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON local :

```text
http://127.0.0.1:8000/openapi.json
```

---

### URL déployée sur Hugging Face Spaces

L’API est également déployée sur Hugging Face Spaces :

```text
https://thecruiser-p5-ml-api-futurisys.hf.space
```

Documentation Swagger en ligne :

```text
https://thecruiser-p5-ml-api-futurisys.hf.space/docs
```

OpenAPI JSON en ligne :

```text
https://thecruiser-p5-ml-api-futurisys.hf.space/openapi.json
```

---

## 2. Endpoints disponibles

| Endpoint      | Méthode | Description                                                            |
| ------------- | ------- | ---------------------------------------------------------------------- |
| `/`           | GET     | Redirige vers la documentation Swagger                                 |
| `/health`     | GET     | Vérifie que l’API fonctionne                                           |
| `/model-info` | GET     | Retourne les informations du modèle chargé                             |
| `/predict`    | POST    | Retourne une prédiction d’attrition à partir d’un profil collaborateur |

---

# 3. Endpoint `/`

## Description

L’endpoint `/` sert de point d’entrée simple vers l’API.

Il redirige automatiquement vers la documentation Swagger afin de faciliter l’utilisation de l’API par un développeur ou un utilisateur technique.

## Méthode

```text
GET
```

## URL locale

```text
http://127.0.0.1:8000/
```

## Commande de test

```bash
curl http://127.0.0.1:8000/
```

## Résultat attendu

L’utilisateur est redirigé vers :

```text
/docs
```

---

# 4. Endpoint `/health`

## Description

L’endpoint `/health` permet de vérifier que l’API est disponible.

Il est utile pour :

* contrôler que le serveur FastAPI est lancé ;
* vérifier que le service répond ;
* intégrer un contrôle de disponibilité dans la CI/CD ;
* tester rapidement l’API locale ou déployée.

## Méthode

```text
GET
```

## URL locale

```text
http://127.0.0.1:8000/health
```

## Commande locale

```bash
curl http://127.0.0.1:8000/health
```

## Commande sur Hugging Face Spaces

```bash
curl https://thecruiser-p5-ml-api-futurisys.hf.space/health
```

## Exemple de réponse

```json
{
  "status": "ok",
  "service": "p5-ml-api",
  "version": "0.5.0"
}
```

## Description des champs

| Champ     | Type   | Description                 |
| --------- | ------ | --------------------------- |
| `status`  | string | État du service             |
| `service` | string | Nom technique de l’API      |
| `version` | string | Version applicative exposée |

## Code HTTP attendu

| Code  | Signification                 |
| ----- | ----------------------------- |
| `200` | L’API fonctionne correctement |

---

# 5. Endpoint `/model-info`

## Description

L’endpoint `/model-info` retourne les métadonnées du modèle de machine learning chargé dans l’API.

Il permet de vérifier :

* le nom du modèle ;
* la version du modèle ;
* le type d’algorithme utilisé ;
* la variable cible ;
* la description du modèle ;
* la liste des variables d’entrée attendues.

Cet endpoint est important pour garantir que l’API utilise bien le modèle attendu.

## Méthode

```text
GET
```

## URL locale

```text
http://127.0.0.1:8000/model-info
```

## Commande locale

```bash
curl http://127.0.0.1:8000/model-info
```

## Commande sur Hugging Face Spaces

```bash
curl https://thecruiser-p5-ml-api-futurisys.hf.space/model-info
```

## Exemple de réponse

```json
{
  "model_name": "attrition-random-forest",
  "model_version": "0.5.0",
  "model_type": "RandomForestClassifier",
  "target": "attrition_bin",
  "description": "Modèle Random Forest entraîné sur le dataset central du projet P4 pour prédire l'attrition des collaborateurs.",
  "input_features": [
    "age",
    "genre",
    "revenu_mensuel",
    "statut_marital",
    "departement",
    "poste",
    "nombre_experiences_precedentes",
    "nombre_heures_travailless",
    "annee_experience_totale",
    "annees_dans_l_entreprise",
    "annees_dans_le_poste_actuel",
    "satisfaction_employee_environnement",
    "note_evaluation_precedente",
    "niveau_hierarchique_poste",
    "satisfaction_employee_nature_travail",
    "satisfaction_employee_equipe",
    "satisfaction_employee_equilibre_pro_perso",
    "note_evaluation_actuelle",
    "heure_supplementaires",
    "augementation_salaire_precedente",
    "nombre_participation_pee",
    "nb_formations_suivies",
    "nombre_employee_sous_responsabilite",
    "distance_domicile_travail",
    "niveau_education",
    "domaine_etude",
    "ayant_enfants",
    "frequence_deplacement",
    "annees_depuis_la_derniere_promotion",
    "annes_sous_responsable_actuel"
  ]
}
```

## Description des champs

| Champ            | Type         | Description                                 |
| ---------------- | ------------ | ------------------------------------------- |
| `model_name`     | string       | Nom technique du modèle                     |
| `model_version`  | string       | Version du modèle chargé                    |
| `model_type`     | string       | Algorithme utilisé                          |
| `target`         | string       | Variable cible prédite                      |
| `description`    | string       | Description fonctionnelle du modèle         |
| `input_features` | list[string] | Liste des variables attendues par le modèle |

## Code HTTP attendu

| Code  | Signification                             |
| ----- | ----------------------------------------- |
| `200` | Les métadonnées du modèle sont retournées |

---

# 6. Endpoint `/predict`

## Description

L’endpoint `/predict` est l’endpoint principal de l’API.

Il reçoit un profil collaborateur au format JSON, applique la validation Pydantic, appelle le modèle de machine learning, puis retourne une prédiction d’attrition.

Le flux de traitement est le suivant :

```text
Payload JSON
   ↓
Validation Pydantic
   ↓
Transformation en format attendu par le modèle
   ↓
Prédiction avec le RandomForestClassifier
   ↓
Application du seuil de décision
   ↓
Réponse API
   ↓
Traçabilité PostgreSQL en environnement local
```

## Méthode

```text
POST
```

## URL locale

```text
http://127.0.0.1:8000/predict
```

## Headers attendus

```text
Content-Type: application/json
```

---

## 7. Payload attendu pour `/predict`

Le payload doit contenir les 30 variables attendues par le modèle.

```json
{
  "age": 41,
  "genre": "F",
  "revenu_mensuel": 5993,
  "statut_marital": "Célibataire",
  "departement": "Commercial",
  "poste": "Cadre Commercial",
  "nombre_experiences_precedentes": 8,
  "nombre_heures_travailless": 80,
  "annee_experience_totale": 8,
  "annees_dans_l_entreprise": 6,
  "annees_dans_le_poste_actuel": 4,
  "satisfaction_employee_environnement": 2,
  "note_evaluation_precedente": 3,
  "niveau_hierarchique_poste": 2,
  "satisfaction_employee_nature_travail": 4,
  "satisfaction_employee_equipe": 1,
  "satisfaction_employee_equilibre_pro_perso": 1,
  "note_evaluation_actuelle": 3,
  "heure_supplementaires": "Oui",
  "augementation_salaire_precedente": 11,
  "nombre_participation_pee": 0,
  "nb_formations_suivies": 0,
  "nombre_employee_sous_responsabilite": 0,
  "distance_domicile_travail": 1,
  "niveau_education": 2,
  "domaine_etude": "Sciences de la Vie",
  "ayant_enfants": "Y",
  "frequence_deplacement": "Occasionnel",
  "annees_depuis_la_derniere_promotion": 0,
  "annes_sous_responsable_actuel": 5
}
```

---

## 8. Description des champs d’entrée

| Champ                                       | Type attendu | Description                                                 |
| ------------------------------------------- | ------------ | ----------------------------------------------------------- |
| `age`                                       | integer      | Âge du collaborateur                                        |
| `genre`                                     | string       | Genre du collaborateur                                      |
| `revenu_mensuel`                            | integer      | Revenu mensuel                                              |
| `statut_marital`                            | string       | Situation familiale                                         |
| `departement`                               | string       | Département du collaborateur                                |
| `poste`                                     | string       | Poste occupé                                                |
| `nombre_experiences_precedentes`            | integer      | Nombre d’expériences professionnelles précédentes           |
| `nombre_heures_travailless`                 | integer      | Volume horaire travaillé                                    |
| `annee_experience_totale`                   | integer      | Nombre total d’années d’expérience                          |
| `annees_dans_l_entreprise`                  | integer      | Ancienneté dans l’entreprise                                |
| `annees_dans_le_poste_actuel`               | integer      | Ancienneté dans le poste actuel                             |
| `satisfaction_employee_environnement`       | integer      | Score de satisfaction lié à l’environnement                 |
| `note_evaluation_precedente`                | integer      | Note d’évaluation précédente                                |
| `niveau_hierarchique_poste`                 | integer      | Niveau hiérarchique du poste                                |
| `satisfaction_employee_nature_travail`      | integer      | Score de satisfaction lié à la nature du travail            |
| `satisfaction_employee_equipe`              | integer      | Score de satisfaction lié à l’équipe                        |
| `satisfaction_employee_equilibre_pro_perso` | integer      | Score d’équilibre vie professionnelle / personnelle         |
| `note_evaluation_actuelle`                  | integer      | Note d’évaluation actuelle                                  |
| `heure_supplementaires`                     | string       | Indique si le collaborateur fait des heures supplémentaires |
| `augementation_salaire_precedente`          | integer      | Pourcentage d’augmentation précédente                       |
| `nombre_participation_pee`                  | integer      | Nombre de participations au PEE                             |
| `nb_formations_suivies`                     | integer      | Nombre de formations suivies                                |
| `nombre_employee_sous_responsabilite`       | integer      | Nombre d’employés sous responsabilité                       |
| `distance_domicile_travail`                 | integer      | Distance domicile-travail                                   |
| `niveau_education`                          | integer      | Niveau d’éducation                                          |
| `domaine_etude`                             | string       | Domaine d’étude                                             |
| `ayant_enfants`                             | string       | Indique si le collaborateur a des enfants                   |
| `frequence_deplacement`                     | string       | Fréquence des déplacements                                  |
| `annees_depuis_la_derniere_promotion`       | integer      | Années depuis la dernière promotion                         |
| `annes_sous_responsable_actuel`             | integer      | Années sous le responsable actuel                           |

---

## 9. Commande locale complète pour `/predict`

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 41,
    "genre": "F",
    "revenu_mensuel": 5993,
    "statut_marital": "Célibataire",
    "departement": "Commercial",
    "poste": "Cadre Commercial",
    "nombre_experiences_precedentes": 8,
    "nombre_heures_travailless": 80,
    "annee_experience_totale": 8,
    "annees_dans_l_entreprise": 6,
    "annees_dans_le_poste_actuel": 4,
    "satisfaction_employee_environnement": 2,
    "note_evaluation_precedente": 3,
    "niveau_hierarchique_poste": 2,
    "satisfaction_employee_nature_travail": 4,
    "satisfaction_employee_equipe": 1,
    "satisfaction_employee_equilibre_pro_perso": 1,
    "note_evaluation_actuelle": 3,
    "heure_supplementaires": "Oui",
    "augementation_salaire_precedente": 11,
    "nombre_participation_pee": 0,
    "nb_formations_suivies": 0,
    "nombre_employee_sous_responsabilite": 0,
    "distance_domicile_travail": 1,
    "niveau_education": 2,
    "domaine_etude": "Sciences de la Vie",
    "ayant_enfants": "Y",
    "frequence_deplacement": "Occasionnel",
    "annees_depuis_la_derniere_promotion": 0,
    "annes_sous_responsable_actuel": 5
  }'
```

---

## 10. Exemple de réponse `/predict`

```json
{
  "prediction": 1,
  "prediction_label": "leave",
  "probability_leave": 0.8955,
  "model_name": "attrition-random-forest",
  "model_version": "0.5.0"
}
```

## Description des champs de sortie

| Champ               | Type    | Description                     |
| ------------------- | ------- | ------------------------------- |
| `prediction`        | integer | Classe prédite par le modèle    |
| `prediction_label`  | string  | Libellé métier de la prédiction |
| `probability_leave` | float   | Probabilité estimée de départ   |
| `model_name`        | string  | Nom du modèle utilisé           |
| `model_version`     | string  | Version du modèle utilisé       |

---

## 11. Règle de décision

Le modèle retourne une probabilité de départ appelée :

```text
probability_leave
```

La classe finale est calculée avec le seuil suivant :

```text
probability_leave >= 0.5 → prediction = 1 → leave
probability_leave < 0.5  → prediction = 0 → stay
```

Interprétation métier :

| Valeur | Libellé | Interprétation                                                     |
| ------ | ------- | ------------------------------------------------------------------ |
| `0`    | `stay`  | Le collaborateur est prédit comme restant dans l’entreprise        |
| `1`    | `leave` | Le collaborateur est prédit comme risquant de quitter l’entreprise |

---

## 12. Codes de réponse HTTP

| Code HTTP | Signification                                      |
| --------- | -------------------------------------------------- |
| `200`     | Requête valide, prédiction retournée               |
| `422`     | Payload invalide, champ manquant ou type incorrect |
| `500`     | Erreur serveur non prévue                          |

---

# 13. Gestion des erreurs `422`

FastAPI et Pydantic valident automatiquement les données entrantes.

Une erreur `422 Unprocessable Entity` peut apparaître dans plusieurs cas :

* champ obligatoire absent ;
* type incorrect ;
* valeur hors limites ;
* payload JSON mal formé ;
* donnée catégorielle incompatible avec le schéma attendu.

---

## Exemple : champ obligatoire manquant

Si le champ suivant est absent :

```text
departement
```

l’API retourne une erreur `422`.

Exemple de réponse simplifiée :

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "departement"],
      "msg": "Field required"
    }
  ]
}
```

---

## Exemple : âge invalide

Si l’âge est inférieur à la limite attendue :

```json
{
  "age": 12
}
```

l’API retourne une erreur `422`.

---

## Exemple : mauvais type de donnée

Si le champ suivant reçoit une valeur non numérique :

```json
{
  "revenu_mensuel": "abc"
}
```

l’API retourne une erreur `422`.

---

# 14. Traçabilité PostgreSQL

En environnement local, chaque appel valide à :

```text
POST /predict
```

est tracé dans PostgreSQL.

Deux tables sont utilisées :

| Table                         | Rôle                                 |
| ----------------------------- | ------------------------------------ |
| `ml_api.prediction_requests`  | Stocke l’input envoyé à l’API        |
| `ml_api.prediction_responses` | Stocke l’output généré par le modèle |

La vue suivante permet de relier les inputs et outputs :

```text
ml_api.v_prediction_traces
```

---

## Vérifier les traces

```bash
psql p5_ml_api -f db/sql/07_visualize_prediction_traces.sql
```

## Exemple de résultat

```text
request_id | response_id | prediction | prediction_label | probability_leave | model_name              | model_version
3          | 3           | 1          | leave            | 0.89550           | attrition-random-forest | 0.5.0
2          | 2           | 0          | stay             | 0.40030           | attrition-random-forest | 0.5.0
1          | 1           | 1          | leave            | 0.74450           | attrition-baseline-api  | 0.3.0
```

---

# 15. Générer plusieurs prédictions de démonstration

Le script suivant envoie automatiquement plusieurs lignes du dataset à l’API :

```bash
python scripts/generate_demo_predictions.py
```

Par défaut, il envoie les 20 premières lignes du dataset.

Pour choisir un autre nombre :

```bash
DEMO_LIMIT=50 python scripts/generate_demo_predictions.py
```

Avant d’exécuter ce script, l’API doit être lancée :

```bash
python -m uvicorn app.main:app --reload
```

---

# 16. Tests liés à l’API

Les tests liés à l’API sont répartis dans plusieurs fichiers.

| Fichier                        | Rôle                                                           |
| ------------------------------ | -------------------------------------------------------------- |
| `tests/test_health.py`         | Vérifie l’endpoint `/health`                                   |
| `tests/test_prediction.py`     | Vérifie `/model-info`, `/predict` et les erreurs de validation |
| `tests/test_functional_api.py` | Vérifie le parcours complet `/health → /model-info → /predict` |
| `tests/test_schemas.py`        | Vérifie les schémas Pydantic utilisés par l’API                |

---

## Lancer les tests API

```bash
python -m pytest tests/test_health.py tests/test_prediction.py tests/test_functional_api.py
```

## Lancer toute la suite de tests

```bash
python -m pytest
```

## Lancer les tests avec couverture

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Résultat validé :

```text
24 passed
coverage 98%
```

---

# 17. Documentation Swagger/OpenAPI

FastAPI génère automatiquement une documentation interactive.

## Swagger UI

```text
/docs
```

## OpenAPI JSON

```text
/openapi.json
```

En local :

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/openapi.json
```

Sur Hugging Face Spaces :

```text
https://thecruiser-p5-ml-api-futurisys.hf.space/docs
https://thecruiser-p5-ml-api-futurisys.hf.space/openapi.json
```

---

# 18. Commandes opérationnelles API

## Lancer l’API

```bash
python -m uvicorn app.main:app --reload
```

## Ouvrir Swagger

```bash
open http://127.0.0.1:8000/docs
```

## Tester `/health`

```bash
curl http://127.0.0.1:8000/health
```

## Tester `/model-info`

```bash
curl http://127.0.0.1:8000/model-info
```

## Tester `/predict`

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 41,
    "genre": "F",
    "revenu_mensuel": 5993,
    "statut_marital": "Célibataire",
    "departement": "Commercial",
    "poste": "Cadre Commercial",
    "nombre_experiences_precedentes": 8,
    "nombre_heures_travailless": 80,
    "annee_experience_totale": 8,
    "annees_dans_l_entreprise": 6,
    "annees_dans_le_poste_actuel": 4,
    "satisfaction_employee_environnement": 2,
    "note_evaluation_precedente": 3,
    "niveau_hierarchique_poste": 2,
    "satisfaction_employee_nature_travail": 4,
    "satisfaction_employee_equipe": 1,
    "satisfaction_employee_equilibre_pro_perso": 1,
    "note_evaluation_actuelle": 3,
    "heure_supplementaires": "Oui",
    "augementation_salaire_precedente": 11,
    "nombre_participation_pee": 0,
    "nb_formations_suivies": 0,
    "nombre_employee_sous_responsabilite": 0,
    "distance_domicile_travail": 1,
    "niveau_education": 2,
    "domaine_etude": "Sciences de la Vie",
    "ayant_enfants": "Y",
    "frequence_deplacement": "Occasionnel",
    "annees_depuis_la_derniere_promotion": 0,
    "annes_sous_responsable_actuel": 5
  }'
```

## Tester l’API déployée

```bash
curl https://thecruiser-p5-ml-api-futurisys.hf.space/health
open https://thecruiser-p5-ml-api-futurisys.hf.space/docs
```

---

# 19. Résumé

L’API FastAPI fournit une interface REST complète pour exploiter le modèle de machine learning.

Elle permet de :

* vérifier l’état du service ;
* consulter les informations du modèle ;
* envoyer un profil collaborateur ;
* obtenir une prédiction d’attrition ;
* consulter la probabilité estimée de départ ;
* documenter automatiquement les endpoints avec Swagger/OpenAPI ;
* tracer les prédictions en base PostgreSQL en environnement local.
