"""Static checks of the experiment scripts (they are not imported: they need the data on disk)."""

import ast
from pathlib import Path

EXPERIMENTS = Path(__file__).resolve().parents[1] / "experiments"


def _bound_names(node: ast.AST) -> list[str]:
    """Names bound by assignments, loops, comprehensions excluded (they have their own scope), in ``node``'s own scope."""
    names: list[str] = []
    stack = list(ast.iter_child_nodes(node))
    while stack:
        n = stack.pop()
        if isinstance(n, (ast.FunctionDef, ast.Lambda, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            continue
        targets = []
        if isinstance(n, ast.Assign):
            targets = n.targets
        elif isinstance(n, (ast.AugAssign, ast.AnnAssign, ast.For)):
            targets = [n.target]
        elif isinstance(n, ast.With):
            targets = [i.optional_vars for i in n.items if i.optional_vars is not None]
        for t in targets:
            names += [x.id for x in ast.walk(t) if isinstance(x, ast.Name)]
        stack += list(ast.iter_child_nodes(n))
    return names


def test_e4_result_file_names_are_not_rebound():
    """``save_parts`` of ``e4_mhd3d.run`` names the result files from ``tag``, ``seed`` and ``groups`` of the
    enclosing scope. A later loop ``for tag, keys in …`` once rebound ``tag``: every file written after the
    variant W7 went to ``e4_mhd3dab_s<k>_<g>.json`` and was not brought back from the pod (2026-11-12)."""
    tree = ast.parse((EXPERIMENTS / "e4_mhd3d.py").read_text(encoding="utf-8"))
    run = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "run")
    bound = _bound_names(run)
    for name in ("tag", "groups"):
        assert bound.count(name) == 1, f"`{name}` is bound {bound.count(name)} times in run()"
    assert "seed" not in bound and "group" not in bound          # arguments of run(), never reassigned
