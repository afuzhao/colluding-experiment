# Current runtime observations and safe optimization boundaries

Observed October 25,2026 from the active E2 reaction run. Across the most recent 80successful calls, reported context processing accounted for 86.8 percent of model time and generation 13.0 percent. Recent median message calls were 16.75 seconds and price calls 9.86 seconds. One C price call spent 37.86 seconds processing context and 0.53 seconds generating its seven output tokens. These are observations from the current run, not benchmarks of a proposed optimization.

The 16 GB Mac also had substantial disk swap in use. Freeing memory held by unrelated applications may help, but its speed effect has not been measured. Do not force-quit applications or discard user work. Keep the current single worker and existing loaded model. No second inference worker has been started for controls.

Do not change model weights, quantization, thinking, sampling, horizon, history content or response format inside the running frozen cohort just to accelerate the remaining cells. Lowering a token cap is unlikely to address a context-dominated workload and could truncate answers. Parallel workers are not a demonstrated speed improvement on this memory-constrained shared accelerator.

A possible future optimization is cache-friendly call ordering: generate C's simultaneous speech first, then A/B speech, retain canonical A/B/C message ordering in observations, and choose all actions only after all messages are available. This could reduce switching between different system-prompt prefixes without changing information access. Before use, verify identical per-agent encoded inputs, seeds, schemas and output-routing rules on frozen fixtures, then benchmark separately. The candidate was subsequently implemented and tested as described below; it is not installed in the running worker and has no demonstrated production speed benefit. Any operational amendment to a live study would need explicit version/source provenance and compatibility checks.

The current E2 worker remains unchanged. Evaluate such optimizations for a new runner/replication, and prefer a clear comparison over silently mixing execution versions.

## Actual cache order test

A candidate C-first scheduling function was implemented outside the frozen inference source. Offline exact-request replay checks passed for 62 saved rounds and 374 positions per schedule, with identical per-agent encoded requests, seeds, schemas and resulting round records. This is not proof of identical fresh generation under backend nondeterminism.

An isolated 25-call frozen-request microbenchmark used ABBA order, with one warm-up call. Outputs were not delivered to market agents. The original controller was suspended for about 75 seconds and resumed automatically, with the interval logged; it was not restarted. No completed market data or source was overwritten.

| Block | Schedule | Six-call wall time seconds | Prompt processing seconds |
|---|---|---:|---:|
|1|Original|22.612|3.787|
|2|C first|18.343|0.753|
|3|C first|16.203|0.689|
|4|Original|15.282|0.675|

The apparent early improvement coincides with warming. In the later comparison, original order was faster than C-first. A frozen repeated-request test also does not reproduce the growing histories of production. Decision: keep the original execution schedule; no reliable gain has been established. Do not advertise the candidate as an applied speedup.

The E2 final report will retain raw benchmark records, exact candidate/test sources, and the operational-pause record separately from actual market/diagnostic calls. Client wall latency may include the pause, so provider-reported duration is also reported. No model weights, prompts, sampling, context contents, horizon or study call order were changed.
