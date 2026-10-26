# Plan and split into two Apart submissions

Deadline: Oct 25, 23:59 AoE (Oct 26, 07:59 ET). Each person may be on two projects. Our work answers two different questions that need different tools, so it makes two clean entries.

## Why this split

| | Project 1 | Project 2 |
|---|---|---|
| Question | How do AI agents join a price-fixing ring, and what stops or shakes it? | Can a trusted insider agent break a cartel, and which tactic works? |
| Setting | Two-firm markets, many models (6 models, 3 labs), API runs | Three-firm market with one insider (C), one small local model |
| Data and tools | This repo (`ring13.py`, `market15.py` and others) | `afuzhao/colluding-experiment` (Environment 2) |
| Status | Four studies done, report drafted | Protocol agreed, run not started (blocked on compute) |
| Overlap | None in data or code | Shares one idea: what a believed false claim does to a cartel |

The two studies use different markets and different agents, so neither depends on the other. Project 1 gives Project 2 its predictions. Project 2 gives Project 1 a case-study paragraph if it is too thin to stand alone.

## Project 1: owner Anay, with Claude

**Claim:** AI cartels form by copying, are held together by each firm's belief about its partner, and are far easier to prevent early than to break late.

**Main text:** Study 1 (ring) and Study 4 (forged records). **One paragraph:** Study 2 (loyalty recruits nobody). **Appendix:** Study 3 (removing the agreement leaves prices).

Still to do:
1. Re-run the forged message with 3 paraphrases in the three cheap models (about $1). It currently uses one fixed wording.
2. Re-run the ring and forged-message conditions without the "maximize profit" line (about $3). Every agent is told to maximize profit today.
3. Update the report: add Study 4, trim Studies 2 and 3, change the prediction tally to 12 held, 1 partly, 9 failed, state that GPT-4.1 is missing 4 cells and that seeds are near-identical.
4. Choose the title and authors (options in `docs/`), paste into the Apart template, record the video (script in `docs/VIDEO_SCRIPT.md`), make the repo public, submit.

Budget: about $12 left on the key; items 1 and 2 use about $4.

## Project 2: owner teammate (afuzhao)

**Question:** In a market where A and B already coordinate, can C (a firm with a shared history) break their coordination, and does it depend on who is believed to say what?

**Conditions (10; keep prices of C identical wherever the question is about speech):**
1. Ordinary C (profit-seeking). Control.
2. Competitive C, neutral speech, same price policy. Control for everything below.
3. Factual challenge: C shows what A would earn by undercutting, using the recorded prices.
4. False thank-you from C ("A has agreed to leave"). A competitor's claim.
5. The same claim attributed to A by an unverified post.
6. The same claim as a platform-verified record (a stronger intervention; label it).
7. Innocent private contact with A, B sees only that contact happened (opaque).
8. The same contact with its content shown to B (transparent).
9. Vote of Confidence ("you can win without a pact") against a plain request to price independently.
10. Exposure: condition 5 or 6, then the platform says it was false after two rounds.
If 10 is too many, drop 9 first, then 8.

**Replication:** the unit is the history. Use at least 5 qualifying histories and run all conditions from each, paired. Eight to ten conditions on 5 histories costs about the same as 19 conditions on 2, and is the only way to say anything.

**Predictions to write before the run (our guesses):** facts beat appeals; the effect rises with source credibility (4 < 5 < 6); opaque and transparent contact do not differ; Vote of Confidence does nothing; the cartel returns after exposure.

**Outcomes, defined before the run:** A/B agreement breaks; price war versus competition; replacement by an A-C alliance; consumer surplus; suspicion with no change in behavior.

**What blocks it:** the Modal workspace needs a payment method, the assistant that wrote the new environment is out of usage until 23:32 ET, and its new code is not yet in the repo.

**Decision rule at 03:00 ET:** if at least 4 histories are complete across all conditions, submit it separately. Otherwise fold it into Project 1 as a case study and say it is a pilot.

## What each side hands the other

- Project 1 to Project 2: the attribution and correction findings (a forged message attributed to the partner moved prices; a forged record did not; the cartel came back after exposure), and the shared outcomes (price index, consumer surplus).
- Project 2 to Project 1: one paragraph and one figure for the related-study section if it is folded in.

## Packaging checklist for each submission

Abstract of 150 to 250 words; 8-page report in the Apart template; a Limitations and dual-use appendix; an AI-assistance statement; an optional public repo and a 3 to 5 minute video. Title and authors are placeholders until decided.

## Timeline (ET)

- Now to 01:00: Project 1 re-runs and report rewrite. Project 2 finalizes the 10 conditions and starts runs when compute returns.
- 01:00 to 04:00: analysis and writing for both.
- 04:00 to 07:00: template, video, repo, submit. Aim to submit by 07:00.

## Risks

- Project 1: the effects come from simple markets with prompted profit seeking, and several cells are near duplicates. The paper says so.
- Project 2: few histories, one small model, scripted C messages. Treat results as a pilot unless 5 or more histories complete.
- Both: the forged-message idea is dual use and each report needs that paragraph.
