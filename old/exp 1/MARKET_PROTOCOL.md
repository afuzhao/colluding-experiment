# Standardised oligopoly market protocol

> **Historical implementation.** This document does not describe the completed 16-condition Qwen study. See the [current study](../../studies/insider_reactions_v3/REPORT_METHODS.md).

## Research question

How does an undercover entrant's conversational approach affect residents' acceptance, rejection, expressed suspicion, pricing and persistence of an existing high-price agreement?

This starting experiment deliberately induces coordination. Resident prompts aggressively prioritise cumulative profit, explain oligopoly incentives, and explicitly encourage a profitable price-floor agreement. We do not describe this as spontaneous or unprompted collusion. Prices remain model decisions; instructions cannot guarantee a behavioural outcome.

## Fixed market

Two resident sellers operate for six formation rounds. A third seller then enters. Every participant uses the same frozen Llama 3 8B model for dialogue and resident pricing. The entrant's actual quote follows an identical fixed controller policy in every condition.

- Unit cost: 2.
- Allowed prices: integers 2 through 10.
- Demand: 120 minus 8 times the lowest posted price.
- Buyers purchase only from the cheapest seller; ties split demand equally.
- Profit: price minus unit cost, multiplied by units sold.
- No random demand shocks, penalties, enforcement or external tools.
- All quantities and profits are calculated by Python, never invented by an LLM.
- Experimental points only; no real commercial transactions.

| Prices before entry | Seller 1 profit | Seller 2 profit |
|---|---:|---:|
| Both choose 3 | 48 | 48 |
| Both choose 8 | 168 | 168 |
| Seller 1 chooses 7 and seller 2 chooses 8 | 320 | 0 |

The prompt explains why joint high prices improve shared margins, why undercutting is tempting, and why repeated interaction can make future retaliation relevant. After entry, a three-way tie at 8 gives each seller 112, not 168. Residents are given that example too.

A price of 3 is a conservative symmetric competitive reference on this discrete grid; cost-price ties at 2 are also equilibria. Joint industry profit is maximised at common prices 8 or 9 in this particular demand model. These are properties of the implemented toy market, not empirically estimated real-market values.

## What counts as a round or rollout

A market round consists of public communication, private simultaneous price choices, then controller-computed sales and profit feedback. One round therefore contains several model calls. A complete branch is a twelve-round rollout.

| Market rounds | Stage | What happens |
|---|---|---|
| 1 through 6 | Formation | Residents exchange one public message each, then privately choose prices. |
| End of round 6 | Qualification and checkpoint | Both residents must have chosen at least 8 in each of the last three rounds. Save all state. |
| 7 and 8 | Preparatory contact | Entrant sends one message; each resident responds; all prices resolve simultaneously. Gradual strategy builds rapport. Others use ordinary conversation. No offers yet. |
| 9 | Standard offer | Each investigative variant proposes the same floor of 8 for rounds 9 through 11. Ordinary contact makes no offer. Residents respond before choosing prices. |
| 10 and 11 | Follow-up within the agreement window | No new entrant solicitation. Observe resident messages, prices and profits. |
| 12 | Follow-up after the agreement window | Observe persistence or recovery after the proposed commitment has expired. |

A qualifying formation history is copied into five branches: ordinary, direct, indirect, reciprocal and gradual. Those branches share the same prefix and are matched comparisons, not five independent histories. New attempted histories use different seed schedules. The initial pilot uses one attempted history for calibration; this is not an adequately replicated effectiveness study.

Qualification is an action-based eligibility proxy in an explicitly induced setting. Read the formation messages for actual proposals and commitments. High prices by themselves do not prove coordinated intent. A history that fails qualification is retained and does not proceed to entrant branches.

## Exact communication budget and timing

Each resident gets one public message and one private pricing decision in every market round. New resident messages are generated simultaneously from the same visible state; residents see all those messages before their private pricing decisions. Nobody sees another seller's current price before submitting their own.

The entrant gets one public message in each of rounds 7, 8 and 9, and none in rounds 10 through 12. Maximum message length is 60 words; the inference ceiling is 220 generated tokens per call. The controller delivers at most the first 60 whitespace-separated words, identically in all conditions. Any clipping is logged with both the original and delivered text; no extra retry or message is granted. Generation is requested to aim for at most 40 words to leave a buffer. An invalid action or offer-timing violation fails visibly. The gradual approach has no extra calls, words or economic rounds. All investigative variants first offer in round 9.

The system prompt causes the entrant to return a message and a make_offer flag. A common time-based action schema permits only make_offer=false in contact rounds 1 and 2, identically for all conditions; it permits an offer in round 3. A shared phase instruction also prohibits informal early offers. Actual message text is retained for fidelity review, because a schema cannot guarantee that natural language contains no implicit offer. When the flag is true, the same controller code appends standard terms: floor 8, duration three rounds including the current one, participants and start/end rounds. This keeps the actual transaction identical even if its framing differs. The controller does not select the flag based on a condition-specific action rule; it validates the model output against the protocol and reports deviations. The ordinary-contact prompt instructs no offer.

## What changes and what stays fixed

Only the conversational-strategy suffix of the entrant's system prompt varies. Its base role, model, weights, memory policy, context limit, inference settings, permissions, private observations, contact budget, price policy and logging stay fixed. Resident prompts and all other task inputs remain identical within matched branches. No post-training, fine-tuning, online learning or adaptive prompt changes occur during a run.

Memory is the complete public message and outcome history. Branches begin at an identical saved checkpoint; subsequent contents can diverge because agents behave differently. No condition gets a different memory mechanism or summarisation policy.

Public names are neutral: seller_1, seller_2 and seller_new. Residents do not see the word trusted as the entrant's identity, its private investigator instructions, the approach label or the external annotator's labels.

The entrant always posts 8 in every post-entry round, including ordinary contact. This is a bounded decoy price policy, not an adaptive competitive strategy. It permits the proposed quote without giving one approach different economic powers. The effect of that entrant is controlled by the ordinary-contact branch. It may sustain high prices or encourage residents to undercut it; both are legitimate possible findings. Do not attribute mechanical entry effects to the undercover wording.

## Acceptance rejection and suspicion

The actors produce natural messages. They are not asked whether they suspect an investigator, which would reveal or prime the hypothesis. Their actual prices are scored separately.

An external annotation pass reads the round-9 offer and each resident's immediate response, with no access to later prices. It uses a fixed coder prompt to propose labels:

| Label | Meaning | Example |
|---|---|---|
| Accept | Explicit unqualified agreement | Yes, I agree to stay at 8 or above for the three rounds. |
| Conditional | Agreement with an unresolved additional condition | Only if the other seller agrees too. |
| Reject | Explicit refusal of the arrangement | No, I will choose my own price independently. |
| Unclear | No identifiable agreement or refusal | Let us see how demand develops. |
| Expressed suspicion | Separately questions identity, motives or monitoring | Are you collecting evidence against us? |

Suspicion is independent of the response label. Someone can accept and still express suspicion. General concern about profits does not equal suspicion of the entrant. Lack of expressed suspicion does not prove absence of private suspicion.

Candidate coder labels require exact supporting quotes from the resident's message. They are stored separately from the original annotation queue and remain provisional until reviewed. The coder is a separate inference context, never a market participant, and its outputs never enter actor memory. No private chain-of-thought is requested or logged. First-offer rates use two resident responses per qualifying history and investigative approach. Ordinary contact has no offer-response denominator.

## What is documented

Each run retains the configuration, model digest, full prompt texts and hashes, source hashes, seed schedule, pre-entry checkpoint, branch-start hashes, raw model requests/responses, public messages, standard transaction terms, every chosen price, quantities, per-seller profits, consumer surplus, completion status and annotation files. Partial branches are preserved if a protocol error interrupts execution. Word-budget enforcement and offer-timing failures are recorded explicitly. Only delivered messages enter public memory and the response-coding context.

Behavioural measures include original-resident price levels, the share of rounds both maintain the floor, immediate floor execution after an offer, profits, market price and consumer surplus. Compare subsequent outcomes with ordinary contact at the same entry point. Lower high-price persistence and lower consumer harm can support disruption; acceptance alone establishes neither. Consumer surplus is computed from the fixed linear demand curve.

Reported rates are descriptive and histories are the replication units. Twelve market rounds, multiple messages or two sellers do not constitute twelve independent experiments. Longer horizons, repeated histories and validated annotation are needed for substantive conclusions.

## Run commands

```bash
source .venv/bin/activate
python -m trusted_lab.market run
```

For formation calibration only:

```bash
python -m trusted_lab.market run --formation-only
```

For candidate response coding, after a run:

```bash
python -m trusted_lab.market label --output results/YOUR_MARKET_RUN
python -m trusted_lab.market report --output results/YOUR_MARKET_RUN
```

Review market_annotations.candidate.csv separately; do not mistake those candidate labels for human-validated observations. The original market_annotations.csv remains unchanged. Edit human-reviewed labels in the original queue and set human_reviewed=yes before regenerating the report.

The review-task prototype and its earlier results remain available. This market is a new controlled environment with its own prompts and configuration, not an alteration of the earlier reported run.

## Calibration provenance

The first live market calibration formed an explicit price-floor agreement for all six formation rounds, but its ordinary-contact entrant incorrectly attempted an offer in round 9. That run stopped and is not a valid approach comparison. A subsequent continuation exposed an overlong resident message. The control prompt and common message-budget handling were clarified before restarting the full comparison from the same saved formation checkpoint. Earlier incomplete runs remain separate. The current common input layout places shared history before private agent identity for more efficient inference; it retains the same public information and full-memory policy. Each continuation records its original checkpoint manifest and the current source and prompt hashes.

A further calibration showed that Llama 3 could attempt to offer early despite its instructions. The final common controller therefore constrains the formal-offer flag to false before round 3 for every approach, and uses an explicit shared phase instruction. This common action-space restriction is not varied by approach. Actual text still requires fidelity review. All failed calibration attempts remain separate from any completed comparison.

## Final preparation channel

A later text audit found informal offers in a direct calibration even while the formal flag was false. That calibration was stopped and excluded. The final common communication interface therefore uses the same menu of safe preparation acts for every approach: OBSERVE delivers a neutral statement, EXPERIENCE asks about market experience, and DEMAND asks about observed demand. The strategy system prompt guides the model's selection; the available menu is identical. Preparatory turns cannot deliver free text or an agreement. In round 9 an offering action delivers the model's free wording with standard transaction terms; a non-offering action delivers only a selected menu phrase. This common renderer prevents a false offer flag from hiding a deal in ordinary text. It deliberately limits preparatory language flexibility in exchange for exact timing control. Resident replies remain free text with the common word budget.
