# Page contract — MilaDy 2027 site

All pages are in **English**. Quarto source `index.qmd`, published page `index.html` (rendered by `python3 tools/render.py <path>`).
Never edit an `index.html` by hand.

## Header

Create the page with `python3 tools/new_page.py <path> "Title" "Subtitle"`: the header (pinned KaTeX, top bar, side table of contents, footer) is generated. Do not modify it.

## Structure of a preparation module (`prep/<id>/index.qmd`)

1. `## Objectives {#objectives}` — 4 to 8 verifiable abilities ("be able to compute…", "be able to prove…").
2. `## Prerequisites {#prerequisites}` — starting level (L1, L2…), site modules to read beforehand (relative links `../<id>/index.html`).
3. `## Work plan {#plan}` — table: session, estimated duration, level (1 = foundations, 2 = core, 3 = close to research; the level never goes back down), content, associated exercises. Total hours stated.
4. Numbered chapters `## 1. Title {#ch1}`, `## 2. … {#ch2}` … Each chapter: physical or practical motivation in one or two sentences, definitions, results (statement + proof or honest sketch), worked numerical example, executable Python code, recap callout.
5. `## Exercises {#exercises}` — at least 10 exercises graded ★ / ★★ / ★★★, each with a complete solution (*Solution*: …). At least one coding exercise.
6. `## Link with the internship {#internship-link}` — where this module is used in the MilaDy internship (point to the report `../../report/index.html#…` and to the thesis proposal `../../thesis/index.html` when relevant).
7. `## Further reading {#further-reading}` — 3 to 6 annotated readings.
8. `## Sources {#sources}` — complete references (authors, year, title, journal/publisher, DOI or URL). Verified references only.

## Callouts (Quarto divs, classes defined in `site/assets/paper.css`)

```markdown
::: def
[Definition 1.2 — Solenoidal field]{.tag}
Text.
:::

:::: thm
[Theorem 1.3 — Helmholtz–Hodge decomposition]{.tag}
Statement.

::: proof
Proof. [∎]{.qed}
:::
::::

::: prop
[Proposition 2.1 — …]{.tag}
:::

::: ex
[Example 2.2 — …]{.tag}
:::

::: note
[Remark]{.tag}
:::

::: key
[Key point]{.tag}
Formula or central idea.
:::

:::: recap
::: recap-title
Key takeaways — chapter 2
:::
- point 1
- point 2
::::
```

Numbering: `Definition <chapter>.<n>` (a single counter per chapter for all callout types).

## Mathematics

- KaTeX: `$…$` inline, `$$…$$` display (one equation per block, linking sentences between blocks). No `\label`/`\eqref`; number by hand with `\tag{2.3}` if needed.
- Common notation: see `docs/specs/notation.md`. Vectors in upright bold `\mathbf{u}`, `\mathbf{B}`; operators `\nabla\cdot`, `\nabla\times`, `\Delta`; spatial average `\langle\cdot\rangle`; expectation `\mathbb{E}`.
- No custom macros (KaTeX without preamble).

## Code

- Static ```` ```python ```` blocks (Quarto does not execute them). Each block must run as is in under 30 s on a CPU with NumPy, SciPy, Matplotlib, PyTorch (CPU). The author runs each block and copies the useful output into a comment (`# output: …`).
- No downloaded data unless explicitly stated.

## Figures

- Conceptual diagrams shared between pages: `site/figures/<name>/` (generator in `figure/`, output `figure/out/<name>.png`), inserted with `![Full caption.](../../figures/<name>/figure/out/<name>.png){width="100%" fig-alt="Text description."}`.
- Module figures: every image in a module's folder is written by the module's script `figures_pN.py` (one function per figure, fixed seeds, output folder = the module by default, run with `python3 figures_pN.py`); `tools/check_gates.py` checks it. The function reuses the code block of the page that precedes the figure and prints every measured number the caption quotes; the caption copies them from that output. Style: `site/assets/figstyle.py` (shared palette and rcParams).
- Result plots: `site/experiments/figures/*.png` (written by `experiments/figures.py`) (matplotlib).

## Writing style

- Complete sentences, the tone of a written course; no telegraphic style; one idea per paragraph.
- Every figure taken from the literature is sourced (author, year) and appears in the Sources.
- Clearly distinguish what is **measured in this repository** (experiments `experiments/`), what is **published** (with reference) and what is **conjectured**.
- No invented fact about the supervisors, the offer or the MilaDy project: cite only the verified entries of `docs/specs/sources/*.md` or the offer itself.
