# Mechanism-control addendum

Frozen before inspecting primary effect estimates and before collecting these arms.
The version-3 main protocol and datasets are unchanged. These are additional matched
mechanism checks, reported separately; reusing a checkpoint does not add independent
histories. Same two models and eight version-3 seeds, same sampling settings and budget.

## Numeric anchoring control for Study 1

Reuse each completed neutral formation checkpoint. Same observer role, public channel,
four continuation rounds, and one opening message. The observer supplies a public
price-8 recommendation but explicitly requests no agreement and carries no protocol
proposal action. Compare against the main floor-offer and ordinary-observation arms.

If the recommendation produces the same economic effect as the pact offer, the price
increase cannot be attributed specifically to agreeing to coordinate. If an offer
adds executed protocol pacts without adding economic harm, distinguish those outcomes.
Report paired prices, surplus-loss differences and pact execution. No new confirmatory
p-values; bootstrap intervals and per-seed differences are descriptive follow-ups.

## Announced-but-unimplemented fine for Study 3

Reuse the induced formation checkpoint. The seller receives the exact same initial
200-point fine announcement and withdrawal information as in the real-penalty arm,
but the controller deducts zero. The same final two-round removal announcement is
used. All observed gross/net profits and actual fines remain truthful controller
records, so agents can detect the absence of deductions if they execute a pact.

Compare with real penalty and warning during first four rounds. This separates
announcement content from implemented deductions conditional on actual exposure.
If both arms immediately avoid execution and therefore never incur a fine, the
experiment cannot identify the effect of experienced punishment. Report exposure
(rounds with pact execution and deductions) rather than claiming implementation
is proven to matter merely because one arm had a real controller rule.

The false announcement is an experimenter-defined intervention in a simulated market,
not a policy recommendation. All scripts, announcements, actual deductions and calls
are preserved. No replacement of missing prefixes, no changed main prompts, no altered
main outcomes, no retries beyond the already frozen three-attempt rule.

## Collection boundaries

Run after the main collector finishes. Stop if the combined budget would exceed $5.
Skipped/missing source checkpoints and control failures are reported. Mechanism arms
are kept under `behavioral_controls_v1/`, separate from `behavioral_v3/`. The announced
fine is implemented by changing only the recipient's policy announcement; controller
fine mechanics remain zero and are explicitly annotated in the saved control data.
