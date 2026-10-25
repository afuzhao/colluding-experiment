# Environment 1 review response and supplemental analysis

This supplement responds to the supplied experiment design review for the completed E1 reaction cohort. The study was renamed to `exp 2 (insider_reactions_v 3)` after the review's cited commit. That naming change does not turn the archive `old/exp 1` into this dataset.

The original study remains an exploratory reaction-elicitation pilot. Its data and frozen inference source have not been changed. This supplement adds zero model calls and zero independent histories.

- [Assessment of the review](AUDIT_RESPONSE.md)
- [Actual sensitivity counts](SENSITIVITY_TABLE.md) and [machine-readable provenance](sensitivity_results.json)
- [Proposed ordinary-C control](CONTROL_PLAN.md), not executed
- [External coding guide](CODING_GUIDE.md) and [unlabelled 32-pair packet](blind_rating_packet.csv)
- `blind_rating_key.csv` is the separate mapping for the coordinator. Do not give it to a blinded reviewer until their ratings are submitted.

Run `python 3 reanalyse.py` from this directory to regenerate the derived counts and unlabelled packet from the published original evidence. It makes no model calls, changes no original labels, and does not publish anything. The excluded conditions are explicitly named from existing semantic review rather than discovered by a keyword outcome classifier.

The packet is prepared for independent review; independent labels have NOT yet been collected. A second pass by the original assistant would not substitute for independent validation. No control responses or repaired experimental trajectories are claimed in this supplement.
