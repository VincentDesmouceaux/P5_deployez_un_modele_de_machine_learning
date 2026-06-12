from fastapi.testclient import TestClient

import pytest


@pytest.fixture(autouse=True)
def mock_prediction_database_logging(monkeypatch):
    monkeypatch.setattr("app.main.save_prediction_request", lambda input_data: 1)
    monkeypatch.setattr("app.main.save_prediction_response", lambda request_id, output_data: 1)


from app.main import app

client = TestClient(app)


VALID_PAYLOAD = {
    "satisfaction_level": 0.38,
    "last_evaluation": 0.86,
    "number_project": 6,
    "average_monthly_hours": 260,
    "time_spend_company": 4,
    "work_accident": False,
    "promotion_last_5years": False,
    "department": "technical",
    "salary": "low",
}


def test_model_info_returns_metadata():
    response = client.get("/model-info")

    assert response.status_code == 200
    data = response.json()

    assert data["model_name"] == "attrition-baseline-api"
    assert data["model_version"] == "0.3.0"
    assert data["target"] == "employee_attrition"
    assert "satisfaction_level" in data["input_features"]


def test_predict_returns_valid_prediction():
    response = client.post("/predict", json=VALID_PAYLOAD)

    assert response.status_code == 200
    data = response.json()

    assert data["prediction"] in [0, 1]
    assert data["prediction_label"] in ["stay", "leave"]
    assert 0 <= data["probability_leave"] <= 1
    assert data["model_name"] == "attrition-baseline-api"
    assert data["model_version"] == "0.3.0"


def test_predict_rejects_invalid_satisfaction_level():
    payload = VALID_PAYLOAD.copy()
    payload["satisfaction_level"] = 1.5

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_rejects_invalid_salary_value():
    payload = VALID_PAYLOAD.copy()
    payload["salary"] = "very_high"

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_rejects_missing_required_field():
    payload = VALID_PAYLOAD.copy()
    del payload["department"]

    response = client.post("/predict", json=payload)

    assert response.status_code == 422
