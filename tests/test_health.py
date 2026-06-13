def test_health_check_returns_ok(client):
    """
    Vérifie que l'endpoint de monitoring /health répond correctement.

    Ce test permet de contrôler que :
    - l'API est disponible ;
    - le service retourne le bon nom ;
    - la version exposée correspond à la version actuelle du projet.
    """
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "p5-ml-api"
    assert data["version"] == "0.5.0"