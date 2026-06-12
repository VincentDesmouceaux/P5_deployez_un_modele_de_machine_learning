import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_prediction_database_logging(monkeypatch):
    monkeypatch.setattr("app.main.save_prediction_request", lambda input_data: 1)
    monkeypatch.setattr("app.main.save_prediction_response", lambda request_id, output_data: 1)


VALID_PAYLOAD = {
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
    "annes_sous_responsable_actuel": 5,
}


def test_model_info_returns_exported_model_metadata():
    response = client.get("/model-info")

    assert response.status_code == 200

    data = response.json()

    assert data["model_name"] == "attrition-random-forest"
    assert data["model_version"] == "0.5.0"
    assert data["model_type"] == "RandomForestClassifier"
    assert data["target"] == "attrition_bin"
    assert len(data["input_features"]) == 30


def test_predict_returns_valid_prediction():
    response = client.post("/predict", json=VALID_PAYLOAD)

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] in [0, 1]
    assert data["prediction_label"] in ["stay", "leave"]
    assert 0 <= data["probability_leave"] <= 1
    assert data["model_name"] == "attrition-random-forest"
    assert data["model_version"] == "0.5.0"

    if data["prediction"] == 0:
        assert data["prediction_label"] == "stay"

    if data["prediction"] == 1:
        assert data["prediction_label"] == "leave"


def test_predict_rejects_invalid_age():
    payload = VALID_PAYLOAD.copy()
    payload["age"] = 12

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_rejects_invalid_satisfaction_score():
    payload = VALID_PAYLOAD.copy()
    payload["satisfaction_employee_environnement"] = 8

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_rejects_missing_required_field():
    payload = VALID_PAYLOAD.copy()
    del payload["departement"]

    response = client.post("/predict", json=payload)

    assert response.status_code == 422
