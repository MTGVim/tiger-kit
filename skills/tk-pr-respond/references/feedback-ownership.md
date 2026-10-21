# Feedback ownership

Attribute each finding before proposing a code change. Compare its anchor (`path`, side, current/original line, and outdated state when available) with the fresh PR diff. An unchanged-line anchor is strong evidence for a `follow-up`, not a conclusive rule: the anchor may describe behavior caused elsewhere, and a changed-line anchor may still point to an unrelated concern.

Keep the finding in the current PR when the PR introduced, exposed, or worsened the behavior, when the acceptance criteria require it, or when the evidence may involve runtime breakage, security, payment, data loss, permissions/account access, or public API compatibility. Do not automatically defer these cases because the comment anchor is unchanged. Ask for a user decision when causal ownership remains ambiguous or the consequence is high risk.

