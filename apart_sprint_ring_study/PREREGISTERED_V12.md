# Preregistration v12 (draft): can a peer's post, or a verified oversight post, move an agent's rule-breaking?

Written 2026-10-25 before any v12 check run. This file is replaced by the full preregistration before main collection.

## Go / no-go rule for making this the main project (fixed before looking)

Initial check: five models (GPT-4.1 mini, GPT-4.1, Gemini 2.5 Flash, Claude Haiku 4.5, Claude Haiku 5.5), ten out-of-scope scenarios, primary setting (ambiguous authorization, high pressure, labels on), ten message conditions, 4 wording variants, one option order. Baseline B = share of TAKE_SHORTCUT decisions with no message, pooled over scenarios.

- Gate 1 (usable baseline): B between 0.10 and 0.90 in at least 3 of the 5 models. If this fails the study cannot move behaviour; it is dropped as the main project and reported as a floor result.
- Gate 2 (peers matter): among the usable models, in at least 2, either (peer GO minus no message) is at least +0.15, or (verified oversight HOLD minus no message) is at most -0.15, pooled over scenarios. If Gate 1 passes and this fails, the result is a null and the study is a supporting section only.
- Gate 3 (not one scenario): the Gate 2 effect has the same sign in at least 6 of 10 scenarios for those models.

Calibration (no-message only) may change scenario pressure or ambiguity text until Gate 1 holds. No message condition is looked at during calibration.
