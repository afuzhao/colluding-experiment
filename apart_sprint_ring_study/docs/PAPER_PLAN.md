# Paper plan v2: announced vs done in LLM cartels (Anay + Sumin + Chirag)

## 1. Thesis and abstract
**Thesis:** LLM firms in a cartel follow what they believe their partner will do next. An unauthenticated announcement of a move triggers defection at the next decision, a provenance label stops this only in some models, and once actions can be observed, actions decide while contradicted words are discounted.

**Abstract (about 235 words).** We ask what makes language-model firms leave a cartel: words or actions. In two-firm markets with six API models, one forged line in the partner's name ("I am moving to the competitive choice") made four models cut at the next decision (Flash 12 of 12, Flash Lite 10 of 12, GPT-4.1 5 of 5, GPT-4.1 mini 8 of 12; Claude Haiku 3 of 6 and 2 of 6), against 1 cut in 88 placebo cells. The dip usually lasted about one round, since the partner's real choice did not move. On 17 cartels, an "unverified" label cut the forged line's effect to 1 and 0 of 17 for Opus and Fable subagents, not for Sonnet (17 of 17), and barely helped API models answering without reasoning (GPT-4.1 17 to 14). The Haiku subagent changes its choice without news, so we exclude it. In a separate three-firm quantity market with a local 9B model, two formation histories agree: a greedy offer with unchanged output left the price at 52, while greater output with no offer sent it to cost from round 10. Together: announcements of the sender's own next move trigger action when the receiver must choose before seeing it, and observed actions then decide. How a model is called changes the result. Of 51 preregistered predictions, 20 held and 26 failed; we report both. Cells reuse borrowed histories and are not independent draws.

## 2. Titles (recommended first)
1. **Phantom Defection: announced words trigger, observed actions decide in LLM cartels.** Names the attack, says "trigger", covers Sumin's result.
2. Announced, Not Done. Fits the unified story, hides the forgery.
3. Borrowed Voice. Plain, less specific.

## 3. Team evidence (read from `afuzhao/colluding-experiment`, read-only)
Branches: `main` (Chirag), `sumin/disruption` (Sumin, pinned a10db99), `anay/apart-sprint-ring-study` (Anay). No separate Chirag branch.
- **Anay** (with Claude): 2-firm markets, 6 API models, about 4,000 runs; forged line 40/53 cells; 17 cartels x 10 configurations.
- **Sumin Hong**: Qwen 3.5 9B, 3-firm quantity market. Greed curve, 1 history, 4 arms: C's share 18 and 24 tolerated (price 50, 44), 32 sent price to 4. Talk vs action, seeds 6101 and 6102, 5 arms each (`reports/talk_vs_action_summary.md`): talk_only 52 throughout, act_only 36 then 4 from round 10, unequal 4 from round 10 or 11, iago (a doubt question) 52. In unequal, A and B said "return to 16" while producing 32.
- **Chirag**: environment 1 and 2 builds, audits and cohorts, each 16 conditions on one shared formation (E1-R 32 public pairs, 48 private calls; E2-R 14 original plus 2 revised, 48 calls). Equal offers from a trusted peer: A/B adhered 5/5 in every arm; unequal 0/5. Private suspicion 15 of 32 pairs, explicit public suspicion 0 of 32 (`docs/INSIDER_REACTIONS_V3_SUMMARY.md`). Audited Sumin's 150 round records and 88 C checks (`exp 5`). Ordinary-C controls and E2-D have no results.

**Relation to our thesis.** Sumin complements. His headline ("words do not break a cartel") appears to conflict with ours ("one line moves firms"). Reconcile by what was announced and what could be seen: our line announces the sender's own next move and the receiver chooses at once; his words were a demand about shares, and C's real output (16) was visible at round 9, so the offer was rejected in words and discounted. Our one-round dip is the same pattern: the partner's real choice stayed high, so the cue faded. His act_only matches our three forced cuts, which left round 8 lower in 3 of 3 cheap models. Chirag's 5/5 adherence matches our proposal result (followed in 6 of 9 runs). State the contradiction in the text, not the abstract. Differences: models, 3 firms vs 2, quantity vs price, 2 histories vs 53 cells, T=0.7 vs 0.3.

**Placement and credit.** Main text: Sumin's talk vs action (one section, Fig 1D; authors Sumin Hong, audit Chirag). Appendix: Chirag's E1-R and E2-R as one paragraph, plus Studies 1 to 3 (Anay). Discussion: monitoring warning from the say-do gap (Sumin) and 0/32 explicit suspicion (Chirag). Not reported: ordinary-C controls, E2-D, the old one-history pilot. Author list: Anay Garodia, Sumin Hong, Chirag (repo owner afuzhao; confirm the identity), with a contribution table per study. Never pool datasets.

## 4. Claim hierarchy
**Main 1: forged line triggers a cut.** 40/53 (CP 62 to 86%) vs placebo 1/54 and 0/34 at T=1.0; wordings 28/34 and 23/34; T=1.0 28/34; verified record 38/50, outsider 33/52, forged record 15/53, hidden history 0/53. Files: V15_main, V16_main, V17_main.
**Main 2: words trigger, observed actions decide.** Index vs placebo at rounds 5 to 8, mini -0.59, -0.28, -0.16, -0.16; Flash Lite -0.53, -0.07, -0.08, -0.08 (`scratchpad/cheap.py`). Three forced cuts: round 8 index -0.37, -1.12, -0.50 (V17_main). Plus Sumin's two histories.
**Main 3: label protection is model- and method-specific.** Subagent partner / tagged / placebo: Opus 17/1/4, Fable 17/0/2, Sonnet 17/17/2. API partner to tagged: GPT-4.1 17 to 14, mini 8 to 7, Flash 16 to 14, Lite 14 to 14, Haiku 4.5 11 to 11, Haiku 5.5 6 to 3; reasoning first: Haiku 5.5 14 to 10 without, 14 to 9 with. Files V18_main, V18_api, V18_reason, V18_change. Reasoning on four more models: [V18_reason4.md, pending].
**Secondary A:** harness gap (Haiku 5.5 2/6 own episodes, 6/17 halfway, 14/17 any change). **Secondary B:** content: announcement vs proposal vs leak vs irrelevant note (V18_leak); controls: reverse direction [V18_ctrl*.md, pending], reassurance [V18_ctrl*.md, pending].
**Cut:** Studies 1 to 3 to appendix; exposure, forged record, hide to control columns; V12, v2 to v10 dropped.

## 5. Pages and hero
p1 intro; p1.5 related work (short); p2 setup (both families, never pooled); p3-4 results 1 and 2 with Fig 1; p5-6 label and harness with Table 2; p6.5 announced vs done (Sumin) and content; p7 discussion and monitoring; p8 limitations, credit. Appendix: predictions, Chirag, Studies 1 to 3.
**Fig 1 (2x2).** A: forged vs placebo cut rate per model, exact CIs (V15_main, V16_main). B: round 4 to 8 index change per model, plus 3-round cut (episodes; V17_main). C: label, moves out of 17 for placebo, partner, tagged, Subagent vs API (V18_*). D: price by round, Sumin's direct, talk_only, act_only, unequal, iago, both seeds (`exp 5` `round_outcomes.csv`). Tables: T1 full episodes; T2 single decisions with the control columns.

## 6. Objections and checks
1. **"Rational cue."** "Unauthenticated line 40/53 vs verified record 38/50; partner profit falls in 5 of 6 models." Controls: reverse and reassurance [pending], irrelevant note, proposal.
2. **"Not independent; one-round effect."** Exact CIs, wordings, T=1.0; histories are the unit in Sumin's data (n=2, no rates).
3. **"Instrument."** Haiku subagent excluded; no pooling; Opus/Fable API test below.
Free analyses: Fisher tests, paired sign tests on `out/*.json`, profit transfer (`scratchpad/prof.py`). Fix the "0 placebo" line (Haiku 5.5 1/6).
Experiments: E1 Sonnet, Opus, Fable through the API, max_tokens 600 or more (cap $1). E2 Sumin's talk_only and act_only repeated on a third seed 6103 (his next step; local, free).

## 7. Limitations and dual use
- Told to maximise profit; borrowed histories; cells not independent; single reaction in Study 5; subagent vs API differ.
- Sumin: 2 histories, one 9B model, T=0.7, retrospective endpoint, outputs assigned by script; Chirag: one formation per environment, labels by assistant.
- Label is an explicit cue; leak and proposal one wording; Sonnet 5.5 API and belief probe not run.
- Dual use: the same line can wreck lawful coordination or start price wars; defence is signed messages and not acting on unsigned claims. Message-only monitors miss say-do gaps.

## 8. Score estimate (1 to 5)
Impact and Innovation 3 to 3.5 (cross-environment words vs actions helps); Execution 3.5 to 4 (breadth, but two sources with n=2); Presentation 3, 3.5 to 4 after the rewrite.
