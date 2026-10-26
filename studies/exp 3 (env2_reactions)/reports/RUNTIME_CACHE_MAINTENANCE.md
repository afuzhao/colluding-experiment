# Runtime cache maintenance

User requested implementation of a speed improvement during the E2 reaction run. The model server reported approximately16.4GB allocated on a16GB Mac, with about22GB system swap in use. This is consistent with memory pressure; swap usage alone does not establish that the inference runner caused all swap or prove a memory leak.

`tools/runtime_cache_reset.py` temporarily stops only the study controller, queues a documented Ollama unload behind pending inference, reloads identical model weights using an exact previously recorded request, and resumes the same controller. It has a finally block and independent resume watchdog. A pending study response is retained, not cancelled, retried or replaced. The isolated probe outputs are saved as development data and never delivered as market actions.

All market prompts, complete histories, weights, sampling settings, seeds, action schemas and study source files remain unchanged. Resetting runtime state may change floating-point/cache behaviour; this is operational maintenance, not proof of bitwise equivalence. Exact memory reports, probe requests/outputs and timing are saved in `artifacts/development/development_runtime_reset` after finalization. All pauses are included in final runtime reporting.

This first maintenance test measures the benefit before any periodic reset policy is adopted. Do not claim acceleration until actual timings are available. Do not automatically apply model changes, shortened histories or reduced reasoning.

Primary references: [Ollama keep_alive API](https://docs.ollama.com/api/generate), [reported MLX cache accumulation](https://github.com/ollama/ollama/issues/17875), [reported growth independent of context size](https://github.com/ollama/ollama/issues/17924). Issue reports motivate this test but are not a diagnosis of this particular run.

## Applied first reset

At2026-10-26T00:04:26–00:05:58UTC the same controllerPID36145 was briefly stopped and resumed. Allocation fell16,411,470,292→7,962,565,208bytes; reported swap22,907.69→13,559.81MiB. Three isolated requests were saved. Before-reset49.27seconds includes queue time from pending market inference; cold reload40.75seconds and immediate identical repeat0.498seconds are NOT evidence of a repeatable market speedup. Do not compare these as equivalent warm/cold conditions. The memory reduction is the established benefit.

`tools/watch_runtime_memory.py` is installed as a separate operational monitor. It checks only completed-scenario boundaries, resets only above12GB reported model allocation, waits at least10minutes between resets, and performs at most5 further resets. It never resumes a stopped/user-paused controller and exits on finished/nonactive states orPIDchange. Every reset retains weights/settings/full requests and saves separate maintenance/probe records. It does not duplicate experiment workers. The remaining study runtime must establish whether memory relief improves throughput.
