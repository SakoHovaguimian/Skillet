---
name: grimoire-project-scaffolding-protocol
description: Execute the initial scaffolding of a new iOS project from the Grimoire base template, including project-wide renaming, git reset, entry-point routing, and configuration, while strictly maintaining existing architecture and formatting patterns. Use when starting a new app from the Grimoire template. Do not use for feature work in an existing project.
disable-model-invocation: true
---

# Grimoire Project Scaffolding Protocol

## Outcome

A renamed, re-configured, freshly git-initialized copy of the Grimoire template that matches the user's answers exactly, with no architecture drift and no invented project details.

## Inputs and preconditions

Do not assume project details or modify any file until the user has answered all five questions. Present them together and stop to wait for the response:

1. **Project name.** What is the new project name?
2. **Entry flow.** Are Welcome / Login / Signup required as intro screens, or should the app go directly to the main screen?
3. **Bundle ID.** What should the bundle ID be?
4. **Git repository.** What remote git repo URL should the project point to? The existing git history is always removed during scaffolding; the remote is added only when a URL is provided.
5. **Firebase configuration.** If the project uses Firebase, is there a configuration file (`GoogleService-Info.plist` or Firebase JSON) to replace the existing one at the same location?

Destructive-step gate: this protocol deletes the template's `.git` directory. Before executing any step, restate all five collected answers in a summary and get explicit confirmation. Only that confirmation authorizes execution.

## Workflow

### 1. Collect and confirm

Ask the five questions, wait for answers, restate them, and obtain explicit confirmation as defined above. If any answer is missing or ambiguous, ask again for that item; do not fill the gap with a guess.

### 2. Global renaming and header standardization

1. Rename the physical folder structure of the app.
2. Rename Xcode targets, schemes, and build settings.
3. Replace every string, variable, or configuration that references the original project name (`Grimoire` or `GlowPro`) with the new project name.
4. Overwrite top-of-file Xcode header comments: replace the original project name with the new one and replace all file creation timestamps with today's date.

### 3. Git and config scaffolding

1. Remove the existing git tracking (`rm -rf .git`), then initialize a fresh repository (`git init`). This happens only after the confirmation in step 1.
2. If a remote URL was provided, add it (`git remote add origin <url>`); otherwise leave the repository local and note that in the report.
3. Update the `.pbxproj`, `Info.plist`, and target build settings to reflect the provided bundle ID exactly.
4. If the user indicated Firebase usage and provided the configuration file, overwrite the existing file at the identical path and confirm it remains linked in the Xcode project hierarchy. If Firebase was indicated but no file provided, skip the swap and mark it `NO` in the checklist.

### 4. Initial routing configuration

Configure the app's entry point from the entry-flow answer:

- Intro screens required: keep the default wiring. `AppRootView` and `NavigationService` already default to the unauthenticated state (Welcome, then Signup/Login, then main app); change nothing and keep the existing auth UI patterns intact.
- Main screen only: bypass the auth/intro flow. Set the initial route directly to the main app (tab bar or home screen) and strip or disable the intro-flow presentation logic from the default launch path. In `MainViewModel`, hardcode the corresponding booleans (the template's welcome-screen and home-screen flags; read `MainViewModel` first and use the exact flag names found there rather than assuming their spelling).

### 5. Verify before finalizing

Validate every applicable item:

- All five questions were answered and the confirmation summary was approved before any modification.
- Global rename from `Grimoire` or `GlowPro` to the new project name is complete across folders, targets, and build settings.
- All file headers carry the new project name and today's date.
- `.git` was removed, a fresh repository was initialized, and the remote origin was added when a URL was provided.
- Bundle ID is updated globally.
- Initial route logic matches the requested entry flow.
- Firebase config replaced when applicable.
- Exact spacing, naming, and formatting parity with the template is preserved.

## Constraints

- Treat the existing Grimoire architecture as authoritative: match its patterns; do not invent alternatives.
- Follow the template's spacing, naming, and formatting exactly.
- Do not introduce architecture drift during scaffolding.
- Do not run any step before the confirmation gate has passed.

## Failure handling

- The user declines the confirmation summary or changes an answer: update the summary and re-confirm; execute nothing in the meantime.
- A rename collision or unreplaceable reference is found: stop that item, report the exact path and conflict, and continue with the remaining independent steps.
- A referenced template symbol (for example a routing flag in `MainViewModel`) does not exist under the expected name: search for the equivalent, use what the template actually contains, and record the discrepancy in the report.

## Output contract

Return, in this order:

- Scaffolding execution report
- Global rename summary (targets, folders, headers)
- Git and config status
- Routing setup summary
- Integration checklist with `YES` or `NO` per item
