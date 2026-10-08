# Triage configuration

Read on an actual issue-triage run, and on first-run configuration. Per-field
precedence: explicit active user instructions, ignored `.tigerkit/repository.json`,
tracked `tigerkit.config.json`. An unavailable, invalid or unsupported file is
not an invitation to erase it or choose a different tracker.

The script-consumed machine keys `version`, `issueManagement.primary`, and
`issueManagement.sources` keep existing strict types; remote providers are
`jira|clickup|github|local` with verified ids and safe local paths.

The project-specific judgement fields `triage.policy`,
`triage.statePolicy`, `triage.priorityPolicy`,
`triage.categoryPolicy`, `triage.duplicatePolicy`, and
`triage.replyPolicy` are freeform **strings**. They inform classification
only, not execution, permissions, remote writes or tool selection. Do not
encode programmatic states/labels as if an unconfigured tracker shared them.

If missing, inspect known project labels and prior items using available
read-only access, then ask the minimum unresolved business questions. Show
the config target and resulting valid JSON and save only with approval.
Do not auto-create company-wide statuses or extra setup machinery.

Example:
```json
{
  "version": 1,
  "issueManagement": {
    "primary": "team",
    "sources": [{"name":"team","type":"jira","id":"PROJECT"}]
  },
  "triage": {
    "policy": "Preview each result before applying any changes.",
    "statePolicy": "Ask which labels indicate waiting and ready states.",
    "priorityPolicy": "Use verified customer impact and reproducibility."
  }
}
```
