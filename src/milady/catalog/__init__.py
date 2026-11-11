"""MilaDy catalog: campaigns, simulations, files, diagnostics, datasets, models, evaluations, tasks.

PostgreSQL 16 in production (``db`` service of the docker-compose, schema ``infra/db/schema.sql``); SQLite in
portable mode or on a cluster with no reachable database. See :class:`milady.catalog.api.Catalog`.
"""

from __future__ import annotations

from milady.catalog.api import Catalog, default_url, normalize_url

__all__ = ["Catalog", "default_url", "normalize_url"]
