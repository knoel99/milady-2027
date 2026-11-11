"""``python -m milady.eval``: evaluation of a model.

Target of ``make eval`` and template ``infra/slurm/eval.sbatch``.

Same options as ``python -m milady.eval.metrics`` (see ``--help``).
"""

from __future__ import annotations

import sys

from milady.eval.metrics import main

if __name__ == "__main__":
    sys.exit(main())
