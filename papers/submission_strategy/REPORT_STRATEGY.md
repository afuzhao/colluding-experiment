# Submission strategy after reviewing all repository branches

## Recommendation

**Recommended title: What Breaks an AI Cartel**

**Subtitle: Trusted insiders, forged messages and market outcomes**

Build one argument around three separately measured outcomes: stated agreement, immediate action and sustained economic outcome. A plausible countermeasure can change one without changing the others. This connects the team’s completed experiments while avoiding the unsupported claim that any single tactic reliably ends collusion.

The most useful practical contribution is an evaluation discipline for defenders: verify what intervention was actually delivered, distinguish a first reaction from persistence, and measure realized harm and recovery alongside messages. A source-attribution attack and an ordinary trusted firm have different powers; make those differences visible.

This is a report-design recommendation, not a completed submission or a novelty certification. No new experiments, paid calls, contributor messages, branch merges or E2 disruption execution were performed for this review.

## Sources and scope of review

Read the supplied DOCX body and tables, extracted all four PDF pages and visually inspected all four. The template asks for Introduction, Related Work, Methods, Results, Discussion and Limitations, Conclusion, Code and Data, references and an LLM usage statement. Its four-page recommendation is a target, not the current event’s hard cap.

The official [AI Collusion Research Sprint page](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25) evaluates impact and innovation, execution, and clarity. It requires the template PDF, at most eight main pages, a 150–250-word abstract, authors/affiliations and a limitations/dual-use appendix. My recommendation is six to seven main pages, with technical detail in appendices. The template’s generic optional appendix does not remove the event-specific required ethics appendix.

Inspected the full tracked-file inventory on all three remote branches, their major reports, corrections, methods and analysis code:

| Branch snapshot | Files | Role in report |
|---|---:|---|
| main `23c9c84202ad7093d4f31021fb556f57cbdb2f4c` | 635 | Reviewed reaction cohorts, repairs, ordinary-C controls, mathematical environment and three-study foundation |
| sumin/disruption `a10db995c8d0e8206d4ae935118cf9b8727fc067` | 394 | Credited quantity-market greed pilot and talk/action disruption comparison |
| anay/apart-sprint-ring-study `e3c0b8790cd2fb802251187faa72a71a6f98c767` | 4,627 | Forged-message, source/provenance, control and multi-round experiments; older and other-market studies remain separate |

Branch inventories overlap; file counts are not counts of experiments. Loaded 642 selected JSON records to independently recount focal V15 and V18 outcomes. This is a broad evidence map and targeted outcome check, not a claim to have independently verified every provider transcript, every archived result or every preregistration timestamp. The [focal audit](FOCAL_BRANCH_AUDIT.json) records exact metrics and caveats. Main reaction/control and Sumin audit evidence was already reviewed in the [foundation](../three_study_foundation/README.md).

Archived prototypes under old/exp 1 and the earlier ten-condition pilot use different models, prompts or timing. Anay’s V2–V10 legacy studies, early interrogations, ring studies and loyalty tests contain additional evidence, but should not be pooled with the proposed main comparisons. Count original development, corrections, replays, aborted calls and repeated prefixes separately.

## First principles and the main inference

A cartel is a pattern of coordinated behavior with consequences. A declaration, a diagnostic answer and a price are imperfect observations of different parts of that process. A defender needs to know what it can actually control and what outcome matters.

Separate two intervention powers:

1. **Economic participant:** C has genuine shared history, can speak under its own identity and change its own quantity or price. This is the trusted-insider evidence.
2. **Information-channel controller:** the harness inserts a message attributed to a partner or platform. This is the forged-message evidence. It does not demonstrate that an ordinary firm can forge authenticated records in a real deployment.

Then distinguish three outcomes: a verbal agreement changes; the next action changes; economic harm stays lower after the initial response and intervention window. Do not infer the third from the first two. Preserve attempted restoration, alternative coalitions and recovery where observable.

The strongest unifying interpretation is that messages can induce immediate action, while persistence must be established from trajectories. Sumin’s talk-only result does not refute Anay’s forged-message result: the content, attributed speaker, market and timing differ. The former demands an unequal allocation; the latter announces a partner’s next action. No matched experiment isolates which difference explains their contrast.

## Claim hierarchy and what belongs in the main text

| Priority | Supported result | Qualification |
|---|---|---|
| Main | The V15 saved episodes contain 40/53 first-decision changes under a forged partner message versus 1/54 in placebo | Recounted directly. These are changes of choice; use directional classification if calling them competitive moves. Report by model and market. Shared histories and seeds are not independent replications. |
| Main | Immediate movement and persistence differ; several forged-message dips recover, whereas sustained action treatments leave some markets lower | Recompute matched trajectories and history-level contrasts. Exploratory associations between simultaneous rival choices are not causal mediation. |
| Main companion | In Sumin’s two action-only histories, price reaches cost and all profits are zero in rounds 10–13, with positive profits after the window | Economic suppression endpoint chosen retrospectively. A/B escalation is observed, not guaranteed by game theory; zero-profit output is not a unilateral Nash equilibrium. |
| Main or compact panel | Public reaction suspicion is 0/32 in each Qwen market; explicit private suspicion is 15/32 in E1 and 6/32 in selected E2, sometimes overlapping acceptance | Different elicitation tasks, assistant labels, one formation each. No private ground truth or detector accuracy. Ordinary-C controls include a suspicion flag about ordinary C. |
| Secondary | Provenance labels have model- and execution-dependent effects | Preserve halfway-to-benchmark versus any-change definitions and placebo rates. API and agent runs differ in more than reasoning; not a clean capability ranking. |
| Appendix | Ring joining, loyalty, greed curve, early audits and legacy pilots | Retain useful negative findings and contradictions without turning the main text into a chronology of every run. |

The precise E2 reaction result 64/64/52 is an excellent short illustration: aggregate transaction price falls to 58 although A/B still charge 64. It shows why a market-level price change alone need not establish A/B breakdown. It is not E2 disruption data.

## A defensible novelty claim

Do not sell the paper as the first observation that agents’ words and actions disagree. [Colosseum](https://arxiv.org/abs/2602.15198) already reports collusion in text without corresponding actions. [Fish et al.](https://arxiv.org/abs/2404.00806) already study LLM pricing and prompt sensitivity. [Keppo et al.](https://arxiv.org/abs/2603.20281) already examine disruption through heterogeneity.

The candidate contribution is more specific: a reproducible comparison of insider elicitation, attributed defection, provenance cues and competitive actions, explicitly separating immediate response from persistence and market harm. The supplied evidence supports this as a research direction and descriptive empirical contribution. A focused full-text related-work check is still required before claiming priority or broad novelty.

## Structure within the supplied template

| Template section | Approximate main-text space | Content |
|---|---:|---|
| Title, authors, abstract and Introduction | 1 page | Concrete defender question, three outcomes, threat/power distinction, three contributions |
| Related Work | 0.5 page | LLM market coordination, communication/action mismatch, countermeasures and provenance; explain the incremental contribution |
| Methods | 1–1.5 pages | A compact dataset table; distinct models/markets/horizons; matched prefixes; timing; outcome definitions; interventions and powers; failures and annotation |
| Results | 2–2.5 pages | Immediate response, persistence/recovery, trusted-insider comparison and neutral/ordinary controls; show contradictory/negative cases |
| Discussion and Limitations | 0.75–1 page | What can be inferred, what cannot; practical evaluation lesson; small-history and execution confounds |
| Conclusion plus Code and Data | 0.25 page | Bounded claim and exact evidence entry points |

Aim for six to seven main pages; stop at the official cap. Include author contributions and honest LLM usage. Do not copy the template example claiming independent human verification when much annotation was performed by an assistant.

Appendices: required limitations and dual-use discussion; full payoff derivations and discrete-grid checks; protocol/prompts; all condition rows and label overlaps; original failures and repaired prompts; prediction/amendment record; dataset lineage and reproducibility instructions. Explain that a forgery disrupting harmful coordination can also damage legitimate cooperation. Do not claim cryptographic authentication was tested merely because a message carried a verified/unverified label.

## Three figures and one table

**Figure 1 — Information and measurement timeline.** Show reaction formation, offer, public reply, action window and frozen diagnostic; a separate row shows the forged-message intervention. Mark genuine C speech versus inserted identity/platform claims. This prevents most reader confusion in one figure.

**Figure 2 — First response and persistence.** Panel A shows forged-message versus placebo responses by model, with exact denominators and the specified metric. Panel B plots the full price-index trajectory against placebo and sustained-action treatments. Use a shared scale within each market family; label clipping and raw values. Do not put independent-binomial intervals on reused histories or treat all cells as independent.

**Figure 3 — Genuine insider words versus actions.** Plot both Sumin histories separately for talk-only and action-only, mark rounds 9–13 and cost 4, and show recovery in 14–15. An inset can show public/private suspicion and ordinary/neutral controls without treating private answers as truth.

**Table 1 — Evidence contract.** Rows are datasets; columns list firms, economics, model/execution method, horizon, independently generated histories, matched branches, intervention powers and annotation. This makes incompatible studies legible without pretending they are one experiment.

## Fix before claiming the report is submission ready

- V15 placebo has one first-choice change in 54 episodes. Some current prose says zero. Use the saved-episode recount.
- V18 halfway-to-benchmark, any change and direction-only criteria give different numbers. Lock a primary metric per comparison, retain original definitions and show sensitivity. Haiku subagent changes all 17 placebo choices under any-change scoring, so do not advertise its 17/17 intervention movement as informative treatment evidence.
- Anay’s paper plan is stale about the ordinary-C controls: all four are completed and published on main. Its old prediction tallies also differ from current FINDINGS; do not copy counts without reconciliation.
- The current deep-analysis script refers to v18_io, while tracked scenario files are under behavioral_v18_claude_code. Supply a documented path mapping or repair before promising one-command clean-clone reproduction.
- Confidence intervals and tests must respect shared histories, duplicated/replayed prefixes and model/market strata. The pooled Fisher tests in exploratory deep analysis are not automatically valid confirmatory evidence. Do not call repeated cells independent histories merely because full serialized prefixes hash differently.
- A known 15-round horizon is not an infinite repeated-game equilibrium demonstration. Keep the exact mathematical model and benchmark incentives concise in main text; derivations go to the appendix.
- Do not claim the planned three-firm quadratic E2 disruption study has run. Anay’s two-firm logit market is a different environment. No new E2-D collection is needed or authorized by this report review.
- Confirm exact author names/affiliations and contribution allocation before a final document; preserve Sumin’s credit and the distinction between original data and audit/synthesis.

## If the team retains two submissions

The contributor plan proposes a separate forged-message paper. That plan is context, not an instruction from the user to combine submissions. If retained, use the title **Trusted Insiders in AI Cartels** with subtitle **Elicited agreement private suspicion and economic disruption** for the three-study foundation report. Keep its three-cell evidence and controls central, with the forgery work as a clearly separate related companion. Give Anay’s paper the sharper attribution/provenance focus.

My preference for a single team-wide paper is the recommended umbrella title with the three-outcome argument. My preference for two papers is a clean evidence split with disclosed overlap, rather than two manuscripts reusing the same headline as if independently discovered. The final authors decide the submission allocation; this review sends no messages and makes no submission.
