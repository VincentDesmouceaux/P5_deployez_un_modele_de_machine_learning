import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Client de test FastAPI utilisé pour tester les endpoints de l'API."""
    return TestClient(app)


@pytest.fixture
def valid_prediction_payload():
    """Payload représentatif d'un collaborateur issu du dataset P4."""
    return {
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


@pytest.fixture(autouse=True)
def mock_prediction_database_logging(monkeypatch):
    """
    Mock automatique des écritures PostgreSQL pendant les tests.

    Les tests API ne doivent pas dépendre d'une base PostgreSQL locale active.
    La traçabilité réelle est testée localement avec PostgreSQL et DBeaver.
    """
    monkeypatch.setattr("app.main.save_prediction_request", lambda input_data: 1)
    monkeypatch.setattr("app.main.save_prediction_response", lambda request_id, output_data: 1)