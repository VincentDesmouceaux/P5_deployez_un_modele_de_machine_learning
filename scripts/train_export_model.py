import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


DATA_PATH = Path("data/employee_attrition.csv")
MODEL_PATH = Path("models/attrition_random_forest.joblib")
METADATA_PATH = Path("models/model_metadata.json")

TARGET_COLUMN = "attrition_bin"

EXCLUDED_COLUMNS = [
    "id_employee",
    "eval_number",
    "code_sondage",
    "a_quitte_l_entreprise",
    TARGET_COLUMN,
]


def main():
    print("Chargement du dataset...")
    df = pd.read_csv(DATA_PATH)

    print("Shape dataset :", df.shape)

    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Colonne cible absente : {TARGET_COLUMN}")

    X = df.drop(columns=EXCLUDED_COLUMNS)
    y = df[TARGET_COLUMN].astype(int)

    numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_features = X.select_dtypes(include=["object", "string", "bool"]).columns.tolist()

    print("Features utilisées :", len(X.columns))
    print("Features numériques :", len(numeric_features))
    print("Features catégorielles :", len(categorical_features))

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    print("X_train :", X_train.shape)
    print("X_test  :", X_test.shape)

    print("Entraînement du modèle...")
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "f1": round(f1_score(y_test, y_pred), 4),
        "roc_auc": round(roc_auc_score(y_test, y_proba), 4),
    }

    print("Métriques test :")
    for metric_name, metric_value in metrics.items():
        print(f"- {metric_name}: {metric_value}")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(pipeline, MODEL_PATH)

    metadata = {
        "model_name": "attrition-random-forest",
        "model_version": "0.5.0",
        "model_type": "RandomForestClassifier",
        "target": TARGET_COLUMN,
        "description": (
            "Modèle Random Forest entraîné sur le dataset central du projet P4 "
            "pour prédire l'attrition des collaborateurs."
        ),
        "features": X.columns.tolist(),
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "excluded_columns": EXCLUDED_COLUMNS,
        "metrics": metrics,
    }

    METADATA_PATH.write_text(json.dumps(metadata, indent=4, ensure_ascii=False))

    print()
    print(f"Modèle exporté : {MODEL_PATH}")
    print(f"Métadonnées exportées : {METADATA_PATH}")


if __name__ == "__main__":
    main()
