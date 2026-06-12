TRUNCATE TABLE ml_api.employees_dataset RESTART IDENTITY;

CREATE TEMP TABLE employee_attrition_staging (
    satisfaction_level TEXT,
    last_evaluation TEXT,
    number_project TEXT,
    average_monthly_hours TEXT,
    time_spend_company TEXT,
    work_accident TEXT,
    left_company TEXT,
    promotion_last_5years TEXT,
    department TEXT,
    salary TEXT
);

\copy employee_attrition_staging FROM 'data/employee_attrition.csv' WITH (FORMAT csv, HEADER true);

INSERT INTO ml_api.employees_dataset (
    satisfaction_level,
    last_evaluation,
    number_project,
    average_monthly_hours,
    time_spend_company,
    work_accident,
    left_company,
    promotion_last_5years,
    department,
    salary
)
SELECT
    satisfaction_level::NUMERIC,
    last_evaluation::NUMERIC,
    number_project::INTEGER,
    average_monthly_hours::INTEGER,
    time_spend_company::INTEGER,
    work_accident::INTEGER::BOOLEAN,
    left_company::INTEGER::BOOLEAN,
    promotion_last_5years::INTEGER::BOOLEAN,
    department,
    salary
FROM employee_attrition_staging;
