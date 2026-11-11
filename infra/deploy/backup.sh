#!/usr/bin/env bash
# Backup of the MilaDy stack: compressed PostgreSQL dumps ("milady" catalogue and "mlflow") and
# mirror of the object storage (buckets milady-data, milady-models, mlflow) to a target.
#
# Usage :
#   infra/deploy/backup.sh TARGET [--keep N] [--no-objects]
#
# TARGET:
#   /path/to/dir          local disk or mounted volume (e.g. provider block disk);
#   s3://bucket/prefix    bucket of an S3 provider; credentials in the environment:
#                           BACKUP_S3_ENDPOINT   (e.g. https://s3.fr-par.scw.cloud)
#                           BACKUP_ACCESS_KEY, BACKUP_SECRET_KEY
#
# Options :
#   --keep N       (local target) keep only the N latest dumps per database (default 14)
#   --no-objects   PostgreSQL dumps only (no S3 mirror)
#
# Result:
#   TARGET/db/milady-YYYYMMDDTHHMMSSZ.dump, TARGET/db/mlflow-....dump   (pg_dump -Fc, compressed)
#   TARGET/objects/<bucket>/...                                         (mc mirror, incremental)
# Restore: see infra/README.md, "Backup and restore" section.
#
# Idempotent and incremental: run before each VM shutdown, or from cron:
#   17 3 * * * cd ~/milady-2027 && infra/deploy/backup.sh s3://my-bucket/milady >> backups.log 2>&1
set -euo pipefail

usage() { sed -n '2,24p' "$0"; }
[[ $# -ge 1 ]] || { usage; exit 2; }
case "$1" in -h|--help) usage; exit 0 ;; esac
TARGET="$1"; shift
KEEP=14
OBJECTS=1
while [[ $# -gt 0 ]]; do
    case "$1" in
        --keep) KEEP="$2"; shift ;;
        --no-objects) OBJECTS=0 ;;
        *) echo "Unknown option: $1" >&2; exit 2 ;;
    esac
    shift
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ENV_FILE="${MILADY_ENV_FILE:-${REPO_ROOT}/infra/docker/.env}"
[[ -f "${ENV_FILE}" ]] || { echo "infra/docker/.env missing: nothing to back up here." >&2; exit 1; }
COMPOSE=(docker compose -f "${REPO_ROOT}/infra/docker/docker-compose.yml" --env-file "${ENV_FILE}")
env_get() { sed -n "s/^$1=//p" "${ENV_FILE}" | tail -n 1; }
PGUSER_="$(env_get POSTGRES_USER)"; PGUSER_="${PGUSER_:-milady}"
PGDB_="$(env_get POSTGRES_DB)"; PGDB_="${PGDB_:-milady}"
TS="$(date -u +%Y%m%dT%H%M%SZ)"

# Working directory: the target itself if local, otherwise a temporary directory.
if [[ "${TARGET}" == s3://* ]]; then
    : "${BACKUP_S3_ENDPOINT:?set BACKUP_S3_ENDPOINT for an s3:// target}"
    : "${BACKUP_ACCESS_KEY:?set BACKUP_ACCESS_KEY}"
    : "${BACKUP_SECRET_KEY:?set BACKUP_SECRET_KEY}"
    WORK="$(mktemp -d)"
    trap 'rm -rf "${WORK}"' EXIT
    REMOTE=1
else
    mkdir -p "${TARGET}"
    WORK="$(cd "${TARGET}" && pwd)"
    REMOTE=0
fi
mkdir -p "${WORK}/db" "${WORK}/objects"

# --- 1. PostgreSQL dumps ------------------------------------------------------------------------
"${COMPOSE[@]}" exec -T db pg_isready -U "${PGUSER_}" >/dev/null \
    || { echo "the db service is not responding (make up?)" >&2; exit 1; }
for db in "${PGDB_}" mlflow; do
    out="${WORK}/db/${db}-${TS}.dump"
    echo "==> pg_dump ${db} → ${out}"
    # Custom format (-Fc) compressed (-Z 6): selective restore with pg_restore.
    "${COMPOSE[@]}" exec -T db pg_dump -U "${PGUSER_}" -d "${db}" -Fc -Z 6 > "${out}.part"
    mv "${out}.part" "${out}"
    du -h "${out}" | awk '{print "    " $1}'
done
if [[ ${REMOTE} -eq 0 ]]; then
    # Rotation: keep the KEEP latest dumps of each database.
    for db in "${PGDB_}" mlflow; do
        # Timestamped names without special characters: ls -t is enough to sort.
        # shellcheck disable=SC2012
        mapfile -t old < <(ls -1t "${WORK}/db/${db}-"*.dump 2>/dev/null | tail -n "+$((KEEP + 1))")
        [[ ${#old[@]} -eq 0 ]] || rm -f -- "${old[@]}"
    done
fi

# --- 2. Object storage mirror (mc, s3-init container) ---------------------------------------
# The mc container joins the compose network (access to http://s3:9000); the target is mounted on /backup.
# shellcheck disable=SC2016  # expanded in the mc container, not here
MC_SCRIPT='set -eu
mc alias set src http://s3:9000 "$S3_ROOT_USER" "$S3_ROOT_PASSWORD" >/dev/null
if [ -n "${DEST_URL:-}" ]; then
    mc alias set dst "$BACKUP_S3_ENDPOINT" "$BACKUP_ACCESS_KEY" "$BACKUP_SECRET_KEY" >/dev/null
    dest="dst/${DEST_URL#s3://}"
    if [ "$OBJECTS" = 1 ]; then
        for b in milady-data milady-models mlflow; do mc mirror --overwrite "src/$b" "$dest/objects/$b"; done
    fi
    mc mirror --overwrite /backup/db "$dest/db"
else
    if [ "$OBJECTS" = 1 ]; then
        for b in milady-data milady-models mlflow; do mc mirror --overwrite "src/$b" "/backup/objects/$b"; done
    fi
fi'
# Credentials passed to the container by name (-e VAR): never visible in the process list.
export BACKUP_S3_ENDPOINT="${BACKUP_S3_ENDPOINT:-}" BACKUP_ACCESS_KEY="${BACKUP_ACCESS_KEY:-}" \
       BACKUP_SECRET_KEY="${BACKUP_SECRET_KEY:-}"
dest_url=""
[[ ${REMOTE} -eq 1 ]] && dest_url="${TARGET}"
echo "==> Object storage mirror → ${TARGET}"
"${COMPOSE[@]}" run --rm --no-deps -T \
    --user "$(id -u):$(id -g)" \
    -e MC_CONFIG_DIR=/tmp/mc -e OBJECTS="${OBJECTS}" -e DEST_URL="${dest_url}" \
    -e BACKUP_S3_ENDPOINT -e BACKUP_ACCESS_KEY -e BACKUP_SECRET_KEY \
    -v "${WORK}:/backup" \
    --entrypoint /bin/sh s3-init -c "${MC_SCRIPT}"

echo "==> Backup finished (${TS}): ${TARGET}"
