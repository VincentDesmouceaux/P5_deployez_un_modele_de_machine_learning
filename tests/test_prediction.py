def test_model_info_returns_exported_model_metadata(client):
    """
    Vérifie que l'endpoint /model-info retourne les métadonnées
    du modèle réellement chargé par l'API.
    """
    response = client.get("/model-info")

    assert response.status_code == 200

    data = response.json()

    assert data["model_name"] == "attrition-random-forest"
    assert data["model_version"] == "0.5.0"
    assert data["model_type"] == "RandomForestClassifier"
    assert data["target"] == "attrition_bin"
    assert isinstance(data["input_features"], list)
    assert len(data["input_features"]) == 30


def test_predict_returns_valid_prediction(client, valid_prediction_payload):
    """
    Vérifie qu'un payload valide retourne une prédiction complète.

    Le test contrôle :
    - le code HTTP ;
    - la classe prédite ;
    - le libellé métier ;
    - la probabilité de départ ;
    - le nom et la version du modèle.
    """
    response = client.post("/predict", json=valid_prediction_payload)

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


def test_predict_rejects_invalid_age(client, valid_prediction_payload):
    """
    Vérifie que l'API refuse un âge hors limites.

    Le schéma Pydantic impose un âge entre 18 et 70 ans.
    """
    payload = valid_prediction_payload.copy()
    payload["age"] = 12

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_rejects_invalid_satisfaction_score(client, valid_prediction_payload):
    """
    Vérifie que l'API refuse un score de satisfaction invalide.

    Les scores de satisfaction sont attendus entre 1 et 4.
    """
    payload = valid_prediction_payload.copy()
    payload["satisfaction_employee_environnement"] = 8

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_rejects_missing_required_field(client, valid_prediction_payload):
    """
    Vérifie que l'API refuse une requête incomplète.

    Ici, le champ obligatoire 'departement' est supprimé.
    """
    payload = valid_prediction_payload.copy()
    del payload["departement"]

    response = client.post("/predict", json=payload)

    assert response.status_code == 422