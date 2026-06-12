CREATE SCHEMA IF NOT EXISTS ml_api;

DROP TABLE IF EXISTS ml_api.prediction_responses;
DROP TABLE IF EXISTS ml_api.prediction_requests;
DROP TABLE IF EXISTS ml_api.employees_dataset;

CREATE TABLE ml_api.employees_dataset (
    employee_id SERIAL PRIMARY KEY,

    satisfaction_level NUMERIC(4, 3) NOT NULL CHECK (satisfaction_level >= 0 AND satisfaction_level <= 1),
    last_evaluation NUMERIC(4, 3) NOT NULL CHECK (last_evaluation >= 0 AND last_evaluation <= 1),
    number_project INTEGER NOT NULL CHECK (number_project >= 1),
    average_monthly_hours INTEGER NOT NULL CHECK (average_monthly_hours >= 0),
    time_spend_company INTEGER NOT NULL CHECK (time_spend_company >= 0),

    work_accident BOOLEAN NOT NULL,
    left_company BOOLEAN NOT NULL,
    promotion_last_5years BOOLEAN NOT NULL,

    department VARCHAR(50) NOT NULL,
    salary VARCHAR(20) NOT NULL CHECK (salary IN ('low', 'medium', 'high')),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE ml_api.prediction_requests (
    request_id BIGSERIAL PRIMARY KEY,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source VARCHAR(50) NOT NULL DEFAULT 'api',

    satisfaction_level NUMERIC(4, 3) NOT NULL CHECK (satisfaction_level >= 0 AND satisfaction_level <= 1),
    last_evaluation NUMERIC(4, 3) NOT NULL CHECK (last_evaluation >= 0 AND last_evaluation <= 1),
    number_project INTEGER NOT NULL CHECK (number_project >= 1),
    average_monthly_hours INTEGER NOT NULL CHECK (average_monthly_hours >= 0),
    time_spend_company INTEGER NOT NULL CHECK (time_spend_company >= 0),

    work_accident BOOLEAN NOT NULL,
    promotion_last_5years BOOLEAN NOT NULL,

    department VARCHAR(50) NOT NULL,
    salary VARCHAR(20) NOT NULL CHECK (salary IN ('low', 'medium', 'high')),

    raw_payload JSONB NOT NULL
);

CREATE TABLE ml_api.prediction_responses (
    response_id BIGSERIAL PRIMARY KEY,

    request_id BIGINT NOT NULL REFERENCES ml_api.prediction_requests(request_id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    prediction INTEGER NOT NULL CHECK (prediction IN (0, 1)),
    prediction_label VARCHAR(20) NOT NULL CHECK (prediction_label IN ('stay', 'leave')),
    probability_leave NUMERIC(6, 5) NOT NULL CHECK (probability_leave >= 0 AND probability_leave <= 1),

    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,

    raw_output JSONB NOT NULL
);

CREATE INDEX idx_employees_dataset_left_company
ON ml_api.employees_dataset(left_company);

CREATE INDEX idx_prediction_requests_created_at
ON ml_api.prediction_requests(created_at);

CREATE INDEX idx_prediction_responses_request_id
ON ml_api.prediction_responses(request_id);
