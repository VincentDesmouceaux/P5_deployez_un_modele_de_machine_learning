SELECT
    r.request_id,
    r.created_at,
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
