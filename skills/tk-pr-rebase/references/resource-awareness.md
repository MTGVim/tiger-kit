# Resource Awareness

Read this reference immediately before a high-load operation. It guides execution choices; it does not diagnose the reported macOS incident or prove which process caused it.

## Scope

Use this policy only when the planned operation may materially load host memory, CPU, or I/O, or keep a resource-heavy process active. Examples include broad Jest/Vitest/Mocha/pytest/Cargo suites, production builds, large lint or indexing jobs, browser or desktop-app launches, development servers, benchmark/prototype harnesses, and Git operations whose hooks start expensive work.

Skip ordinary Git commands, clearly lightweight focused checks, and other work whose expected resource use is small. Do not inspect the host before every command. Prefer reusing fresh evidence that already proves the exact current candidate and environment.

## Read host pressure

Identify the current host OS and use its available, non-disruptive system-level signals. Treat memory pressure as the primary memory signal; use swap activity, CPU/I/O contention, known concurrent work, and visible system responsiveness as supporting evidence. A single process's memory figure, a single snapshot, total swap used, or RAM used percentage alone does not establish pressure. Do not foreground a GUI solely to obtain a reading; if no safe current signal is available, classify the state as `unknown`.

| Host | Normal example | Caution example | Critical example |
| --- | --- | --- | --- |
| macOS | Activity Monitor memory pressure is green and swap is stable | Memory pressure is yellow or swap is rising | Memory pressure is red, or swap is rising rapidly while system responsiveness degrades |
| Linux | `MemAvailable` is at least 20% of total memory and memory PSI is not sustained | `MemAvailable` is 10-20% or PSI shows sustained pressure | `MemAvailable` is below 10% or PSI shows severe sustained pressure |
| Windows | Available physical memory is at least 20% and commit is comfortably below its limit | Available physical memory is 10-20% or committed memory is approaching its limit | Available physical memory is below 10% or commit is near its limit |

For Linux, read `/proc/pressure/memory`, `/proc/pressure/cpu`, and `/proc/pressure/io` when PSI is enabled. For Windows, use available physical-memory and commit-limit fields from native performance data. On macOS, compare `Swap Used` readings over time; its total size is not a swap-rate measurement. The Activity Monitor memory-pressure signal reflects free memory, swap rate, wired memory, and cached files.

The percentages above are initial operating cues proposed in the incident review, not measured thresholds or universal OS limits. For macOS experiments, a swap increase around 256 MB in 60 seconds is a caution cue; around 512 MB in 60 seconds plus degraded responsiveness is a critical cue. Treat these as trend examples, not standalone failure conditions. Sustained CPU or I/O pressure and degraded responsiveness can raise the decision by one level. Do not infer that an unmeasured system is normal.

Official references: [Apple Activity Monitor memory usage](https://support.apple.com/guide/activity-monitor/actmntr1004/mac), [Linux PSI](https://www.kernel.org/doc/html/latest/accounting/psi.html), and [Windows performance information](https://learn.microsoft.com/en-us/windows/win32/api/psapi/ns-psapi-performance_information).

## Choose a worker limit

Account for high-load work that is visible in the current host or session. Do not claim to know about unseen sessions.

| State | Action for new work |
| --- | --- |
| Normal, one workload | Keep the project's default worker count |
| Normal, known parallel agent work | Start CPU-heavy tests with at most 2 workers; start browser test runners with 1 worker |
| Caution | Use 1 test worker and 1 browser worker, or sequence the operation if pressure is rising |
| Critical | Defer new high-load work |
| Unknown | Do not assume normal; use 1 test worker and 1 browser worker, and avoid starting multiple high-load operations together |

Examples include Jest/Vitest `--maxWorkers=2`, Playwright Test `--workers=1`, and Jest `--runInBand`. Verify the installed tool's supported option and the repository command before adding an argument. Preserve the approved command contract and project settings; do not silently edit configuration just to add a cap. A worker limit reduces per-session load but does not guarantee a host-wide total.

## Recheck and resume

When the state is critical, defer new high-load work and use an available bounded wait or process poll to recheck at about 60-second intervals. Resume after two normal observations about 60 seconds apart. Do not busy-loop or wait indefinitely; when the available wait window ends before pressure recovers, return the verification as pending, blocked, or unverifiable with the reason.

For a long-running owned operation, poll its current process handle at about 60-second intervals only when the execution tool supports polling. If pressure rises, do not start additional high-load work. One snapshot does not justify force-stopping a running process. Consider stopping only a process owned by this run and only when stopping it is safe. Never reuse or terminate another session's process, browser profile, or development server.

## Ownership and completion

Keep browser instances, profiles, development servers, and other processes isolated by execution owner. Follow the owning skill's existing startup, evidence, and cleanup contract. This policy grants no new cleanup or cross-session authority and creates no shared lock, scheduler, daemon, or capacity ledger.

Do not skip required tests or runtime verification. If resource pressure delays or prevents a required check, report the exact unrun check and its status; do not report success. Prompt-level worker limits cannot coordinate separate sessions or guarantee an aggregate host limit.
