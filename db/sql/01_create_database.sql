SELECT 'CREATE DATABASE p5_ml_api'
WHERE NOT EXISTS (
    SELECT FROM pg_database WHERE datname = 'p5_ml_api'
)\gexec
