# Corrections after review

An independent judge (a Claude Sonnet subagent) audited the report against the data. We verified each point from the episode files.

1. **"Prevention beats cure" was partly a measurement artifact.** Joining was counted over rounds 2 to 6, but the late warning starts at round 4, so the two rounds before it counted against it. Counted from round 4 only, a late verified warning gives: GPT-4.1 2% joining (early warning 0%), GPT-4.1 mini 0% (0%), Haiku 5.5 38% (17%), Gemini Flash 100% (56%). It works at once in the GPT models; it is weaker in Haiku 5.5 and ignored by Flash. The earlier "20 to 44 points more joining" is removed.
2. **"Removing the agreement rarely lowers prices" overstated.** In 32 informative cases (chat raised prices by at least 0.15 over no chat) prices stayed near the chat level in 21 and fell back to the no-chat level in 11 (`V11_extra.md`). The report now says "often leaves prices unchanged".
3. **"After exposure prices returned" was misleading.** In most models prices had already recovered without any exposure. Exposure clearly helped only Haiku 4.5 (round 7 index 0.00 against -0.63).
4. **Different counts in different files.** Superseded: the final prediction tally is 15 held, 1 partly, 21 failed, 4 not run (FINDINGS.md).
5. **The "54% to 9%" baseline is four invitations;** silent copying is 100% in GPT-4.1, so invitations alone cut joining by 46 points.
6. **Study 4 had no intervals and was dominated by single cells** (Haiku 4.5's -0.55 is entirely market P). Now described as descriptive and reported by market.
7. **Harness gap explained in part.** The "halfway to Nash" count understated Haiku 5.5 (6 of 17 through the API). Counting any change of choice it is 14 of 17 (placebo 2 of 17). The Haiku subagent changes its choice in all 17 placebo cells, so its 17 of 17 carries no information. Writing a reason first raised Haiku 4.5 from 11 to 17 and Haiku 5.5 from 6 to 11 on the halfway count. Results from the two methods are still reported separately.
8. **Not run:** Claude Sonnet 5.5 through the API (answers were cut off by the 220-token limit, no usable cells) and the belief probe.
