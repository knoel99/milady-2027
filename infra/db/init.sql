-- PostgreSQL initialisation for MilaDy (run only once, when the volume is created, by
-- the official postgres image via /docker-entrypoint-initdb.d/, connected to the POSTGRES_DB database).
--
-- Databases:
--   milady  catalogue of campaigns, simulations, files, datasets, models, evaluations
--           (created by the image from POSTGRES_DB; recreated here if another name was chosen);
--           the tables are created by infra/db/schema.sql (run right after this file, in
--           alphabetical order) or, failing that, by milady.catalog (SQLAlchemy, create_all);
--   mlflow  MLflow server metadata (tables created by MLflow at first start).
--
-- Idempotent: can be replayed by hand without error:
--   docker compose -f infra/docker/docker-compose.yml --env-file infra/docker/.env \
--     exec -T db psql -U milady -d postgres -f /docker-entrypoint-initdb.d/init.sql

SELECT 'CREATE DATABASE milady'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'milady')\gexec

SELECT 'CREATE DATABASE mlflow'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mlflow')\gexec

-- UTC timestamps in both databases (the catalogue stores UTC timestamptz).
ALTER DATABASE milady SET timezone TO 'UTC';
ALTER DATABASE mlflow SET timezone TO 'UTC';

-- Extension useful to the catalogue (gen_random_uuid is native since PostgreSQL 13; pg_trgm is used
-- for text searches on campaign and model names).
\connect milady
CREATE EXTENSION IF NOT EXISTS pg_trgm;
