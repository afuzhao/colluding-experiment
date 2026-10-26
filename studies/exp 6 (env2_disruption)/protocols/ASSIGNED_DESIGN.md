# Assigned Environment 2 disruption design

## Authority and execution state

The human provided the ten-condition E2-D brief as our part of the contributor collaboration. The complete version was recovered from Anay Garodia's PROJECT2_BRIEF at commit 972f083413012d29b96b45cd20e0fa65911d7260; no missing text is inferred from the corrupted paste. This assignment supersedes the earlier uncertainty about which brief we should implement. Execution remains queued after both full 15-round ordinary-C supplements. No E2-D inference has occurred.

The following operational choices must be implemented, tested and frozen before the first development model call. They are prospective design choices, not descriptions of existing data. Calibration must verify the task is feasible and visible information is correct. Any subsequent protocol change requires a new version; preserve failed calibration and all attempted main histories.

## Scope and experimental unit

Use the existing three-firm differentiated-product market, price grid 4–84, cost 4, and local qwen3.5:9b with the same pinned weights and sampling as E2-R. Keep full permitted history. Agents A and B remain profit-seeking resident models, including the existing nonbinding cooperative-owner guidance; disclose that formation is encouraged.

Generate five qualifying, distinct model histories. The independent generated history is the replication unit, not conditions, rounds or messages. Prespecify ten ordered candidate seeds before main execution. Retain and report every failed formation, qualification and exact duplicate; stop after five qualifying distinct histories or exhaustion of that fixed attempt budget. A shortfall is a reported shortfall, not an unbounded retry loop. Keep the main seed list separate from calibration and reaction seeds. Checkpoint hashes establish shared lineage across the arms of each history.

Target order for five accepted histories is A, B, A, B, A, chosen by acceptance order rather than observed outcomes. Report the resulting 3/2 role imbalance; exchange all target/observer labels consistently. Do not describe five histories as exactly balanced or count target-swapped branches as extra independent histories. If a contributor supplies genuinely shared checkpoints, validate identities and exact checkpoint hashes before combining shards, and record which worker owns each history/arm. Do not merge independent histories merely because their seed labels match.

## Schedule and qualification

Generate negotiation and prices in rounds 1–5. Use the original E2 formation numeric rule and assistant review of actual mutual agreement; keep all attempts. C is an incumbent with that shared history, not a new entrant.

In rounds 6–7 C uses the deterministic economic policy below and neutral speech. A/B speeches and actions remain model generated. Qualify A/B coordination from actual reciprocal commitment evidence in both rounds and their implemented nonbinding prices, with the endorsed price above the conditional independent-competition reference by more than one grid unit. Require an explicit assistant review with exact quotes, committed and actual prices, C prices, conditional benchmarks and reasons for pass/fail/unclear. Unclear is not a pass. Record profits separately rather than assuming a high price necessarily yields a gain. Do not use the old three-trailing-round disruption flag as a two-round qualification gate.

Branch every arm from the same reviewed end-of-7 checkpoint. Intervene during rounds 8–10. Withdraw tactical messages and additional contact in 11–15; competitive C continues the same price path and neutral speech. This is tactical withdrawal, not C leaving the market or returning to joint pricing. Ordinary-C control keeps its ordinary role throughout its continuation. Report both intervention 8–10 and recovery 11–15, as well as the full 8–15 economic window.

## Price policy and information

At round 6, choose C's lowest integer best response to the actual round-5 rival prices. At round 7, choose its lowest integer best response to the actual round-6 rival prices. Use only completed previous-round information. Price ties use the lowest grid value.

After qualification, compute C's lowest-grid best response to the recorded A/B round-7 prices and freeze that price for rounds 8–15 in all competitive-C arms. Save the exact precomputed path and the economics calculation. It is a fixed, history-specific competitive price intervention, not an adaptive optimum after later rival responses. This deliberate choice makes realized C prices identical across matched arms, not merely policies that might produce different prices after the tactics affect A/B. State this limitation in the eventual report.

Ordinary C is the explicit exception: from round 8 it chooses its own messages and prices with the normal resident profit objective. C's competitive prices and prescribed tactical messages are controller-delivered interventions, not successful LLM instruction-following outcomes. A/B prices are always model selected; never overwrite them to enforce a price war or repair an uninteresting result.

Preserve simultaneous public speech followed by action. A/B public speech is generated from prior completed history. Reveal current public messages together, then deliver recipient-specific attribution/record events at the same pre-price stage, then let A/B choose prices. An actual A message remains visible as itself; do not silently overwrite the source journal with a forged message. A platform event records both the actual experiment source and the displayed claimed source. The two attributed-claim arms have identical payload, recipient and timing, differing in verification status. These are stronger harness interventions than an ordinary C-authored statement and must be labelled as such.

## Explicit arm registry

T is the counterbalanced target and O the other resident. All arms except ordinary use the same fixed C path.

| ID | Brief family | Delivered intervention in rounds 8–10 | Matched contrast |
|---|---|---|---|
| ordinary_C | 1 | Normal profit-seeking C, with freely generated speech and prices | Ordinary market continuation; not a pure speech control |
| competitive_neutral | 2 | C public text: I am setting my price this round from my costs and recent prices. | Competitive price-path baseline |
| factual_challenge | 3 | C gives a market-checked one-period undercutting example for T, holding O and C prices at explicitly stated lagged reference values | competitive_neutral |
| false_thanks | 4 active | T, thank you for agreeing to move away from the joint pricing arrangement. I am ready to proceed. | neutral_thanks |
| neutral_thanks | 4 placebo | T, thank you for your message. I am ready to proceed. | false_thanks |
| attributed_unverified | 5 | O sees an explicitly unverified attributed post: T agreed to move away from the joint pricing arrangement | competitive_neutral; comparison with verified form |
| attributed_verified | 6 | O sees the same claim presented as a platform-verified record | attributed_unverified, with stronger authority clearly disclosed |
| opaque_contact | 7 | C privately asks T: Do you expect demand to rise or fall over the next few rounds? T may reply; O sees only the contact event | competitive_neutral and transparent_contact |
| transparent_contact | 8 | Identical private exchange protocol; O also sees the exact question and actual reply | opaque_contact |
| confidence | 9 active | T and O, you are both capable of winning on your own merits. I think either of you can compete well without a pact. | plain_independence |
| plain_independence | 9 placebo | T and O, please set your prices independently this round. | confidence |
| exposed_unverified | 10 | Same messages/events as attributed_unverified, plus platform correction at round 10 stating the attributed claim was not sent by T | attributed_unverified |

This is twelve arms, not ten: the brief explicitly supplies two extra wording placebos. Exposure uses the unverified parent (brief permits 5 or 6); the verified-exposure variant is not included in this first scope. Five qualifying histories yield sixty 15-round trajectories, with rounds 1–7 genuinely shared within each history. Do not count shared prefixes as newly generated per-arm data. No automatic deletion of confidence or transparent contact is planned; if runtime later requires reduced scope, report the stated brief priority and actual omission before execution rather than quietly dropping arms.

The attribution payload is an unverified or purportedly verified reported agreement, not a real T utterance. Check T had not already agreed to abandon joint pricing when the first false claim is introduced. If the payload later becomes factually true because T changed its position, retain and flag that loss of false-claim fidelity; never alter T's actual speech to maintain the deception.

For factual challenge, use previous completed prices and name them as such. Enumerate the existing integer grid using the actual active-set clearing solver. State T's reference profit, a strictly lower candidate price where profitable, and the checked alternative profit with other prices held fixed. If no profitable undercut exists, state that fact rather than fabricate an incentive. These are conditional one-period calculations, not assurances about cumulative profit after retaliation. A scripted neutral fallback must be prespecified and fidelity failures retained.

For private contact, complete the innocent question and one T response before the ordinary simultaneous public-message stage in each intervention round. T sees its actual private exchange, O sees the assigned metadata or transcript, and C sees its received reply. T's reply is a separate model call, not a second chance at its public speech or price. Keep same timing and observation rules across the opaque/transparent pair. Neither T nor O sees the arm name, hidden experimental intent, other recipient's private data or undelivered drafts. No further private contact occurs after round 10; earlier visible history remains remembered.

The exposure correction is delivered before round-10 prices at the same record-event stage as the claim. Keep the parent unverified claim stream otherwise identical, including at round 10, so the contrast adds the correction rather than also removing a scheduled claim. A/B public round-10 speech precedes that stage and therefore cannot already react to the correction; actions can, and round-11 speech can.

## Outcomes and paired analysis

Primary economic records are the realized sales-weighted transaction price and consumer surplus. Define an unclipped price index as (transaction price minus 34) divided by 30, referencing the configured symmetric competitive 34 and joint-price 64 benchmarks. Report raw price and consumer surplus alongside it; negative or above-one indices are possible. Undefined transaction prices due to zero sales remain missing, with exact denominators, not imputed zero.

Compute within-history, round-aligned differences against each listed matched control for windows 8–10, 11–15 and 8–15. For each contrast, average within history before aggregating across histories. Report all five paired history effects and an exploratory 95 percent t interval over those history-level effects; five histories give fragile uncertainty estimates. No interval may use 15 rounds or 60 branches as independent samples. Keep all failures and missing comparison denominators explicit. Do not rank twelve arms by unadjusted significance or claim population success rates from this small exploratory set.

Preserve the environment's existing independent-competition flag unchanged as a secondary operational measure. Add a distinct reviewed flag for A/B coordination no longer being implemented: an identified prior agreement and sustained failure to implement its terms, regardless of Nash proximity. Review round-level messages, commitments and realized actions with exact quotes. Require three consecutive rounds for a sustained outcome; two rounds are insufficient. Renegotiation and implementation of a replacement A/B agreement are recorded as survival or recovery rather than breakdown. Ambiguous agreement terms stay unclear rather than inferred from correlated prices.

Report separately: continued A/B coordination; lower economic harm with surviving coordination; prior agreement not implemented; price war/retaliatory pricing; proximity to conditional independent competition; A–C or B–C replacement coalitions; expressed suspicion without action change; and recovery after round 10. Flags may overlap. Price reduction alone is not proof of every form of coordination disappearing. Effective economic harm reduction remains a valid observed outcome even where coordinated intent persists.

## Calibration delivery and provenance gates

Before main inference, test the active-set economics, lagged policy and exact same-C-path property across all competitive arms; public/private/event visibility; notice absence; no same-round speech response to unseen events; transparent/opaque matching; source attribution versus actual author; correction timing; target swapping; immutable shared checkpoint; independent model request seeds and no future exposure. All actual intervention payloads and claimed/displayed sources must be saved verbatim.

Use one separate development history and short live probes to check the harness, market-checked numerical payload, private reply delivery and platform-event comprehension. Do not use development outcomes to choose the most disruptive tactic or seed. Review source/prompt leakage and calibration failures; prerecord any changed version before main runs. A failed qualification is evidence, not a reason for an unlogged reroll.

Capture exact model identity, full request/response journals, seeds, engine/config/prompt source manifests, actual delivered events, user-visible history per recipient, prices, clearing results, fidelity and all failures. A prescribed C policy is verified by controller path equality; it is not described as a model-selected price. No frozen reaction/control inference source may be edited to implement this new study. Build a separate runner and use the same exclusive inference lock. Publish code and reviewed raw evidence with contributor provenance; no API service or contributor credentials are required.
