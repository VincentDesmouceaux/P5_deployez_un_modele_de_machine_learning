from app.schemas import PredictionInput
from app.services.model_service import get_model_info, predict_attrition


def test_get_model_info_returns_real_model_metadata():
    """
    Vérifie que le service retourne les métadonnées du modèle réellement chargé.

    Ce test contrôle directement la fonction get_model_info(),
    sans passer par l'endpoint FastAPI /model-info.
    """
    model_info = get_model_info()

    assert model_info.model_name == "attrition-random-forest"
    assert model_info.model_version == "0.5.0"
    assert model_info.model_type == "RandomForestClassifier"
    assert model_info.target == "attrition_bin"
    assert isinstance(model_info.input_features, list)
    assert len(model_info.input_features) == 30
    assert "age" in model_info.input_features
    assert "revenu_mensuel" in model_info.input_features
    assert "departement" in model_info.input_features


def test_predict_attrition_returns_complete_prediction(valid_prediction_payload):
    """
    Vérifie que predict_attrition() retourne une prédiction complète.

    Ce test appelle directement le service modèle :
    - sans passer par l'API ;
    - sans écrire en base PostgreSQL ;
    - avec un payload représentatif du dataset P4.
    """
    input_data = PredictionInput(**valid_prediction_payload)

    result = predict_attrition(input_data)

    assert result.prediction in [0, 1]
    assert result.prediction_label in ["stay", "leave"]
    assert 0 <= result.probability_leave <= 1
    assert result.model_name == "attrition-random-forest"
    assert result.model_version == "0.5.0"


def test_predict_attrition_label_matches_prediction(valid_prediction_payload):
    """
    Vérifie la cohérence entre la classe numérique et le libellé métier.

    Règle attendue :
    - prediction = 0 => stay
    - prediction = 1 => leave
    """
    input_data = PredictionInput(**valid_prediction_payload)

    result = predict_attrition(input_data)

    if result.prediction == 0:
        assert result.prediction_label == "stay"

    if result.prediction == 1:
        assert result.prediction_label == "leave"


def test_predict_attrition_label_matches_probability_threshold(valid_prediction_payload):
    """
    Vérifie la règle métier du seuil de décision.

    Règle attendue :
    - probability_leave >= 0.5 => leave
    - probability_leave < 0.5 => stay
    """
    input_data = PredictionInput(**valid_prediction_payload)

    result = predict_attrition(input_data)

    if result.probability_leave >= 0.5:
        assert result.prediction == 1
        assert result.prediction_label == "leave"

    if result.probability_leave < 0.5:
        assert result.prediction == 0
        assert result.prediction_label == "stay"