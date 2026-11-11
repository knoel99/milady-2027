# MilaDy data format — MFF 1.0 (MilaDy Field Format)

Reference specification of the format of the project's simulation results (M2 internship then thesis, stage 1 2D MHD,
stage 2 3D MHD, SFEMaNS data). Reference code: `src/milady/data/format.py` (writing, reading, validation),
`src/milady/data/schema.json` (JSON schema of the metadata), `src/milady/data/convert.py` (converters). Overall
contract: `docs/specs/infra.md`, section 2.

## 1. Principles

1. **Compatible with The Well.** An MFF file on a regular grid is an HDF5 file that follows exactly the
   specification of The Well (Ohana et al., NeurIPS 2024 Datasets & Benchmarks; repository `PolymathicAI/the_well`,
   page `docs/data_format.md`): same groups, same shapes, same attributes. The `WellDataset` loader of
   The Well (1.2.0) must read our fields without modification: its HDF5 accesses, replayed without running the_well, read
   them back identically (§ 8); our tools read files in The Well's format (checked on a dummy file).
2. **One file = one simulation**: one or more trajectories (ensemble members, different seeds) that
   share the same physical parameters and the same grid. The file's `milady_uuid` identifier is that
   of the simulation in the catalog.
3. **MilaDy metadata kept apart**: every addition carries the `milady_` prefix (root attributes, groups
   `milady_diagnostics/`, `milady_spectral/`, `milady_fourier_fe/`). A The Well reader ignores them.
4. **Single precision** for the fields (float32), like The Well; double precision for the diagnostics
   series (energy balances), which are light.
5. **Integrity and reproducibility**: SHA-256 checksum computed at write time and stored in the catalog;
   complete provenance (code, version, git commit, command, host, date, parameters) in the file.

## 2. Tree structure

Real example: a file from experiment E2 (forced 2D MHD, η = 0.008, training split), produced by
`python -m milady.data.convert e2` then displayed by `python -m milady.data.convert info file.h5` (readable
equivalent of `h5dump -H file.h5`). Attributes are written `@name`, datasets `name: type(shape)`.

```text
/
  @dataset_name = 'milady_e2_mhd2d'
  @grid_type = 'cartesian'
  @n_spatial_dims = 2
  @n_trajectories = 16
  @simulation_parameters = ['nu', 'eta', 'Pm', 'alpha', 'eps_u', 'eps_b', 'kf_min', 'kf_max']
  @nu = 0.008   @eta = 0.008   @Pm = 1.0   @alpha = 0.02   @eps_u = 0.05   @eps_b = 0.05   @kf_min = 2.0   @kf_max = 3.0
  @milady_format_version = '1.0'
  @milady_code = 'mhd2d_numpy'
  @milady_code_version = 'milady.sim.mhd2d'
  @milady_git_commit = '07efe3c19375-dirty'
  @milady_parameters = '{"Pm": 1.0, "alpha": 0.02, "eps_b": 0.05, "eps_u": 0.05, "eta": 0.008, ...}'
  @milady_nondimensionalization = "Periodic domain [0, 2π)²; B in Alfvén units ..."
  @milady_created = '2026-11-07T08:03:03Z'
  @milady_host = 'vm'
  @milady_command = 'python -m milady.data.convert e2 data_e2 e2_mff'
  @milady_uuid = '3a3a3ddb-ab0c-47f0-bd08-b94f580880cb'
  @milady_split = 'train'   @milady_seed = 102   @milady_experiment = 'E2'
  @milady_source = 'eta_0.008000_train.npz'   @milady_source_sha256 = '0f323f00…'
  @milady_solver = '{"dt": 0.01, "members": 16, "sampling_interval": 1.0, "scheme": "...", "t_burn": 30.0}'
  dimensions/
    @spatial_dims = ['x', 'y']
    time: float32(150,)                @sample_varying = False
    x: float32(32,)                    @sample_varying = False  @time_varying = False
    y: float32(32,)                    @sample_varying = False  @time_varying = False
  boundary_conditions/
    x_periodic/
      @associated_dims = ['x']  @associated_fields = []  @bc_type = 'periodic'
      @sample_varying = False   @time_varying = False
      mask: bool(32,)                  true at indices 0 and 31
      values: float32(2,)
    y_periodic/                        (same for y)
  scalars/
    @field_names = ['nu', 'eta', 'Pm', 'alpha', 'eps_u', 'eps_b', 'kf_min', 'kf_max',
                    'injection_rate_u', 'injection_rate_b']
    nu: float32()                      @sample_varying = False  @time_varying = False
    ...
    injection_rate_u: float32()        @sample_varying = False  @time_varying = False
  t0_fields/
    @field_names = []
  t1_fields/
    @field_names = ['velocity', 'magnetic_field']
    velocity: float32(16, 150, 32, 32, 2)        chunks=(1, 1, 32, 32, 2) gzip(4)
      @dim_varying = [True, True]  @sample_varying = True  @time_varying = True
    magnetic_field: float32(16, 150, 32, 32, 2)  chunks=(1, 1, 32, 32, 2) gzip(4)
      @dim_varying = [True, True]  @sample_varying = True  @time_varying = True
  t2_fields/
    @field_names = []
  milady_diagnostics/
    @field_names = ['kinetic_energy', 'magnetic_energy', 'enstrophy', 'mean_square_current',
                    'dissipation', 'cross_helicity', 'max_div_b']
    time: float64(150,)
    kinetic_energy: float64(16, 150)   @sample_varying = True  @time_varying = True
    ...
  milady_spectral/
    @field_names = ['vorticity', 'magnetic_potential']
    @transform = 'numpy.fft.rfftn'  @norm = 'backward'  @axes = [2, 3]
    @real_shape = [32, 32]  @spatial_dims = ['x', 'y']  @domain_lengths = [6.2832, 6.2832]
    @wavenumbers = 'k_i = 2π/L_i × numpy.fft.fftfreq(n_i, 1/n_i) ; last axis: numpy.fft.rfftfreq(n_i, 1/n_i)'
    vorticity: complex64(16, 150, 32, 17)        chunks=(1, 1, 32, 17) gzip(4)
      @tensor_order = 0  @physical_field = ''  @kmax = 10
      @sample_varying = True  @time_varying = True
      @description = 'ω = ∂x u_y − ∂y u_x = −Δψ ; u = (∂yψ, −∂xψ) ; state of the mhd2d.py solver'
    magnetic_potential: complex64(16, 150, 32, 17)
      ...
```

For a 3D stage 2 simulation (64³ grid, 4 members, 50 snapshots), the only difference in structure is
`@n_spatial_dims = 3`, `@spatial_dims = ['x', 'y', 'z']`, a `z_periodic/` group and fields
`velocity: float32(4, 50, 64, 64, 64, 3)` split into chunks `(1, 1, 64, 64, 64, 3)`.

## 3. Root attributes

| Attribute | Type | Req. | Origin | Content |
|---|---|---|---|---|
| `dataset_name` | string | yes | The Well | Name of the collection (identical for all files of a folder read by The Well) |
| `grid_type` | string | yes | The Well | `cartesian`, `spherical` (The Well); `fourier_fe_axisym` (MilaDy extension, § 8) |
| `n_spatial_dims` | integer | yes | The Well | 1, 2 or 3; = number of vector components |
| `n_trajectories` | integer | yes | The Well | Number of trajectories B (first axis of the fields) |
| `simulation_parameters` | list of strings | yes | The Well | Names of the **numerical** parameters; each is also a root attribute (float64) and a scalar of `scalars/` |
| `<parameter>` | float | yes | The Well | Value of the parameter (e.g. `@Rm = 12.0`) |
| `milady_format_version` | string | yes | MilaDy | `"1.0"` |
| `milady_code` | string | yes | MilaDy | `mhd3d_torch`, `mhd2d_numpy`, `induction3d_numpy`, `sfemans`, `latu`, `generated` (samples of a model)… |
| `milady_code_version` | string | no | MilaDy | Code version (label, package version) |
| `milady_git_commit` | string | no | MilaDy | Commit (7 to 40 hexadecimal chars, suffix `-dirty` if modified); `MILADY_GIT_COMMIT` in the images |
| `milady_parameters` | JSON string | yes | MilaDy | **All** the parameters, including non-numerical ones: `{"Re": 100, "Rm": 12.0, "Pm": 0.12, "mu_r": 1.0, "forcing": "ABC"}` |
| `milady_nondimensionalization` | string | no | MilaDy | Reference scales (length, velocity, time, Alfvén units for B) |
| `milady_created` | string | yes | MilaDy | ISO 8601 UTC date (`2026-11-07T08:03:03Z`) |
| `milady_host` | string | no | MilaDy | Compute machine |
| `milady_command` | string | no | MilaDy | Command line that produced the file |
| `milady_uuid` | UUID string | yes | MilaDy | Identifier of the simulation in the catalog (`simulation.id`) |
| `milady_<other>` | string / number / JSON | no | MilaDy | Free metadata (`milady_split`, `milady_seed`, `milady_solver`…); structures are in JSON |

Parameter names are identifiers (`[A-Za-z_][A-Za-z0-9_]*`) distinct from the reserved attributes of
The Well and without the `milady_` prefix.

## 4. Groups and datasets

### 4.1 `dimensions/`

`@spatial_dims` gives the order of the spatial axes of the fields (`['x', 'y', 'z']`). `time` (float32, `(T,)`, attribute
`sample_varying`) and a 1D coordinate per axis (float32, attributes `sample_varying` and `time_varying`, always
false for MilaDy). Strictly increasing coordinates; time common to all trajectories. On a periodic domain
`[0, L)`, the points are `x_j = j L / n` (the point `L` is not repeated): `L = n × Δx`.

### 4.2 `boundary_conditions/`

One subgroup per condition, named `<dim>_<type>` (`x_periodic`, `z_wall`…), with the attributes
`associated_dims`, `associated_fields`, `bc_type` ∈ {`periodic`, `wall`, `open`}, `sample_varying`,
`time_varying`, and the datasets `mask` (booleans, shape of the associated dimensions, true where the condition applies:
first and last point for a condition on one axis) and `values` (float32, one value per true point of the mask;
not applicable and zero for `periodic`). By default `write_mff` writes periodic conditions on all axes
(the case of all the project's pseudo-spectral domains).

### 4.3 `scalars/`

`@field_names` lists all the scalars. Each numerical parameter appears there (float32, shape `()`, constant).
Other possible series: shape `()`, `(T,)` (`time_varying`), `(B,)` (`sample_varying`) or `(B, T)`. E2 stores there
the injection rates of the forcing (`injection_rate_u`, `injection_rate_b`).

### 4.4 `t0_fields/`, `t1_fields/`, `t2_fields/`

The three groups always exist (possibly empty), with an exhaustive `@field_names`. Shapes:

| Group | Content | Shape (D = n_spatial_dims) |
|---|---|---|
| `t0_fields` | scalars | `(B, T, n_1, …, n_D)` |
| `t1_fields` | vectors | `(B, T, n_1, …, n_D, D)` |
| `t2_fields` | tensors | `(B, T, n_1, …, n_D, D, D)` (+ `@symmetric`, `@antisymmetric`) |

Attributes of each field: `dim_varying` (booleans, length D), `sample_varying`, `time_varying`. An absent axis
(`dim_varying` false, field constant in time or common to the trajectories) is removed from the shape, as in
The Well. In 2D, an out-of-plane component (B_z of a 2.5D configuration, potential `a` of A = a ẑ) is a field
of `t0_fields`.

**Standard MilaDy fields** (mandatory names, mandatory group, checked by `validate`):

| Name | Group | Quantity |
|---|---|---|
| `velocity` | `t1_fields` | velocity **u** |
| `magnetic_field` | `t1_fields` | magnetic field **B** in Alfvén units (B/√(μ₀ρ), same unit as u) |
| `vector_potential` | `t1_fields` | vector potential **A**, B = ∇×A (gauge specified in `milady_nondimensionalization`) |
| `pressure` | `t0_fields` | pressure (divided by ρ) |

### 4.5 `milady_diagnostics/` (optional)

Light time series, on their own `time` grid (float64, often finer than that of the fields).
Each series: float64, shape `(T_d,)` or `(B, T_d)`, attributes `sample_varying`, `time_varying`. Recommended
names (½⟨·⟩ = spatial average):

| Name | Definition |
|---|---|
| `kinetic_energy`, `magnetic_energy` | ½⟨\|u\|²⟩, ½⟨\|B\|²⟩ |
| `enstrophy`, `mean_square_current` | ⟨\|ω\|²⟩, ⟨\|j\|²⟩ |
| `kinetic_dissipation`, `magnetic_dissipation`, `dissipation` | ν⟨\|ω\|²⟩, η⟨\|j\|²⟩, total (friction included) |
| `injection` | power injected by the forcing |
| `kinetic_helicity`, `magnetic_helicity`, `cross_helicity` | ⟨u·ω⟩, ⟨A·B⟩, ⟨u·B⟩ |
| `max_div_b` | max \|∇·B\| (constraint check) |
| `max_div_u`, `growth_rate`, `magnetic_production`, `u_rms`, `b_rms`, `log_b_rms` | 3D solver (`milady.sim.mhd3d`): max \|∇·u\|, instantaneous growth rate d ln‖B‖/dt, magnetic production ⟨B·∇×(u×B)⟩, root-mean-square values of u and B, logarithm of the root-mean-square value of B (cumulative renormalizations included) |

The catalog keeps a copy (average over the trajectories, `diagnostic` table) for fast queries.

### 4.6 `milady_spectral/` (optional, periodic domains)

`numpy.fft.rfftn` coefficients (`backward` normalization) on the spatial axes, in the layout of the
physical fields: shape `(B, T, n_1, …, n_D//2+1[, D…])`, complex64. Group attributes: `transform`, `norm`, `axes`,
`real_shape`, `spatial_dims`, `domain_lengths`, `wavenumbers` (k_i = 2π/L_i × fftfreq, `rfftfreq` for the
last axis). Attributes of each dataset: `tensor_order`, `physical_field` (name of the physical field of which this is the
**complete** transform — `validate` then checks `irfftn ≈ field` on one snapshot — or an empty string for a
quantity with no stored physical field, such as ω and a in E2), `kmax` (truncation or spectral support, −1 if
none), `description`. Benefits: exact derivatives, constraints ∇·B = 0 and Coulomb gauge k·Â = 0 verifiable
mode by mode, natural representation for generative models in a Fourier basis.

## 5. Physical storage

- **Types**: fields float32, spectral coefficients complex64, diagnostics float64, coordinates float32.
- **Chunks**: one time step of one trajectory per chunk, `chunks = (1, 1, n_1, …, n_D, comp)`; if a chunk
  exceeds 32 MiB (3D beyond ≈ 160³ × 3), the x axis is split in two until it falls below this threshold. Reading
  a snapshot only decompresses its chunks, including from S3.
- **Compression**: `gzip` level 4 with `shuffle` filter (default, readable everywhere) or `lzf` (faster) or none.
- **Integrity**: writing to a temporary file in the same folder then atomic rename; SHA-256 of the final file
  returned by `write_mff` and recorded in `file.sha256`.
- **Layout**: `{MILADY_STORAGE_URI}/{campaign}/{simulation_uuid}/fields.h5` (spectra and diagnostics in this
  file; optional Zarr copy `fields.zarr`; final checkpoint `checkpoint.npz` with
  `runtime.keep_checkpoint`); `MILADY_STORAGE_URI` = `s3://milady-data` (MinIO, AWS, Scaleway, OVHcloud),
  `file:///…`, or `$SCRATCH/milady/store` on a cluster (default of `infra/slurm/env.sh`).
- **Indicative size**: a training E2 file (16 × 150 snapshots 32², u, B, spectra, diagnostics) is
  50 MiB; a 3D 128³ trajectory of 100 snapshots (u, B) ≈ 5 GiB before compression.

## 6. Zarr variant (cloud)

Same hierarchy in Zarr v3 (groups, arrays, identical JSON attributes), same chunking, default Zarr
compression (zstd). It is used to read pieces of very large files from S3 without a full download
or an HDF5 library on the client side. Conversion: `to_zarr("fields.h5", "s3://milady-data/c/<uuid>/fields.zarr")` or
`python -m milady.data.convert zarr fields.h5 s3://…/fields.zarr`. `read_mff`, `validate` and `open_mff`
recognize a URI ending in `.zarr`. The HDF5 file remains the reference (SHA-256 checksum); the Zarr copy
is a reconstructible derivative.

## 7. Python interface and tools

```python
from milady.data import write_mff, read_mff, validate, open_mff, to_zarr

sha = write_mff("s3://milady-data/stage2/<uuid>/fields.h5",
                {"velocity": u, "magnetic_field": b},            # (B, T, nx, ny, nz, 3)
                {"time": t, "x": x, "y": y, "z": z},
                {"Rm": 12.0, "Re": 50.0, "forcing": "ABC"},
                meta={"code": "mhd3d_torch", "code_version": "0.1.0", "uuid": sim_id,
                      "nondimensionalization": "L = 2π, U = 1, B in Alfvén units"},
                diagnostics={"time": t_fine, "magnetic_energy": eb},   # (B, T_d)
                spectral=True)                                   # rfftn of all the fields
d = read_mff(uri, fields=["magnetic_field"], t=slice(-10, None), traj=0)
d["fields"]["magnetic_field"], d["coords"], d["params"], d["meta"], d["diagnostics"], d["scalars"]
assert validate(uri) == []
with open_mff(uri) as f:                                         # h5py.File (or zarr.Group)
    b_last = f["t1_fields/magnetic_field"][0, -1]
```

Command line: `python -m milady.data.convert {e2, validate, info, zarr, sfemans}`; catalog:
`python -m milady.catalog ingest <uri>… --campaign <campaign>` (without `--campaign`, the simulations go into a
"default" campaign) (registers files that have already been written, for example after a Slurm job array
whose nodes cannot reach the database).

**Validation** (`validate(path, well_only=False, full_scan=False)`): root attributes against `schema.json`
(JSON Schema 2020-12, `$defs` subschemas for each node type), mandatory groups, exhaustive `field_names`,
shapes deduced from `sample_varying` / `time_varying` / `dim_varying`, float32, boundary conditions
(masks, values), parameters present at the root, in `scalars/` and equal to `milady_parameters`, standard
fields in their group, consistent diagnostics and spectra, finite values on the first, the median and the
last snapshot of the first trajectory. `full_scan=True` (on the command line: `validate --full`)
checks the values of all trajectories and all snapshots, one chunk at a time: to be done before freezing
a dataset. `well_only=True` only checks The Well part (for The Well's own files).

## 8. Comparison with The Well

| Point | The Well (`docs/data_format.md`) | MFF 1.0 |
|---|---|---|
| Container | HDF5, one file per parameter set, several trajectories | identical; Zarr variant in addition |
| Root attributes | `dataset_name`, `grid_type`, `n_spatial_dims`, `n_trajectories`, `simulation_parameters` + one attribute per parameter | identical, plus the `milady_*` attributes |
| Non-numerical parameters | not provided | in `milady_parameters` (JSON) only |
| `dimensions/` | `spatial_dims`, `time`, coordinates, `sample_varying` / `time_varying` | identical |
| `boundary_conditions/` | subgroups `associated_dims`, `associated_fields`, `bc_type`, `mask`, `values` | identical; lowercase `bc_type` (The Well uppercases them on reading); `values` zero for `periodic` |
| `scalars/` | parameters and series, `float32(1)` | identical; parameters in float32 of shape `()` like the official dummy-data generator (`the_well/utils/dummy_data.py`) |
| `t0/t1/t2_fields/` | `(B, T, W, H[, D][, D, D])` float32, `dim_varying`, `sample_varying`, `time_varying`, `symmetric`, `antisymmetric` | identical; standard names `velocity`, `magnetic_field`, `vector_potential`, `pressure` |
| Chunking, compression | not specified | one-time-step chunks, gzip 4 + shuffle |
| Diagnostics, spectra | absent | `milady_diagnostics/`, `milady_spectral/` |
| Provenance | absent | code, version, commit, command, host, date, catalog UUID, SHA-256 in the catalog |
| Grids | `cartesian`, `spherical` | same, plus `fourier_fe_axisym` (not readable by The Well) |

Practical consequences: (1) a folder of Cartesian MFF files with the same `dataset_name` and the same resolution
loads with The Well's `WellDataset` (normalization: compute `stats.yaml` as for their datasets; files
stored as `<base>/<dataset_name>/data/{train,valid,test}/*.hdf5` or `*.h5`). Checked on 2026-11-07 by replaying
on a 3D MFF file all the HDF5 accesses of `the_well/data/datasets.py` (version 1.2.0: metadata pass,
`_reconstruct_fields`, `_reconstruct_scalars`, `_reconstruct_grids`, `_padding_bcs`): fields read back identically,
expanded names `velocity_x…z`, `PERIODIC` boundary conditions on the three axes. The three groups
`t0_fields`, `t1_fields`, `t2_fields` must exist even if empty (the reader goes through all of them); (2) `read_mff`
and `validate(..., well_only=True)` accept The Well's files (checked on a dummy file built like `the_well/utils/dummy_data.py`, not yet on `MHD_64` nor
`MHD_256`, useful
as external 3D MHD data); (3) The Well imposes a single resolution and a single name per folder: a MilaDy
dataset with several resolutions is stored as one folder per resolution.

## 9. SFEMaNS extension: `grid_type = "fourier_fe_axisym"`

SFEMaNS (Guermond, Léorat, Nore, Ribeiro… ; simulations of Von Kármán dynamos, VKS, precession) discretizes the
fields as a **Fourier series in azimuth θ** and **Lagrange finite elements on the meridian plane (r, z)**:

    f(r, θ, z, t) = Σ_m [ f_m^c(r, z, t) cos(mθ) + f_m^s(r, z, t) sin(mθ) ],   m ∈ {m_0, …, m_{M−1}}.

The format stores these coefficients **as they are, without interpolation** (interpolation to a Cartesian grid
would degrade ∇·B = 0, the jump conditions at the μ_r permeability interfaces and the axial symmetry).

```text
/
  @grid_type = 'fourier_fe_axisym'   @n_spatial_dims = 3   @n_trajectories = B
  @simulation_parameters, parameters, milady_*: as in § 3 (e.g. Rm, Re, mu_r, sigma_r, Ro)
  dimensions/
    @spatial_dims = ['r', 'theta', 'z']
    time: float32(T,)                  @sample_varying = False
  boundary_conditions/                 empty: boundary nodes are in the meshes
  scalars/                             parameters (as in § 4.3)
  t0_fields/ t1_fields/ t2_fields/     @field_names = [] (no tensor grid)
  milady_fourier_fe/
    @field_names = ['velocity', 'magnetic_field', 'pressure']
    @azimuthal_convention = 'f(r, θ, z) = Σ_m [ f_m^c cos(mθ) + f_m^s sin(mθ) ] ; index 0 = cos, 1 = sin'
    @component_basis = 'cylindrical'   (vector components: r, θ, z)
    @n_modes = M
    modes: int32(M,)                   azimuthal wavenumbers m (integers ≥ 0, distinct)
    meshes/
      fluid/                           one subgroup per mesh (SFEMaNS: fluid, conductor, vacuum…)
        @element_type = 'P2'           'P1' (3 nodes) or 'P2' (3 vertices then 3 edge midpoints)
        @n_nodes = N   @n_elements = E
        nodes: float64(N, 2)           coordinates (r, z), r ≥ 0
        connectivity: int32(E, 6)      node indices, 0-based, counterclockwise
        vertices: int32(N_v,)          (optional) vertex indices, support of the P1 fields
        boundary_nodes: int32(N_b,)    (optional) boundary nodes
        region: int32(E,)              (optional) subdomain number (μ_r, σ per region)
      conductor/ ...
    fields/
      velocity: float32(B, T, M, 2, N_fluid, 3)       @mesh = 'fluid'  @node_set = 'all'  @tensor_order = 1
      magnetic_field: float32(B, T, M, 2, N_cond, 3)  @mesh = 'conductor'  @node_set = 'all'  @tensor_order = 1
      pressure: float32(B, T, M, 2, N_v)              @mesh = 'fluid'  @node_set = 'vertices'  @tensor_order = 0
        (axis 3: 0 = cos, 1 = sin ; chunks (1, 1, 1, 2, N[, 3]): one mode of one snapshot per chunk)
```

Rules: vector fields are in **cylindrical** components; the sin coefficients of mode m = 0 are
zero; a field carried by the vertices only (P1 pressure of a P2/P1 discretization) declares
`node_set = 'vertices'` and the mesh provides `vertices`; the scalar potential of the vacuum (H–φ formulation) is
a `t0`-like field of its own mesh. `validate` checks the consistency of the meshes (indices, number of
nodes per element, r ≥ 0), of the modes and of the shapes.

**Tools** (`src/milady/data/convert.py`):

- `write_fourier_fe_mff(path, meshes, modes, fields, time, params, meta=…)` writes this format from arrays;
- `fourier_fe_to_grid(path, field, r, θ, z)` evaluates the field on a regular cylindrical grid
  `(n_r, n_θ, n_z[, 3])`; `fourier_fe_to_cartesian(path, field, x, y, z)` on a Cartesian grid, Cartesian
  components (u_x = u_r cos θ − u_θ sin θ, u_y = u_r sin θ + u_θ cos θ), NaN outside the domain. The meridian
  interpolation is piecewise linear on a Delaunay triangulation of the nodes (exact for a field affine
  in (r, z), approximate for P2); the Fourier summation in θ is exact. For learning, it is often preferable
  to keep the native representation (modes × nodes), which respects the geometry.
- Reader of native SFEMaNS files: **not implemented** (`read_sfemans_native` raises `NotImplementedError`);
  the data are not public. When they become available, it will have to produce the arrays above
  (one mesh per domain, modes, cos/sin coefficients per node), without interpolation.

## 10. Conversion of the E2 data

`python -m milady.data.convert e2 <npz_folder> <output> [--catalog [URL]] [--store URI]` reads the
`eta_<η>_<split>.npz` files of `experiments/e2_data.py` (`rfft2` coefficients of ω and a, `[ky, kx]` layout,
16 members × n snapshots grouped by member) and writes one MFF file per source file:
u = (∂yψ, −∂xψ) with ψ̂ = ω̂/k², B = (∂y a, −∂x a), transposed to the `[x, y]` layout; times
t_j = 30 + j (j = 1…n); parameters ν, η, Pm, α, eps_u, eps_b, kf_min, kf_max; injection rates in `scalars/`;
ω̂ and â (transforms of the `[x, y]` layout) in `milady_spectral/`; per-snapshot diagnostics. Check:
on the real files, the mean dissipation equals the injection to within 1 % (energy balance at the law level). With
`--catalog`, the campaign `e2_mhd2d`, the simulations, files, mean diagnostics and the `e2_mhd2d` v1.0 dataset
(train → train, ref → test) are registered; the command is idempotent.

## 11. Format evolution

Version `milady_format_version = "1.0"`. Versions 1.x only add optional elements (`milady_*` attributes,
`milady_*` groups, diagnostic names): a 1.0 reader reads any 1.x file. Any change to the
shape, type or meaning of an existing element moves to 2.0, with a converter in `src/milady/data/convert.py`.
