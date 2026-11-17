---
name: whats-new-app-store
description: Turn the changes since the most recent GitHub release tag into short, emoji-prefixed App Store update notes. Use when asked for App Store release notes, copy for the What's New field, or a customer-facing summary of the features, improvements, and fixes in an app update. Do not use for internal changelogs, App Review instructions, or store publication.
disable-model-invocation: true
---

# What's New for the App Store

## Outcome

Produce paste-ready App Store update notes that cover the shipped changes users can notice. Use the fewest words that still convey those changes and any action users need to take.

## Inputs and preconditions

Use the selected app, repository, release target, and any baseline or language the user supplied. Discover the app from the repository or conversation. Default to committed `HEAD` as the target and the tag for the app's most recently published GitHub release as the baseline. Honor a user-specified tag, ref, or date instead. Ask only when app scope or release history remains materially ambiguous after inspection.

## Workflow

1. Fix the Git comparison range using [release range](references/release-range.md). Check that the baseline and target describe the same app and release line. Keep draft work outside the target commit out of the range.
2. Review the full history in the range and the net diff. Use commit subjects, PR summaries, changelogs, and release metadata as discovery aids. Confirm meaningful user-facing changes in the final state, including changes introduced through merges. Group related commits by what changed for the user and omit work that was reverted or remains unavailable to the intended release audience.
3. Cover distinct new features, visible improvements, fixes, changes to supported behavior, and required user steps. Check rollout and platform scope before promising availability. Include internal changes only when there is an evidenced user-facing effect.
4. Draft the shortest complete copy using [note format](references/note-format.md). Lead with any change that requires action or affects existing access, followed by the most useful new capabilities, improvements, and fixes. Combine related changes when each point stays clear.
5. Reconcile the lines against the range. Check that important user-facing changes survived the compression and that every line is supported. Check the destination's current field limits when needed, using the [official App Store Connect field reference](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information).

## Constraints

- Keep repository inspection read-only. Draft copy for the user. Tagging, publishing, or editing store metadata requires its own authorization.
- Use the names that appear in the released app. Keep commit IDs, issue numbers, ticket titles, code names, and raw technical detail out of the public copy unless a user explicitly needs a public identifier to act.
- Honor requested release scope, audience, and language. Keep uncertain claims out of the paste-ready text and explain material gaps separately.

## Failure handling

- If the baseline is missing, history is incomplete, or the target and baseline are incompatible, explain which ref or release evidence is needed. A summary from supplied evidence may be useful if its coverage is stated. Avoid presenting an arbitrary range as the release.
- If the range is empty or has no evidenced user-facing changes, say so outside the release copy. Use a factual maintenance line only if the requester needs copy and the reviewed changes support it.
- For a confirmed first App Store release, explain that the update-only field is unavailable and offer launch copy only if requested.

## Output contract

Return plain-text lines with one leading emoji per line. Keep the paste-ready copy free of headings, Markdown bullets, version numbers, and source notes by default. Put any material scope assumption, coverage gap, or requested Git range outside the copy. Return in chat unless the user specifies another destination.
