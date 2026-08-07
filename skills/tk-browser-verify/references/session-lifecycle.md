# Headless session lifecycle

Classify ownership before interaction. An owned browser/context/page/process was
created by this run; an attached resource was independently proven to pre-exist.
Close only owned resources. Unknown ownership means do not close.

Every new owned Chrome/Chromium process uses exact `--headless=new` with a
run-owned isolated profile. If provider launch arguments cannot be proved, attach
to a directly launched verified endpoint or return `Unverifiable`; never retry
with a visible browser. A default user profile, stale port file, or prior UUID is not reusable
session evidence.

Binary evidence belongs in the parent-supplied or standalone run-owned evidence
directory. Create no Markdown file. Each cited screenshot must exist, be
non-empty, and be actually inspected. An unresolved directory, missing image, or
failed inspection makes required browser evidence `Unverifiable`.

On success, failure, interruption, or exception, clean up in order:

1. run-created pages/tabs;
2. run-created contexts;
3. run-started browser instances;
4. the exact owned process only when normal shutdown failed.

Before forced termination, match PID and profile against process arguments.
Never use `killall`, broad `pkill`, or task-name bulk kills. Preserve attached
browsers, user tabs/profiles, shared MCP/CDP instances, other verification runs,
and user-owned servers. Report cleanup residue without changing the application
verdict.
