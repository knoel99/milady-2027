# Render pipeline: prototype and feasibility (measured on this machine)

Machine: 4 vCPU, 15 GB RAM, no GPU, Chromium headless shell 1243 via Playwright 1.63, ffmpeg 6.1.1 (libx264, libx265, libsvtav1, libass, loudnorm). Prototype: `video_plan/proto/` (all paths below are relative to it). Every number in this file comes from a run whose metrics JSON is in `proto/bench/` or `proto/out/`.

## Summary

- **The pipeline works end to end on this CPU-only machine.** One HTML page per scene with a deterministic runtime (`window.seek(t)`, virtual clock, seeded randomness, fixed-step simulations), recorded frame by frame with headless Chromium (PNG over CDP) into x264, subtitles from the script burned in per scene, narration (placeholder until the Fish Audio key) aligned by sentence and normalised to −16 LUFS, film assembled by stream copy. The demo film (5 scenes, 65.6 s, one section *pending* then *provisional*) builds in **186 s**; incremental rebuilds after a data change take **14 to 23 s** and touch only the affected scene.
- **Measured throughput, 1080p30, 4 cores, best configuration** (frames rendered and encoded per wall-clock second): equations, diagrams and plots **44 fps (1.5× real time)**; dense 2D particles and field lines **7.5 fps (0.25×)**; Three.js 3D through SwiftShader **4.1 fps (0.14×)**. 60 fps has the same per-frame cost (twice the time). 4K: 11 / 3.2 / 3.1 to 4.4 fps (3D costs the same as at 1080p: it is geometry-bound, not pixel-bound).
- **Frames are deterministic**: bit-identical whether reached directly, sequentially or in a fresh browser for the Canvas, KaTeX/GSAP and Three.js scenes; the SVG plot differs on 155 anti-aliased pixels (PSNR 75 dB) after animated states.
- **What matters most**: Chromium flags (CPU raster instead of SwiftShader-for-everything: **14×**), one browser per worker (+26 to +38 %), PNG with `optimizeForSpeed` (+31 % fps; JPEG is barely faster and adds 33 % bitrate), CRF 21 instead of 18 for particle scenes (−29 % size, SSIM 0.976). Disk, not CPU, is the tightest constraint here (8.8 GB free).
- **Full film on this machine** (typical mix 50 % flat / 30 % particles / 20 % 3D, one complete pass): 30 / 45 / 60 min take **1.5 / 2.2 / 3.0 h at 1080p30**, 3.0 / 4.5 / 6.0 h at 1080p60, 2.8 / 4.2 / 5.6 h at 4K30; final files 2.1 to 6.0 GB at CRF 18. **Recommended: 1080p30 master**, CRF 18 (21 for particle scenes), 4 isolated workers, boxed subtitles, −16 LUFS; 60 fps or 4K only if review shows the need.
- **Regenerable sections**: scenes read every number from `data/*.json`; `timeline.json` lists scenes, durations (from audio), cues, status and data dependencies; `build.js` (or `make film`) re-renders only scenes whose inputs changed and re-assembles. A pending section renders a hatched AWAITING frame so the film always assembles; when its data file appears, it is promoted to provisional and re-rendered automatically.

## 1. Architecture

```
script/<film>.json            narration text by scene and paragraph, cue names, status, data deps
   │  audio/tts.py            one TTS request per scene (Fish Audio drama-3), cached by request hash
   ▼
audio/chunks/<scene>.wav      exact durations (decoded PCM)  ──audio/align.py──▶ <scene>.align.json (sentence times)
   │
   ▼  build.js                durations = lead-in + audio + tail, rounded to whole frames; cues = sentence starts
timeline.json  ─────────────▶ subs/film.ass (+ .srt, .vtt) from the SCRIPT text      (subs.js)
   │
   ▼  capture.js              per scene, only if its input hash changed: headless Chromium, window.seek(t)
out/scenes/<scene>.mp4        frame by frame, PNG over CDP, piped to ffmpeg x264, subtitles burned in here
   │
   ▼  build.js                concat (stream copy, no re-encode) + narration (two-pass EBU R128, optional ducked music)
out/film.mp4
```

Files: `runtime/scene.js` (deterministic runtime), `runtime/theme.css` (colour key, fonts), `scenes/*.html` (one self-contained page per scene), `vendor/` (KaTeX 0.16.11, Three.js r160 with Line2, GSAP 3.12.5, Inter, Inter Display, JetBrains Mono, all local), `data/*.json` (scene data), `tools/extract_data.py` (repository results to scene data), `capture.js`, `stills.js`, `subs.js`, `build.js`, `Makefile`, `audio/{tts.py,align.py,lexicon.json}`, `bench/` (benchmark scripts and results), `tools/determinism.js`.

Network: cdn.jsdelivr.net, cdnjs.cloudflare.com, unpkg.com and registry.npmjs.org are reachable, but **nothing is loaded from a CDN at render time**: libraries were installed with npm and copied into `vendor/` (pinned versions, offline renders, no font fallback surprises). api.fish.audio is reachable (no key yet, no call made).

## 2. Deterministic capture

### 2.1 Scene contract (`runtime/scene.js`)

Each scene includes `runtime/scene.js` and calls `Scene.define({duration, cues, data, params, setup(ctx), render(t, ctx)})`.

- `window.seek(t)` (alias `window.__seek`) renders the frame at time `t` and resolves when it is on screen; `window.DURATION`; `window.READY` (fonts loaded, data fetched, `setup` finished). Errors (missing data, bad font name, exceptions) set `window.__SCENE_ERROR__` and make the recorder fail loudly instead of recording a blank scene.
- **Virtual time.** When the recorder sets `window.__CAPTURE__`, `Date.now`, `performance.now` and `requestAnimationFrame` follow the virtual clock; queued rAF callbacks are flushed once per `seek`. Web Animations (CSS animations and transitions included) are paused and set to `currentTime = t`. GSAP is used only as paused timelines driven by `tl.seek(t)` (scene b). Three.js renders inside `render(t)` with `preserveDrawingBuffer: true` (scene c).
- **Seeded randomness**: `Math.random` is replaced by mulberry32 (seed from the timeline entry).
- **Simulations inside scenes**: `Scene.stepper(init, step, dt)` integrates with a fixed `dt` and an integer step count, so the state at time `t` is the same whatever the fps, the seek order or the worker split (scene a: 3,000 tracers with trails and one adaptively refined material line).
- **Timeline injection**: the recorder injects `window.__ENTRY__ = {duration, cues, status, data, params, seed}` from `timeline.json`. Scenes animate relative to named cues (`ctx.cue('adv', 1.2)`), so when the narration changes, the visuals re-time themselves with no code change.
- **Preview mode**: opening a scene in a normal browser plays it in real time with a scrub bar (space, arrow keys), for authoring and review.
- **Status overlay**: `status: "provisional"` adds a PROVISIONAL DATA stamp; `pending` is handled by the scene template (section 6).

### 2.2 Recorder (`capture.js`)

For each frame `f`: `await page.evaluate(seek, f/fps)`, then CDP `Page.captureScreenshot` (`format: png`, `optimizeForSpeed: true`, `fromSurface: true`, `clip.scale` = device scale factor), and the bytes are written to the stdin of `ffmpeg -f image2pipe -c:v png -i - … -c:v libx264 -preset medium -crf 18 -tune animation -pix_fmt yuv420p` with explicit BT.709 conversion and tags (`scale=out_color_matrix=bt709:out_range=tv`, `-colorspace/-color_primaries/-color_trc bt709`), keyframe every 2 s, `+faststart`. No frame touches the disk. With `--workers N` the frame range is split into N contiguous parts, each in its own browser context (with `--isolate`, its own browser) and its own ffmpeg, and the parts are joined by the concat demuxer without re-encoding. Each run writes a metrics JSON (wall time, fps, per-frame ms for seek / screenshot / pipe, whole-machine CPU busy, ffmpeg CPU seconds, measured frame size, MB per minute, page errors). A static HTTP server inside the recorder serves the prototype folder (scenes fetch their JSON data, which `file://` would block).

Chromium flags matter more than anything else on a CPU-only machine:

| `--gpu` mode | flags | scene a, 60 frames, 1 worker | use |
|---|---|---|---|
| `cpu` (default) | `--disable-gpu-compositing --disable-accelerated-2d-canvas --use-angle=swiftshader --enable-unsafe-swiftshader` | **4.52 fps** (screenshot 177 ms/frame) | everything on this machine: Canvas 2D, SVG and DOM rasterised by Skia on the CPU, WebGL still available through SwiftShader |
| `swgl` | `--use-angle=swiftshader --enable-unsafe-swiftshader` (GPU-accelerated 2D canvas emulated by SwiftShader) | 0.32 fps (screenshot 3,071 ms/frame) | never on CPU: **14× slower** |
| `hw` | `--use-angle=default --enable-gpu-rasterization` | not testable here | a cloud GPU instance (WebGL scenes) |

Other flags: `--force-color-profile=srgb` (colours identical to the site), `--font-render-hinting=none`, `--hide-scrollbars`, no background throttling. `--isolate` gives each worker its own browser (own GPU/compositor process).

Two traps found and fixed while building the prototype, worth keeping in the scene checklist:
- Playwright's `waitForFunction` polls with `requestAnimationFrame` by default; the runtime freezes rAF in capture mode, so waiting for `READY` deadlocked whenever the page was not ready at the first poll (it happened with 3 parallel workers). All waits now poll every 50 ms.
- An invalid CSS font shorthand in `document.fonts.load` (`'bold 400 40px …'`) throws; the runtime now turns any setup error into `__SCENE_ERROR__` and the recorder aborts with the message instead of hanging.

Quality checks: `stills.js` renders chosen times to PNG (contact sheets); `tools/determinism.js` checks that a frame is identical whether reached directly, sequentially or in a second browser.

**Determinism, measured** (`tools/determinism.js`, frame at t = 3 s; `bench/determinism.jsonl`): for scenes a (Canvas + fixed-step simulation), b (KaTeX + SVG + GSAP) and c (Three.js) the PNG is **bit-identical** whether the frame is reached directly, after 90 sequential seeks, or in a second fresh browser. Scene d (SVG plot) is identical direct/direct but differs after sequential seeking on 155 of 2,073,600 pixels (max 22/255, PSNR 75.5 dB): anti-aliasing of an SVG path whose opacity and dash offset had been animated (Chromium keeps a different paint state). Invisible, and harmless here because each worker always renders its frames in order; if bit-exactness of SVG ever matters (for example to diff renders in review), the template should set its final styles without intermediate animated states, or the recorder can reload the page per segment.

## 3. Measurements

All runs: 1920×1080 unless stated, H.264 High, CRF 18, preset medium, `-tune animation`, yuv420p BT.709, PNG frames over CDP, `--gpu cpu`. "Capture+encode fps" is frames written to the final mp4 per wall-clock second, page load and segment concatenation included (the encoder runs concurrently in the pipe, so this is the end-to-end throughput). "CPU busy" is the whole machine (4 vCPU) from `/proc/stat`; "ffmpeg CPU s" is the encoder's own CPU time (from the parent shell's `cutime`). Raw data: `proto/bench/*.json`, table generator `proto/bench/summarize.py`.

Test scenes, 6 s each: **a** Canvas 2D, 3,000 tracers with 18-step trails + one material line refined up to 30,000 points (a deliberately heavy 2D case: every pixel changes every frame); **b** SVG + KaTeX + GSAP equation build-up (typical of equations, diagrams, plots, titles); **c** Three.js, 40 fat streamlines (28,000 `LineSegments2` instances), MSAA, orbiting camera, through SwiftShader; **d** the data-driven plot template (SVG).

### 3.1 Frame format (first 60 frames of each scene, 1 worker)

| scene | format | capture+encode fps | screenshot ms | frame kB | MB per min of video |
|---|---|---|---|---|---|
| a (particles) | png (optimizeForSpeed) | 4.57 | 176 | 708 | 81 |
| a (particles) | png, optimizeForSpeed off | 3.48 | 242 | 566 | 81 |
| a (particles) | jpeg q92 | 4.86 | 162 | 395 | 107.4 |
| a (particles) | webp q92 | 2.4 | 370 | 271 | 93.9 |
| b (equation) | png (optimizeForSpeed) | 20.59 | 32 | 49 | 0.6 |
| b (equation) | png, optimizeForSpeed off | 14.97 | 49 | 21 | 0.6 |
| b (equation) | jpeg q92 | 19.27 | 32 | 26 | 0.7 |
| b (equation) | webp q92 | 6.01 | 149 | 11 | 0.7 |

(MB/min here covers only the first 2 s of scene a, before the material line has grown; the full scene is in 3.2.) PNG with `optimizeForSpeed` is the right choice: JPEG saves under 10 % of time but is lossy and its block artefacts make x264 spend **+33 % bitrate** (scene a, 107 against 81 MB/min); WebP is 2 to 5× slower to encode in Chromium. The screenshot (rasterisation + PNG encoding + base64 over CDP) is the bottleneck, not the scene's JavaScript (2 to 14 ms per frame).

### 3.2 Parallel workers, 1080p30 (180 frames)

| run | workers | frames | wall s | capture+encode fps | × real time | ms per frame: seek / screenshot (per worker) | CPU busy | ffmpeg CPU s | MB per min |
|---|---|---|---|---|---|---|---|---|---|
| a particles | 1 | 180 | 48.93 | **3.68** | 0.123 | 14.2 / 233.6 | 49.5 % | 40.1 | 185.9 |
| a particles | 2 | 180 | 31.61 | **5.69** | 0.19 | 27.6 / 245.1 | 71.1 % | 39.3 | 187.3 |
| a particles | 3 | 180 | 26.79 | **6.72** | 0.224 | 38.6 / 250.1 | 83.4 % | 39.8 | 182.9 |
| a particles | 4 | 180 | 25.09 | **7.17** | 0.239 | 55.5 / 271.3 | 89.4 % | 39.4 | 184.2 |
| a particles | 3 iso | 180 | 26.09 | **6.9** | 0.23 | 20.7 / 252.5 | 89.3 % | 40.5 | 182.9 |
| a particles | 4 iso | 180 | 24.13 | **7.46** | 0.249 | 29 / 260.9 | 94.2 % | 39.8 | 184.2 |
| b equation | 1 | 180 | 7.19 | **25.04** | 0.835 | 2.8 / 31.1 | 44 % | 4.8 | 1.4 |
| b equation | 2 | 180 | 5.62 | **32.02** | 1.067 | 2.9 / 42.1 | 57 % | 5.1 | 1.6 |
| b equation | 3 | 180 | 5.13 | **35.09** | 1.17 | 2.7 / 54.6 | 63.1 % | 5.2 | 1.3 |
| b equation | 4 | 180 | 4.95 | **36.38** | 1.213 | 2.6 / 66 | 66.6 % | 5.3 | 1.6 |
| b equation | 3 iso | 180 | 4.07 | **44.18** | 1.473 | 2.8 / 34.7 | 79.7 % | 5 | 1.3 |
| b equation | 4 iso | 180 | 4.31 | **41.78** | 1.393 | 4.3 / 46.2 | 85.8 % | 5.4 | 1.6 |
| d data plot | 3 | 180 | 5.23 | **34.42** | 1.147 | 4.7 / 57.4 | 71.1 % | 5.8 | 2.2 |
| c 3D (WebGL) | 1 | 180 | 66.47 | **2.71** | 0.09 | 4.2 / 354.9 | 77.8 % | 13.4 | 66 |
| c 3D (WebGL) | 2 | 180 | 61.69 | **2.92** | 0.097 | 6.6 / 641.7 | 85.1 % | 14.1 | 67.2 |
| c 3D (WebGL) | 3 | 180 | 60.4 | **2.98** | 0.099 | 13.8 / 918.4 | 85.9 % | 14.1 | 65.7 |
| c 3D (WebGL) | 4 | 180 | 60.83 | **2.96** | 0.099 | 19.7 / 1239.3 | 86.3 % | 14 | 66.4 |
| c 3D (WebGL) | 3 iso | 180 | 49.81 | **3.61** | 0.12 | 10.5 / 522.1 | 90.7 % | 13.8 | 65.7 |
| c 3D (WebGL) | 4 iso | 180 | 44.06 | **4.09** | 0.136 | 15.8 / 578.2 | 93 % | 13.9 | 66.4 |
| c 3D, no MSAA | 3 iso | 180 | 44.86 | **4.01** | 0.134 | 9.1 / 454.9 | 89.7 % | 13.5 | 73.2 |

Reading: flat scenes (equations, diagrams, plots) render **faster than real time** (44 fps, ×1.47); dense 2D particle fields reach **7.5 fps** (×0.25); WebGL through SwiftShader **4.1 fps** (×0.14). Workers sharing one browser stop scaling for WebGL (2.7 → 3.0 fps: one GPU process does all SwiftShader work); one browser per worker (`--isolate`) lifts it to 4.1 fps (+38 %) and the flat scene to 44 fps (+26 %). MSAA costs only 11 % on SwiftShader; halving the resolution does not speed the 3D scene up at all (540p: 4.0 fps), so its cost is geometry (vertex work on 28,000 instanced segments), not pixels: budget 3D scenes by segment and particle counts, not by resolution. The machine is CPU-bound in every heavy case (86 to 94 % busy). Scene a at CRF 18 needs 184 MB per minute (25 Mb/s): high-entropy motion is the size driver (section 3.5).

### 3.3 60 fps (360 frames, 3 shared workers)

| run | workers | frames | wall s | capture+encode fps | × real time | ms per frame: seek / screenshot (per worker) | CPU busy | ffmpeg CPU s | MB per min |
|---|---|---|---|---|---|---|---|---|---|
| a particles | 3 | 360 | 46.77 | **7.7** | 0.128 | 37.5 / 268.1 | 86.5 % | 63.4 | 200.1 |
| b equation | 3 | 360 | 8.84 | **40.73** | 0.679 | 5.1 / 54.1 | 68.5 % | 9.5 | 1.5 |
| c 3D (WebGL) | 3 | 360 | 120.12 | **3** | 0.05 | 9.1 / 946.6 | 85.9 % | 25.1 | 83.3 |

The per-frame cost is unchanged, so a 60 fps film takes twice the render time of 30 fps; the file grows only 9 to 26 % (x264 exploits the smaller differences between frames).

### 3.4 Draft mode (960×540, 15 fps, veryfast, CRF 23, 3 isolated workers)

| run | workers | frames | wall s | capture+encode fps | × real time | ms per frame: seek / screenshot (per worker) | CPU busy | ffmpeg CPU s | MB per min |
|---|---|---|---|---|---|---|---|---|---|
| a particles | 3 iso | 90 | 9.07 | **9.93** | 0.662 | 23.8 / 218.7 | 72.7 % | 2.4 | 35.4 |
| c 3D (WebGL) | 3 iso | 90 | 22.41 | **4.02** | 0.268 | 9.8 / 458.4 | 90.5 % | 1.3 | 10.3 |

Drafts for animatics and review: ×0.66 real time for particles (2.7× faster than 1080p30 per second of film, mostly from half the frames and a faster preset), no gain for WebGL (geometry-bound, see above). These draft runs used scene a's fixed 1920×1080 canvas; the runtime now has `Scene.hidpi(canvas)`, which sizes the backing store from `devicePixelRatio`, so Canvas scenes get both a cheaper draft and a sharp 4K.

### 3.5 4K (3840×2160, 30 fps, `--scale 2`)

| run | workers | frames | wall s | capture+encode fps | × real time | ms per frame: seek / screenshot | CPU busy | MB per min |
|---|---|---|---|---|---|---|---|---|
| b equation | 3 | 180 | 16.4 | **10.97** | 0.366 | 11 / 210 | 70.9 % | 2.9 |
| a particles (hi-DPI canvas) | 3 | 90 | 28.5 | **3.16** | 0.105 | 42 / 525 | 84.9 % | 283.5 |
| c 3D (WebGL) | 3 | 90 | 28.6 | **3.14** | 0.105 | 17 / 737 | 70.7 % | 67.8 |
| c 3D, no MSAA | 3 iso | 90 | 20.6 | **4.37** | 0.146 | 13 / 368 | 80.3 % | 71.1 |

4K is feasible on this machine: flat scenes are 3 to 4× slower than 1080p, particle scenes 2.4× slower (and 54 % larger per minute), and WebGL costs the same as at 1080p (geometry-bound). The encoder alone needs 0.70 CPU-s per 4K particle frame (3.6). Two fixes were needed and are in the prototype: CDP screenshots need `clip.scale = 2` (without it the headless shell returns 1080p frames even with `deviceScaleFactor: 2`; with it the frame is pixel-identical, PSNR ∞, to Playwright's own 4K screenshot), and Canvas scenes must size their backing store from `devicePixelRatio` (`Scene.hidpi`), otherwise a 1080p bitmap is upscaled (the discarded runs are kept in `bench/invalid/` with a note).

### 3.6 Encoder alone (90 saved PNG frames, `bench/run_encode.sh`, `bench/encode.txt`)

| frames | encoder | wall s | encode fps | CPU s | size (3 s of video) | SSIM vs PNG |
|---|---|---|---|---|---|---|
| a 1080p | x264 veryfast CRF 18, tune animation | 2.28 | 39.5 | 8.0 | 11.72 MB | |
| a 1080p | x264 medium CRF 18, tune animation | 6.83 | 13.2 | 23.5 | 11.71 MB | |
| a 1080p | x264 slow CRF 18, tune animation | 11.99 | 7.5 | 42.5 | 11.40 MB | |
| a 2160p (upscaled) | x264 medium CRF 18, tune animation | 18.49 | 4.9 | 63.3 | 19.64 MB | |
| a 1080p | x264 medium CRF 18 (no tune) | 5.65 | 15.9 | 19.9 | 10.64 MB | 0.9863 |
| a 1080p | x264 medium CRF 21 | 5.45 | 16.5 | 18.8 | 7.56 MB (−29 %) | 0.9759 |
| a 1080p | x264 slow CRF 21 | 8.67 | 10.4 | 30.6 | 7.41 MB (−30 %) | 0.9768 |
| a 1080p | x264 medium CRF 24 | 5.09 | 17.7 | 17.6 | 5.30 MB (−50 %) | 0.9602 |
| a 1080p | x265 medium CRF 22 | 11.62 | 7.7 | 43.7 | 9.36 MB (−12 %) | 0.9795 |
| b 1080p | x264 veryfast / medium / slow CRF 18, tune animation | 0.78 / 1.04 / 1.13 | 116 / 86 / 80 | 2.2 / 2.6 / 2.9 | 59 / 70 / 71 kB | |
| b 2160p (upscaled) | x264 medium CRF 18, tune animation | 3.09 | 29 | 7.8 | 141 kB | |
| PNG decoding only | a / b | 0.56 / 0.17 | 161 / 523 | 1.9 / 0.5 | | |

Reading: for flat scenes the encoder is negligible. For dense particle scenes x264 medium costs 0.26 CPU-s per 1080p frame, i.e. about **2 of the 4 cores** at the measured 7.5 fps: the encoder and the browser compete for the CPU. `-tune animation` makes this high-entropy content 10 % larger (10.64 against 11.71 MB) and `slow` saves only 3 %; x265 is 2.2× slower for −12 % at similar SSIM. The best lever is the CRF of particle-heavy scenes: CRF 21 is −29 % for an SSIM still above 0.975 (YouTube re-encodes 1080p to roughly 5–10 Mb/s anyway, far below the 25 Mb/s of scene a at CRF 18). `build.js` accepts a per-scene `"encode": {"crf": 21, "preset": "medium"}` in the script for this.

## 4. Subtitles

- **Source**: the script text, never a transcription (Videobook rule). `subs.js` reads the global cue sheet `subs/cues.json` (sentence id, text, start, end on the film clock, written by `build.js` from the alignment) and writes `subs/film.ass` plus `film.srt` and `film.vtt` (upload them to YouTube as captions too: they are searchable and translatable, the burned-in track is not).
- **Splitting**: at most 2 lines of 42 characters per cue; long sentences are cut at punctuation first, inside a sentence time is shared in proportion to characters; balanced two-line breaks; cue = sentence start − 80 ms to end + 250 ms, minimum gap 80 ms, 1.2 to 6 s per cue; reading speed checked against 17 characters/s (the script reports the cues above it).
- **Key terms**: the script can mark `{u}flow{/}`, `{b}magnetic field{/}`, `{param}Rm{/}`, `{model}…{/}`, `{metric}…{/}`; the first marked term of a cue takes its key colour (one per cue), the markup is stripped from the spoken text.
- **Look** (styles.md 3.9): Inter Medium 42 px at 1920×1080 (`PlayResY: 1080`), `#F2F4F7`, opaque box `rgba(11,15,20,0.78)` with 12 px padding (`BorderStyle 3`), bottom-centre, 64 px from the bottom, 120 ms fade-in with a 4 px rise and 100 ms fade-out (`\fad`, `\move`). The fonts are passed to libass with `fontsdir=vendor/fonts`, so burning does not depend on system fonts. libass cannot round box corners; if rounded boxes are required, subtitles can instead be drawn by the runtime as a DOM layer (same cue sheet), at no extra cost.
- **Where they are burned**: inside `capture.js`, in the same ffmpeg command that encodes the scene (`-vf ass=…`), with the scene's start time as offset. Burning at scene level keeps the final assembly a stream copy; burning on the assembled film would cost a full re-encode of every frame (at the measured encoder speed, about 1.3 h for 60 min at 1080p30 with the typical scene mix, from the encoder-only speeds in 3.6) every time a single word changes.
- **Readability check** (`proto/out/stills/subs_compare_a.png`: top box, bottom outline, both on the densest scene; `subs_box_*.png`, `subs_outline_*.png` full frames): over 3,000 moving tracers the outline-only style lets particles cross the glyphs and the text vibrates; the box keeps it calm and legible, the key-term colour (`flow` in `--u`) stays readable on the box. **Box is recommended.** The two-line block sits between y ≈ 930 and 1016, under the lower-thirds (y 800 to 890) and inside the reserved bottom 180 px. On the demo script: 16 cues, maximum 16 characters/s, none above 17, every line ≤ 42 characters, no orphan words (the splitter balances the parts of a long sentence and checks that each part can be wrapped).

## 5. Audio

**TTS request** (`audio/tts.py`, dry run by default; `--live` needs `FISH_API_KEY`, never written to disk or logs). One request per *logical spoken sequence*: in the prototype one scene's narration (typically 20 to 90 s), which keeps prosody continuous across sentences and keeps a correction local (one scene re-synthesised, not the film). The exact requests are written to `audio/requests/<scene>.json`; the response is cached by the SHA-256 of the request body, so unchanged text is never re-synthesised (and never re-billed).

- `POST https://api.fish.audio/v1/tts`, header `model: drama-3`; body `temperature 0.1, format mp3, mp3_bitrate 192, sample_rate 44100, latency normal, language en, normalize true, condition_on_previous_chunks true, prosody {speed 1.0, normalize_loudness true}, reference_id <narrator voice>` (the validated brainstorm settings).
- Text: one sober acting cue at the start (`[calm, natural narrator voice]`), `[long pause]` only between main paragraphs (the script's `paragraphs` arrays), no short or medium pauses, no `<emphasis>`/`<stress>`, `<slow>` only for a title. To slow down, never `prosody.speed < 1`: use ffmpeg `atempo` in post (it changes the scene duration, which the timeline then absorbs automatically).
- **Phoneme pinning**: `audio/lexicon.json` maps words to ARPAbet pins inserted as `<|phoneme_start|>…<|phoneme_end|>`: MHD `EH1 M EY1 CH D IY1`, ABC `EY1 B IY1 S IY1`, Gissinger `ZH IY0 S AE0 N ZH EY1` (French pronunciation), Reynolds `R EH1 N AH0 L D Z`, Rm `AA1 R EH1 M`, VKS, DRESDYN, SFEMaNS, MilaDy, Kármán, Ohmic, Slurm. Five entries are flagged CHECK (preferred pronunciations to confirm with the supervisors). Example request text: `[calm, natural narrator voice] One equation keeps the score. On one side, the flow stretches and folds the field. On the other, diffusion lets it leak away. [long pause] Their ratio is the magnetic <|phoneme_start|>R EH1 N AH0 L D Z<|phoneme_end|> number, <|phoneme_start|>AA1 R EH1 M<|phoneme_end|>.` (`proto/audio/requests/b_induction.json`).
- **Voice**: `reference_id` is a parameter of the script file. The pipeline uses an original (or properly licensed) narrator voice; it does not clone or imitate any real person.
- mp3 headers give approximate durations and the encoder adds a ~25 ms delay: each response is decoded once to 44.1 kHz PCM and all durations come from the sample count.

**Scene durations from audio** (`build.js`): `frames = round((lead_in + audio_duration + tail) × fps)`, `duration = frames / fps`; the narration track pads each chunk to exactly that length (`adelay` + `apad=whole_dur` + `atrim`), so audio and video can never drift, scene by scene. Cues inside a scene are the sentence starts (`cue = lead_in + sentence.start`), named in the script (`"cue": "adv"`), and the scene animates on those names.

**Sentence timing without a forced aligner** (`audio/align.py`): since each chunk is one scene, its ends are exact; inside it, `silencedetect` (−38 dB, ≥ 0.18 s) finds the pauses, the script predicts where each sentence boundary should be (characters, plus a bonus for paragraph breaks), and a small dynamic programme picks, in order, the pauses that best match, preferring long ones (sentence pauses are longer than commas). Falls back to proportional timing if too few pauses are found. Tested on the placeholder voice, whose true sentence times are known: mean boundary error 4.6 ms, max 7 ms over 5 scenes and 12 sentences; with sentence pauses shortened to comma length (0.22–0.40 s against 0.20–0.32 s for commas, `PLACEHOLDER_HARD=1`), 4.4 ms mean, 7 ms max: the script-based prior picks the right pauses. The placeholder has cleaner pauses than real speech; expect tens of milliseconds on Fish output, to be measured on the first live chunk (the subtitle rules already add 80 ms lead and 250 ms tail).

**Aligners available here** (checked with `pip index versions`, nothing installed): openai-whisper 20250625, faster-whisper 1.2.1, whisperx 3.8.6, stable-ts 2.19.1, ctc-forced-aligner 1.0.2, aeneas 1.7.3.0, vosk 0.3.45, torch 2.15.0 (CPU wheels at download.pytorch.org reachable), onnxruntime 1.29.0 already installed; huggingface.co answers (307 redirect to its CDN), alphacephei.com (Vosk models) reachable. So word-level timing is possible later on CPU (faster-whisper `base.en` int8 or ctc-forced-aligner, a few hundred MB of weights); it is only needed for word-by-word subtitle emphasis. `align.py` is the only file to change, its output format stays the same. A cheaper option to test with the key: Fish Audio's own speech-to-text endpoint, if it returns segment timestamps.

**Loudness**: two-pass `loudnorm` (EBU R128) on the whole narration, target −16 LUFS integrated, −1.5 dBTP, LRA 11, `linear=true` with the measured values of pass 1; then resampled to 48 kHz and encoded AAC 192 kb/s stereo. YouTube normalises playback to about −14 LUFS, so −16 leaves headroom without being quiet; a −14 master is a one-parameter change. Measured on the demo build (placeholder voice + `--music synth` bed): narration pass 1 at −23.9 LUFS / −10.6 dBTP, final mix **−16.0 LUFS integrated, true peak −5.7 dBFS** (checked with `ebur128` on the encoded AAC); the whole audio step (pad, concat, two loudnorm passes, ducking, AAC) took 5.7 s for 65.6 s of film, so about 5 min for 60 min. Audio and video durations match to the frame: 65.600 s, 1,968 video frames and 3,076 AAC frames.

**Music bed (optional)**: `--music file.wav` (or `--music synth` for the test pad) loops the track at −20 dB, ducks it under the voice with `sidechaincompress` (threshold 0.02, ratio 6, attack 30 ms, release 500 ms) keyed by the narration, mixes, then re-runs `loudnorm` on the sum. Music must be licensed for YouTube (Content ID) or original; none is included.

## 6. Regenerable sections

**Data contract.** Scenes never read the repository. `tools/extract_data.py` converts results into small scene-ready JSON files under `data/` (schema for curves: `meta{source, sha256, extracted, stamp}`, `x{label, values, train}`, `y{label}`, `series[{name, kind: simulated|generated, field, y}]`; fields and volumes go to `.f32` Float32 arrays, which the runtime loads as `Float32Array`). Each output keeps the source path and SHA-256 and is rewritten only when its content changes. The pending campaigns get one extractor function each (`palier1_eta_sweep()` is the stub), to fill when `palier1_mhd2d`, `palier2_abc3d`, `palier2_tg3d`, `fm3d`, SFEMaNS/VKS or DRESDYN outputs exist.

**Template + data + cues.** A regenerable scene is a template that reads every number from its data file (no number typed in scene code). `scenes/d_curve.html` is the prototype: with `data/e1_rate.json` (E1 reversal rate versus Γ, 41 points from `experiences/resultats/e1_gissinger.json`: simulation solid, generative model dashed, training Γ filled dots, test Γ open dots, source and hash in the lower third) it draws the result; used for `p1_eta_sweep` with a data file that does not exist yet and `status: pending`, the same template draws the same axes with hatched data areas and `AWAITING · palier1_mhd2d campaign`. A missing data file in a non-pending scene is a build error, never a silent blank.

**Manifest** (`timeline.json`, written by `build.js`): per scene `id, file, status (ready | provisional | pending), start, duration, frames, lead_in, audio, audio_duration, align_method, deps (data files), entry (duration, cues, status, data, params, seed), render, hash, up_to_date`. Status rules: a `pending` scene whose dependencies now exist is promoted to `provisional` automatically (stamp PROVISIONAL DATA on screen until a human marks it `ready` in the script); a `ready` scene whose data disappeared falls back to `pending`.

**Incremental build** (`node build.js script/demo_script.json`, or `make film`; `make plan` lists what would re-render; `make scene S=id` forces one scene): the hash of each scene covers its HTML, the runtime and recorder, the vendored library lockfile, the content of each data dependency, its timeline entry (so a narration change that moves a cue re-renders that scene only), the subtitle events inside its time window, and the render settings. Unchanged scenes are skipped; the film is then re-assembled by stream copy, and only the audio mix is recomputed.

**Demo, measured** (`bench/run_build_demo.sh`, `bench/run_build_demo2.sh`, times in `bench/build_times.txt`, reports `bench/build_report_*.json`). Script `script/demo_script.json`: 5 scenes, 12 sentences, 65.6 s of film (1,968 frames at 1080p30), 4 isolated workers:

| build | what changed | re-rendered | wall time |
|---|---|---|---|
| v1 | everything new | all 5 (a 49.8 s, b 9.5 s, c 103.3 s, d 8.9 s, p1 7.1 s) + audio 5.7 s + assembly 0.2 s | **186 s** (0.35× real time) |
| v2 | nothing | none | 7 s (audio mix and stream-copy assembly only) |
| v3 | the palier1 data file appears (E2 stand-in, `extract_data.py --provisional-e2`) | p1 (promoted to provisional) and d, because the extractor had rewritten `e1_rate.json` with a new extraction date: fixed, the date is now ignored when comparing | 23 s |
| v4 | one E1 result file changes | d only | 17 s |
| vA | re-extraction restores the E1 file | d only | 16 s |
| vB | the palier1 data file disappears | p1 only (back to pending, hatched AWAITING frame) | 14 s |
| vC | the palier1 data file arrives again | p1 only (provisional, stamp on screen, source hash in the lower third) | 14 s |

Outputs: `proto/out/film_v1_pending.mp4` (pending section), `proto/out/film_v3_provisional.mp4` (same film after the data arrived), `proto/out/film.mp4` (latest), contact sheet `proto/out/stills/film_v1_contact.png`, provisional frame `proto/out/stills/film_v3_provisional_t63.png`. The placeholder narration is a synthetic buzz with speech-like timing, useful only to check timing and loudness.

## 7. Estimates for the full film

Method (`proto/bench/estimate.py`, rerun it after new benchmarks): each minute of film is split between three scene classes, each priced at the best measured end-to-end throughput of its test scene (render + encode, 4 cores); 60 fps uses the same per-frame cost with twice the frames and the measured 60 fps file sizes; 2160p60 is extrapolated from 2160p30 (+10 % size). The "typical" mix (50 % flat diagrams, equations, plots and titles; 30 % dense 2D fields and particles; 20 % 3D) follows the style guide's registers (NIGHT about 75 % with simulations, PAPER 15 %, BLUEPRINT 10 %); light and heavy mixes bracket it.

Best measured throughput per class (frames rendered and encoded per second, 4 cores):

| class | format | best run | capture fps | x realtime | MB/min |
|---|---|---|---|---|---|
| flat | 1080p30 | b_30_w3_iso | 44.18 | 1.473 | 1.6 |
| flat | 1080p60 | b_30_w3_iso | 44.18 | 0.736 | 1.5 |
| flat | 2160p30 | b_4k30_w3 | 10.97 | 0.366 | 2.9 |
| dense2d | 1080p30 | a_60_w3 | 7.7 | 0.257 | 184.2 |
| dense2d | 1080p60 | a_60_w3 | 7.7 | 0.128 | 200.1 |
| dense2d | 2160p30 | a_4k30_w3_hidpi | 3.16 | 0.105 | 283.5 |
| webgl | 1080p30 | c_30_w4_iso | 4.09 | 0.136 | 66.4 |
| webgl | 1080p60 | c_30_w4_iso | 4.09 | 0.068 | 83.3 |
| webgl | 2160p30 | c_4k30_w3_iso_noaa | 4.37 | 0.146 | 67.8 |

Estimated wall time (hours) and final file size (GB) for the whole film on this machine:

| mix (flat / dense2d / webgl %) | format | 30 min | 45 min | 60 min | size 30 / 45 / 60 min |
|---|---|---|---|---|---|
| typical (50 / 30 / 20) | 1080p30 | 1.5 | 2.2 | 3.0 | 2.1 / 3.1 / 4.2 |
| typical (50 / 30 / 20) | 1080p60 | 3.0 | 4.5 | 6.0 | 2.3 / 3.5 / 4.6 |
| typical (50 / 30 / 20) | 2160p30 | 2.8 | 4.2 | 5.6 | 3.0 / 4.5 / 6.0 |
| typical (50 / 30 / 20) | 2160p60 | 5.6 | 8.4 | 11.2 | 3.3 / 5.0 / 6.6 |
| light (70 / 20 / 10) | 1080p30 | 1.0 | 1.5 | 2.0 | 1.3 / 2.0 / 2.7 |
| light (70 / 20 / 10) | 1080p60 | 2.0 | 3.0 | 4.0 | 1.5 / 2.2 / 3.0 |
| light (70 / 20 / 10) | 2160p30 | 2.2 | 3.4 | 4.5 | 2.0 / 2.9 / 3.9 |
| light (70 / 20 / 10) | 2160p60 | 4.5 | 6.7 | 9.0 | 2.2 / 3.2 / 4.3 |
| heavy (30 / 40 / 30) | 1080p30 | 2.0 | 3.0 | 4.0 | 2.8 / 4.2 / 5.6 |
| heavy (30 / 40 / 30) | 1080p60 | 4.0 | 5.9 | 7.9 | 3.2 / 4.7 / 6.3 |
| heavy (30 / 40 / 30) | 2160p30 | 3.3 | 5.0 | 6.7 | 4.0 / 6.1 / 8.1 |
| heavy (30 / 40 / 30) | 2160p60 | 6.7 | 10.0 | 13.4 | 4.4 / 6.7 / 8.9 |

What these numbers mean in practice:
- **One full render of a 60 min film at 1080p30 is about 3 h on this machine** (2 to 4 h depending on the mix), at 1080p60 about 6 h, at 4K30 about 5.6 h. A 30 min cut takes half of that. These are single-pass costs: thanks to the incremental build, review cycles only re-render the scenes that changed (the demo in section 6 re-renders one scene in seconds to a minute).
- The test scenes are deliberately heavy for their class (3,000 particles plus a 30,000-point line; 28,000 3D segments). Lighter scenes are faster; the estimate is on the safe side for 2D, and 3D cost scales with geometry, not with resolution.
- **Disk**: final film 2 to 6 GB at CRF 18 (particle scenes dominate: 184 MB/min at 1080p, 284 MB/min at 4K). The build keeps every scene file (for incremental rebuilds) plus the final film, so plan **twice the final size plus margin**. This machine has 8.8 GB free on `/`: enough for 30 to 45 min at 1080p, tight for 60 min at CRF 18 (4.2 GB × 2), not enough for 60 min in 4K. CRF 21 on particle scenes (−29 %, section 3.6) brings 60 min 1080p30 to about 3.2 GB. No frame is ever written to disk (PNG frames would be 0.05 to 0.7 MB each, 75 GB for 60 min of particles).
- Audio, subtitles and assembly are negligible: TTS dry run + alignment of 5 scenes 0.5 s, loudness two-pass and mux a few seconds per minute of film, final concatenation by stream copy.
- **Scaling out**: scenes are independent, so a rented 16 or 32 vCPU machine (or several) renders scenes in parallel with the same code (`build.js --only`, or one `capture.js` per scene); expect close to linear speed-up per core for 2D. A GPU instance (`--gpu hw`) would remove the SwiftShader bottleneck for 3D scenes (not measurable here).

## 8. Recommended settings

| topic | recommendation | why (measured) |
|---|---|---|
| Delivery format | **1080p30** master for the first release; 1080p60 only if the camera moves and particle shots look choppy in review; 4K only if needed for a big screen | 1080p30 ≈ 3 h per full 60 min render; 60 fps doubles it; 4K30 ≈ 1.9× and needs > 8.8 GB disk |
| Recorder | `--gpu cpu --isolate --workers 4`, PNG with `optimizeForSpeed`, `clip.scale` = device scale | swiftshader-everything is 14× slower; isolation +26 % (flat) to +38 % (3D); JPEG costs +33 % bitrate |
| Encoder | x264 High, yuv420p BT.709, CRF 18, preset medium, keyframe every 2 s; `-tune animation` for flat scenes only; **CRF 21 for particle-heavy scenes** (per-scene `encode` in the script) | particles: tune animation +10 % size, CRF 21 −29 % at SSIM 0.976; slow preset −3 % for 1.8× CPU; x265 2.2× slower for −12 % |
| Scene budget | 3D: count segments and particles (cost is geometry, not pixels); 2D Canvas: use `Scene.hidpi`; every simulation through `Scene.stepper`; no timers, no free-running CSS or rAF | 3D at 540p = 3D at 4K = ~4 fps |
| Banding | static dither (a fixed noise texture at 1 to 2 %) rather than animated grain on dark gradients | animated grain is high-entropy motion, the most expensive content to encode (see scene a); 10-bit masters are an option for the archive, but YouTube re-encodes to 8-bit for most viewers |
| Subtitles | box style, burned in per scene at capture time; upload `film.srt` as captions too | outline style is unreadable over particles; per-scene burn keeps assembly a stream copy |
| Audio | one Fish request per scene, cached by request hash; decode to PCM; scene duration from audio; two-pass loudnorm −16 LUFS, −1.5 dBTP; AAC 192 kb/s 48 kHz | durations exact to the frame; demo measured below |
| Review workflow | `make plan` to see what changes; `stills.js` contact sheets for visual QA; 540p15 drafts for animatics; final passes overnight | drafts ×0.66 real time for particles; flat scenes render faster than real time anyway |
| Regenerable sections | template + `data/*.json` + cues; pending status renders hatched AWAITING frames so the film always assembles; data arrival promotes to provisional automatically | demo below |

## 9. Open points for the user

1. **Narrator voice.** The brainstorm mentions looking for a celebrity voice. The pipeline does not clone or imitate a real person; it needs the `reference_id` of an original Fish Audio voice (from the library or a voice you own the rights to, for example a cloned voice of a consenting narrator). Which voice, and do you confirm drama-3 with the validated settings for English?
2. **Fish Audio key and budget.** Set `FISH_API_KEY` in the environment (never in a file); the first live run should be one scene, to check pacing (words per minute), `[long pause]` length and the phoneme pins.
3. **Pronunciations** to confirm: Gissinger (French or English), DRESDYN, SFEMaNS, MilaDy, Kármán (`audio/lexicon.json`, entries marked CHECK).
4. **Frame rate and resolution**: 1080p30 (recommended), 1080p60 for the 3D and particle-heavy chapters only, or 4K (needs a GPU or a larger cloud machine, see section 7)?
5. **Music**: none, a licensed track, or an original bed? (the mix chain is ready, `--music`).
6. **Subtitle look**: box (default, styles.md) or outline only; the burned-in check frames are in `proto/out/stills/subs_*.png`.
7. **Word-level timing**: is sentence-level subtitle timing enough, or do you want word-by-word emphasis (then install a CPU aligner, about 0.5 GB, or use Fish ASR timestamps)?
8. **Where to render**: this 4-core machine (section 7 times) or a rented cloud VM / GPU instance for the final passes?
9. **Pending data**: for each regenerable section, which file and which figure will carry the result (palier 1 η sweep, palier 2 ABC/TG thresholds, fm3d samples and metrics, VKS/SFEMaNS, DRESDYN), and should the film ship with schematic fallbacks if a campaign is late?
