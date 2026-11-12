#!/usr/bin/env bash
# Install the figure skills used for the deliverables (race/DELIVERABLES.md), at pinned commits:
#   schematic-figure (MIT, lgwrightlab)  -> scientific schematics as SVG/PDF/PNG from code
#   archify (Apache-2.0, tt-a1i)         -> architecture, workflow and data-flow diagrams as HTML
# into .claude/skills/ (Claude Code) and .cursor/skills/ (Cursor), both git-ignored.
# Needs git, Node.js >= 22 and a Chromium (Playwright's is fine). Idempotent.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SF_REPO=https://github.com/lgwrightlab/schematic-figure.git
SF_SHA=09d8b6e98d04b91de6e8b6632b3356b9fc237417
AR_REPO=https://github.com/tt-a1i/archify.git
AR_SHA=7e45f36c66de1254d5ad6ba1d878f6499ea269fd
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

fetch() {  # repo sha dir
  git init -q "$3" && git -C "$3" remote add origin "$1"
  git -C "$3" fetch -q --depth 1 origin "$2" && git -C "$3" checkout -q FETCH_HEAD
}
fetch "$SF_REPO" "$SF_SHA" "$TMP/sf"
fetch "$AR_REPO" "$AR_SHA" "$TMP/ar"
(cd "$TMP/ar/archify" && npm ci --silent --no-audit --no-fund >/dev/null 2>&1 || npm install --silent --no-audit --no-fund >/dev/null)

for dest in "$ROOT/.claude/skills" "$ROOT/.cursor/skills"; do
  mkdir -p "$dest"
  rm -rf "$dest/schematic-figure" "$dest/archify"
  cp -r "$TMP/sf/.claude/skills/schematic-figure" "$dest/schematic-figure"
  cp -r "$TMP/ar/archify" "$dest/archify"
  printf 'schematic-figure %s\narchify %s\n' "$SF_SHA" "$AR_SHA" > "$dest/.figure-skills-pinned"
done
echo "installed schematic-figure@${SF_SHA:0:7} and archify@${AR_SHA:0:7} in .claude/skills and .cursor/skills"
echo "archify CLI: node .claude/skills/archify/bin/archify.mjs --help"
