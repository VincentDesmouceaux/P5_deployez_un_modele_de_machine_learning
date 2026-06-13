import pytest
from pydantic import ValidationError

from app.schemas import PredictionInput, PredictionOutput


def test_prediction_input_accepts_valid_payload(valid_prediction_payload):
    """
    Vérifie que le schéma PredictionInput accepte un payload complet et valide.

    Ce test est un test unitaire pur :
    - il ne lance pas l'API ;
    - il ne charge pas le modèle ;
    - il ne dépend pas de PostgreSQL.
    """
    input_data = PredictionInput(**valid_prediction_payload)

    assert input_data.age == 41
    assert input_data.departement == "Commercial"
    assert input_data.heure_supplementaires == "Oui"
    assert input_data.augementation_salaire_precedente == 11


def test_prediction_input_rejects_age_below_minimum(valid_prediction_payload):
    """
    Vérifie que le schéma refuse un âge inférieur à 18 ans.
    """
    payload = valid_prediction_payload.copy()
    payload["age"] = 17

    with pytest.raises(ValidationError):
        PredictionInput(**payload)


def test_prediction_input_rejects_age_above_maximum(valid_prediction_payload):
    """
    Vérifie que le schéma refuse un âge supérieur à 70 ans.
    """
    payload = valid_prediction_payload.copy()
    payload["age"] = 71

    with pytest.raises(ValidationError):
        PredictionInput(**payload)


def test_prediction_input_rejects_invalid_probability_related_score(valid_prediction_payload):
    """
    Vérifie que les scores métier bornés sont bien contrôlés.

    Exemple : la satisfaction environnement doit être comprise entre 1 et 4.
    """
    payload = valid_prediction_payload.copy()
    payload["satisfaction_employee_environnement"] = 0

    with pytest.raises(ValidationError):
        PredictionInput(**payload)


def test_prediction_input_rejects_missing_required_field(valid_prediction_payload):
    """
    Vérifie qu'un champ obligatoire manquant provoque une erreur de validation.
    """
    payload = valid_prediction_payload.copy()
    del payload["revenu_mensuel"]

    with pytest.raises(ValidationError):
        PredictionInput(**payload)


def test_prediction_output_accepts_valid_model_response():
    """
    Vérifie que le schéma PredictionOutput accepte une réponse modèle valide.
    """
    output_data = PredictionOutput(
        prediction=1,
        prediction_label="leave",
        probability_leave=0.7825,
        model_name="attrition-random-forest",
        model_version="0.5.0",
    )

    assert output_data.prediction == 1
    assert output_data.prediction_label == "leave"
    assert output_data.probability_leave == 0.7825


def test_prediction_output_rejects_invalid_prediction_value():
    """
    Vérifie que la prédiction est obligatoirement comprise entre 0 et 1.
    """
    with pytest.raises(ValidationError):
        PredictionOutput(
            prediction=2,
            prediction_label="leave",
            probability_leave=0.7825,
            model_name="attrition-random-forest",
            model_version="0.5.0",
        )


def test_prediction_output_rejects_invalid_probability():
    """
    Vérifie que probability_leave est obligatoirement comprise entre 0 et 1.
    """
    with pytest.raises(ValidationError):
        PredictionOutput(
            prediction=1,
            prediction_label="leave",
            probability_leave=1.5,
            model_name="attrition-random-forest",
            model_version="0.5.0",
        )