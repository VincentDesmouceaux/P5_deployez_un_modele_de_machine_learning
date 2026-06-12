CREATE SCHEMA IF NOT EXISTS ml_api;

DROP TABLE IF EXISTS ml_api.prediction_responses CASCADE;
DROP TABLE IF EXISTS ml_api.prediction_requests CASCADE;
DROP TABLE IF EXISTS ml_api.employees_dataset CASCADE;

CREATE TABLE ml_api.employees_dataset (
    id_employee INTEGER PRIMARY KEY,

    age INTEGER,
    genre VARCHAR(10),
    revenu_mensuel INTEGER,
    statut_marital VARCHAR(50),
    departement VARCHAR(100),
    poste VARCHAR(100),

    nombre_experiences_precedentes INTEGER,
    nombre_heures_travailless INTEGER,
    annee_experience_totale INTEGER,
    annees_dans_l_entreprise INTEGER,
    annees_dans_le_poste_actuel INTEGER,

    satisfaction_employee_environnement INTEGER,
    note_evaluation_precedente NUMERIC(8, 3),
    niveau_hierarchique_poste INTEGER,
    satisfaction_employee_nature_travail INTEGER,
    satisfaction_employee_equipe INTEGER,
    satisfaction_employee_equilibre_pro_perso INTEGER,

    eval_number VARCHAR(50),
    note_evaluation_actuelle NUMERIC(8, 3),

    heure_supplementaires VARCHAR(20),
    augementation_salaire_precedente INTEGER,
    a_quitte_l_entreprise VARCHAR(20),

    nombre_participation_pee INTEGER,
    nb_formations_suivies INTEGER,
    nombre_employee_sous_responsabilite INTEGER,

    code_sondage VARCHAR(50),
    distance_domicile_travail INTEGER,
    niveau_education INTEGER,
    domaine_etude VARCHAR(100),
    ayant_enfants VARCHAR(20),
    frequence_deplacement VARCHAR(100),

    annees_depuis_la_derniere_promotion INTEGER,
    annes_sous_responsable_actuel INTEGER,

    attrition_bin INTEGER NOT NULL CHECK (attrition_bin IN (0, 1)),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE ml_api.prediction_requests (
    request_id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    source VARCHAR(50) NOT NULL DEFAULT 'api',
    employee_id INTEGER REFERENCES ml_api.employees_dataset(id_employee),

    input_payload JSONB NOT NULL
);

CREATE TABLE ml_api.prediction_responses (
    response_id BIGSERIAL PRIMARY KEY,
    request_id BIGINT NOT NULL REFERENCES ml_api.prediction_requests(request_id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    prediction INTEGER NOT NULL CHECK (prediction IN (0, 1)),
    prediction_label VARCHAR(20) NOT NULL CHECK (prediction_label IN ('stay', 'leave')),
    probability_leave NUMERIC(8, 5) NOT NULL CHECK (probability_leave >= 0 AND probability_leave <= 1),

    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,

    output_payload JSONB NOT NULL
);

CREATE INDEX idx_employees_dataset_attrition_bin
ON ml_api.employees_dataset(attrition_bin);

CREATE INDEX idx_employees_dataset_departement
ON ml_api.employees_dataset(departement);

CREATE INDEX idx_prediction_requests_created_at
ON ml_api.prediction_requests(created_at);

CREATE INDEX idx_prediction_requests_employee_id
ON ml_api.prediction_requests(employee_id);

CREATE INDEX idx_prediction_responses_request_id
ON ml_api.prediction_responses(request_id);
