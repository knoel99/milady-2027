# Convenience wrapper around build.js (which does the incremental work itself).
SCRIPT ?= script/demo_script.json
WORKERS ?= 4
FPS ?= 30
export NODE_PATH := /opt/node22/lib/node_modules

.PHONY: data plan film scene force stills clean
data:                       ## refresh data/*.json from the repository results (changed files => scenes re-render)
	python3 -I tools/extract_data.py
plan: data                  ## show which scenes would re-render, render nothing
	node build.js $(SCRIPT) --fps $(FPS) --plan
film: data                  ## incremental build of out/film.mp4
	node build.js $(SCRIPT) --fps $(FPS) --workers $(WORKERS)
scene: data                 ## make scene S=b_induction : re-render one scene, then re-assemble
	node build.js $(SCRIPT) --fps $(FPS) --workers $(WORKERS) --only $(S) --force
stills:                     ## make stills S=scenes/b_induction.html T=0.5,2,4
	node stills.js --scene $(S) --times $(T) --outdir out/stills
clean:
	rm -rf out/scenes out/film*.mp4 out/narration.m4a .tmp
