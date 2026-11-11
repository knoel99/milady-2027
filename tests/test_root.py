"""Resolution of the project root (``milady.project_root``)."""

from __future__ import annotations

from pathlib import Path

import pytest

import milady

REPO = Path(__file__).resolve().parent.parent


def test_project_root_is_the_repository_from_any_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The package lives in ``src/milady``: the root is two levels up, whatever the current directory."""
    monkeypatch.delenv("MILADY_ROOT", raising=False)
    monkeypatch.chdir(tmp_path)
    root = milady.project_root()
    assert root == REPO
    assert (root / "pyproject.toml").is_file()
    assert (root / "experiments" / "common.py").is_file()


def test_milady_root_variable_takes_precedence(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MILADY_ROOT", str(tmp_path))
    assert milady.project_root() == tmp_path.resolve()
