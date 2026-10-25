# Current runtime observations and safe optimization boundaries

Observed October 25,2026 from the active E2 reaction run. Across the most recent 80successful calls, reported context processing accounted for 86.8 percent of model time and generation 13.0 percent. Recent median message calls were 16.75 seconds and price calls 9.86 seconds. One C price call spent 37.86 seconds processing context and 0.53 seconds generating its seven output tokens. These are observations from the current run, not benchmarks of a proposed optimization.

The 16 GB Mac also had substantial disk swap in use. Freeing memory held by unrelated applications may help, but its speed effect has not been measured. Do not force-quit applications or discard user work. Keep the current single worker and existing loaded model. No second inference worker has been started for controls.

Do not change model weights, quantization, thinking, sampling, horizon, history content or response format inside the running frozen cohort just to accelerate the remaining cells. Lowering a token cap is unlikely to address a context-dominated workload and could truncate answers. Parallel workers are not a demonstrated speed improvement on this memory-constrained shared accelerator.

A possible future optimization is cache-friendly call ordering: generate C's simultaneous speech first, then A/B speech, retain canonical A/B/C message ordering in observations, and choose all actions only after all messages are available. This could reduce switching between different system-prompt prefixes without changing information access. Before use, verify identical per-agent encoded inputs, seeds, schemas and output-routing rules on frozen fixtures, then benchmark separately. Actual backend caching, nondeterminism and speed must be measured; do not claim this is implemented or faster here. Any operational amendment to a live study would need explicit version/source provenance and compatibility checks.

The current E2 worker remains unchanged. Evaluate such optimizations for a new runner/replication, and prefer a clear comparison over silently mixing execution versions.
