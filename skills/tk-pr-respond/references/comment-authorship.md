## Comment authorship

Comment authorship is a per-comment property, not an account property. Classify each feedback comment in this order:

1. If its body carries a prefix from `toolAuthoredCommentMarkers` in the repository-scope
   `$XDG_CONFIG_HOME/tigerkit/pr-triage.json`, classify it as `tool-authored` regardless of account type.
2. Otherwise, if `user.type == "Bot"` or the login ends with `[bot]`, classify it as `tool-authored`.
3. Otherwise classify it as `human-authored`.

With no configured marker, apply only steps 2 and 3. Record that the human classification used no marker evidence;
never invent a tool marker or infer tool authorship from writing style. A marker is comment-local: the same `User`
account may have both tool-authored and human-authored comments.

Use this classification only for the user-confirmation boundary before publishing a reply. A tool-authored finding needs
no extra human-communication confirmation after the exact resolution/publication plan is approved. A human-authored
finding requires current approval of the reply's exact substance, but the existing one-plan approval satisfies that
requirement when it already covered that substance; never ask twice for the same decision.

Authorship never changes whether a finding must be investigated or addressed. It also never controls re-review targets:
`CHANGES_REQUESTED`, approval, and review-request capability belong to accounts, so those paths use account identity only.

When a reviewer reply or current-head summary must explain a nontrivial architecture, flow,
dependency or state change, read [GitHub-native PR visuals](github-visuals.md). Use
Mermaid only when it reduces review effort and every relationship is verified; keep exact values
and compact comparisons in GFM tables.

