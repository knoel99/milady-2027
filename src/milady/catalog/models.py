"""SQLAlchemy 2.x model of the MilaDy catalog (equivalent of ``infra/db/schema.sql``).

Portable types:

- identifiers: UUID strings (native ``uuid`` in PostgreSQL, ``VARCHAR(36)`` in SQLite);
- parameters, grids, hyperparameters: ``JSONB`` in PostgreSQL, ``JSON`` (text) in SQLite;
- timestamps: ``timestamptz`` in UTC.

Enumerations (status, file kind, split, scheduler) are ``CHECK`` constraints bearing
the same names as in ``schema.sql``; default values also exist server-side (SQL ``DEFAULT``:
a raw SQL insert, from ``psql`` or another tool, gets them); a test checks that the two
definitions stay identical (columns, types, ``DEFAULT``, constraints, indexes, view).

Schema evolution: ``create_all`` never modifies an existing table. As long as the schema is at
version 1.0, every change is made identically in this file and in ``infra/db/schema.sql``.
Once a production database holds results worth keeping, changes will go through
Alembic migrations (``alembic init infra/db/migrations``; ``target_metadata = Base.metadata``;
``alembic revision --autogenerate`` reviewed by hand, then ``alembic upgrade head`` on PostgreSQL and on
each cluster SQLite catalog): never modify a production table by hand.
"""

from __future__ import annotations

import datetime as _dt
import uuid as _uuid
from typing import Any

from sqlalchemy import (
    JSON,
    BigInteger,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import FunctionElement

__all__ = [
    "FILE_KINDS",
    "JOB_STATUSES",
    "SCHEDULERS",
    "SIMULATION_STATUSES",
    "SPLITS",
    "VIEW_EVAL_SUMMARY_SQL",
    "Base",
    "Campaign",
    "Dataset",
    "DatasetMember",
    "Diagnostic",
    "Evaluation",
    "File",
    "JSONType",
    "Job",
    "Model",
    "Simulation",
    "UUIDStr",
    "new_uuid",
    "utcnow",
    "v_eval_summary",
]

SIMULATION_STATUSES = ("queued", "running", "done", "failed")
FILE_KINDS = ("fields", "spectral", "diagnostics", "checkpoint", "log")
SPLITS = ("train", "val", "test")
SCHEDULERS = ("local", "docker", "slurm")
JOB_STATUSES = ("queued", "submitted", "running", "done", "failed", "cancelled")

#: JSONB in PostgreSQL (indexable, structural equality), JSON elsewhere.
JSONType = JSON().with_variant(JSONB(), "postgresql")
#: Native UUID in PostgreSQL, 36-character string elsewhere; always a ``str`` on the Python side.
UUIDStr = String(36).with_variant(PG_UUID(as_uuid=False), "postgresql")
TZDateTime = DateTime(timezone=True)


class _GenRandomUUID(FunctionElement[str]):
    """Server default of an identifier: ``gen_random_uuid()`` (PostgreSQL ≥ 13), textual UUID v4 elsewhere."""

    type = String(36)
    inherit_cache = True
    name = "gen_random_uuid"


@compiles(_GenRandomUUID, "postgresql")
def _gen_random_uuid_pg(element: Any, compiler: Any, **kw: Any) -> str:
    return "gen_random_uuid()"


@compiles(_GenRandomUUID)
def _gen_random_uuid_default(element: Any, compiler: Any, **kw: Any) -> str:
    # SQLite: 8-4-4-4-12 hexadecimal digits, version 4 and RFC 4122 variant (8, 9, a or b).
    return (
        "(lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || "
        "substr(lower(hex(randomblob(2))), 2) || '-' || substr('89ab', 1 + (abs(random()) % 4), 1) || "
        "substr(lower(hex(randomblob(2))), 2) || '-' || lower(hex(randomblob(6))))"
    )


#: Server-side default values (identical to ``DEFAULT`` in ``infra/db/schema.sql``).
SD_UUID = _GenRandomUUID()
SD_NOW = func.now()
SD_EMPTY = text("''")
SD_ZERO = text("0")
SD_JSON = text("'{}'")


def new_uuid() -> str:
    """New identifier (UUID v4, string)."""
    return str(_uuid.uuid4())


def utcnow() -> _dt.datetime:
    """Current instant in UTC (timezone-aware)."""
    return _dt.datetime.now(_dt.UTC)


def _in(column: str, values: tuple[str, ...], name: str) -> CheckConstraint:
    return CheckConstraint(f"{column} IN ({', '.join(repr(v) for v in values)})", name=name)


class Base(DeclarativeBase):
    """Declarative base of the catalog."""

    type_annotation_map = {dict[str, Any]: JSONType}  # noqa: RUF012 (SQLAlchemy class-level registry)


class Campaign(Base):
    """Campaign: a set of simulations described by a YAML file (``infra/configs/*.yaml``)."""

    __tablename__ = "campaign"
    id: Mapped[str] = mapped_column(UUIDStr, primary_key=True, default=new_uuid, server_default=SD_UUID)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="", server_default=SD_EMPTY)
    config_yaml: Mapped[str] = mapped_column(Text, nullable=False, default="", server_default=SD_EMPTY)
    created_at: Mapped[_dt.datetime] = mapped_column(
        TZDateTime, nullable=False, default=utcnow, server_default=SD_NOW
    )

    simulations: Mapped[list[Simulation]] = relationship(back_populates="campaign", passive_deletes=True)


class Simulation(Base):
    """Simulation: a code, a parameter set, a grid; produces one or more files."""

    __tablename__ = "simulation"
    __table_args__ = (
        _in("status", SIMULATION_STATUSES, "ck_simulation_status"),
        CheckConstraint("n_gpus >= 0 AND n_cpus >= 0", name="ck_simulation_resources"),
        Index("ix_simulation_campaign", "campaign_id"),
        Index("ix_simulation_status", "status"),
        Index("ix_simulation_parameters", "parameters", postgresql_using="gin").ddl_if(dialect="postgresql"),
    )
    id: Mapped[str] = mapped_column(UUIDStr, primary_key=True, default=new_uuid, server_default=SD_UUID)
    campaign_id: Mapped[str] = mapped_column(
        UUIDStr, ForeignKey("campaign.id", ondelete="CASCADE"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    code_version: Mapped[str] = mapped_column(String(64), nullable=False, default="", server_default=SD_EMPTY)
    git_commit: Mapped[str] = mapped_column(String(64), nullable=False, default="", server_default=SD_EMPTY)
    parameters: Mapped[dict[str, Any]] = mapped_column(
        JSONType, nullable=False, default=dict, server_default=SD_JSON
    )
    grid: Mapped[dict[str, Any]] = mapped_column(
        JSONType, nullable=False, default=dict, server_default=SD_JSON
    )
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="queued", server_default=text("'queued'")
    )
    host: Mapped[str] = mapped_column(String(255), nullable=False, default="", server_default=SD_EMPTY)
    n_gpus: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=SD_ZERO)
    n_cpus: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=SD_ZERO)
    wall_time_s: Mapped[float | None] = mapped_column(Float, nullable=True)
    started_at: Mapped[_dt.datetime | None] = mapped_column(TZDateTime, nullable=True)
    finished_at: Mapped[_dt.datetime | None] = mapped_column(TZDateTime, nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=False, default="", server_default=SD_EMPTY)
    created_at: Mapped[_dt.datetime] = mapped_column(
        TZDateTime, nullable=False, default=utcnow, server_default=SD_NOW
    )

    campaign: Mapped[Campaign] = relationship(back_populates="simulations")
    files: Mapped[list[File]] = relationship(
        back_populates="simulation", passive_deletes=True, order_by="File.created_at"
    )


class File(Base):
    """File produced by a simulation (MFF, checkpoints, logs), located by its URI."""

    __tablename__ = "file"
    __table_args__ = (
        _in("kind", FILE_KINDS, "ck_file_kind"),
        CheckConstraint("size_bytes >= 0", name="ck_file_size"),
        Index("ix_file_simulation", "simulation_id"),
        Index("ix_file_kind", "kind"),
    )
    id: Mapped[str] = mapped_column(UUIDStr, primary_key=True, default=new_uuid, server_default=SD_UUID)
    simulation_id: Mapped[str] = mapped_column(
        UUIDStr, ForeignKey("simulation.id", ondelete="CASCADE"), nullable=False
    )
    kind: Mapped[str] = mapped_column(String(16), nullable=False)
    uri: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    format_version: Mapped[str] = mapped_column(
        String(16), nullable=False, default="1.0", server_default=text("'1.0'")
    )
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0, server_default=SD_ZERO)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False, default="", server_default=SD_EMPTY)
    n_t: Mapped[int | None] = mapped_column(Integer, nullable=True)
    t_start: Mapped[float | None] = mapped_column(Float, nullable=True)
    t_end: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[_dt.datetime] = mapped_column(
        TZDateTime, nullable=False, default=utcnow, server_default=SD_NOW
    )

    simulation: Mapped[Simulation] = relationship(back_populates="files")


class Diagnostic(Base):
    """Point of a lightweight time series (energies, dissipation…) for fast queries."""

    __tablename__ = "diagnostic"
    simulation_id: Mapped[str] = mapped_column(
        UUIDStr, ForeignKey("simulation.id", ondelete="CASCADE"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(64), primary_key=True)
    t: Mapped[float] = mapped_column(Float, primary_key=True)
    value: Mapped[float | None] = mapped_column(Float, nullable=True)


class Dataset(Base):
    """Versioned dataset: frozen list of files split into train / val / test."""

    __tablename__ = "dataset"
    __table_args__ = (UniqueConstraint("name", "version", name="uq_dataset_name_version"),)
    id: Mapped[str] = mapped_column(UUIDStr, primary_key=True, default=new_uuid, server_default=SD_UUID)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="", server_default=SD_EMPTY)
    created_at: Mapped[_dt.datetime] = mapped_column(
        TZDateTime, nullable=False, default=utcnow, server_default=SD_NOW
    )

    members: Mapped[list[DatasetMember]] = relationship(back_populates="dataset", passive_deletes=True)


class DatasetMember(Base):
    """Membership of a file in a dataset, with its split."""

    __tablename__ = "dataset_member"
    __table_args__ = (
        _in("split", SPLITS, "ck_dataset_member_split"),
        Index("ix_dataset_member_file", "file_id"),
    )
    dataset_id: Mapped[str] = mapped_column(
        UUIDStr, ForeignKey("dataset.id", ondelete="CASCADE"), primary_key=True
    )
    file_id: Mapped[str] = mapped_column(UUIDStr, ForeignKey("file.id", ondelete="CASCADE"), primary_key=True)
    split: Mapped[str] = mapped_column(String(8), nullable=False)

    dataset: Mapped[Dataset] = relationship(back_populates="members")


class Model(Base):
    """Trained generative model (link to the MLflow run and the checkpoint)."""

    __tablename__ = "model"
    __table_args__ = (Index("ix_model_name", "name"), Index("ix_model_dataset", "dataset_id"))
    id: Mapped[str] = mapped_column(UUIDStr, primary_key=True, default=new_uuid, server_default=SD_UUID)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    architecture: Mapped[str] = mapped_column(
        String(200), nullable=False, default="", server_default=SD_EMPTY
    )
    constraint_mechanism: Mapped[str] = mapped_column(
        String(200), nullable=False, default="", server_default=SD_EMPTY
    )
    hyperparams: Mapped[dict[str, Any]] = mapped_column(
        JSONType, nullable=False, default=dict, server_default=SD_JSON
    )
    dataset_id: Mapped[str | None] = mapped_column(
        UUIDStr, ForeignKey("dataset.id", ondelete="SET NULL"), nullable=True
    )
    mlflow_run_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    checkpoint_uri: Mapped[str | None] = mapped_column(Text, nullable=True)
    git_commit: Mapped[str] = mapped_column(String(64), nullable=False, default="", server_default=SD_EMPTY)
    created_at: Mapped[_dt.datetime] = mapped_column(
        TZDateTime, nullable=False, default=utcnow, server_default=SD_NOW
    )


class Evaluation(Base):
    """One measurement of a metric for a model, at given physical parameters and seed."""

    __tablename__ = "evaluation"
    __table_args__ = (
        Index("ix_evaluation_model_metric", "model_id", "metric"),
        CheckConstraint("n_samples >= 0", name="ck_evaluation_n_samples"),
    )
    id: Mapped[str] = mapped_column(UUIDStr, primary_key=True, default=new_uuid, server_default=SD_UUID)
    model_id: Mapped[str] = mapped_column(UUIDStr, ForeignKey("model.id", ondelete="CASCADE"), nullable=False)
    parameters: Mapped[dict[str, Any]] = mapped_column(
        JSONType, nullable=False, default=dict, server_default=SD_JSON
    )
    metric: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[float | None] = mapped_column(Float, nullable=True)
    n_samples: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=SD_ZERO)
    seed: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=SD_ZERO)
    details: Mapped[dict[str, Any] | None] = mapped_column(JSONType, nullable=True)
    created_at: Mapped[_dt.datetime] = mapped_column(
        TZDateTime, nullable=False, default=utcnow, server_default=SD_NOW
    )


class Job(Base):
    """Task submitted to a scheduler (local, docker, slurm) for a simulation or a model."""

    __tablename__ = "job"
    __table_args__ = (
        _in("scheduler", SCHEDULERS, "ck_job_scheduler"),
        _in("status", JOB_STATUSES, "ck_job_status"),
        CheckConstraint("simulation_id IS NULL OR model_id IS NULL", name="ck_job_target"),
        Index("ix_job_status", "status"),
        Index("ix_job_external", "scheduler", "external_id"),
        Index("ix_job_simulation", "simulation_id"),
        Index("ix_job_model", "model_id"),
    )
    id: Mapped[str] = mapped_column(UUIDStr, primary_key=True, default=new_uuid, server_default=SD_UUID)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    scheduler: Mapped[str] = mapped_column(String(16), nullable=False)
    external_id: Mapped[str] = mapped_column(String(128), nullable=False, default="", server_default=SD_EMPTY)
    simulation_id: Mapped[str | None] = mapped_column(
        UUIDStr, ForeignKey("simulation.id", ondelete="SET NULL"), nullable=True
    )
    model_id: Mapped[str | None] = mapped_column(
        UUIDStr, ForeignKey("model.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="queued", server_default=text("'queued'")
    )
    submitted_at: Mapped[_dt.datetime] = mapped_column(
        TZDateTime, nullable=False, default=utcnow, server_default=SD_NOW
    )
    started_at: Mapped[_dt.datetime | None] = mapped_column(TZDateTime, nullable=True)
    finished_at: Mapped[_dt.datetime | None] = mapped_column(TZDateTime, nullable=True)
    log_uri: Mapped[str] = mapped_column(Text, nullable=False, default="", server_default=SD_EMPTY)


# ---------------------------------------------------------------------------------------------
# View v_eval_summary: mean and standard deviation per model, metric and parameters.
# Same text as in infra/db/schema.sql. In SQLite, stddev_samp is an aggregate function
# registered by milady.catalog.api on each connection.
# ---------------------------------------------------------------------------------------------
VIEW_EVAL_SUMMARY_SQL = """
CREATE VIEW v_eval_summary AS
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
GROUP BY e.model_id, m.name, m.constraint_mechanism, e.metric, e.parameters
""".strip()

#: Typed description of the view (not created by ``create_all``: separate metadata).
view_metadata = MetaData()
v_eval_summary = Table(
    "v_eval_summary",
    view_metadata,
    Column("model_id", UUIDStr),
    Column("model_name", String),
    Column("constraint_mechanism", String),
    Column("metric", String),
    Column("parameters", JSONType),
    Column("n_runs", Integer),
    Column("mean", Float),
    Column("std", Float),
    Column("min", Float),
    Column("max", Float),
    Column("n_samples_total", BigInteger),
)
