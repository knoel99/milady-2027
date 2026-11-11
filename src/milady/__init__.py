"""MilaDy: conditional generative models under physical constraints for parametric MHD fields.

Subpackages and modules:

- ``milady.data``    : MFF 1.0 data format (HDF5 compatible with The Well, Zarr variant), validation,
                       converters (E2 → MFF, SFEMaNS skeleton);
- ``milady.catalog`` : SQL catalog of campaigns, simulations, files, datasets, models,
                       evaluations and tasks (PostgreSQL in production, SQLite in portable mode);
- ``milady.storage`` : storage of heavy objects through fsspec (``file://``, HPC paths, ``s3://``);
- ``milady.sim``, ``milady.train``, ``milady.eval``, ``milady.sweep``: solver, training, evaluation,
  campaigns (see ``docs/specs/infra.md``).

Submodules are not imported here: ``import milady`` stays lightweight (no torch, h5py or SQLAlchemy).
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

__version__ = "0.1.0"

__all__ = ["__version__", "git_commit", "project_root"]


def project_root() -> Path:
    """Project root (the folder containing ``pyproject.toml``, ``milady/`` and ``infra/``).

    Resolution order: the ``MILADY_ROOT`` environment variable; the package's parent folder if it
    looks like the repository (editable install ``pip install -e .``); otherwise the current directory.
    Serves as the base for the default catalog (``data/catalog.sqlite``) and storage
    (``data/store``).
    """
    env = os.environ.get("MILADY_ROOT")
    if env:
        return Path(os.path.expandvars(env)).expanduser().resolve()
    here = Path(__file__).resolve().parent.parent
    if (here / "pyproject.toml").is_file() or (here / "infra").is_dir():
        return here
    return Path.cwd().resolve()


def git_commit(path: str | os.PathLike[str] | None = None) -> str:
    """Identifier of the current git commit (12 characters, ``-dirty`` suffix if the tree is modified).

    Order: the ``MILADY_GIT_COMMIT`` variable (set when building the Docker/Apptainer images, where
    ``.git`` is absent), then ``git rev-parse`` in ``path`` (default: project root). Returns
    an empty string if nothing is available: provenance must never make a computation fail.
    ``safe.directory=*``: in a container, the mounted repository is often owned by a different UID than
    the current user ("dubious ownership"); reading the commit remains safe.
    """
    env = os.environ.get("MILADY_GIT_COMMIT")
    if env:
        return env.strip()
    cwd = Path(path) if path is not None else project_root()
    try:
        head = subprocess.run(
            ["git", "-c", "safe.directory=*", "rev-parse", "--short=12", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        ).stdout.strip()
        dirty = subprocess.run(
            # core.fsmonitor disabled: with safe.directory=*, "git status" must not run any
            # command defined in the configuration of a repository owned by another user.
            [
                "git",
                "-c",
                "safe.directory=*",
                "-c",
                "core.fsmonitor=false",
                "status",
                "--porcelain",
                "--untracked-files=no",
            ],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""
    return f"{head}-dirty" if dirty else head
