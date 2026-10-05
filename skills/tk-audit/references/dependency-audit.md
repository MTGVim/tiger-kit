# Dependency and Dependabot evidence

Read for a selected dependency/security audit. Keep local resolved dependencies and
provider advisory backlog as separate evidence populations.

Inspect the relevant manifests and lockfiles first. Preserve each affected manifest,
package/ecosystem and resolved version; distinguish direct, transitive and unknown
relationship only when the source supports it. Record the inspected revision and
missing or conflicting lockfile evidence.

When the audited repository is identified on GitHub and existing read access is
available, check its unresolved Dependabot alerts. Use the repository's verified
host and identity with the REST list endpoint, `state=open`, and up to `per_page=100`.
Complete pagination through the returned Link cursor or an existing client's
equivalent pagination; do not substitute a guessed page number for before/after.
Keep the request scope, collection time, inspected default-branch revision when
available, and any unfinished pages. A complete successful empty collection means
only zero open alerts in that provider scope at that time.

Preserve alert number/URL, GHSA or CVE, severity, package/ecosystem, manifest,
dependency scope/relationship when supplied, vulnerable range and nullable first
patched version. Keep distinct manifest instances even when package/advisory match.
The REST alert is not a resolved-version inventory: corroborate the relevant
lockfile separately. Do not silently replace missing fields with a confident value.

Report partial collection, access failure, unavailable/disabled provider, malformed
data or unknown scope as an inspection limit, never a clean zero. Existing evidence
may still support local findings. Do not request new credentials, connect an account
or widen access as part of the audit; hand off that need only when required.

Keep local checkout and default-branch exposure distinct. Preserve alert state;
dismissed/auto-dismissed is not fixed, and local patched dependencies do not prove
the provider's default branch is fixed. Report a fix PR only with an explicit,
verified alert-to-PR relationship. A version-update PR, matching package name or
merged PR alone does not establish that relationship or remediation. If unavailable,
leave the relationship or resolution unknown. A missing patched version is not
permission to upgrade speculatively.

Remain read-only: do not dismiss alerts, edit dependencies/lockfiles, install or run
new scanners, merge PRs, or change provider settings. Follow existing root-cause
finding grouping while preserving affected instances and audited/unaudited coverage.

Sources: [REST alerts](https://docs.github.com/en/rest/dependabot/alerts#list-dependabot-alerts-for-a-repository),
[pagination](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api).
