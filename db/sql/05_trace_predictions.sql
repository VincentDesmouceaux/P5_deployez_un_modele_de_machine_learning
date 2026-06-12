-- Trace complète des prédictions
-- Objectif : vérifier que chaque input envoyé au modèle est relié
-- à un output généré par le modèle via le même request_id.

SELECT
    r.request_id,
    o.response_id,
    r.created_at AS request_created_at,
    o.created_at AS response_created_at,
    r.source,
    r.employee_id,
    o.prediction,
    o.prediction_label,
    o.probability_leave,
    o.model_name,
    o.model_version,
    r.input_payload,
    o.output_payload
FROM ml_api.prediction_requests r
JOIN ml_api.prediction_responses o
    ON r.request_id = o.request_id
ORDER BY r.request_id DESC
LIMIT 10;