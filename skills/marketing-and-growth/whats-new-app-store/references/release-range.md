# Release range

## Choose the baseline

1. Resolve the target to a commit. Use a named release, branch, or commit when supplied. Otherwise use `HEAD`.
2. Honor a user-supplied tag, ref, or date cutoff. Use a supplied date as the actual time boundary and inspect the corresponding history and net changes. Otherwise identify the GitHub repository that publishes releases for the selected app.
3. Read the [GitHub release history](https://docs.github.com/en/rest/releases/releases#list-releases). Pick the applicable published release with the most recent `published_at` and use its `tag_name`. Exclude drafts and, for App Store updates, prereleases. For an explicitly targeted historical release, use the applicable release published immediately before it unless the user gives a different baseline.
4. For a repository that releases through GitHub tags alone, use the newest applicable remote release tag by date. Use the annotated tag date where available and the tagged commit's committer date as a proxy for a lightweight tag. Identify the date source if it matters. If GitHub is unavailable, disclose that limit and label any comparison based on local tags as provisional.
5. Resolve the chosen tag to its commit and verify that it is an ancestor of the target. If the latest GitHub tag is on a different line from the selected target, report the mismatch and resolve the intended ref before claiming a release range. If the baseline and target are the same, the default since-last-release range is empty. A request for notes for that tagged version itself uses the prior applicable release as its baseline.

Check explicit package or platform scope in a multi-app repository. Include shared changes only if they affect the selected app. If several plausible release tags point to different baselines and the release evidence cannot settle the choice, ask which version was last shipped for the selected app.

## Inspect the range

Useful read-only Git commands are `git ls-remote --tags <remote>` to check remote tag refs, `git log --first-parent --decorate --oneline <target>` to inspect release lineage, and `git merge-base --is-ancestor <base> <target>` to verify ancestry. After selecting the refs, inspect `git log <base>..<target>` for the full commit history and `git diff <base> <target>` for the actual net change. Start with a diff summary on large releases, then inspect the evidence behind each user-facing claim.

Use the first-parent view to understand the release line and the full range to see changes from merged branches. A commit in the range may have been reverted, shipped before, or left behind a disabled rollout. Use the end state and release evidence to decide what belongs in the copy.
