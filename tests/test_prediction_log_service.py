import json

from app.schemas import PredictionInput, PredictionOutput
from app.services import prediction_log_service


class FakeResult:
    """
    Faux résultat SQLAlchemy.

    Il simule le résultat retourné par connection.execute().
    """

    def __init__(self, value=123):
        self.value = value

    def scalar_one(self):
        """
        Simule le retour d'un identifiant SQL généré par PostgreSQL.
        """
        return self.value


class FakeConnection:
    """
    Fausse connexion SQLAlchemy.

    Elle enregistre les requêtes exécutées pour permettre de les tester.
    """

    def __init__(self):
        self.executed_queries = []

    def execute(self, sql_query, parameters=None):
        self.executed_queries.append(
            {
                "sql": str(sql_query),
                "parameters": parameters or {},
            }
        )
        return FakeResult(value=123)


class FakeTransaction:
    """
    Faux contexte transactionnel.

    Il simule le comportement de engine.begin().
    """

    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        return False


class FakeEngine:
    """
    Faux moteur SQLAlchemy.

    Il évite d'appeler une vraie base PostgreSQL pendant les tests.
    """

    def __init__(self):
        self.connection = FakeConnection()

    def begin(self):
        return FakeTransaction(self.connection)


def extract_json_payload(value):
    """
    Convertit un payload JSON stocké sous forme de string ou dict.

    Cette fonction rend le test compatible avec plusieurs styles
    d'implémentation : dict Python ou JSON sérialisé.
    """
    if isinstance(value, str):
        return json.loads(value)

    return value


def test_save_prediction_request_inserts_input_payload_and_returns_request_id(
    monkeypatch,
    valid_prediction_payload,
):
    """
    Vérifie que save_prediction_request() écrit l'input dans la table
    prediction_requests et retourne un request_id.

    Ce test ne dépend pas d'une vraie base PostgreSQL.
    """
    fake_engine = FakeEngine()

    monkeypatch.setattr(
        prediction_log_service,
        "get_engine",
        lambda: fake_engine,
    )

    input_data = PredictionInput(**valid_prediction_payload)

    request_id = prediction_log_service.save_prediction_request(input_data)

    assert request_id == 123
    assert len(fake_engine.connection.executed_queries) == 1

    executed_query = fake_engine.connection.executed_queries[0]

    assert "prediction_requests" in executed_query["sql"]

    parameters = executed_query["parameters"]

    assert "input_payload" in parameters

    payload = extract_json_payload(parameters["input_payload"])

    assert payload["age"] == 41
    assert payload["departement"] == "Commercial"
    assert payload["poste"] == "Cadre Commercial"


def test_save_prediction_response_inserts_output_payload(monkeypatch):
    """
    Vérifie que save_prediction_response() écrit l'output modèle dans
    la table prediction_responses.

    L'appel utilise des arguments positionnels, comme dans app/main.py :
    save_prediction_response(request_id, prediction_output)
    """
    fake_engine = FakeEngine()

    monkeypatch.setattr(
        prediction_log_service,
        "get_engine",
        lambda: fake_engine,
    )

    output_data = PredictionOutput(
        prediction=1,
        prediction_label="leave",
        probability_leave=0.8955,
        model_name="attrition-random-forest",
        model_version="0.5.0",
    )

    prediction_log_service.save_prediction_response(
        99,
        output_data,
    )

    assert len(fake_engine.connection.executed_queries) == 1

    executed_query = fake_engine.connection.executed_queries[0]

    assert "prediction_responses" in executed_query["sql"]

    parameters = executed_query["parameters"]

    assert parameters["request_id"] == 99
    assert parameters["prediction"] == 1
    assert parameters["prediction_label"] == "leave"
    assert parameters["probability_leave"] == 0.8955
    assert parameters["model_name"] == "attrition-random-forest"
    assert parameters["model_version"] == "0.5.0"


def test_save_prediction_response_stores_complete_output_payload(monkeypatch):
    """
    Vérifie que l'output complet est bien conservé sous forme de payload JSON.

    Ce test garantit la traçabilité complète de la réponse modèle.
    """
    fake_engine = FakeEngine()

    monkeypatch.setattr(
        prediction_log_service,
        "get_engine",
        lambda: fake_engine,
    )

    output_data = PredictionOutput(
        prediction=0,
        prediction_label="stay",
        probability_leave=0.4003,
        model_name="attrition-random-forest",
        model_version="0.5.0",
    )

    prediction_log_service.save_prediction_response(
        100,
        output_data,
    )

    assert len(fake_engine.connection.executed_queries) == 1

    parameters = fake_engine.connection.executed_queries[0]["parameters"]

    assert "output_payload" in parameters

    payload = extract_json_payload(parameters["output_payload"])

    assert payload["prediction"] == 0
    assert payload["prediction_label"] == "stay"
    assert payload["probability_leave"] == 0.4003
    assert payload["model_name"] == "attrition-random-forest"
    assert payload["model_version"] == "0.5.0"