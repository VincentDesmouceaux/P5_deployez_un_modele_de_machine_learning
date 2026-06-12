from sqlalchemy import text

from app.database import get_engine
from app.schemas import PredictionInput, PredictionOutput


def save_prediction_request(input_data: PredictionInput) -> int:
    engine = get_engine()

    query = text("""
        INSERT INTO ml_api.prediction_requests (
            employee_id,
            input_payload
        )
        VALUES (
            NULL,
            CAST(:input_payload AS JSONB)
        )
        RETURNING request_id;
    """)

    with engine.begin() as connection:
        request_id = connection.execute(
            query,
            {
                "input_payload": input_data.model_dump_json()
            },
        ).scalar_one()

    return request_id


def save_prediction_response(
    request_id: int,
    output_data: PredictionOutput,
) -> int:
    engine = get_engine()

    query = text("""
        INSERT INTO ml_api.prediction_responses (
            request_id,
            prediction,
            prediction_label,
            probability_leave,
            model_name,
            model_version,
            output_payload
        )
        VALUES (
            :request_id,
            :prediction,
            :prediction_label,
            :probability_leave,
            :model_name,
            :model_version,
            CAST(:output_payload AS JSONB)
        )
        RETURNING response_id;
    """)

    with engine.begin() as connection:
        response_id = connection.execute(
            query,
            {
                "request_id": request_id,
                "prediction": output_data.prediction,
                "prediction_label": output_data.prediction_label,
                "probability_leave": output_data.probability_leave,
                "model_name": output_data.model_name,
                "model_version": output_data.model_version,
                "output_payload": output_data.model_dump_json(),
            },
        ).scalar_one()

    return response_id
