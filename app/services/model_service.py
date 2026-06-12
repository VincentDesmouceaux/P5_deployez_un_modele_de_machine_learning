import json
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

from app.schemas import ModelInfo, PredictionInput, PredictionOutput

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "attrition_random_forest.joblib"
METADATA_PATH = BASE_DIR / "models" / "model_metadata.json"


@lru_cache(maxsize=1)
def load_model():
    return joblib.load(MODEL_PATH)


@lru_cache(maxsize=1)
def load_metadata() -> dict:
    return json.loads(METADATA_PATH.read_text())


def get_model_info() -> ModelInfo:
    metadata = load_metadata()

    return ModelInfo(
        model_name=metadata["model_name"],
        model_version=metadata["model_version"],
        model_type=metadata["model_type"],
        target=metadata["target"],
        description=metadata.get("description", "Modèle Random Forest de prédiction d attrition."),
        input_features=metadata["features"],
    )


def predict_attrition(input_data: PredictionInput) -> PredictionOutput:
    model = load_model()
    metadata = load_metadata()

    input_payload = input_data.model_dump()
    features = metadata["features"]

    input_dataframe = pd.DataFrame([input_payload], columns=features)

    probability_leave = float(model.predict_proba(input_dataframe)[0][1])
    prediction = int(probability_leave >= 0.5)
    prediction_label = "leave" if prediction == 1 else "stay"

    return PredictionOutput(
        prediction=prediction,
        prediction_label=prediction_label,
        probability_leave=round(probability_leave, 4),
        model_name=metadata["model_name"],
        model_version=metadata["model_version"],
    )
