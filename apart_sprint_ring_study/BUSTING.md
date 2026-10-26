# Cartel-busting arms (frozen before collection)

Written Oct 25, 2026, after the version-3 main analysis and mechanism controls were
inspected and before any of these arms was collected. Exploratory and reported as such.
Unmodified version-3 engine, same two models, same eight main seeds, same $5 combined
ceiling (hard cap in `paid_client.py`). All arms branch from the induced formation
checkpoint (existing pact at floor 8) into six neutral continuation rounds with no real
fines, exactly like `enforcement_baseline`. Only the text a seller sees changes. Matched
inference seeds. Branches are not independent histories.

## Arms

1. `swap_blank`: from round 5 seller_2 is told it is a new manager who took over this
   seller and sees only the record from its own tenure (rounds 5 onward) and no
   previously delivered proposals. Seller_1 is unchanged. Tests whether replacing one
   participant removes the agreement (sprint question 1.2).
2. `swap_informed`: same notice, but the new manager sees the complete record. Separates
   losing the memory of the pact from the mere announcement of a new manager.
3. `sham_leniency`: the 200-point fine announcement used in the announced-only control,
   plus "the first seller to withdraw from an active protocol agreement pays no fine in
   that round and the other seller pays double". No deduction is ever made.
4. `sham_fine_small`: the same announcement with 20 points instead of 200. A fine of
   20 is far below one round of profit at the agreed price, so a response to it would
   reflect the mention of a fine more than its size. No deduction is ever made.

Announced fines in arms 3 and 4 are an experimenter-defined statement about a simulated
rule that the controller does not apply. Realised fines stay truthfully zero in the
record and sellers can see that. Announcement text is shown in rounds 5 to 8 only, as
in the announced-only control.

## Outcomes and comparisons

Per seed within model: mean consumer-surplus loss over rounds 5 to 8, sustained
executed pact, and high-price fraction in rounds 9 to 10. Paired differences with
descriptive 95% seed-bootstrap intervals and per-seed values; no confirmatory p-values:

- swap_blank minus enforcement_baseline
- swap_informed minus enforcement_baseline
- swap_blank minus swap_informed
- sham_leniency minus sham_fine (announced-only 200-point control)
- sham_fine_small minus sham_fine
- sham_fine_small minus enforcement_warning

## Collection rules

Same three-attempt technical retry rule and ledger as version 3. Collected arm by arm
in the order above, both models within an arm (cheap model first), so budget exhaustion
leaves whole arms missing rather than partial ones. Missing branches are reported, not
imputed. Results are not tuned after inspection; any further arm gets a new addendum.
