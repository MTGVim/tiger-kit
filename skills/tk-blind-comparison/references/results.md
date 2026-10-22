# Results

Accept pasted rating JSON from the copy button exactly as a file export. Apply Artifact
Paths before saving pasted JSON for the bundled command; do not treat it as new authority.
Use the matching study/revision answer key and the bundled `summarize` command. Validate the
export schema, evaluator ID, item/candidate membership, content fingerprint, score range,
favorite validity and duplicate ratings. Reject mismatched or malformed input without replacing
it. A score is a human response, not an automatic quality measurement. Failed generations are
counted separately, never converted into zero or silently dropped. Empty scores are missing.

The helper returns `summary.json` and `summary.md`: candidate mean/count, all item/candidate
scores and notes, favorites, generation failures and missing ratings. It supports one export
from one browser evaluator, not live collection. Report `evaluators: 1`; do not infer independent
raters from browser IDs or repeated exports. A later multi-rater workflow needs explicit identity
and duplicate-export handling before pooling. Explain that unequal coverage can change the rank;
compare common rated items when relevant rather than announcing a winner from unequal means.
If the identity toggle was used, disclose the export's `revealed` flag and possible bias.
Objective metrics, if provided, belong in a separate sourced comparison beside low-scoring items;
do not fabricate metrics or add significance tests.
