-- =============================================================================================
-- MilaDy catalogue — PostgreSQL 16 schema (version 1.0)
--
-- Exact equivalent of the SQLAlchemy model src/milady/catalog/models.py (same tables, columns, CHECK
-- constraints and indexes; tests/test_catalog.py checks the match). In portable mode (SQLite), the same
-- schema is created by SQLAlchemy (Catalog(create=True)); this file is for PostgreSQL:
--   - automatically at the first start of the "db" service of the docker-compose
--     (mounted in /docker-entrypoint-initdb.d/);
--   - by hand:  psql "$MILADY_DB_URL" -v ON_ERROR_STOP=1 -f infra/db/schema.sql
-- Idempotent: CREATE ... IF NOT EXISTS, CREATE OR REPLACE VIEW. UUID identifiers, UTC timestamps
-- (timestamptz), parameters in JSONB. MLflow uses a separate database (no table here).
--
-- Changes: CREATE TABLE IF NOT EXISTS does not modify an existing table. As long as the schema is
-- at version 1.0, any change is made identically here and in models.py (the match test
-- compares columns, types, DEFAULT, constraints and indexes). Once a production database
-- holds results worth keeping, use Alembic migrations (see the header of
-- src/milady/catalog/models.py) rather than hand-written ALTER TABLE.
-- =============================================================================================

BEGIN;

-- Campaign: set of simulations described by a YAML file (infra/configs/*.yaml).
CREATE TABLE IF NOT EXISTS campaign (
    id           UUID         NOT NULL DEFAULT gen_random_uuid(),
    name         VARCHAR(200) NOT NULL,
    description  TEXT         NOT NULL DEFAULT '',
    config_yaml  TEXT         NOT NULL DEFAULT '',
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT now(),
    PRIMARY KEY (id),
    UNIQUE (name)
);

-- Versioned dataset (frozen list of files split into train / val / test).
CREATE TABLE IF NOT EXISTS dataset (
    id           UUID         NOT NULL DEFAULT gen_random_uuid(),
    name         VARCHAR(200) NOT NULL,
    version      VARCHAR(32)  NOT NULL,
    description  TEXT         NOT NULL DEFAULT '',
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT now(),
    PRIMARY KEY (id),
    CONSTRAINT uq_dataset_name_version UNIQUE (name, version)
);

-- Trained generative model; mlflow_run_id links to the MLflow run, checkpoint_uri to the S3 storage.
CREATE TABLE IF NOT EXISTS model (
    id                    UUID         NOT NULL DEFAULT gen_random_uuid(),
    name                  VARCHAR(200) NOT NULL,
    architecture          VARCHAR(200) NOT NULL DEFAULT '',
    constraint_mechanism  VARCHAR(200) NOT NULL DEFAULT '',
    hyperparams           JSONB        NOT NULL DEFAULT '{}'::jsonb,
    dataset_id            UUID,
    mlflow_run_id         VARCHAR(64),
    checkpoint_uri        TEXT,
    git_commit            VARCHAR(64)  NOT NULL DEFAULT '',
    created_at            TIMESTAMPTZ  NOT NULL DEFAULT now(),
    PRIMARY KEY (id),
    FOREIGN KEY (dataset_id) REFERENCES dataset (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_model_name    ON model (name);
CREATE INDEX IF NOT EXISTS ix_model_dataset ON model (dataset_id);

-- Simulation: a code, a parameter set, a grid.
CREATE TABLE IF NOT EXISTS simulation (
    id            UUID         NOT NULL DEFAULT gen_random_uuid(),
    campaign_id   UUID         NOT NULL,
    code          VARCHAR(64)  NOT NULL,
    code_version  VARCHAR(64)  NOT NULL DEFAULT '',
    git_commit    VARCHAR(64)  NOT NULL DEFAULT '',
    parameters    JSONB        NOT NULL DEFAULT '{}'::jsonb,
    grid          JSONB        NOT NULL DEFAULT '{}'::jsonb,
    status        VARCHAR(16)  NOT NULL DEFAULT 'queued',
    host          VARCHAR(255) NOT NULL DEFAULT '',
    n_gpus        INTEGER      NOT NULL DEFAULT 0,
    n_cpus        INTEGER      NOT NULL DEFAULT 0,
    wall_time_s   DOUBLE PRECISION,
    started_at    TIMESTAMPTZ,
    finished_at   TIMESTAMPTZ,
    notes         TEXT         NOT NULL DEFAULT '',
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
    PRIMARY KEY (id),
    CONSTRAINT ck_simulation_status CHECK (status IN ('queued', 'running', 'done', 'failed')),
    CONSTRAINT ck_simulation_resources CHECK (n_gpus >= 0 AND n_cpus >= 0),
    FOREIGN KEY (campaign_id) REFERENCES campaign (id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_simulation_campaign   ON simulation (campaign_id);
CREATE INDEX IF NOT EXISTS ix_simulation_status     ON simulation (status);
-- Queries on the parameters: parameters @> '{"Rm": 12.0}', parameters ? 'mu_r'...
CREATE INDEX IF NOT EXISTS ix_simulation_parameters ON simulation USING gin (parameters);

-- Lightweight time series (energies, dissipation, helicities, max |div B|) for fast queries.
CREATE TABLE IF NOT EXISTS diagnostic (
    simulation_id  UUID             NOT NULL,
    name           VARCHAR(64)      NOT NULL,
    t              DOUBLE PRECISION NOT NULL,
    value          DOUBLE PRECISION,
    PRIMARY KEY (simulation_id, name, t),
    FOREIGN KEY (simulation_id) REFERENCES simulation (id) ON DELETE CASCADE
);

-- One measurement of a metric for a model, at given physical parameters and seed.
CREATE TABLE IF NOT EXISTS evaluation (
    id          UUID             NOT NULL DEFAULT gen_random_uuid(),
    model_id    UUID             NOT NULL,
    parameters  JSONB            NOT NULL DEFAULT '{}'::jsonb,
    metric      VARCHAR(100)     NOT NULL,
    value       DOUBLE PRECISION,
    n_samples   INTEGER          NOT NULL DEFAULT 0,
    seed        INTEGER          NOT NULL DEFAULT 0,
    details     JSONB,
    created_at  TIMESTAMPTZ      NOT NULL DEFAULT now(),
    PRIMARY KEY (id),
    CONSTRAINT ck_evaluation_n_samples CHECK (n_samples >= 0),
    FOREIGN KEY (model_id) REFERENCES model (id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_evaluation_model_metric ON evaluation (model_id, metric);

-- File produced by a simulation (MFF, checkpoints, logs), identified by its URI
-- ({MILADY_STORAGE_URI}/{campaign}/{simulation_uuid}/{kind}.h5).
CREATE TABLE IF NOT EXISTS file (
    id              UUID             NOT NULL DEFAULT gen_random_uuid(),
    simulation_id   UUID             NOT NULL,
    kind            VARCHAR(16)      NOT NULL,
    uri             TEXT             NOT NULL,
    format_version  VARCHAR(16)      NOT NULL DEFAULT '1.0',
    size_bytes      BIGINT           NOT NULL DEFAULT 0,
    sha256          VARCHAR(64)      NOT NULL DEFAULT '',
    n_t             INTEGER,
    t_start         DOUBLE PRECISION,
    t_end           DOUBLE PRECISION,
    created_at      TIMESTAMPTZ      NOT NULL DEFAULT now(),
    PRIMARY KEY (id),
    CONSTRAINT ck_file_kind CHECK (kind IN ('fields', 'spectral', 'diagnostics', 'checkpoint', 'log')),
    CONSTRAINT ck_file_size CHECK (size_bytes >= 0),
    FOREIGN KEY (simulation_id) REFERENCES simulation (id) ON DELETE CASCADE,
    UNIQUE (uri)
);
CREATE INDEX IF NOT EXISTS ix_file_simulation ON file (simulation_id);
CREATE INDEX IF NOT EXISTS ix_file_kind       ON file (kind);

-- Task submitted to a scheduler; targets a simulation or a model (or neither: job board).
CREATE TABLE IF NOT EXISTS job (
    id             UUID         NOT NULL DEFAULT gen_random_uuid(),
    kind           VARCHAR(32)  NOT NULL,
    scheduler      VARCHAR(16)  NOT NULL,
    external_id    VARCHAR(128) NOT NULL DEFAULT '',
    simulation_id  UUID,
    model_id       UUID,
    status         VARCHAR(16)  NOT NULL DEFAULT 'queued',
    submitted_at   TIMESTAMPTZ  NOT NULL DEFAULT now(),
    started_at     TIMESTAMPTZ,
    finished_at    TIMESTAMPTZ,
    log_uri        TEXT         NOT NULL DEFAULT '',
    PRIMARY KEY (id),
    CONSTRAINT ck_job_scheduler CHECK (scheduler IN ('local', 'docker', 'slurm')),
    CONSTRAINT ck_job_status CHECK (status IN ('queued', 'submitted', 'running', 'done', 'failed', 'cancelled')),
    CONSTRAINT ck_job_target CHECK (simulation_id IS NULL OR model_id IS NULL),
    FOREIGN KEY (simulation_id) REFERENCES simulation (id) ON DELETE SET NULL,
    FOREIGN KEY (model_id) REFERENCES model (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_job_status     ON job (status);
CREATE INDEX IF NOT EXISTS ix_job_external   ON job (scheduler, external_id);
-- Indexed foreign keys: tasks of a simulation or a model, and ON DELETE SET NULL without a full scan.
CREATE INDEX IF NOT EXISTS ix_job_simulation ON job (simulation_id);
CREATE INDEX IF NOT EXISTS ix_job_model      ON job (model_id);

-- Membership of a file in a dataset, with its split.
CREATE TABLE IF NOT EXISTS dataset_member (
    dataset_id  UUID       NOT NULL,
    file_id     UUID       NOT NULL,
    split       VARCHAR(8) NOT NULL,
    PRIMARY KEY (dataset_id, file_id),
    CONSTRAINT ck_dataset_member_split CHECK (split IN ('train', 'val', 'test')),
    FOREIGN KEY (dataset_id) REFERENCES dataset (id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES file (id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_dataset_member_file ON dataset_member (file_id);

-- Evaluation summary: mean and standard deviation (over seeds) per model, metric and parameters.
-- Same query as VIEW_EVAL_SUMMARY_SQL in src/milady/catalog/models.py.
CREATE OR REPLACE VIEW v_eval_summary AS
SELECT e.model_id                AS model_id,
       m.name                    AS model_name,
       m.constraint_mechanism    AS constraint_mechanism,
       e.metric                  AS metric,
       e.parameters              AS parameters,
       COUNT(e.value)            AS n_runs,
       AVG(e.value)              AS mean,
       STDDEV_SAMP(e.value)      AS std,
       MIN(e.value)              AS min,
       MAX(e.value)              AS max,
       SUM(e.n_samples)          AS n_samples_total
FROM evaluation e
JOIN model m ON m.id = e.model_id
GROUP BY e.model_id, m.name, m.constraint_mechanism, e.metric, e.parameters;

COMMENT ON TABLE campaign       IS 'Simulation campaign (YAML configuration)';
COMMENT ON TABLE simulation     IS 'Simulation: code, physical parameters (JSONB), grid, status, resources';
COMMENT ON TABLE file           IS 'Produced file (MFF 1.0, checkpoint, log), URI and SHA-256';
COMMENT ON TABLE diagnostic     IS 'Lightweight time series (mean over trajectories)';
COMMENT ON TABLE dataset        IS 'Versioned, frozen dataset';
COMMENT ON TABLE dataset_member IS 'Files of a dataset and split (train, val, test)';
COMMENT ON TABLE model          IS 'Trained generative model (MLflow link and checkpoint)';
COMMENT ON TABLE evaluation     IS 'Measurement of a physical or statistical metric of a model';
COMMENT ON TABLE job            IS 'Submitted task (local, docker, slurm)';
COMMENT ON VIEW  v_eval_summary IS 'Mean and standard deviation of the evaluations per model, metric and parameters';

COMMIT;
