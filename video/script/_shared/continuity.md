# Continuity notes (both cuts)

Consistency editor, 2026-11-08. Read with `symbols.md` (symbols, glossary, recurring numbers, badges) and
`question_register.json` (every question, numbered Q1-Q30). Durations are estimated at **130 effective words
per minute** (words ÷ 130), which is within 1 % of the assembler's estimate (146 raw words per minute, 0.9 s per
paragraph break, holds, lead-in, tail) for every unit. Checked by assembling both cuts with
`tools/assemble_cut.py --variant pending` into a scratch folder: no lint warning other than missing data files.

## 1. Running orders after this pass

**Core cut** (both-cut units chSOA1, chSOA2 and ch10q are planned, not written):

ch00 → ch01 → ch02 → *chSOA1* → ch03 → ch04 → ch05 → ch06 → ch07 → ch08 → ch09 → *chSOA2* → ch10 (10.1-10.9, ch10.Q)
→ *ch10q* → ch11. Each chapter ends on its question card; ch11 has none (deviation kept by its writer, BRIEF
§3.1: the lead confirms; ch10q plays that role).

**Extended cut** (anchors as now set in the unit scripts):

ch00 … ch07 → ch08 (08.1-08.7, **ch08.Q**) → X2 (… X2.Q) → X3a (… X3a.Q) → ch09 (09.1-09.6, **ch09.Q**) → X4a (… X4a.Q) →
*chSOA2* → 10.1-10.3 → X5a (… X5a.Q) → X1 (… X1.Q) → 10.4, 10.5 → X4b (X4.4) → 10.6, 10.7 → X3b (X3.5) → **ch10.Q** →
10.9-bridge → X6 (… X6.Q) → X5b (X5.5, X5.6, X5b.Q) → *ch10q* → ch11.

Changes of this pass, and why:

| Change | Before | After | Reason |
|---|---|---|---|
| `X2.insert_after` | `08.7` | `ch08.Q` | X3a.Q and ch08.Q played back to back, and ch08.Q landed 7 min after the chapter it closes |
| `X4a.insert_after` | `09.6` | `ch09.Q` | X4a.Q and ch09.Q played back to back |
| scene order in `ch10.json` | … 10.9, 10.9-bridge, ch10.Q | … 10.9, ch10.Q, 10.9-bridge | core unchanged (10.9 and 10.9-bridge are cut-specific); in the extended cut ch10.Q (Taylor–Green settings) now closes the Taylor–Green block (10.5, X4.4, 10.7, X3.5) instead of landing after X6.Q and X5b.Q, three cards in a row |

Result: no two question cards are adjacent in either cut (until ch10q, which is the questions chapter). The
outline's `scene_order` check of the assembler still passes (question cards are not in it).

For the foundation engineer: chSOA1 goes before ch03 and chSOA2 before ch10 in both cuts (BRIEF §10); the
assembler knows only `ch10q` as an extra unit. With the module anchors above, the extended cut places X4a
before chSOA2 (X4a is anchored to ch09.Q), which is the intended order.

## 2. Chapter openings: each first line picks up the previous chapter

| Chapter | Last line before it (both cuts unless noted) | First line | Status |
|---|---|---|---|
| ch01 | 00.4/00.5: two questions; title | 01.1 "Is there a giant magnet hidden inside the Earth?" (answers 00.2 "It feels permanent. It is not.") | ok |
| ch02 | 01.6 "Then what motion can do it, and how fast?" | 02.1 "What kind of motion can grow a magnetic field?" | ok |
| chSOA1 (planned) | 02.6 VKS flips, ch02.Q | SOA1.1 the empty map; must open from the seafloor stripes (00.3) and the three tanks (02.4) | for its writer |
| ch03 | chSOA1 (planned) or ch02 | 03.1 "Back to the race: the flow stretches the field, and diffusion smudges it." | **changed**: it said "In the last chapter", wrong once chSOA1 sits in between |
| ch04 | 03.8 "Can anyone say when it flips next?" | 04.1 "Here is the caricature: three dials" (03.8 announced it) | ok |
| ch05 | 04.6 tag "how often D crosses zero · chapter 05"; 04.7 crowd laws | 05.1 the toll-counter puzzle, 05.2 "Back to the shoebox" | ok |
| ch06 | 05.5 "How do you get snapshots at a setting nobody simulated?" | 06.1 "New snapshots start as pure noise" | ok |
| ch07 | 06.4 snapshots join the shoebox; 06.5 noise floor | 07.1 "Physics hands the machine two kinds of laws", then "Back to the three dials" | ok |
| ch08 | 07.5 "On the next test bench, a cruder score is fooled"; 07.6 "The next tests will tell" | 08.1 "New test bench: whole fields, not three dials" | ok |
| ch09 | 08.7 "One question remains: from snapshots, how well can we answer how often?" | 09.1 "The toll counter is back" | ok (in the extended cut the payoff waits through X2 and X3a, as in the outline) |
| chSOA2 (planned) | 09.6 three lessons, ch09.Q (core); X4a.Q (extended) | SOA2.1 "Back to the map" | for its writer |
| ch10 | chSOA2 (planned) | 10.1 "Back to the staircase." | ok |
| ch10q (planned) | ch10.Q (core); X5b.Q (extended) | must gather the questions and hand over to 11.1 | 11.1.s1 "Questions first, then computing." already expects it, and reads correctly after a card meanwhile |
| ch11 | ch10q | 11.1 "Questions first, then computing." | ok |

Module entries in the extended cut: X2.1 "An aside: the five statements behind the pictures" (after ch08.Q);
X3.0 "Earlier, a distribution distance meant moving sand" (06.5); 09.1 after X3a.Q; X4.1 "How wide should Rice's
strip be?" (after ch09.Q; the module tag marks the aside); 10.1 after X4a.Q; X5.1 "Open one oven" (10.2's
factory); X1.1 "Before trusting the solver…" and X1.3 "That unresolved sign is where Bet one begins" hand over to
10.4 "Bet one"; X4.4 follows 10.5 on the same Taylor–Green flow and recalls 09.3's stiff sheet; X3.5 follows
10.7 ("Now the crowd law in three dimensions"); ch10.Q, then 10.9-bridge "Two steps remain … First, what exact
means once there are walls, metals and meshes; then their bets" opens X6.0 "Before the walls, one convention";
X5b follows X6.Q. All read naturally where inserted.

## 3. Recurring devices: planted before paid off, in both cuts

| Device | Planted | Recalled | Paid off | Extended-only uses | Status |
|---|---|---|---|---|---|
| M1 compass needle, the two questions | 00.1, 00.4 | 02.6 "Like the compass needle at the start" | 11.2 "Back to the compass, and to the two questions" | — | ok |
| seafloor stripes (barcode) | 00.3 | 02.6, 04.2 "like the seafloor" | 11.2 montage and chip | chSOA1 (planned, SOA1.1) | ok |
| the box test (lines in = lines out) | 01.2 "Keep this box in mind" | 08.2 "lines appear and vanish inside the box" | 08.3 "The box agrees"; 09.6 lesson glyph | X5.4 | ok |
| the squeal (loop with a threshold) | 01.3 | 02.2 "like the squeal" | — | — | ok |
| the mirror (B → −B) | 01.5 "mirror twins" | 04.1, 04.2, 04.5, 06.1 | 07.2 built-in mirror; 08.6; 10.6; 11.2 "The mirror holds by construction" | X2.4 (proof), X4.5 and X2.Q (impeller swap, always qualified), X6.6 | ok |
| the race (stretch vs smudge), threads | 02.1-02.2 | 03.1 "Back to the race" | 03.1 the equation | X1.2 threads | ok |
| knob, dots | 02.2, 03.6 | 03.5 panel, 05.5, 06.4 filled/open dots | 09.5 "Every test sits between trained settings"; 09.6 promise card 1; 11.2 "between the simulated settings" | X3.2, X3.4 | ok |
| M7 staircase | 03.7 "climbs a staircase"; 03.3 "This box returns higher on our climb" | 04.1 "the bottom step"; 08.1 (visual, step 2 lit) | 10.1 "Back to the staircase"; 11.1 bets column; 11.2 montage | X4.2 and X4.5 ("the staircase's first step"), X5.6 | ok |
| promise cards 1-3 ("the study's three questions") | 03.7 | 05.3 card 3, first tick (visual); 08.6 card 2 ticked (visual); 09.1 "the study's third question" | **09.6** all three cards: card 1 half-ticked, card 2 and 3 recalled | — | **fixed**: card 1 had no payoff anywhere; 09.6 P2 now pays it off ("between the dots, the shapes come out right, but no model reaches its noise floor") |
| shoebox | 04.6 | 04.7, 05.2 "Back to the shoebox", 05.5, 06.4, 07.5 | 11.2 "a shoebox of snapshots, read with the equations" | X4.3 "No shoebox holds that shape" | ok |
| bank account / ledger | 04.7 | 07.5 "like a bank account over the years" | 07.5 the ledger where every day balances | — | ok |
| corridor | 04.2 | 09.3 | 09.3 clouds in the corridor | X4.3 short runs from the corridor | ok |
| toll counter | 05.1 | — | 09.1 "The toll counter is back: every car is now generated"; 09.6 rate row glyph; 11.2 montage | — | ok |
| noise floor (sand piles, die) | 06.5 | 07.3, 08.5, 09.5 | 09.6 third lesson | X3.0 "Earlier, a distribution distance meant moving sand", X4.5 | ok |
| the two shelves | 07.1 "Two shelves, still empty" | 07.2, 07.5 (crowd shelf), 08.2 (every-snapshot shelf) | 08.6 "Back to the two shelves, now full"; 09.6 scoreboard on the shelves | — | ok |
| the spike | 07.5 | 07.6, 08.5 | 08.6, 09.4 "a faint echo of the spike", 09.6 | — | ok |
| crowd loss, two juries | 07.6 (now named there) | 08.5 "the crowd loss, with its two juries" | 09.4, 09.6 | X3.4, X3a.Q, X3.5, X5.6 | **fixed**: the name "crowd loss" was first heard in 08.5 as a callback; 07.6.s3 now names it |
| hill maps, projection | 08.3 | 08.6, 08.7 | 10.6 "hill maps become potentials"; 09.6 | X2.1, X2.2 | ok ("both projections" removed from 09.6: the core never names two) |
| the spring (stiffness at the end of the clock) | 08.4 | — | — | X2.2 "the spring, in full" | ok |
| the stiff sheet | 09.3 | — | 11.2 "A smooth machine rounds off a steep change" | X4.4 | ok |
| empty seat: bet, confidence, criterion, ask; grey tag; lamps | 10.1 (bets), 10.2 (grey tag) in the core | 10.3-10.9 | 11.1 bets column and lamps | first empty seat of the extended cut is X4.2, before 10.1: **fixed** by X4.2.s5 "The bet, written before the data, …" and by 10.2.s7 no longer saying "From now on" | ok |
| M11 the map (planned) | chSOA1 (SOA1.1-SOA1.6, "We come back here near the end") | — | chSOA2 SOA2.1 "Back to the map" | — | for the chSOA writers: plant it in chSOA1, pay it off in chSOA2; never call the staircase "the map" in narration; `styles.md` §3.5 is read-only, so the id M11 is assigned here |

## 4. The core cut does not depend on the modules

- Every term the core needs is planted in a core scene. The one dependency found, 10.4's "a long fit and a late
  fit" (defined only in X1.3), is fixed: 10.4.s4 now says "two fits agreeing: one over the kept part of the run,
  one over its last quarter" (the result variant says "the two fits").
- Core chips that point to modules are pointers, not dependencies: 08.4 "full statement: Proposition 2 and
  Remark 3.6 · extension X2.2", 08.5 "details: description and extension X3.4". Keep them.
- Repetitions that the extended cut hears twice, kept on purpose because the core needs them: 10.4's anchor
  sentence after X1.3 (one sentence), 10.2's grey-tag sentence after X4.2 and X4.5, 10.1's staircase after X4.5.

## 5. Level climb

| Cut | Sequence of levels | Declared steps down |
|---|---|---|
| core | L0 (ch00) → L0-L1 (ch01) → L1 (ch02) → *L1-L2 (chSOA1)* → L2 (ch03, ch04) → L2-L3 (ch05) → L3 (ch06) → L3-L4 (ch07) → **L3** (08.1-08.4) → L4 (08.5-ch09) → *L4-L5 (chSOA2)* → **L4** (10.1-10.4) → L5 (10.5-ch10.Q) → *ch10q* → L5 → L0 (ch11) | 08.1 "new test bench" (L4 → L3, unchanged); **10.1 "back on the staircase" (L5 → L4, new)**; 11.2 closing descent |
| extended | as the core, with the modules as asides: X2, X3a at L4; X4a L4 → L5; 10.1-10.3 at L4; X5a, X1 at L4; 10.4 L4; 10.5 onward and X4b, X3b, X6, X5b at L5 | the same three; each module's rail marks it as an aside |

Changes: the 03.1 chapter card now holds at L2 (`levelFrom: 'L2'`), because chSOA1 already climbs from L1 to L2;
the 10.1 chapter card now steps down from L5 (`levelFrom: 'L5'`, rail tag "back on the staircase"), because
chSOA2 (both cuts) and X4a (extended) end at L5. **If chSOA1 or chSOA2 is not ready at render time**, revert
these two values (L1 and L4) so the rail does not jump. ch10q should end at L5 so that the 11.1 card (from L5)
holds. Time per level now (written units): core L0 3.7, L1 5.2, L2 9.3, L3 10.3, L4 11.0, L5 3.5 min; extended
L4 23.5, L5 12.5 min (other levels as the core).

## 6. Duration per cut (130 effective words per minute)

| Unit | Core: words / min | Extended: words / min | Target (s) |
|---|---|---|---|
| ch00 | 181 / 1.4 | same | 84 |
| ch01 | 385 / 3.0 | same | 177 |
| ch02 | 411 / 3.2 | same | 194 |
| ch03 | 574 / 4.4 | same | 271 |
| ch04 | 549 / 4.2 | same | 254 |
| ch05 | 361 / 2.8 | same | 169 |
| ch06 | 437 / 3.4 | same | 194 |
| ch07 | 542 / 4.2 | same | 252 |
| ch08 | 663 / 5.1 | same | 298 |
| ch09 | 578 / 4.4 | same | 254 (09.6: 40 → 45 s) |
| ch10 | 653 / 5.0 | 522 / 4.0 (no 10.8, 10.9; bridge) | 294 / 239 |
| ch11 | 265 / 2.0 | same | 120 |
| modules | — | X2 503, X3a 382, X4a 399, X5a 339, X1 302, X4b 97, X3b 85, X6 622, X5b 201 (2,930 words, 22.5 min) | |
| **written total** | **5,599 words = 43.1 min** | **8,398 words = 64.6 min** | |
| planned: chSOA1 + card, chSOA2 + card, ch10q | ≈ 2.6 + 4.6 + 2.5 = **≈ 9.7 min** | same | 150 + 270 + 150 s, cards 8 s |
| **expected total** | **≈ 52.8 min** | **≈ 74.3 min** | target ≈ 41 / ≈ 60 |

Against the target: the written units are 2.1 min (+5 %) over in the core and 4.6 min (+8 %) over in the
extended cut; the question cards account for 1.4 and 2.3 min of it. The three units added by BRIEF §3.3 and §10
bring both cuts about 10 minutes further. The 41/60-minute targets predate those additions: the lead either
accepts ≈ 53 / ≈ 74 min, or trims. Trim menu (estimates, nothing applied):

| Option | Saves (core / extended) | Cost |
|---|---|---|
| chSOA2 at ≈ 2.5 min in the core, full ≈ 4.5 min in the extended cut | 2.0 / 0 | the supervisors' pins move to the extended cut |
| ch10q at 2 min instead of 2.5-3 | 0.5 / 0.5 | fewer questions spoken; the register and the French sheet keep all |
| 10.8 out of the core (walls are in X6 for the extended cut) | 0.7 / 0 | the core no longer says what "exact" means with walls |
| one checkpoint less (01.6 or 03.8 merged into the next chapter card) | 0.2-0.3 / same | weaker recap at L1-L2 |
| X4b and X3b folded into the ch10 seats (their bets as chips) | 0 / 1.4 | two L5 bets lose their own scene |

## 7. Question cards

- Numbering (`question.n`, card stub "ASK · Q<n>"): film order of the extended cut, planned cards included:
  Q1 ch00 · Q2 ch01 · Q3 ch02 · Q4 (no card: chSOA1 has none) · Q5 ch03 · Q6 ch04 · Q7 ch05 · Q8 ch06 · Q9 ch07 ·
  Q10 ch08 · Q11 X2 · Q12 X3a · Q13 ch09 · Q14 X4a · Q15 chSOA2 · Q16 X5a · Q17 X1 · Q18 ch10 · Q19 X6 · Q20 X5b.
  The core cut shows Q1-Q3, Q5-Q10, Q13, Q15, Q18 (it skips the module cards). Q4 and Q21-Q37 have no card (Q31:
  the PBFM question, formerly the planned Q15; Q32-Q37: `ETAT-DE-L-ART.md` §4). All 19 written cards now carry
  their number and their stub text in the visual matches (integration pass 2026-11-08).
- Overlaps resolved in the register, not on the cards: ch04.Q / ch09.Q / ch00.Q (sampling for statistics vs
  counting reversals vs warning signs: three distinct decisions, cross-referenced); ch06.Q owns the metric list,
  ch07.Q the budgets and the spread criterion, X5a.Q topology; ch08.Q (operator, exactness) and X6.Q (labels)
  stay separate; ch03.Q absorbs the 10.4 ask (D17); ch01.Q absorbs the X4.4 ask; ch02.Q the 10.7 ask; the 10.5
  and X3.5 asks merge into Q24 (D18).
- ch08.Q and ch10.Q no longer address the supervisors in the second person ("your solvers", "comparable with
  yours"): the narrator speaks to the viewer, and the card says who to ask.
- Open for the lead (BRIEF D6): every card stub prints the supervisors' names from ch00.Q on, before 03.7 names
  them; this is text only, as D6 allows.

## 8. Requests and open decisions

- **Foundation engineer.** (1) Subscript rule for plain strings (`symbols.md` §4). (2) chSOA1 before ch03 and
  chSOA2 before ch10 in the assembler's extra units. (3) The existing requests of the unit notes are unchanged
  (met / not_met / inconclusive booleans, missing data files).
- **chSOA1 and chSOA2 writers.** Use the numbers Q4 and Q15 and the texts of the register; plant and pay off the
  map (M11); chSOA1 ends at L2 (03.1 holds at L2); chSOA2 ends at L5 (10.1 steps down, declared); do not reuse
  "the staircase" or "the study's three questions" for the map.
- **ch10q writer.** Present the register in `order_for_ch10q` (priority, then category a, b, c); point to
  `infra/cloud/RECOMMANDATION-CLOUD.md` §0; end at L5 on a line that 11.1.s1 "Questions first, then computing."
  can follow.
- **Audio engineer.** Lexicon pins still missing: "eta" (08.1, 08.5, X3.2, X3.4), "I-projection" (X3.1),
  Cadarache, Karlsruhe, Prandtl (ch02), "X-point", "O-point" (X5.4).
- **Lead.** Keep or drop the SCHEMATIC badge of 05.1 and 06.2 (`symbols.md` §7); confirm no ch11.Q; accept or
  trim the durations of §6.

## 9. Edits made in the unit scripts (this pass)

| Unit | Edit |
|---|---|
| ch00 | 00.4 badge note |
| ch01 | 01.4, 01.5 badge notes |
| ch03 | 03.1.s1 "Back to the race"; chapter card levelFrom L2; badge notes 03.1, 03.4, 03.7; ch03.Q → Q5 |
| ch04 | badge notes 04.2-04.4, 04.6, 04.7; ch04.Q → Q6 |
| ch05 | badge notes 05.2-05.4; ch05.Q → Q7 |
| ch06 | badge notes 06.3, 06.4; ch06.Q → Q8 |
| ch07 | 07.6.s3 names the crowd loss; ch07.Q → Q9 |
| ch08 | 08.5.s12 "training seed"; 08.3 potential A; ch08.Q wording (no "your") → Q10 |
| ch09 | 09.1.s7 "training seed"; 09.4 "model F"; 09.6 rewritten (promise cards paid off, no repeat of 08.6, target 45 s); ch09.Q → Q13 |
| ch10 | 10.1 card from L5 with tag; 10.2.s7; 10.4.s4 and r3 (two fits defined); 10.7.r8; ch10.Q moved before 10.9-bridge, wording (no "our/yours") → Q18 |
| ch11 | 11.1.s6 "lamp" |
| X2 | insert_after ch08.Q; X2.4 asymmetry ticks; X2.5 "models D, F", drift f; X2.Q why → Q11 |
| X3a | X3.3.s6 "PhD plan"; X3.2 ⟨A²⟩; X3a.Q → Q12 |
| X4a | insert_after ch09.Q; X4.2.s5 "written before the data"; X4.1 chip; X4a.Q → Q14 |
| X5a | X5.4 potential A; X5a.Q → Q16 |
| X1 | X1.Q → Q17 |
| X6 | X6.6 drift f; X6.Q → Q19 |
| X5b | X5.6.s1 "five steps"; potential A; X5b.Q → Q20 |

Every edited unit's `notes` ends with a "CONSISTENCY EDITOR (2026-11-08)" sentence. Reviewers' fixes were kept.
