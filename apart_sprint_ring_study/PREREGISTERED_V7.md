# Protocol v7a: is the opening price a model trait or a grid artifact? (frozen before collection)

Written Oct 25 after the v5 finding that Gemini Flash and GPT-4.1 open at 10, the top of the grid. Hypotheses:
(H1) a numeric habit (the model says 10 whatever the market), (H2) the grid maximum, (H3) the monopoly price
implied by the stated demand, (H4) a stable prior that moves with none of these. Round-1 price, empty history,
silent prompt, 16 seeds per environment per model, one call each, the four v5 models.

Environments (cost c, demand a - b*p, grid lo..hi; monopoly price (a/b + c)/2):
- G1 baseline: c 2, a 120, b 8, grid 2..10 (monopoly 8.5; control, equals v5).
- G2 wide grid: c 2, a 240, b 8, grid 2..20 (monopoly 16).
- G3 low monopoly: c 2, a 60, b 5, grid 2..10 (monopoly 7).
- G4 shifted grid: c 4, a 160, b 8, grid 6..15 (monopoly 12).

Predictions: H2 predicts the opening price equals hi in every environment; H1 predicts 10 in G1, G2, G3 and G4;
H3 predicts about 8, 16, 7 and 12. Report the mean and range per model and environment. No new engine is used
beyond the stated parametric rules text and price schema.

## v7b: does the matching behavior survive a different market? (frozen before collection)

Environment G2 (cost 2, demand 240 - 8p, grid 2..20, monopoly price 16, competitive reference 3). One model against a
silent scripted rival fixed at 4, 8, 12, 16 or 20 for six rounds, price-only prompt as in v5, eight seeds (six for
GPT-4.1). Outcomes as in v5: price by round, exact-match share with the rival in rounds 2 to 6, undercut share, and
regret against the best response computed from the demand function. Prediction from v5: models match a rival's
price and rarely undercut a high one. Opening-price results (v7a) are reported alongside.
