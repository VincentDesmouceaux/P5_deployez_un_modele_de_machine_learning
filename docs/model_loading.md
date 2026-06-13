# 🧠 Documentation technique du modèle de machine learning

## Objectif

Cette documentation décrit le modèle de machine learning utilisé dans le projet **P5 — Déployez un modèle de Machine Learning**.

Elle couvre :

* le modèle utilisé ;
* les fichiers exportés ;
* les variables d’entrée ;
* la variable cible ;
* les performances obtenues ;
* le chargement du modèle dans l’API FastAPI ;
* les limites connues ;
* le protocole de maintenance ;
* le protocole de réentraînement ;
* le versioning du modèle.

L’objectif est de permettre à un utilisateur technique ou à un développeur de comprendre, utiliser, maintenir et faire évoluer le modèle.

---

## 1. Vue d’ensemble du modèle

Le modèle utilisé est un **RandomForestClassifier** entraîné sur le dataset central du projet P4.

Il permet d’estimer le risque d’attrition d’un collaborateur.

La prédiction retournée par l’API correspond à deux classes :

```text
0 → stay
1 → leave
```

Le modèle retourne également une probabilité :

```text
probability_leave
```

Cette probabilité représente le risque estimé que le collaborateur quitte l’entreprise.

---

## 2. Choix technique du modèle

Le modèle retenu est un **Random Forest**.

Ce choix est justifié par plusieurs raisons :

* il fonctionne bien sur des données tabulaires ;
* il gère efficacement les relations non linéaires ;
* il est robuste aux interactions entre variables ;
* il limite le surapprentissage par agrégation de plusieurs arbres ;
* il nécessite moins de préparation qu’un modèle linéaire strict ;
* il permet de produire rapidement un modèle fiable pour une API de prédiction ;
* il reste plus interprétable qu’un modèle de type réseau de neurones.

Dans ce projet, le modèle est utilisé comme outil d’aide à l’analyse du risque d’attrition, et non comme outil de décision automatique.

---

## 3. Dataset utilisé

Le modèle est entraîné à partir du dataset central issu du projet P4.

Fichier utilisé dans ce projet :

```text
data/employee_attrition.csv
```

Ce dataset contient des informations RH relatives aux collaborateurs :

* informations démographiques ;
* poste et département ;
* revenu mensuel ;
* ancienneté ;
* satisfaction ;
* formation ;
* équilibre professionnel / personnel ;
* distance domicile-travail ;
* historique professionnel ;
* variable cible d’attrition.

---

## 4. Variable cible

La variable cible utilisée pour l’entraînement est :

```text
attrition_bin
```

Elle encode la situation du collaborateur :

```text
0 → le collaborateur reste dans l’entreprise
1 → le collaborateur quitte l’entreprise
```

Dans la réponse API, cette cible est traduite en libellé métier :

```text
0 → stay
1 → leave
```

---

## 5. Variables d’entrée du modèle

Le modèle utilise 30 variables d’entrée.

Ces variables sont exposées par l’endpoint :

```text
GET /model-info
```

Liste des variables attendues :

```text
age
genre
revenu_mensuel
statut_marital
departement
poste
nombre_experiences_precedentes
nombre_heures_travailless
annee_experience_totale
annees_dans_l_entreprise
annees_dans_le_poste_actuel
satisfaction_employee_environnement
note_evaluation_precedente
niveau_hierarchique_poste
satisfaction_employee_nature_travail
satisfaction_employee_equipe
satisfaction_employee_equilibre_pro_perso
note_evaluation_actuelle
heure_supplementaires
augementation_salaire_precedente
nombre_participation_pee
nb_formations_suivies
nombre_employee_sous_responsabilite
distance_domicile_travail
niveau_education
domaine_etude
ayant_enfants
frequence_deplacement
annees_depuis_la_derniere_promotion
annes_sous_responsable_actuel
```

Ces variables doivent être fournies à l’API dans le payload JSON de l’endpoint :

```text
POST /predict
```

---

## 6. Préparation des données

Le script d’entraînement applique une préparation adaptée aux données tabulaires.

Les étapes principales sont :

1. chargement du dataset ;
2. séparation entre les variables explicatives et la cible ;
3. identification des variables numériques ;
4. identification des variables catégorielles ;
5. encodage des variables catégorielles ;
6. entraînement du modèle Random Forest ;
7. évaluation du modèle ;
8. export du pipeline complet ;
9. export des métadonnées.

Le pipeline exporté contient donc la logique de transformation et le modèle entraîné.

Cela évite de devoir reproduire manuellement le prétraitement dans l’API.

---

## 7. Script d’entraînement

Le script principal d’entraînement est :

```text
scripts/train_export_model.py
```

Pour réentraîner le modèle :

```bash
python scripts/train_export_model.py
```

Ce script génère ou met à jour les fichiers suivants :

```text
models/attrition_random_forest.joblib
models/model_metadata.json
```

---

## 8. Fichiers du modèle

| Fichier                                 | Rôle                                                                          |
| --------------------------------------- | ----------------------------------------------------------------------------- |
| `models/attrition_random_forest.joblib` | Pipeline complet exporté avec le prétraitement et le modèle                   |
| `models/model_metadata.json`            | Métadonnées du modèle                                                         |
| `scripts/train_export_model.py`         | Script d’entraînement et d’export                                             |
| `app/services/model_service.py`         | Service applicatif chargé de charger le modèle et de produire les prédictions |

---

## 9. Métadonnées du modèle

Les métadonnées sont stockées dans :

```text
models/model_metadata.json
```

Elles permettent de documenter :

* le nom du modèle ;
* la version du modèle ;
* le type de modèle ;
* la variable cible ;
* la description ;
* la liste des variables d’entrée ;
* les métriques obtenues.

Ces informations sont exposées par l’API via :

```text
GET /model-info
```

Commande de vérification :

```bash
curl http://127.0.0.1:8000/model-info
```

---

## 10. Performances du modèle

Les métriques obtenues sur le jeu de test sont les suivantes :

| Métrique  |  Score |
| --------- | -----: |
| Accuracy  | 0.8367 |
| Precision | 0.4865 |
| Recall    | 0.3830 |
| F1-score  | 0.4286 |
| ROC AUC   | 0.7975 |

---

## 11. Interprétation des métriques

### Accuracy

L’accuracy mesure la proportion totale de prédictions correctes.

Dans ce projet :

```text
accuracy = 0.8367
```

Cela indique que le modèle classe correctement une majorité d’observations.

### Precision

La precision mesure la proportion de prédictions positives réellement correctes.

Dans ce projet :

```text
precision = 0.4865
```

Cela signifie que parmi les collaborateurs prédits comme risquant de partir, environ 48,65 % appartiennent réellement à la classe d’attrition dans le jeu de test.

### Recall

Le recall mesure la capacité du modèle à retrouver les vrais cas d’attrition.

Dans ce projet :

```text
recall = 0.3830
```

Cela indique que le modèle détecte environ 38,30 % des collaborateurs ayant réellement quitté l’entreprise dans le jeu de test.

### F1-score

Le F1-score combine precision et recall.

Dans ce projet :

```text
f1-score = 0.4286
```

Il permet d’évaluer l’équilibre entre les faux positifs et les faux négatifs.

### ROC AUC

Le ROC AUC mesure la capacité du modèle à séparer les deux classes.

Dans ce projet :

```text
roc_auc = 0.7975
```

Ce score indique que le modèle distingue correctement les collaborateurs à risque de départ des collaborateurs qui restent.

---

## 12. Analyse des limites

Les performances doivent être interprétées avec prudence.

La classe d’attrition est minoritaire dans le dataset, ce qui explique :

* une precision inférieure à l’accuracy ;
* un recall limité ;
* un F1-score modéré.

Le modèle est donc utile comme outil d’aide à l’analyse du risque, mais il ne doit pas être utilisé comme décision automatique.

Les prédictions doivent être interprétées dans un contexte métier plus large.

---

## 13. Règle de décision

Le modèle retourne une probabilité de départ :

```text
probability_leave
```

La classe finale est déterminée avec le seuil suivant :

```text
probability_leave >= 0.5 → prediction = 1 → leave
probability_leave < 0.5  → prediction = 0 → stay
```

Ce seuil peut être ajusté dans le futur selon l’objectif métier :

* réduire les faux négatifs ;
* réduire les faux positifs ;
* augmenter la détection des profils à risque ;
* améliorer la précision des alertes.

Toute modification du seuil doit être documentée, testée et versionnée.

---

## 14. Chargement du modèle dans l’API

Le chargement du modèle est géré par le service :

```text
app/services/model_service.py
```

Ce service réalise les opérations suivantes :

1. chargement du fichier `models/attrition_random_forest.joblib` ;
2. chargement du fichier `models/model_metadata.json` ;
3. récupération de la liste des features attendues ;
4. transformation du payload API en DataFrame ;
5. appel du modèle ;
6. calcul de la probabilité de départ ;
7. application du seuil de décision ;
8. construction de la réponse API.

---

## 15. Réponse produite par le modèle

L’API retourne une réponse structurée avec :

```json
{
  "prediction": 1,
  "prediction_label": "leave",
  "probability_leave": 0.8955,
  "model_name": "attrition-random-forest",
  "model_version": "0.5.0"
}
```

Description des champs :

| Champ               | Description                            |
| ------------------- | -------------------------------------- |
| `prediction`        | Classe numérique prédite               |
| `prediction_label`  | Libellé métier associé à la prédiction |
| `probability_leave` | Probabilité estimée de départ          |
| `model_name`        | Nom du modèle utilisé                  |
| `model_version`     | Version du modèle utilisé              |

---

## 16. Traçabilité des prédictions

Chaque appel à :

```text
POST /predict
```

est tracé dans PostgreSQL en environnement local.

Le flux est le suivant :

```text
1. input API enregistré dans prediction_requests
2. modèle appelé
3. output modèle enregistré dans prediction_responses
4. réponse retournée à l’utilisateur
```

La vue suivante permet de contrôler la trace complète :

```text
ml_api.v_prediction_traces
```

Commande de vérification :

```bash
psql p5_ml_api -f db/sql/07_visualize_prediction_traces.sql
```

---

## 17. Tests associés au modèle

Le modèle est couvert par plusieurs tests.

| Fichier de test                | Rôle                                                 |
| ------------------------------ | ---------------------------------------------------- |
| `tests/test_model_service.py`  | Vérifie le chargement et l’appel du service modèle   |
| `tests/test_prediction.py`     | Vérifie les endpoints `/model-info` et `/predict`    |
| `tests/test_functional_api.py` | Vérifie le parcours complet API avec le modèle       |
| `tests/test_schemas.py`        | Vérifie la validation des inputs et outputs Pydantic |

Commande de test :

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Résultat validé :

```text
24 passed
coverage 98%
```

---

## 18. Protocole de maintenance du modèle

La maintenance du modèle doit suivre un protocole reproductible.

### Étape 1 — Mettre à jour le dataset

Remplacer ou mettre à jour :

```text
data/employee_attrition.csv
```

### Étape 2 — Réentraîner le modèle

```bash
python scripts/train_export_model.py
```

### Étape 3 — Vérifier les métriques

Comparer les nouvelles métriques aux métriques de référence :

| Métrique  | Référence actuelle |
| --------- | -----------------: |
| Accuracy  |             0.8367 |
| Precision |             0.4865 |
| Recall    |             0.3830 |
| F1-score  |             0.4286 |
| ROC AUC   |             0.7975 |

### Étape 4 — Vérifier les fichiers exportés

```text
models/attrition_random_forest.joblib
models/model_metadata.json
```

### Étape 5 — Vérifier l’API

Lancer l’API :

```bash
python -m uvicorn app.main:app --reload
```

Vérifier les métadonnées :

```bash
curl http://127.0.0.1:8000/model-info
```

Tester une prédiction :

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

### Étape 6 — Lancer les tests

```bash
python -m pytest --cov=app --cov-report=term-missing
```

### Étape 7 — Générer le rapport de couverture

```bash
python -m pytest \
  --cov=app \
  --cov-report=term-missing \
  --cov-report=xml:reports/coverage.xml \
  --cov-report=html:reports/coverage_html
```

### Étape 8 — Versionner la mise à jour

```bash
git add .
git commit -m "Update trained model and metadata"
git tag -a vX.Y.Z -m "Mise à jour du modèle"
git push origin main
git push origin vX.Y.Z
```

---

## 19. Points de vigilance

Avant de livrer une nouvelle version du modèle, vérifier :

* que les 30 features attendues sont toujours présentes ;
* que les noms des colonnes sont inchangés ;
* que les types des données sont compatibles avec le schéma Pydantic ;
* que le pipeline `joblib` se charge correctement ;
* que les métriques sont documentées ;
* que le seuil de décision est explicitement défini ;
* que les tests passent ;
* que la CI/CD passe ;
* que les prédictions sont correctement tracées en base ;
* que le README et la documentation technique sont à jour.

---

## 20. Commandes opérationnelles

### Réentraîner le modèle

```bash
python scripts/train_export_model.py
```

### Lancer l’API

```bash
python -m uvicorn app.main:app --reload
```

### Consulter les métadonnées du modèle

```bash
curl http://127.0.0.1:8000/model-info
```

### Lancer les tests

```bash
python -m pytest --cov=app --cov-report=term-missing
```

### Générer le rapport de couverture

```bash
python -m pytest \
  --cov=app \
  --cov-report=term-missing \
  --cov-report=xml:reports/coverage.xml \
  --cov-report=html:reports/coverage_html
```

### Vérifier les traces PostgreSQL

```bash
psql p5_ml_api -f db/sql/07_visualize_prediction_traces.sql
```

---

## 21. Résumé

Le modèle de machine learning est intégré dans une architecture complète :

```text
Dataset P4
→ Entraînement Random Forest
→ Export joblib
→ Chargement FastAPI
→ Prédiction API
→ Traçabilité PostgreSQL
→ Tests
→ CI/CD
```

Cette documentation permet de comprendre :

* le rôle du modèle ;
* les données utilisées ;
* les performances obtenues ;
* les limites connues ;
* le fonctionnement du chargement dans l’API ;
* le protocole de réentraînement ;
* le protocole de validation ;
* le protocole de maintenance.
