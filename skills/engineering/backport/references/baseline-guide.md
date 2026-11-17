# Baseline guide

Use this guide when the creation date or historical template snapshot requires inference. Keep the creation date as the assumed branch-off even when the target has received later template improvements; those improvements affect adoption status, not the baseline.

## Establish the target's creation date

1. Use an explicitly supplied creation date as the requested assumption. If repository evidence conflicts, record the conflict rather than silently replacing the date.
2. Inspect project-specific scaffolding records, origin notes, and initial project metadata. Prefer records that describe creating this target, not creating the original template or a remote repository later used to host it.
3. Inspect initial target history and corroborating file headers. A freshly initialized repository's first project commit can approximate creation. An inherited root commit belongs to the template's history and does not establish when this target began. A later history reset or import can also hide the actual creation event.
4. Use filesystem birth times only as a low-confidence estimate when the surrounding evidence supports them. Copies, archive extraction, clones, and restores can create new timestamps. Modification times and the current checkout date do not establish project creation.

Distinguish an observed timestamp from its interpretation. State, for example, that an initial target commit is being used as a creation-date estimate; do not claim it proves the exact scaffolding time.

Scaffolding may rename every source file, rewrite creation headers, and reset Git history. Corroborated headers may therefore reflect target creation even though the source originated earlier. Conversely, unchanged template headers cannot date the target. Do not require shared ancestry or treat a missing merge base as an error.

Record date precision and timezone. For a date without a time, use end of that day in the supplied or evidenced timezone as the selection boundary. If no timezone is available, disclose a UTC assumption. Flag template revisions on that same day as boundary-sensitive; do not claim their inclusion proves they were available at the actual creation time. If plausible dates select materially different snapshots, state the uncertainty and request the missing information while continuing independent inspection.

## Select the historical template snapshot

1. Resolve the template's relevant branch from the user's choice, project provenance, or clear repository evidence. Do not use a convenient feature branch simply because it is currently checked out. Ask when multiple plausible branches represent different template lines.
2. Pin that branch's current committed tip. Inspect its first-parent history to find the latest mainline snapshot at or before the creation boundary. Use committer timestamps as selection evidence and inspect nearby revisions; record the full selected commit ID and the boundary used.
3. Inspect the resulting tree and adjacent changes for plausibility. A feature commit with an old author timestamp may have reached the template branch after target creation. Compare available branch snapshots rather than collecting all commits with old author dates across unrelated branches.
4. If an exact imported template revision is documented, use it to corroborate the date-selected snapshot. If it conflicts, describe the mismatch and its effect; do not silently replace the required creation-date baseline with a different synchronization date.

Treat timestamp selection as an estimate: rebases, squashes, rewritten clocks, and later merges can obscure when a snapshot became available. If timestamps are non-monotonic or the relevant historical branch cannot be reconstructed, lower confidence or leave affected timing `Undated`. Do not present a current branch's inferred history as verified historical provenance.

Inspect historical trees and blobs through read-only history access. A checkout, worktree, fetch, or temporary rewrite of either project is unnecessary for this report-only workflow. If the required objects are absent, name the missing history and use the fallback below.

## Separate the comparison layers

| Layer | What it establishes | What it does not establish |
| --- | --- | --- |
| Historical template to current committed template | Net template evolution since the assumed branch-off | Whether the target needs or already contains it |
| Current template to current target | Present implementation differences | When either side changed or which implementation is better |
| Initial target to current target, when available | Evolution visible in the target's retained history | The intent behind a divergence without further evidence |
| Committed tip to working tree, on either side | Relevant uncommitted additions, edits, and deletions | A dated template release or a historical creation snapshot |

Keep uncommitted template changes as candidate improvements with `Undated` timing unless independent history establishes the specific change. Do not assign their timing from file modification dates. A committed improvement with additional uncommitted edits may need separate findings.

Trace replacements across paths and responsibilities. For example, a removed template service may have been superseded by a module under another name; recommend the coherent migration rather than reporting an isolated missing file and a deletion. Inspect actual consumers before declaring a target implementation equivalent or obsolete.

Use the initial target snapshot only if it represents the target at creation. If the earliest retained snapshot is a later import, it can support some target evolution claims but cannot establish what was copied originally. Without that evidence, describe current divergence without inventing when or why it arose.

## Fall back without inventing history

- Creation date known, historical template unavailable: preserve the date in the report, state that no valid historical snapshot was established, and use `Undated` for changes whose timing cannot be independently verified.
- Creation date unknown: request it, report available date evidence, and continue a current-state comparison. Do not use today, the latest target commit, or the previous report date as a substitute.
- Earliest available template snapshot later than creation: treat it as a history limit, not the baseline. The same applies to a shallow boundary that hides earlier objects.
- Partial historical evidence: date only the changes supported by that evidence. Do not extrapolate a file's history to the entire project.
- No Git repository: compare accessible files and any trustworthy supplied snapshots or records. Name unavailable revision identities and chronology rather than requiring Git initialization.

Current-state findings can still support useful adoption recommendations. Keep timing `Undated` and explain the target evidence supporting the recommendation. An uncertainty about chronology need not erase a well-supported implementation comparison; uncertainty about equivalence or applicability must still constrain the adoption judgment.
