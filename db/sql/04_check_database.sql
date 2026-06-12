SELECT 'employees_dataset' AS table_name, COUNT(*) AS total_rows
FROM ml_api.employees_dataset;

SELECT 'prediction_requests' AS table_name, COUNT(*) AS total_rows
FROM ml_api.prediction_requests;

SELECT 'prediction_responses' AS table_name, COUNT(*) AS total_rows
FROM ml_api.prediction_responses;

SELECT
    attrition_bin,
    COUNT(*) AS total
FROM ml_api.employees_dataset
GROUP BY attrition_bin
ORDER BY attrition_bin;

SELECT
    a_quitte_l_entreprise,
    attrition_bin,
    COUNT(*) AS total
FROM ml_api.employees_dataset
GROUP BY a_quitte_l_entreprise, attrition_bin
ORDER BY attrition_bin, a_quitte_l_entreprise;

SELECT
    departement,
    COUNT(*) AS total
FROM ml_api.employees_dataset
GROUP BY departement
ORDER BY total DESC;

SELECT
    id_employee,
    age,
    genre,
    departement,
    poste,
    a_quitte_l_entreprise,
    attrition_bin
FROM ml_api.employees_dataset
ORDER BY id_employee
LIMIT 10;
