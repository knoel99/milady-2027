single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/biblio.md`. No separate role process ran. No publisher page was opened in this session. The passages below are copied from `docs/specs/sources/literature.md`, which already tags them. They are not a new verification.

Question. Is a divergence-free decoder by a stream function or a vector potential already published, relative to Proposition 1?

Facts.

- [verified] in `docs/specs/sources/literature.md` section 3.1, not re-opened here. FunDiff (Wang et al., Nature Communications 17, 5749, 2026, DOI 10.1038/s41467-026-72292-0). The file's passage: the decoder outputs a stream function ψ, u = ∂ψ/∂y, v = −∂ψ/∂x. Predicted divergence "negligible". No numerical value in the text. Location in the source file: the "Zero divergence" bullet. URL recorded there: https://arxiv.org/abs/2506.07902
- [verified] in the same file, section on divergence-free networks, not re-opened here. Richter-Powell, Park, and Lipman type constructions are summarized as divergence-free by d² = 0. Location: the paragraph that cites https://ar5iv.labs.arxiv.org/html/2210.01741
- [verified] in the same file, not re-opened here. Genuist et al. impose incompressibility by a Leray projector. Location: the paragraph that cites https://arxiv.org/html/2601.19368
- [argued synthesis] in section 8, item 2, not a verified primary passage. The file says the vector potential A with B = curl A is the 3D generalization of the FunDiff stream function, and that a gauge has to be chosen. No paper in that item is claimed to have done this for generated 3D MHD fields.

What was not done. The PDFs and the arXiv HTML were not opened in this session, so no tag was lifted and no quote was checked against the primary page.

Closest prior work already in the file. A 2D stream-function decoder (FunDiff) and a Leray projector (Genuist, PCDM). The 3D magnetic potential as a generative decoder is listed as a gap, not as a published MilaDy result.
