# MilaDy 2027 film: pipeline commands (README.md, NARRATION.md). build.js does the incremental work itself.
#   make plan  CUT=core|extended          what would be synthesised / re-rendered (no API call, nothing rendered)
#   make film  CUT=core|extended          full build: TTS (live, cached) + render changed scenes + mix + MP4
#   make films                            both cuts
#   make draft CUT=...                    960x540 15 fps review build (cached voice, placeholder where none)
#   make scene S=04.1 [CUT=...]           re-render one scene (forced), then re-assemble
#   make check U=ch04                     one still per cue for every scene of a unit + page errors + layout QA
#   make narration VOICE=<id>|default     re-synthesise every paragraph with another voice, rebuild both cuts
#   make narration-script CUT=...         reading script for an external narrator (out/narration_script_<cut>.md)
#   make fit DIR=takes/ [CUT=..] [RETIME=auto]   fit an external recording (NARRATION.md)
#   make tts-dry CUT=...                  print every TTS request and the word counts
#   make test                             end-to-end test on script/_test (placeholder audio, draft, no API)
export NODE_PATH := /opt/node22/lib/node_modules
CUT ?= extended
CUTS ?= core extended
WORKERS ?= 4
NARRATION ?= tts
RETIME ?= none
TTS ?=
OPTS ?=
BUILD = node build.js --workers $(WORKERS) --narration $(NARRATION) $(if $(TTS),--tts $(TTS)) $(OPTS)

.PHONY: help data plan film films draft scene check narration narration-script fit tts-dry tts-test stills test serve sfx-demo clean clean-draft

help:
	@sed -n '1,13p' Makefile

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
	$(BUILD) --cut $(CUT) --draft

scene: data
	@test -n "$(S)" || (echo "usage: make scene S=<scene id> [CUT=core|extended]"; exit 2)
	$(BUILD) --cut $(CUT) --only $(S) --force

check:
	@test -n "$(U)" || (echo "usage: make check U=<unit> [S=id,id]"; exit 2)
	node build.js --unit $(U) --check $(if $(S),--only $(S)) $(OPTS)

narration: data
	@test -n "$(VOICE)" || (echo "usage: make narration VOICE=<reference_id>|default [CUTS='core extended']"; exit 2)
	python3 -I tools/set_voice.py $(VOICE)
	@set -e; for c in $(CUTS); do $(BUILD) --cut $$c; done

narration-script:
	python3 -I tools/fit_narration.py --cut $(CUT) --export

fit:
	@test -n "$(DIR)$(AUDIO)" || (echo "usage: make fit DIR=<folder of <scene id>.wav> | AUDIO=<one file> [CUT=..] [RETIME=none|auto|all]"; exit 2)
	python3 -I tools/fit_narration.py --cut $(CUT) $(if $(DIR),--dir $(DIR)) $(if $(AUDIO),--audio $(AUDIO)) --retime $(RETIME)

tts-dry:
	python3 -I tools/assemble_cut.py --cut $(CUT)
	python3 -I audio/tts.py script/_build/film_$(CUT).json --mode dry-run

tts-test:                   ## ONE live request: make tts-test SENTENCE="..." UNIT=ch00
	python3 -I audio/tts.py --test "$(SENTENCE)" --voice-from script/$(UNIT).json

stills:                     ## make stills S=scenes/ch04/04_1_x.html T=0.5,2,4 [ENTRY=file.json]
	node stills.js --scene $(S) --times $(T) --outdir out/stills $(if $(ENTRY),--entry $(ENTRY))

test:
	bash tools/test_pipeline.sh

serve:                      ## preview scenes in a browser: http://127.0.0.1:8765/scenes/<unit>/<file>.html
	node tools/server.js 8765

sfx-demo:                   ## every synthesized sound effect once: out/sfx_demo.m4a
	python3 -I audio/mix.py --demo out/sfx_demo.m4a

clean-draft:
	rm -rf out/draft out/check

clean:                      ## renders and builds only (keeps audio/cache: paid TTS)
	rm -rf out/scenes out/draft out/check out/stems out/film_* out/*_build_report.json .tmp
