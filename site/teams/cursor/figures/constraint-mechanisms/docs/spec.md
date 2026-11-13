Skeleton: one principle, three cases. The principle is a magnetic field that should stay solenoidal. Each panel keeps the same B glyph.

Hero: none, these are mechanisms, not hardware.

Facts: design is the vector-potential representation in src/milady/train/data.py. The loss penalty is divergence_penalty in src/milady/train/constraints.py. The sampling projection is project_solenoidal after each Heun step in experiments/cursor_fm_train.py.
