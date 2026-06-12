SELECT 'employees_dataset' AS table_name, COUNT(*) AS total_rows
FROM ml_api.employees_dataset;

SELECT 'prediction_requests' AS table_name, COUNT(*) AS total_rows
FROM ml_api.prediction_requests;

SELECT 'prediction_responses' AS table_name, COUNT(*) AS total_rows
FROM ml_api.prediction_responses;

SELECT
    left_company,
    COUNT(*) AS total
FROM ml_api.employees_dataset
GROUP BY left_company
ORDER BY left_company;

SELECT
    department,
    COUNT(*) AS total
FROM ml_api.employees_dataset
GROUP BY department
ORDER BY total DESC;

SELECT *
FROM ml_api.employees_dataset
LIMIT 5;
