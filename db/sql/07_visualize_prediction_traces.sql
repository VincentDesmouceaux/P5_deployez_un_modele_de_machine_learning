-- Visualisation rapide de la traçabilité des prédictions.
-- Ce script affiche toutes les prédictions enregistrées.
-- Il n'y a volontairement pas de LIMIT afin de voir toutes les traces disponibles.

SELECT
    request_id,
    response_id,
    prediction,
    prediction_label,
    probability_leave,
    model_name,
    model_version
FROM ml_api.v_prediction_traces
ORDER BY request_id DESC;