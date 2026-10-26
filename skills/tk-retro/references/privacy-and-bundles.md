# Private Evidence and Requested Bundles

Read before writing an upstream issue draft or reusable attachment. Conversation remains the
retrospective report; files carry proposals, not implementation or publication authority.

## Requested attachments

When the session produced a reusable reference, script, file set or skill draft and the user
requests it, save it beside the issue draft and bundle both with `MANIFEST.md` into
`<YYYY-MM-DD>-<topic-slug>.zip`. Without that request, keep the issue draft as the only file output.
Use the same upstream package scope and Artifact Paths checks for all files and the archive.
Exclude raw session evidence, scanner input, unrelated files and secrets from the bundle.

For each file, the manifest names one level and concrete evidence:

| Level | Required evidence |
|---|---|
| `field-tested` | The skill loaded this exact file in a real run and the result was accepted. |
| `applied-once` | Its rules were applied by hand to one output and the result was accepted. |
| `unverified` | A draft only, without the above execution evidence. |

Never raise a level because a reviewer approved the text or a static check passed. Record
unperformed checks, hypotheses, and source/license attribution for distilled external material.
Do not copy private examples into an otherwise generic attachment.

## Privacy checks

Before writing, inventory private terms by category: organizations, products/domains,
repositories, ticket keys, people, hosts/IPs, channels and local paths. Preserve public upstream
names, revisions and skill-internal paths. Replace private terms and verbatim requests with
neutral descriptions, including in topic slugs, examples and attachment names.

Check the final draft and every attachment, including the manifest:

1. Fixed-string identifier scan against the inventory; repair until no private terms match.
2. Verbatim scan against available user messages with [the scanner](../scripts/scan_verbatim.py).
   Review shared runs of at least 10 characters; neutralize copied private wording. Only verified
   public names, code literals and generic phrases may be exempted, with a reason. Check examples
   against available source artifacts too: a generic-looking copied incident is still private.
3. A separate read-only reviewer with fresh context reads only the deliverables, without the
   session or private term inventory. Ask it to flag identifying details, distinctive real incidents
   or examples that appear copied from private work. Repair and repeat for the current files.
   Do not spawn more reviewers from that review. If unavailable, label the pending check
   `Unverifiable` and withhold the file delivery; still return sanitized conversational findings.

All three checks must pass before delivering a draft or bundle. If needed evidence is unavailable,
report that gap instead of recording zero matches. A reviewer cannot prove anonymization alone.
Record scanned categories, repaired match counts, reviewed public/generic exceptions and reviewer
verdict in the manifest, or briefly in conversation without a bundle. Never record private terms
themselves. Apply the same sanitization to conversational findings.

## Scanner use

In an ignored run-owned restricted file, provide UTF-8 JSON with `messages` (separate strings),
`terms` (private strings), and optional `allow` (reviewed public/generic exact strings).
Include source-artifact example text as an additional message when available. Keep actual values
out of command arguments, logs and bundles. Run:

```bash
python3 <package>/scripts/scan_verbatim.py --input <private-input.json> <draft.md> <attachment.md>
```

The scanner normalizes Unicode and whitespace for wording comparison, scans each message
separately and reports only counts and normalized offsets by file number. It does not print
matched text. Exit 0 means no mechanical matches, 1 means review/repair required, and 2 means
invalid input or read failure. This is not a semantic review or an automatic privacy verdict.
Delete only the run-owned temporary input after consumption, including a failed scan; do not
delete original evidence. Recreate it only when another repair pass needs it.
