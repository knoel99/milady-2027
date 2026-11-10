# MilaDy 2027 film: pipeline commands (README.md, NARRATION.md). build.js does the incremental work itself.
#   make plan  CUT=core|extended          what would be synthesised / re-rendered (no API call, nothing rendered)
#   make film  CUT=core|extended          full build: TTS (live, cached) + render changed scenes + mix + MP4
#   make films                            both cuts
#   make draft CUT=...                    960x540 15 fps review build (cached voice, placeholder where none)
#   make draft U=ch04 [S=id,id]           960x540 15 fps review video of ONE unit, narration muxed (never writes audio/)
#   make scene S=04.1 [CUT=...]           re-render one scene (forced), then re-assemble
#   make check U=ch04 [S=..] [TIMING=auto|estimate|audio] [EVERY=1.0]   stills around every cue of a unit's scenes
#                                         + page errors + layout QA (never writes audio/, script/_build/ or subs/)
#   make det U=ch04 [S=..] [TIMING=..]    determinism of a unit's scenes (after make check: uses its timeline)
#   make narration VOICE=<id>|default     re-synthesise every paragraph with another voice, rebuild both cuts
#   make narration-script CUT=...         reading script for an external narrator (out/narration_script_<cut>.md)
#   make fit DIR=takes/ [CUT=..] [RETIME=auto]   fit an external recording (NARRATION.md)
#   make tts-dry CUT=...                  print every TTS request and the word counts
#   make test                             end-to-end test on script/_test (placeholder audio, draft, no API)
#   LANG=fr on any target above           French narration over the same English visuals (script/fr/<unit>.json):
#                                         out/film_<cut>_fr.mp4, subs/<cut>_fr.*, stems <cut>_fr_*; LANG=en is the default
export NODE_PATH := /opt/node22/lib/node_modules
# Narration language. LANG is also the locale variable: only the values en and fr select the narration (command
# line or environment); any other value is a locale and means English. The commands themselves then run with
# LANG=C.UTF-8, never with the bare "fr". FILM_LANG=fr is accepted too.
ifneq ($(filter en fr,$(LANG)),)
  FILM_LANG := $(LANG)
  override LANG := C.UTF-8
  export LANG
endif
FILM_LANG ?= en
ifeq ($(filter en fr,$(FILM_LANG)),)
  $(error narration language "$(FILM_LANG)": LANG=en or LANG=fr)
endif
LSFX := $(if $(filter fr,$(FILM_LANG)),_fr,)
LFLAG := --lang $(FILM_LANG)
CUT ?= extended
CUTS ?= core extended
WORKERS ?= 4
NARRATION ?= tts
RETIME ?= none
TTS ?=
OPTS ?=
BUILD = node build.js --workers $(WORKERS) --narration $(NARRATION) $(LFLAG) $(if $(TTS),--tts $(TTS)) $(OPTS)

.PHONY: help data plan film films draft scene check det narration narration-script fit tts-dry tts-test stills test test-fr serve sfx-demo clean clean-draft

help:
	@sed -n '1,17p' Makefile

data:                       ## refresh data/*.json from the repository's existing results (unchanged content is not rewritten)
	python3 -I tools/data_existing.py
	@echo "(cloud results: python3 -I tools/data_cloud.py <converter> ... by hand, see CONTRACT.md section 5)"

plan: data
	$(BUILD) --cut $(CUT) --plan

film: data
	$(BUILD) --cut $(CUT)

films: data
	@set -e; for c in $(CUTS); do $(BUILD) --cut $$c; done

draft: data
	$(if $(U),node build.js --unit $(U) --draft --workers $(WORKERS) $(LFLAG) $(if $(S),--only $(S)) $(if $(TIMING),--timing $(TIMING)) $(OPTS),$(BUILD) --cut $(CUT) --draft)

scene: data
	@test -n "$(S)" || (echo "usage: make scene S=<scene id> [CUT=core|extended] [LANG=fr]"; exit 2)
	$(BUILD) --cut $(CUT) --only $(S) --force

check:
	@test -n "$(U)" || (echo "usage: make check U=<unit> [S=id,id] [TIMING=auto|estimate|audio] [EVERY=1.0] [LANG=fr]"; exit 2)
	node build.js --unit $(U) --check $(LFLAG) $(if $(S),--only $(S)) $(if $(TIMING),--timing $(TIMING)) $(if $(EVERY),--every $(EVERY)) $(OPTS)

EST := $(if $(filter estimate,$(TIMING)),_est,)
det:                        ## make det U=ch04 [S=04.2] [TIMING=estimate]: run make check U=… first (it writes the timeline)
	@test -n "$(U)" || (echo "usage: make det U=<unit> [S=id,id] [TIMING=estimate] [LANG=fr]"; exit 2)
	node tools/determinism.js --timeline out/check/unit_$(U)$(LSFX)$(EST)/build/unit_$(U)$(LSFX)_timeline.json $(if $(S),--only $(S))

narration: data
	@test -n "$(VOICE)" || (echo "usage: make narration VOICE=<reference_id>|default [LANG=fr] [CUTS='core extended']"; exit 2)
	python3 -I tools/set_voice.py $(LFLAG) $(VOICE)
	@set -e; for c in $(CUTS); do $(BUILD) --cut $$c; done

narration-script:
	python3 -I tools/fit_narration.py --cut $(CUT) --export $(LFLAG)

fit:
	@test -n "$(DIR)$(AUDIO)" || (echo "usage: make fit DIR=<folder of <scene id>.wav> | AUDIO=<one file> [CUT=..] [RETIME=none|auto|all] [LANG=fr]"; exit 2)
	python3 -I tools/fit_narration.py --cut $(CUT) $(LFLAG) $(if $(DIR),--dir $(DIR)) $(if $(AUDIO),--audio $(AUDIO)) --retime $(RETIME)

tts-dry:
	python3 -I tools/assemble_cut.py --cut $(CUT) $(LFLAG)
	python3 -I audio/tts.py script/_build/film_$(CUT)$(LSFX).json --mode dry-run

tts-test:                   ## ONE live request: make tts-test SENTENCE="..." UNIT=ch00 [LANG=fr: voice of script/fr/<unit>.json]
	python3 -I audio/tts.py --test "$(SENTENCE)" $(LFLAG) --voice-from $(if $(LSFX),$(firstword $(wildcard script/fr/$(UNIT).json) script/$(UNIT).json),script/$(UNIT).json)

stills:                     ## make stills S=scenes/ch04/04_1_x.html T=0.5,2,4 [ENTRY=file.json]
	node stills.js --scene $(S) --times $(T) --outdir out/stills $(if $(ENTRY),--entry $(ENTRY))

test:                       ## LANG=fr: the French test (tools/test_pipeline_fr.sh)
	bash tools/test_pipeline$(LSFX).sh

test-fr:
	bash tools/test_pipeline_fr.sh

serve:                      ## preview scenes in a browser: http://127.0.0.1:8765/scenes/<unit>/<file>.html
	node tools/server.js 8765

sfx-demo:                   ## every synthesized sound effect once: out/sfx_demo.m4a
	python3 -I audio/mix.py --demo out/sfx_demo.m4a

clean-draft:
	rm -rf out/draft out/check

clean:                      ## renders and builds only (keeps audio/cache: paid TTS)
	rm -rf out/scenes out/scenes_fr out/draft out/check out/stems out/film_* out/*_build_report.json .tmp
