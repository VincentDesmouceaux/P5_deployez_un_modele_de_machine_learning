# 🐘 Documentation PostgreSQL — Base de données et traçabilité

## Objectif

Cette documentation décrit la base PostgreSQL utilisée dans le projet **P5 — Déployez un modèle de Machine Learning**.

La base PostgreSQL permet de :

* stocker le dataset complet utilisé par le projet ;
* enregistrer les inputs envoyés à l’API ;
* enregistrer les outputs générés par le modèle ;
* relier chaque prédiction à sa requête d’origine ;
* auditer les prédictions produites par l’API ;
* visualiser le cheminement complet des données avec SQL ou DBeaver.

L’objectif principal est de garantir une traçabilité claire entre :

```text
API FastAPI → PostgreSQL → Modèle ML → PostgreSQL → Réponse API
```

---

## 1. Choix technique

La base utilisée est **PostgreSQL**.

Ce choix est adapté au projet car PostgreSQL permet :

* de stocker des données structurées ;
* de gérer des relations entre tables ;
* de conserver des payloads JSON avec le type `jsonb` ;
* d’utiliser des contraintes SQL ;
* de tracer les prédictions de manière fiable ;
* de faciliter l’analyse avec des requêtes SQL.

Dans ce projet, PostgreSQL est utilisé localement pour la traçabilité et la démonstration technique.

---

## 2. Base et schéma

Nom de la base :

```text
p5_ml_api
```

Nom du schéma PostgreSQL :

```text
ml_api
```

Le schéma `ml_api` regroupe toutes les tables nécessaires au projet.

---

## 3. Structure générale

La base contient trois tables principales et une vue de synthèse.

| Objet PostgreSQL              | Type  | Rôle                                               |
| ----------------------------- | ----- | -------------------------------------------------- |
| `ml_api.employees_dataset`    | Table | Stocke le dataset complet des collaborateurs       |
| `ml_api.prediction_requests`  | Table | Stocke les inputs envoyés à l’API                  |
| `ml_api.prediction_responses` | Table | Stocke les outputs générés par le modèle           |
| `ml_api.v_prediction_traces`  | Vue   | Relie les inputs et outputs pour faciliter l’audit |

---

## 4. Schéma relationnel simplifié

```text
employees_dataset
    id_employee PK
        ↑
        │ employee_id nullable
        │
prediction_requests
    request_id PK
        ↓
        │ request_id FK
        ↓
prediction_responses
    response_id PK
```

Relation principale :

```text
prediction_requests 1 --- 1 prediction_responses
```

Cela signifie qu’un appel à l’endpoint `/predict` génère :

```text
1 input enregistré
+
1 output enregistré
=
1 trace complète de prédiction
```

---

## 5. Table `ml_api.employees_dataset`

Cette table contient le dataset complet des collaborateurs issu du projet P4.

Elle sert de référence pour :

* conserver les données sources ;
* vérifier le contenu du dataset ;
* analyser la distribution de la cible ;
* rattacher éventuellement une requête de prédiction à un collaborateur existant.

### Rôle

```text
Stockage du dataset central utilisé pour le modèle d’attrition
```

### Exemples de colonnes

La table contient notamment :

```text
id_employee
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
a_quitte_l_entreprise
attrition_bin
```

### Variable cible

La variable cible utilisée par le modèle est :

```text
attrition_bin
```

Elle encode la variable métier :

```text
0 → stay
1 → leave
```

---

## 6. Table `ml_api.prediction_requests`

Cette table enregistre les inputs envoyés à l’endpoint :

```text
POST /predict
```

Chaque appel valide à l’API crée une ligne dans cette table.

### Rôle

```text
Conserver le payload d’entrée envoyé au modèle
```

### Colonnes principales

| Colonne         | Rôle                                    |
| --------------- | --------------------------------------- |
| `request_id`    | Identifiant unique de la requête        |
| `created_at`    | Date et heure de création               |
| `source`        | Origine de la requête, par défaut `api` |
| `employee_id`   | Identifiant collaborateur optionnel     |
| `input_payload` | Payload JSON complet envoyé à l’API     |

Le champ `input_payload` utilise le type PostgreSQL :

```text
jsonb
```

Cela permet de conserver le JSON complet envoyé au modèle.

---

## 7. Table `ml_api.prediction_responses`

Cette table enregistre les outputs générés par le modèle.

Chaque ligne est reliée à une requête via la colonne :

```text
request_id
```

### Rôle

```text
Conserver la prédiction produite par le modèle
```

### Colonnes principales

| Colonne             | Rôle                                          |
| ------------------- | --------------------------------------------- |
| `response_id`       | Identifiant unique de la réponse              |
| `request_id`        | Clé étrangère vers `prediction_requests`      |
| `created_at`        | Date et heure de création                     |
| `prediction`        | Classe prédite, `0` ou `1`                    |
| `prediction_label`  | Libellé métier, `stay` ou `leave`             |
| `probability_leave` | Probabilité estimée de départ                 |
| `model_name`        | Nom du modèle utilisé                         |
| `model_version`     | Version du modèle utilisé                     |
| `output_payload`    | Réponse JSON complète retournée par le modèle |

Le champ `output_payload` utilise également le type :

```text
jsonb
```

---

## 8. Vue `ml_api.v_prediction_traces`

La vue `ml_api.v_prediction_traces` permet de visualiser les requêtes et réponses dans un seul résultat SQL.

Elle relie :

```text
prediction_requests
+
prediction_responses
```

grâce à :

```text
request_id
```

### Rôle

```text
Faciliter l’audit complet des prédictions
```

### Colonnes principales de la vue

| Colonne               | Description                         |
| --------------------- | ----------------------------------- |
| `request_id`          | Identifiant de la requête           |
| `response_id`         | Identifiant de la réponse           |
| `request_created_at`  | Date de création de l’input         |
| `response_created_at` | Date de création de l’output        |
| `source`              | Origine de la requête               |
| `employee_id`         | Identifiant collaborateur optionnel |
| `prediction`          | Classe prédite                      |
| `prediction_label`    | Libellé métier                      |
| `probability_leave`   | Probabilité de départ               |
| `model_name`          | Nom du modèle                       |
| `model_version`       | Version du modèle                   |
| `input_payload`       | JSON d’entrée                       |
| `output_payload`      | JSON de sortie                      |

---

## 9. Scripts SQL

Les scripts SQL sont stockés dans le dossier :

```text
db/sql/
```

| Script                               | Rôle                                                         |
| ------------------------------------ | ------------------------------------------------------------ |
| `01_create_database.sql`             | Création de la base PostgreSQL `p5_ml_api`                   |
| `02_create_tables.sql`               | Création du schéma `ml_api` et des tables                    |
| `03_load_dataset.sql`                | Chargement du dataset CSV dans PostgreSQL                    |
| `04_check_database.sql`              | Vérification du contenu de la base                           |
| `05_trace_predictions.sql`           | Vérification détaillée des prédictions tracées               |
| `06_create_trace_view.sql`           | Création de la vue `ml_api.v_prediction_traces`              |
| `07_visualize_prediction_traces.sql` | Visualisation lisible de toutes les prédictions enregistrées |

---

## 10. Ordre d’exécution des scripts SQL

### 1. Créer la base

```bash
psql postgres -f db/sql/01_create_database.sql
```

### 2. Créer les tables

```bash
psql p5_ml_api -f db/sql/02_create_tables.sql
```

### 3. Charger le dataset

```bash
psql p5_ml_api -f db/sql/03_load_dataset.sql
```

### 4. Créer la vue de traçabilité

```bash
psql p5_ml_api -f db/sql/06_create_trace_view.sql
```

### 5. Vérifier le contenu de la base

```bash
psql p5_ml_api -f db/sql/04_check_database.sql
```

### 6. Visualiser les prédictions tracées

```bash
psql p5_ml_api -f db/sql/07_visualize_prediction_traces.sql
```

---

## 11. Dataset attendu

Le script de chargement attend le fichier suivant :

```text
data/employee_attrition.csv
```

Ce fichier contient le dataset central utilisé pour alimenter PostgreSQL et entraîner le modèle.

Selon la configuration du `.gitignore`, le dataset peut ne pas être versionné s’il est considéré comme volumineux ou sensible.

---

## 12. Vérifications SQL utiles

### Vérifier la connexion à la base

```bash
psql p5_ml_api -c "SELECT current_database(), current_user;"
```

### Compter les lignes du dataset

```bash
psql p5_ml_api -c "SELECT COUNT(*) FROM ml_api.employees_dataset;"
```

Résultat attendu :

```text
1470
```

### Vérifier la distribution de la cible

```bash
psql p5_ml_api -c "
SELECT attrition_bin, COUNT(*) AS total
FROM ml_api.employees_dataset
GROUP BY attrition_bin
ORDER BY attrition_bin;
"
```

Résultat attendu :

```text
0 → collaborateurs restés
1 → collaborateurs partis
```

### Afficher les dernières prédictions

```bash
psql p5_ml_api -f db/sql/07_visualize_prediction_traces.sql
```

---

## 13. Flux de traçabilité complet

Chaque appel à :

```text
POST /predict
```

suit le flux suivant :

```text
1. L’utilisateur envoie un payload JSON à l’API
              ↓
2. FastAPI valide les données avec Pydantic
              ↓
3. L’input est enregistré dans prediction_requests
              ↓
4. Le modèle Random Forest génère une prédiction
              ↓
5. L’output est enregistré dans prediction_responses
              ↓
6. La réponse est retournée à l’utilisateur
              ↓
7. La vue v_prediction_traces permet de consulter la trace complète
```

Cette structure permet de répondre à la question :

```text
Quel input a produit quelle prédiction, avec quel modèle et quelle version ?
```

---

## 14. Exemple de trace SQL

Commande :

```bash
psql p5_ml_api -f db/sql/07_visualize_prediction_traces.sql
```

Exemple de résultat :

```text
request_id | response_id | prediction | prediction_label | probability_leave | model_name              | model_version
3          | 3           | 1          | leave            | 0.89550           | attrition-random-forest | 0.5.0
2          | 2           | 0          | stay             | 0.40030           | attrition-random-forest | 0.5.0
1          | 1           | 1          | leave            | 0.74450           | attrition-baseline-api  | 0.3.0
```

---

## 15. Générer des prédictions de démonstration

Si la vue `v_prediction_traces` affiche peu de lignes, cela signifie simplement que peu d’appels réels ont été envoyés à l’API.

Pour générer plusieurs traces, lancer d’abord l’API :

```bash
python -m uvicorn app.main:app --reload
```

Puis, dans un deuxième terminal :

```bash
python scripts/generate_demo_predictions.py
```

Par défaut, le script envoie les 20 premières lignes du dataset.

Pour choisir un autre nombre :

```bash
DEMO_LIMIT=50 python scripts/generate_demo_predictions.py
```

Ensuite :

```bash
psql p5_ml_api -f db/sql/07_visualize_prediction_traces.sql
```

---

## 16. Visualisation avec DBeaver

La base PostgreSQL peut être explorée avec **DBeaver Community**.

### Connexion locale

| Paramètre | Valeur                       |
| --------- | ---------------------------- |
| Host      | `localhost`                  |
| Port      | `5432`                       |
| Database  | `p5_ml_api`                  |
| Schema    | `ml_api`                     |
| User      | utilisateur PostgreSQL local |

### Arborescence attendue

```text
p5_ml_api
└── Schemas
    └── ml_api
        ├── Tables
        │   ├── employees_dataset
        │   ├── prediction_requests
        │   └── prediction_responses
        └── Views
            └── v_prediction_traces
```

### Requête de visualisation

```sql
SELECT
    request_id,
    response_id,
    prediction,
    prediction_label,
    probability_leave,
    model_name,
    model_version
FROM ml_api.v_prediction_traces
ORDER BY request_id DESC;
```

### Script d’ouverture rapide

```bash
./scripts/open_database_visualization.sh
```

---

## 17. Connexion Python avec SQLAlchemy

L’application utilise **SQLAlchemy** pour se connecter à PostgreSQL.

La connexion est centralisée dans :

```text
app/database.py
```

L’enregistrement des inputs et outputs est centralisé dans :

```text
app/services/prediction_log_service.py
```

Le endpoint `POST /predict` appelle ce service pour tracer automatiquement les prédictions.

---

## 18. Variables d’environnement

Les informations de connexion à la base ne doivent pas être écrites directement dans le code.

Elles sont stockées dans un fichier :

```text
.env
```

Ce fichier n’est pas versionné.

Un fichier d’exemple permet de documenter la variable attendue :

```text
.env.example
```

Exemple de variable :

```text
DATABASE_URL=postgresql://localhost:5432/p5_ml_api
```

---

## 19. Sécurité et points de vigilance

Points de vigilance :

* ne pas versionner le fichier `.env` ;
* ne pas publier de mot de passe ou de token dans le code ;
* ne pas exposer de données sensibles dans le repository ;
* vérifier que chaque input possède un output associé ;
* vérifier que chaque output possède un `request_id` valide ;
* utiliser des transactions lors des écritures ;
* conserver le nom et la version du modèle dans chaque réponse ;
* vérifier que la base locale n’est pas nécessaire au démarrage public de l’API déployée.

Dans ce projet, la base PostgreSQL est locale. Le déploiement Hugging Face Spaces expose l’API, mais ne publie pas la base PostgreSQL locale.

---

## 20. Tests liés à la base

La logique de traçabilité est testée dans :

```text
tests/test_prediction_log_service.py
```

Ces tests utilisent un faux moteur SQLAlchemy afin de vérifier la logique sans dépendre d’une base PostgreSQL active.

La suite complète de tests peut être lancée avec :

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Résultat validé :

```text
24 passed
coverage 98%
```

---

## 21. Commandes opérationnelles

### Reconstruire la base

```bash
psql postgres -f db/sql/01_create_database.sql
psql p5_ml_api -f db/sql/02_create_tables.sql
psql p5_ml_api -f db/sql/03_load_dataset.sql
psql p5_ml_api -f db/sql/06_create_trace_view.sql
```

### Vérifier le contenu

```bash
psql p5_ml_api -f db/sql/04_check_database.sql
```

### Afficher les traces

```bash
psql p5_ml_api -f db/sql/07_visualize_prediction_traces.sql
```

### Ouvrir la visualisation avec DBeaver

```bash
./scripts/open_database_visualization.sh
```

### Lancer les tests

```bash
python -m pytest --cov=app --cov-report=term-missing
```

---

## 22. Résultat attendu

À la fin de la configuration PostgreSQL, le projet doit contenir :

* une base `p5_ml_api` ;
* un schéma `ml_api` ;
* une table contenant le dataset complet ;
* une table d’inputs API ;
* une table d’outputs modèle ;
* une vue SQL de traçabilité ;
* des scripts SQL versionnés ;
* une connexion applicative centralisée ;
* une documentation claire ;
* des tests couvrant la logique de traçabilité.

---

## 23. Résumé

La base PostgreSQL assure la traçabilité complète du projet.

Elle permet de relier :

```text
input API
→ prédiction modèle
→ output API
→ modèle utilisé
→ version du modèle
→ horodatage
```

Cette architecture renforce la robustesse du projet et permet d’auditer les prédictions produites par l’API.
