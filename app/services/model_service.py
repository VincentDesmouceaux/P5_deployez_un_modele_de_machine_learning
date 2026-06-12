from app.schemas import ModelInfo, PredictionInput, PredictionOutput

MODEL_NAME = "attrition-baseline-api"
MODEL_VERSION = "0.3.0"
MODEL_TYPE = "rule-based-baseline"
TARGET = "employee_attrition"


def get_model_info() -> ModelInfo:
    return ModelInfo(
        model_name=MODEL_NAME,
        model_version=MODEL_VERSION,
        model_type=MODEL_TYPE,
        target=TARGET,
        description=(
            "Modèle de référence provisoire pour exposer l'API de prédiction. "
            "Il sera remplacé par le modèle machine learning exporté du projet P4."
        ),
        input_features=[
            "satisfaction_level",
            "last_evaluation",
            "number_project",
            "average_monthly_hours",
            "time_spend_company",
            "work_accident",
            "promotion_last_5years",
            "department",
            "salary",
        ],
    )


def predict_attrition(input_data: PredictionInput) -> PredictionOutput:
    score = 0.15

    score += (1 - input_data.satisfaction_level) * 0.35

    if input_data.average_monthly_hours > 180:
        score += min((input_data.average_monthly_hours - 180) / 170, 1) * 0.20

    if input_data.number_project > 4:
        score += min((input_data.number_project - 4) / 6, 1) * 0.10

    if input_data.last_evaluation > 0.75 and input_data.satisfaction_level < 0.50:
        score += 0.10

    if input_data.time_spend_company >= 4:
        score += 0.05

    if input_data.salary == "low":
        score += 0.10
    elif input_data.salary == "high":
        score -= 0.05

    if input_data.promotion_last_5years:
        score -= 0.10

    if input_data.work_accident:
        score -= 0.05

    probability_leave = round(max(0.01, min(score, 0.99)), 4)
    prediction = 1 if probability_leave >= 0.50 else 0
    prediction_label = "leave" if prediction == 1 else "stay"

    return PredictionOutput(
        prediction=prediction,
        prediction_label=prediction_label,
        probability_leave=probability_leave,
        model_name=MODEL_NAME,
        model_version=MODEL_VERSION,
    )
