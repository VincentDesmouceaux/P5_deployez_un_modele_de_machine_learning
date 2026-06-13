def assert_valid_prediction_response(data):
    """
    Vérifie qu'une réponse de prédiction respecte le contrat fonctionnel attendu.

    Cette fonction est utilisée par plusieurs tests fonctionnels afin d'éviter
    de répéter les mêmes assertions.
    """
    assert data["prediction"] in [0, 1]
    assert data["prediction_label"] in ["stay", "leave"]
    assert 0 <= data["probability_leave"] <= 1
    assert data["model_name"] == "attrition-random-forest"
    assert data["model_version"] == "0.5.0"

    if data["probability_leave"] >= 0.5:
        assert data["prediction"] == 1
        assert data["prediction_label"] == "leave"

    if data["probability_leave"] < 0.5:
        assert data["prediction"] == 0
        assert data["prediction_label"] == "stay"


def test_functional_api_workflow_health_model_info_predict(
    client,
    valid_prediction_payload,
):
    """
    Test fonctionnel du parcours complet de l'API.

    Ce test simule un usage réel :
    1. vérification de l'état de l'API avec /health ;
    2. vérification du modèle chargé avec /model-info ;
    3. envoi d'un collaborateur à /predict ;
    4. contrôle de la cohérence de la prédiction retournée.
    """
    health_response = client.get("/health")

    assert health_response.status_code == 200
    assert health_response.json()["status"] == "ok"

    model_info_response = client.get("/model-info")

    assert model_info_response.status_code == 200

    model_info = model_info_response.json()

    assert model_info["model_name"] == "attrition-random-forest"
    assert model_info["model_version"] == "0.5.0"
    assert len(model_info["input_features"]) == 30

    prediction_response = client.post("/predict", json=valid_prediction_payload)

    assert prediction_response.status_code == 200

    prediction_data = prediction_response.json()

    assert_valid_prediction_response(prediction_data)


def test_functional_predict_accepts_several_realistic_profiles(
    client,
    valid_prediction_payload,
):
    """
    Vérifie que l'endpoint /predict accepte plusieurs profils métier réalistes.

    Cela permet de tester le modèle dans des conditions proches d'un usage réel,
    avec des profils différents de collaborateurs.
    """
    commercial_profile = valid_prediction_payload.copy()

    consulting_profile = valid_prediction_payload.copy()
    consulting_profile.update(
        {
            "age": 36,
            "genre": "M",
            "departement": "Consulting",
            "poste": "Consultant",
            "revenu_mensuel": 4200,
            "heure_supplementaires": "Non",
            "frequence_deplacement": "Rare",
            "distance_domicile_travail": 8,
        }
    )

    hr_profile = valid_prediction_payload.copy()
    hr_profile.update(
        {
            "age": 52,
            "genre": "F",
            "departement": "Ressources Humaines",
            "poste": "Manager RH",
            "revenu_mensuel": 6800,
            "annee_experience_totale": 25,
            "annees_dans_l_entreprise": 14,
            "niveau_hierarchique_poste": 4,
        }
    )

    profiles = [
        commercial_profile,
        consulting_profile,
        hr_profile,
    ]

    for profile in profiles:
        response = client.post("/predict", json=profile)

        assert response.status_code == 200

        data = response.json()

        assert_valid_prediction_response(data)


def test_functional_predict_rejects_business_invalid_payload(
    client,
    valid_prediction_payload,
):
    """
    Vérifie qu'un payload métier invalide est rejeté par l'API.

    Exemple : une augmentation de salaire précédente supérieure à 100 %
    n'est pas acceptée par le schéma Pydantic.
    """
    payload = valid_prediction_payload.copy()
    payload["augementation_salaire_precedente"] = 150

    response = client.post("/predict", json=payload)

    assert response.status_code == 422