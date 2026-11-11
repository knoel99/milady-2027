"""Storage of heavy objects (MFF files, checkpoints, figures) through fsspec.

Supported URI schemes:

- ``file:///absolute/path`` or a plain path (``/scratch/...``, ``$SCRATCH/milady``, ``~/data``): local
  disk or parallel file system of an HPC cluster ($WORK, $SCRATCH);
- ``s3://bucket/key``: S3 object storage — MinIO from the docker-compose, AWS S3, Scaleway, OVHcloud…;
- any other fsspec protocol (``gs://``, ``az://``, ``https://``…) if the corresponding package is installed.

Configuration (environment variables, never a secret in the repository):

- ``MILADY_STORAGE_URI``   : storage root (default ``file://<root>/data/store``);
- ``MILADY_S3_ENDPOINT``   : non-AWS S3 endpoint (``http://s3:9000`` for MinIO, ``https://s3.fr-par.scw.cloud``…);
- ``AWS_ACCESS_KEY_ID`` / ``AWS_SECRET_ACCESS_KEY`` (/ ``AWS_SESSION_TOKEN``): S3 credentials;
- ``AWS_DEFAULT_REGION`` or ``AWS_REGION``: region (default ``us-east-1``, accepted by MinIO).

Layout convention: ``{MILADY_STORAGE_URI}/{campaign}/{simulation_uuid}/{kind}.h5``
(see :func:`simulation_uri`).
"""

from __future__ import annotations

import builtins
import hashlib
import os
import shutil
import uuid
from pathlib import Path
from typing import IO, Any

import fsspec

from milady import project_root

__all__ = [
    "DEFAULT_BUCKETS",
    "base_uri",
    "ensure_bucket",
    "exists",
    "filesystem",
    "get",
    "is_local",
    "join",
    "local_path",
    "ls",
    "open",
    "put",
    "rm",
    "sha256",
    "simulation_uri",
    "size",
    "split_uri",
    "storage_options",
]

#: Buckets created by the docker-compose (data, models, MLflow artifacts).
DEFAULT_BUCKETS = ("milady-data", "milady-models", "mlflow")
_CHUNK = 8 * 2**20


# ---------------------------------------------------------------------------------------------
# URI
# ---------------------------------------------------------------------------------------------
def _expand(path: str) -> str:
    """Expand ``$VAR`` and ``~`` in a local path (``$SCRATCH``, ``$WORK`` on clusters)."""
    return os.path.expanduser(os.path.expandvars(path))


def split_uri(uri: str | os.PathLike[str]) -> tuple[str, str]:
    """Split protocol and path: ``s3://b/k`` → ``("s3", "b/k")``; ``/a/b`` → ``("file", "/a/b")``."""
    s = os.fspath(uri)
    if "://" not in s:
        return "file", os.path.abspath(_expand(s))
    proto, rest = s.split("://", 1)
    proto = proto.lower()
    if proto in ("file", "local"):
        return "file", os.path.abspath(_expand(rest))
    if proto in ("s3a", "s3n"):
        proto = "s3"
    return proto, rest


def is_local(uri: str | os.PathLike[str]) -> bool:
    """True for a local path or a ``file://`` URI."""
    return split_uri(uri)[0] == "file"


def local_path(uri: str | os.PathLike[str]) -> Path:
    """Local path of a ``file://`` URI or of a path (error for a remote URI)."""
    proto, path = split_uri(uri)
    if proto != "file":
        raise ValueError(f"Non-local URI: {uri}")
    return Path(path)


def base_uri() -> str:
    """Storage root: ``MILADY_STORAGE_URI`` (``$VAR`` variables expanded) or ``file://<root>/data/store``."""
    env = os.environ.get("MILADY_STORAGE_URI", "").strip()
    if not env:
        return (project_root() / "data" / "store").as_uri()
    proto, path = split_uri(env)
    if proto == "file":
        return Path(path).as_uri()
    return f"{proto}://{path}".rstrip("/")


def join(base: str | os.PathLike[str], *parts: str) -> str:
    """Concatenate path elements onto a URI or a path (``/`` separator in all cases)."""
    out = os.fspath(base).rstrip("/")
    for p in parts:
        p = str(p).strip("/")
        if p:
            out = f"{out}/{p}"
    return out


def simulation_uri(
    campaign: str, simulation_id: str, kind: str = "fields", ext: str = ".h5", base: str | None = None
) -> str:
    """Conventional URI of a simulation file: ``{base}/{campaign}/{uuid}/{kind}{ext}``."""
    return join(base or base_uri(), campaign, simulation_id, f"{kind}{ext}")


# ---------------------------------------------------------------------------------------------
# File systems
# ---------------------------------------------------------------------------------------------
def storage_options(uri: str | os.PathLike[str]) -> dict[str, Any]:
    """fsspec options for the protocol of ``uri`` (S3 credentials and endpoint read from the environment)."""
    proto, _ = split_uri(uri)
    if proto != "s3":
        return {}
    opts: dict[str, Any] = {}
    key, secret = os.environ.get("AWS_ACCESS_KEY_ID"), os.environ.get("AWS_SECRET_ACCESS_KEY")
    if key and secret:
        opts["key"], opts["secret"] = key, secret
        if os.environ.get("AWS_SESSION_TOKEN"):
            opts["token"] = os.environ["AWS_SESSION_TOKEN"]
    endpoint = os.environ.get("MILADY_S3_ENDPOINT") or os.environ.get("AWS_ENDPOINT_URL")
    region = os.environ.get("AWS_DEFAULT_REGION") or os.environ.get("AWS_REGION") or "us-east-1"
    opts["client_kwargs"] = {"region_name": region}
    if endpoint:
        opts["endpoint_url"] = endpoint
        # MinIO and most compatible providers accept path-style addressing
        # (http://host/bucket/key), the only one that works without wildcard DNS.
        opts["config_kwargs"] = {"s3": {"addressing_style": "path"}}
    return opts


def filesystem(uri: str | os.PathLike[str]) -> tuple[fsspec.AbstractFileSystem, str]:
    """fsspec file system and internal path corresponding to ``uri``."""
    proto, path = split_uri(uri)
    if proto == "file":
        return fsspec.filesystem("file"), path
    return fsspec.filesystem(proto, **storage_options(uri)), path


def ensure_bucket(uri: str) -> None:
    """Create the S3 bucket of ``uri`` if it does not exist (no effect for other protocols)."""
    proto, path = split_uri(uri)
    if proto != "s3":
        return
    fs, _ = filesystem(uri)
    bucket = path.split("/", 1)[0]
    try:
        if fs.exists(bucket):
            return
    except (PermissionError, OSError):
        pass
    # Direct call to CreateBucket: s3fs.mkdir would send LocationConstraint = us-east-1, which AWS rejects.
    params: dict[str, Any] = {"Bucket": bucket}
    region = storage_options(uri)["client_kwargs"]["region_name"]
    if region != "us-east-1":
        params["CreateBucketConfiguration"] = {"LocationConstraint": region}
    try:
        fs.call_s3("create_bucket", **params)
    except FileExistsError:
        pass
    except OSError as exc:
        if "BucketAlready" not in repr(exc) and "already" not in str(exc).lower():
            raise
    fs.invalidate_cache(bucket)


# ---------------------------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------------------------
def put(local: str | os.PathLike[str], uri: str) -> str:
    """Copy the local file ``local`` to ``uri``; returns ``uri``.

    Atomic write locally (copy into a temporary file in the same folder, then rename):
    an interrupted job never leaves a truncated file under the final name. On S3, the object only appears
    once the upload is complete; the bucket is created if needed.
    """
    src = Path(local)
    if not src.is_file():
        raise FileNotFoundError(src)
    proto, path = split_uri(uri)
    if proto == "file":
        dst = Path(path)
        if dst.exists() and dst.resolve() == src.resolve():
            return uri
        dst.parent.mkdir(parents=True, exist_ok=True)
        tmp = dst.with_name(f".{dst.name}.{uuid.uuid4().hex[:8]}.part")
        try:
            shutil.copyfile(src, tmp)
            os.replace(tmp, dst)
        finally:
            tmp.unlink(missing_ok=True)
        return uri
    ensure_bucket(uri)
    fs, _ = filesystem(uri)
    fs.put_file(str(src), path)
    fs.invalidate_cache(path)
    return uri


def get(uri: str, local: str | os.PathLike[str]) -> str:
    """Download ``uri`` to the local path ``local`` (folders created, atomic write); returns that path."""
    dst = Path(local)
    dst.parent.mkdir(parents=True, exist_ok=True)
    proto, path = split_uri(uri)
    if proto == "file" and Path(path).resolve() == dst.resolve():
        return str(dst)
    tmp = dst.with_name(f".{dst.name}.{uuid.uuid4().hex[:8]}.part")
    try:
        if proto == "file":
            shutil.copyfile(path, tmp)
        else:
            fs, _ = filesystem(uri)
            fs.get_file(path, str(tmp))
        os.replace(tmp, dst)
    finally:
        tmp.unlink(missing_ok=True)
    return str(dst)


def open(uri: str | os.PathLike[str], mode: str = "rb", **kwargs: Any) -> IO[Any]:  # noqa: A001 (intended API)
    """Open ``uri`` as a file (use with ``with``); folders/bucket created for writing.

    When reading from S3, the object is read in blocks (no full download): ``h5py.File(storage.open(u))``
    only reads the chunks it needs.
    """
    proto, path = split_uri(uri)
    writing = any(c in mode for c in "wax+")
    if proto == "file":
        if writing:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        return builtins.open(path, mode, **kwargs)
    if writing:
        ensure_bucket(os.fspath(uri))
    fs, _ = filesystem(uri)
    return fs.open(path, mode, **kwargs)


def exists(uri: str | os.PathLike[str]) -> bool:
    """True if the object or folder ``uri`` exists (also False if the bucket is missing or inaccessible)."""
    fs, path = filesystem(uri)
    try:
        fs.invalidate_cache(path)
        return bool(fs.exists(path))
    except (FileNotFoundError, PermissionError):
        return False


def size(uri: str | os.PathLike[str]) -> int:
    """Size in bytes of the object ``uri``."""
    fs, path = filesystem(uri)
    return int(fs.size(path))


def sha256(uri: str | os.PathLike[str]) -> str:
    """SHA-256 sum (hexadecimal) of the contents of ``uri``, read in 8 MiB blocks."""
    h = hashlib.sha256()
    with open(uri, "rb") as f:
        while chunk := f.read(_CHUNK):
            h.update(chunk)
    return h.hexdigest()


def ls(uri: str | os.PathLike[str]) -> list[str]:
    """List the contents of the folder ``uri`` (full URIs, sorted)."""
    proto, path = split_uri(uri)
    fs, _ = filesystem(uri)
    fs.invalidate_cache(path)
    names = sorted(fs.ls(path, detail=False))
    if proto == "file":
        return [Path(n).as_uri() for n in names]
    return [f"{proto}://{n}" for n in names]


def rm(uri: str | os.PathLike[str], recursive: bool = False) -> None:
    """Delete the object (or, with ``recursive=True``, the folder) ``uri``; no effect if absent."""
    fs, path = filesystem(uri)
    try:
        fs.rm(path, recursive=recursive)
    except FileNotFoundError:
        pass
    fs.invalidate_cache(path)
