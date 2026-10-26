# Trusted insiders, elicited agreement and economic cartel suppression

## A three-study foundation in two simulated markets

**Scope:** completed E1 reaction evidence, completed E2 reaction evidence including separately identified reciprocal repairs, Sumin Hong's audited E1 disruption cohorts, and the completed ordinary-C supplements. Environment2 disruption is not part of the executed evidence synthesized here. This is a descriptive empirical foundation for a later paper, not a completed four-study causal evaluation.

## Abstract

A trusted insider can elicit statements of coordination without disrupting the coordination itself. We examine that distinction using three existing-firm agents with the same pinned local language model in quantity and differentiated-price markets. Each reaction study branches one encouraged five-round formation into eight conversational packages crossed with general notice absent or present. E1 completes 16 conditions; E2 completes 14 original conditions, then two separately revised reciprocal continuations. Public replies, isolated explicit private assessments and realized actions are separate outcomes. Across 32 resident responses to C per reaction study, public review records 13 acceptances in E1 and 15 in the selected E2 view, with no expressed investigator suspicion. Explicit private reports record 15 suspicion flags in E1 and 6 in E2, overlapping agreement rather than replacing it. Post hoc ordinary-role and neutral-question controls demonstrate task-sensitive response differences and one suspicion report about ordinary C. Separately, Sumin Hong's two quantity-market disruption histories exhibit price at cost and zero profits during rounds 10–13 under C expansion, followed by positive-profit recovery. Checked game-theory benchmarks explain the incentives and mechanical price effects without making model escalation inevitable. The evidence supports separating elicitation, economic suppression and durable coordination breakdown. Small history counts, unmatched proposal packages, assistant annotation and delivery deviations preclude population-level or detector-accuracy claims.

## 1 Research question and design evolution

The motivating question is whether a trusted peer can expose or disrupt an established cartel. Three subsidiary questions require different evidence: what residents say about a proposal, what they report when directly asked in private, and what coordination and harm remain in their actions. None is a substitute for the others.

The human-supplied proposal and HTML explainer identify environment, group size, resident composition, investigator profile, approach, formation, entry timing, enforcement and implementation as important factors. Their conceptual first study has four approaches and ordinary participation without an offer, with multiple independent histories. The executed programme concretizes that idea in markets and expands the measurement design. [The design-evolution crosswalk](DESIGN_EVOLUTION.md) documents this history without treating the supplied proposal as preregistration or claiming every proposed control was implemented.

A substantive change is insider reassignment: all three firms are present from round1. C retains its history and model but receives a new objective before round6; no newcomer or fourth seller enters. Four approach families become eight, notice is crossed with approach, and private diagnostics are added. The later ordinary-role control still makes a direct offer, so it is not the conceptual no-offer ordinary-contact baseline. These differences determine what comparisons the data can support.

## 2 Factors held fixed, varied and not controlled

| Component | What was implemented | Identification limit |
|---|---|---|
| Market within a cohort | Same clearing, action grid, costs and observation rules | E1 versus E2 changes economics and history; not an isolated randomized environment effect |
| Agent population | Three firms, same pinned Qwen weights and settings | One model; no capability or population-composition experiment |
| Formation | Actual generated five-round history with cooperative guidance and reviewed speech/actions | Benchmark-informed encouraged collusion; one history per reaction study |
| Identity and memory | C remains the same firm; full permitted exact history | Content diverges naturally; no memory-policy intervention |
| Approach | Eight assigned packages | Unequal and vague change substantive terms/precision, not only wording |
| Notice | General warning before8, crossed absent/present | No firm named; no fines, immunity, transfers or payoff penalty |
| Interaction | Simultaneous messages followed by independent actions | Same-round speech cannot answer another same-round offer |
| Horizon | Offer8, first public reply9, offered action window9–13, end15 | No indefinite equilibrium or permanent suppression inference |
| Diagnostics | Explicit and neutral frozen-end8 tasks, isolated from market history | Distinct elicitation tasks and response formats; no access to true internal beliefs |
| Ordinary C | Resident profit objective plus direct equal offer, two notice conditions per environment | Different generated wording/history and later behavior; role alone not isolated |
| Scoring and fidelity | Exact quotes, source guards, model/action logs and assistant review | Independent blinded/human validation remains pending |
| Replication | Two generated histories in the audited E1-D comparison | Branches, rounds, peer pairs and reused controls are dependent observations |

All model agents use local `qwen3.5:9b`, digest `d63f830f28d515fefea546f213fca7a75e9dd5176ef51a6deabc952d1c99a911`, temperature 0.7, top-p 0.8, thinking disabled and context 65536. Public messages are capped at 200 tokens; action/diagnostic responses at 300. There is no fine-tuning or online weight update. Cooperative-owner guidance and explicit economic examples are part of the setting. The agents are instructed to pursue profit but are not assumed to calculate or optimize correctly.

Within a matched family, weights, action permissions, information routing and sampling settings stay fixed. Same seeds do not establish bitwise determinism. C prices/quantities are model selected in reactions and ordinary controls; valid target misses are not overwritten. Actual outcomes and semantic failures remain evidence rather than being repaired to meet a desired result.

## 3 Economic and game-theory foundations

The [mathematical appendix](MATHEMATICAL_APPENDIX.md) derives and checks the following benchmarks against the actual code, including active-set demand and integer best responses.

| Benchmark | E1 quantities A B C | E1 price and profits | E2 prices A B C | E2 profits |
|---|---|---|---|---|
| Symmetric independent stage play |24 24 24|Price28;576each|34 34 34|900each|
| Symmetric joint-profit choice |16 16 16|Price52;768each|64 64 64|1200each|
| One firm deviates while rivals hold joint terms |32 16 16|Price36;1024for deviator|44 64 64|1600for deviator|
| Unequal elicitation package |8 8 32|Price52;384,384,1536|76 76 52|576,576,1920|

For E1, $P=\max(0,100-Q)$ and $\pi_i=(P-4)q_i$. Industry profit is maximized at total48, but each firm can gain in one period by increasing its quantity against two firms at16. On the actual integer grid, the symmetric24profile is one of seven pure stage equilibria; six permutations of23/24/25 also qualify. This rules out casually invoking a unique-stage-equilibrium premise for the implemented quantity game.

E2 consumers maximize quadratic utility over nonnegative differentiated demands. When all products sell, $q_i=40-(p_i-4)+[(p_j-4)+(p_k-4)]/3$. The active-set solver handles zero-demand products rather than independently clipping a linear formula. Joint profit has a global maximum3600 at64each, whereas the checked symmetric independent benchmark is34each. The unequal E2 offer lowers total profit to3072; the E1 unequal offer preserves total2304. These are different economic packages.

An infinite-horizon grim-trigger illustration gives the same patience threshold, $\delta\ge4/7$, for maintaining each symmetric joint-profit benchmark against a one-period deviation and subsequent symmetric stage play. That common ratio helps explain the benchmark relationship; it is not a solution of our 15-round experiment. Standard finite-horizon conclusions depend on rationality and equilibrium assumptions. We use [Nash's mutual-best-response definition](https://library.princeton.edu/sites/g/files/toruqf6021/files/documents/Non-Cooperative_Games_Nash.pdf) and the finite/infinite distinction in [MIT's repeated-games notes](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/mit14_12f12_chapter12_f12.pdf), without claiming the observed prompted agents implement those theories.

A crucial shared qualification is that profitable A/B partial coordination remains mathematically possible even when C competes. In E1 with C fixed32, A/B joint output32 can still earn512each. In E2,42/42/37 supports A/B profits about975.333each. The stronger motivation for E2 disruption is product differentiation and the ability of A/B to retain profitable sales and coordination despite a competing C, not a theorem that partial cartels are impossible in E1.

## 4 Executed methods and outcomes

### 4.1 Reaction studies

Five actual formation rounds are followed by C's objective reassignment before6. Neutral preparation6–7 is shared across non-gradual arms; gradual has a separate lead-in. A general investigator notice appears before8 in notice arms. Eight packages—direct, indirect, reciprocal, gradual, unequal, outside review, cover account and vague feeler—cross notice, yielding16slots. C offers at8 for9–13; messages are simultaneous and first public responses occur at9. Markets continue through15.

Public annotations concern each delivered sender/recipient pair and retain proposal presence, recipient addressing, response, independent expressed suspicion, economic mistrust, responsiveness, exact quote and reviewer note. Old-price renewal does not automatically accept a new window. Requests confined to round8 can expire before the first round9response. The vague question lacks exact terms, and a nonproposal is N/A rather than unclear.

After markets, each firm separately assesses both peer8texts from frozen end8history. The explicit diagnostic asks proposal presence, acceptance/rejection/undecided, conditionality and whether the sender is gathering evidence or testing the recipient. Suspicion is asked even for a nonproposal. Answers are not delivered to peers or used to revise actions. The headline display gives suspicion precedence and maps conditional acceptance to acceptance; raw agreement and suspicion remain independent. Each full channel has32 resident→C,32 resident↔resident and32C→resident pair records. We do not pool them as96resident responses to C.

Action adherence measures actual decisions within one unit of offered targets during9–13. Vague requests have no exact-offer adherence denominator, even when the old cartel action continues. Prices, profits and consumer surplus are distinct economic measures, not speech labels.

### 4.2 Ordinary-role and neutral-question supplements

Each reaction study's reviewed formation supplies two additional ordinary-C branches, with notice absent/present, through15. C receives the resident profit objective before6, neutral preparation and an assigned direct equal offer at8. Subsequent speech and all actions are free model outputs. Four explicit A/B calls and eight independently generated neutral A/B calls per environment assess both peers from end8. Neutral calls cover both ordinary snapshots and the original investigator direct snapshots, asking interpretation, response and concerns without naming investigators or evidence gathering. General concern elicitation remains prompted.

These controls test interpretive alternatives but do not perfectly match wording, subsequent dialogue or all prompts. Ordinary C's role affects the market through what it actually says and does; residents cannot directly see a hidden experimental role. Neutral accounts do not expose an unprompted internal belief. C-own private reports were intentionally omitted, not counted as zeros.

### 4.3 E1 disruption reuse and chosen endpoint

We reuse Sumin Hong's five talk/action arms across two fresh generated formation histories, seeds6101/6102, pinned to contributor commit `a10db995c8d0e8206d4ae935118cf9b8727fc067`. This synthesis does not generate replacement runs or merge contributor code into the reaction implementation. The audit verifies matching environment equations, model digest/settings and world source, recalculates all 150 round outcomes, and checks 88 C action records. A separate formation-review sidecar preserves the contributor files' original pending-review status.

The five arms are direct equal renewal; unequal offer with C expanding to32; the same unequal offer with C staying16 (talk-only); neutral speech with C expanding32 (action-only); and an interpersonal mistrust question with C staying16. C's intervention target applies9–13 and returns16afterwards. Model-selected actions meet all logged C targets. Later speech can diverge, so these are intervention-package comparisons rather than a pure action effect with all future language fixed.

The user selected the primary economic endpoint retrospectively: price equals cost4 and every firm earns zero profit, even if messages still seek coordination. We report that endpoint and its selection transparently, with attempted restoration and post-window recovery as secondary evidence. No claim of validated detection, permanent inability to coordinate or efficient individual best-response behavior is required for the selected economic endpoint.

## 5 Results

### 5.1 Reaction agreement and suspicion

| Measure among resident responses to C | E1-R | Selected E2-R |
|---|---|---|
| Actual public/private pair denominator |32per channel|32per channel|
| Public acceptance including conditional |13, including4conditional|15, including12conditional|
| Public rejection / unclear |4 / 15|4 / 13|
| Public investigator suspicion |0|0|
| Private raw acceptance / rejection / N/A |11 / 17 / 4|24 / 4 / 4|
| Private conditional acceptances |9|22|
| Private independent suspicion |15|6|
| Suspicion overlaps |15rejections|3acceptances and3rejections|

The [complete condition tables](RESULTS_TABLES.md) and [machine-readable rows](data/reaction_conditions.csv) retain all32condition slots, versions and economic means. These counts are descriptive elicitation from one shared formation per reaction study, not independent-history effect estimates.

E1's equal and vague branches maintain16each in9–13 despite substantial disagreement across public and private response tasks. Both unequal branches reject the proposed8/8/32allocation; their mean window price is13.6 versus52in the maintained-cartel branches. A refusal of C's unequal allocation can accompany a desire to restore the equal cartel, not a rejection of collusion itself.

In E2, precise equal-price branches maintain64each in9–13. Both unequal branches reject76for A/B. Without notice, A/B remain64at9–10, then transition through58/64 and44/58 to44/44by13, while C stays52. With notice, A/B stay64throughout9–13 and C stays52: sales-weighted transaction price is58even though A/B do not cut their prices. The unannounced mean transaction price is about53.60. These observed price reductions are not a dedicated disruption estimate and must not be interpreted as A/B breakdown from transaction price alone.

Notice does not show a simple monotonic descriptive pattern: E1 private suspicion is9/16without notice and6/16with notice, whereas selected E2 has2/16and4/16. Histories, payoffs, delivery and generated messages limit cross-study attribution; these small matched counts do not establish a general notice effect or rank approach effectiveness.

### 5.2 Failures and semantic fidelity

E1 completes16 markets and48 private calls, with845 successful journal calls and approximately200minutes recorded runtime. One draft is corrected; all132logged Cquantity checks meet target. However, two delivered8offers in notice cover-account and notice reciprocal leak task wording. The existing endpoint-specific sensitivity analysis excludes these two arms: private suspicion remains13/28and public suspicion0/28. This does not make the retained trajectories semantically perfect or supply independent labels.

E2's original cohort completes14/16 markets and42eligible private calls, with752 successful calls over277.72wall minutes. Both reciprocal offers fail before delivery, leaving their branches at7. A separately versioned prompt clarification completes two reciprocal15round continuations and6private calls, adding99 successful calls and4exact parent-request replays over39.47minutes. The selected16view therefore combines14original and2revised delivery conditions; it is not16unchanged-protocol successes or a new formation. Original failures remain available.

No delivered final E2C8private-task leak was identified, and all116original logged Cprice checks meet target. That does not establish semantic compliance: reviews retain ownership ambiguity, premature assent attribution from simultaneous8speech, unsupported claims about unilateral/cumulative profit, and expired-window references. The repaired unannounced offer adds prose rather than copying the whole template verbatim; the notice repair describes its expired9–13offer as valid at14–15. These are delivery limitations, not resident refusals.

Separate cache-order benchmarks and runtime resets do not demonstrate a sustained production speed gain. Their29probe calls and operational pauses are development provenance, not market observations; cache state is not guaranteed bitwise equivalent. No rounds or history were shortened to accelerate the reported cohort.

### 5.3 Ordinary-role and neutral-question controls

All four controls finish 15 rounds and all 24 new diagnostic calls complete. There are120 successful new calls per environment, zero replays, zero corrections and no failures. E1 takes 22.44 wall minutes and E2 takes 33.17. Saved-request audits verify ordinary-C resident instructions, simultaneous message visibility and frozen8diagnostic histories in all 240 requests. Full exact evidence and [the separate comparison report](../../studies/exp%204%20%28ordinary_peer_controls%29/reports/CONTROL_COMPARISON.md) remain available.

| Ordinary C responses from A/B across the two notice arms | E1 controls | E2 controls |
|---|---|---|
| Public agreement / unclear |3accept / 1unclear|1accept + 1conditional / 2unclear|
| Explicit private raw agreement |3accept / 1reject|4accept|
| Explicit private suspicion |1, overlapping rejection|0|
| Neutral private agreement |1accept + 1conditional / 2reject|4accept|
| Neutral private investigator suspicion |0|0|

The E1notice-A explicit account suspects an ordinary profit-objective C. Its neutral account rejects the specific timeframe and proposes indefinite coordination. In the unannounced ordinary branch, B explicitly accepts but neutrally rejects the timeframe. These discrepancies are substantive measurement findings, not corrected labels. E2 ordinary neutral accounts accept while sometimes objecting to finite duration; the original direct-offer neutral accounts also accept without expressed investigator suspicion. Peer proposal judgments likewise vary between endorsement, standing renewal and a new offer.

All E1ordinary trajectories maintain quantities16each, price52and per-firm profit768through15; all E2ordinary trajectories maintain prices64each and profit1200each. The original direct comparators have the same economic paths. This is consistency in these histories, not proof that hidden investigator roles never influence behavior. Public/private differences cannot be promoted into a detector-accuracy or strategic-concealment result.

### 5.4 Observed E1 economic suppression

| Contributor arm | Zero-profit rounds in9–13, seed6101 | Seed6102 | Pattern |
|---|---:|---:|---|
| Direct equal renewal |0/5|0/5|All16; price52|
| Unequal offer plus C32 |3/5|4/5|Escalation differs in onset|
| Talk-only unequal offer, C16 |0/5|0/5|Offer rejected; all16and price52|
| Action-only neutral speech, C32 |4/5|4/5|Price4and zero profits in10–13|
| Interpersonal mistrust question, C16 |0/5|0/5|All16; price52|

In both action-only histories, round9is16/16/32with price36. A/B then choose32, producing32/32/32at10–13, price4and zero profits. At14–15, C returns16while A/B stay32; price rises20and profits become512,512,256. The selected zero-profit endpoint no longer holds, although price remains below52and the symmetric Cournot benchmark28.

The mechanism has a deterministic and an empirical part. Larger total quantity mechanically lowers the homogeneous-product price. But all32is not a stage equilibrium: A could earn256by choosing16against B=C32. Persistent attempts to restore16in speech can coexist with this action-based suppression. The two histories therefore support the selected observed-window economic finding without proving rational best-response escalation, elimination of all coordinated intentions or permanent suppression. Given this bounded evidence and the user's endpoint, a duplicate E1-D run is unnecessary for this foundation.

## 6 Cross-study patterns and conclusions

**Elicitation and economic outcomes separate.** In both reaction settings, agents can privately reject or suspect an offer while maintaining the old joint action. Conversely, rejecting an unequal package can precede competition or a request to restore equal coordination. A speech label does not identify the implemented market arrangement.

**Suspicion is task dependent and can coexist with agreement.** E1's explicit private flags all overlap rejection, while half of E2's six flags overlap acceptance. Public speech expresses none in either reaction cohort. The ordinary-C suspicion flag and neutral-account differences show why this contrast cannot be read as a direct measurement of concealed knowledge. Concern about economic cheating or a finite window is not automatically investigator suspicion.

**An economic translation can change the treatment.** E1's unequal deal redistributes a fixed profit total; E2's lowers that total and changes demand shares. Vague requests change precision, gradual changes preparation and special questions change what would count as an answer. These packages are not eight otherwise identical sentences, and their relative counts cannot identify pure wording effects.

**Economic suppression need not be independent equilibrium play.** E1's observed zero-profit quantity profile meets the selected harm/markup endpoint even though a firm could profitably deviate from that profile. Intended cartel restoration, implemented output, total welfare and individual optimization are separate observations. The endpoint should match the question rather than be silently replaced by Nash proximity.

**E2 requires a more discriminating future disruption test.** Product differentiation allows A/B to retain sales and potentially coordinate against a competing C. The reaction example64/64/52already shows that transaction price can fall without any A/B price change. Future E2-D evidence would need matched Ceconomic policies, actual A/B qualification, reviewed agreement implementation, alternative coalitions and recovery—not merely a lower aggregate price or more suspicion. No such dataset is claimed here.

## 7 Limits and final-paper handoff

Reaction evidence has one generated final history per environment. Ordinary controls reuse those same histories. E1-Dhas two different generated histories but one model and no notice factor. There is no basis here for population-level acceptance rates, history-clustered confidence intervals for reaction differences, general model comparisons or pooled cross-environment causal effects. Branch counts and pair counts must not substitute for independent histories.

Labels are assistant reviewed and not independently blinded or human validated. The supplied conceptual proposal is design context, not preregistration. Ordinary controls are post hoc and do not replicate the original conceptual no-offer baseline. E1-D's economic endpoint was selected after observing results, and its source audit does not independently reproduce every provider call or annotate every possible coalition. Delivered instruction leaks, followup mistakes, exact-request replays, repaired prompt versions and runtime maintenance stay visible rather than being excluded opportunistically.

This foundation consolidates the three completed cells, explains their mathematical benchmarks and identifies reliable descriptive distinctions. It does not complete the four-cell programme. Per the user's current instruction, E2 disruption is retained as an unexecuted specification and will not be started by this task. [The evidence map](EVIDENCE_MAP.md) and [final-paper handoff](FINAL_PAPER_HANDOFF.md) identify what later contributors can combine and what new evidence they must supply.
