-- Création d'une vue de traçabilité des prédictions.
-- Cette vue permet de visualiser clairement le lien entre :
-- - l'input envoyé au modèle ;
-- - l'output généré par le modèle ;
-- - le modèle utilisé ;
-- - la version du modèle.

CREATE OR REPLACE VIEW ml_api.v_prediction_traces AS
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
    ON r.request_id = o.request_id;