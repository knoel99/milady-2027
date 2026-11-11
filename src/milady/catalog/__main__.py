"""Catalog command line: ``python -m milady.catalog <command>``.

    init                         creates tables, indexes and view (idempotent)
    ingest <uri>… [--campaign C] registers MFF files that are already written (e.g. after a Slurm job array)
    campaigns                    campaigns and number of simulations per status
    sims [--campaign C] [--status S] [--param Rm__gt=8 …]
    summary [--model ID]         v_eval_summary view
The URL comes from ``--url``, otherwise from ``MILADY_DB_URL``, otherwise ``sqlite:///<root>/data/catalog.sqlite``.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from typing import Any

from milady.catalog.api import Catalog


def _value(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point."""
    ap = argparse.ArgumentParser(prog="python -m milady.catalog", description=__doc__.split("\n\n")[0])
    ap.add_argument("--url", default=None, help="SQLAlchemy URL of the catalog")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    p = sub.add_parser("ingest")
    p.add_argument("uris", nargs="+")
    p.add_argument("--campaign", default="default")
    p.add_argument("--kind", default="fields")
    sub.add_parser("campaigns")
    p = sub.add_parser("sims")
    p.add_argument("--campaign")
    p.add_argument("--status")
    p.add_argument(
        "--param", action="append", default=[], help="filter name[__op]=value (op: gt, ge, lt, le, ne, in)"
    )
    p = sub.add_parser("summary")
    p.add_argument("--model")
    args = ap.parse_args(argv)

    cat = Catalog(args.url)
    out: Any
    if args.cmd == "init":
        out = {"url": repr(cat), "status": "ok"}
    elif args.cmd == "ingest":
        out = [{"uri": u, **cat.ingest_mff(u, campaign=args.campaign, kind=args.kind)} for u in args.uris]
    elif args.cmd == "campaigns":
        out = cat.list_campaigns()
    elif args.cmd == "sims":
        filters = dict(item.split("=", 1) for item in args.param)
        out = cat.query_simulations(args.campaign, args.status, **{k: _value(v) for k, v in filters.items()})
    else:
        out = cat.eval_summary(args.model)
    print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
