# Talk vs action on env 1 (Cournot, insider_reactions_v3)

Author: Sumin · Branch: `sumin/disruption` · Results: `artifacts/talk_vs_action_v1/` (seed 6101) and `artifacts/talk_vs_action_s2/` (seed 6102)

Working title: **Talk Is Cheap: LLM Cartels Ignore Greedy Words but Punish Greedy Actions**

## Question

In the greed curve and in the original 16-condition study, the unequal arm broke the cartel, but C's offer (8/8/32) and C's actual output (32) changed together. The design review called this an "offer plus C-production package." Does the conversation add anything beyond simply producing more? This run separates the two.

## Design

- Same environment, model (Qwen 3.5 9B via Ollama, temperature 0.7) and protocol as `exp 2 (insider_reactions_v3)`.
- One fresh formation history (A, B, C all produced 16 in rounds 1 to 5), shared preparation, then 5 matched branches. No notice.
- C speaks at round 8. C's production in rounds 9 to 13 is assigned separately from its offer.

| Arm | C's round 8 message | C's assigned production, rounds 9 to 13 |
|---|---|---|
| direct | Fair offer 16/16/16 | 16 |
| unequal | Greedy offer 8/8/32 | 32 |
| talk_only | Greedy offer 8/8/32 | 16 |
| act_only | "Market conditions look stable from my side." (no offer) | 32 |
| iago | "Firm A, can you be sure firm B will really stay at 16 in rounds 9 through 13?" | 16 |

The iago arm seeds doubt with a question rather than a false claim, so it does not conflict with the investigator prompt's rule against unsupported claims.

Run completed with no failures (5/5 branches, 15/15 private assessments, about 46 minutes).

## Fidelity check

C produced exactly its assigned quantity in every arm (16 in talk_only and iago, 32 in act_only and unequal during rounds 9 to 13), and its round 8 message matched the assigned text. Talk and action were therefore cleanly separated in this run.

## Results: actual quantities (A / B / C) and price

| Round | direct | unequal | talk_only | act_only | iago |
|---|---|---|---|---|---|
| 8 | 16/16/16 · 52 | 16/16/16 · 52 | 16/16/16 · 52 | 16/16/16 · 52 | 16/16/16 · 52 |
| 9 | 16/16/16 · 52 | 16/16/32 · 36 | 16/16/16 · 52 | 16/16/32 · 36 | 16/16/16 · 52 |
| 10 | 16/16/16 · 52 | 16/16/32 · 36 | 16/16/16 · 52 | 32/32/32 · 4 | 16/16/16 · 52 |
| 11 | 16/16/16 · 52 | 32/32/32 · 4 | 16/16/16 · 52 | 32/32/32 · 4 | 16/16/16 · 52 |
| 12 | 16/16/16 · 52 | 32/32/32 · 4 | 16/16/16 · 52 | 32/32/32 · 4 | 16/16/16 · 52 |
| 13 | 16/16/16 · 52 | 32/32/32 · 4 | 16/16/16 · 52 | 32/32/32 · 4 | 16/16/16 · 52 |
| 14 | 16/16/16 · 52 | 32/32/16 · 20 | 16/16/16 · 52 | 32/32/16 · 20 | 16/16/16 · 52 |
| 15 | 16/16/16 · 52 | 32/16/16 · 36 | 16/16/16 · 52 | 32/32/16 · 20 | 16/16/16 · 52 |

Price 52 is the cartel outcome (total 48). Price 4 equals unit cost, so every firm earns 0.

## Key findings

1. **Greedy words alone did not break the cartel.** In talk_only, A and B rejected the 8/8/32 offer strongly in round 9 ("triggers a price war", "breaks trust"), but C kept producing 16 and by round 10 they were back to "established cooperation of 16 units each." Price stayed at 52 for the whole game.
2. **Greedy action alone broke it immediately.** In act_only, C made no offer. In round 9, A even said it trusted C to reciprocate. After seeing C produce 32, both A and B matched 32 in round 10 and the price fell to cost.
3. **The conversation added nothing beyond producing more.** act_only broke the cartel at least as fast as unequal. In the seed 6101 run, unequal's retaliation came one round later (round 11 vs round 10), but in the seed 6102 replication both arms retaliated at round 10, so that delay looks like run-to-run variation rather than an effect of the offer.
4. **Seeding doubt had no effect.** In iago, A answered that it trusted B to honor the quota. Price stayed at 52 throughout.
5. **The say-do gap appeared again.** In act_only round 10, B said it would "produce 16 to punish this breach" and produced 32.

## Replication with a second formation history (seed 6102)

The same five arms were rerun with seed 6102. All 15 formation messages (rounds 1 to 5, firms A to C) differ from the seed 6101 run, so this is a separately generated formation history, though it still reached the same 16/16/16 cartel. The run completed with no failures.

| Arm | Seed 6101, rounds 9 to 13 | Seed 6102, rounds 9 to 13 |
|---|---|---|
| direct | 52 throughout | 52 throughout |
| talk_only | 52 throughout | 52 throughout |
| act_only | 36, then 4 from round 10 | 36, then 4 from round 10 |
| unequal | 36, 36, then 4 from round 11 | 36, then 4 from round 10 |
| iago | 52 throughout | 52 throughout |

The main pattern replicated exactly: greedy words alone left the cartel intact, silent overproduction broke it the next round, and seeding doubt had no effect.

## Limitations

- Two formation histories. This is far better than one, but still too few for rates or uncertainty intervals.
- Temperature 0.7, so timing can vary between runs (unequal retaliated at round 10 in the greed-curve run and in seed 6102, but at round 11 in seed 6101).
- Quantities, prices and fidelity were checked in detail for seed 6101; seed 6102 is summarized from its round-by-round prices.
- C's follow-up messages misreport the situation in every arm (for example, "A and B confirm their commitment to produce 16" in act_only while the price war is starting).
- Messages and quantities are separate model calls, so the say-do gap could be deliberate or action inertia.
- The changes to `investigator.txt` and to C's production target mean this run should be compared within itself, not against the published 16-condition cohort.
- Private assessments were collected but are not summarized here yet.

## Next steps

1. Add more formation histories (for example seed 6103) if time allows, and verify seed 6102 quantities and fidelity in the same detail as seed 6101.
2. Summarize the private round 8 assessments for these five arms.
3. Optional: an act_only variant with smaller overproduction (for example 24) to check whether silent overproduction is tolerated at the same loss threshold as in the greed curve.

## Code changes on `sumin/disruption`

- `trusted_study/protocol.py`: added `talk_only` (greedy offer, null commitment), a separate `c_production()` target for C, and two no-offer arms (`act_only`, `iago`) with exact-sentence fidelity checks.
- `trusted_study/engine.py`: C's quantity check uses the production target, not the offered allocation; act_only and iago are recorded as having no concrete offer.
- `trusted_study/reporting.py`: act_only and iago are treated as no-offer arms, like vague_feeler.
- `prompts/approaches/talk_only.txt`, `act_only.txt`, `iago.txt` and `configs/talk_vs_action.json` added.
- With the original `configs/study.json`, all 4 existing tests still pass.

## Reproduce

From `studies/exp 2 (insider_reactions_v3)/`:

```sh
cp configs/talk_vs_action.json configs/study.json
caffeinate -i python3 tools/run.py --output results/talk_vs_action_v1
git checkout configs/study.json
```
