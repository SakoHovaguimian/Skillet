---
name: how-to-use
description: Write a short guide that helps someone set up, use, and check a product feature. Use when asked how to enable or try a feature, what someone needs to use it, what they should expect to see, or how to explain those steps to users or teammates. Do not use for implementation specs, formal QA reports, or release announcements.
disable-model-invocation: true
---

# How to Use

## Outcome

Give the reader a guide they can follow with the product open. Explain what the feature does, who can use it, how to get started, and how to recognize a successful result.

## Inputs and preconditions

Use the feature or workflow named in the request. Reuse supplied screenshots, recordings, notes, existing guides, product access, and relevant repository evidence. Default to the person using the feature as the reader. Ask only if the feature cannot be identified or the audience, platform, or environment materially changes the steps and cannot be inferred.

## Workflow

1. Follow the feature from the reader's starting screen to the result. Verify exact labels, navigation, defaults, availability, and access requirements using the available evidence for the intended version or environment. Distinguish behavior observed in the product from behavior inferred from code or documentation.
2. Identify what's needed before starting. Include roles, account or workspace settings, required data, or rollout conditions only where they affect use. Distinguish who can enable a feature from who can use it, and say what the change affects when the scope could surprise the reader.
3. Write the shortest complete path. Use a numbered list for ordered steps, one action per step, and bold exact labels for controls the reader must find. Give the expected result immediately after the action, including where and when it appears. If setup and everyday use are separate, describe both in that order.
4. Include a safe way to try it when one exists. Prefer a preview, sandbox, or reversible action supported by the product. When the result is delayed, tell the reader when and where to look for it. If the only available action sends messages, charges money, or changes shared data, state the consequence before the step.
5. Include common sticking points and how to turn the feature off when those details help the reader. Explain what happens to existing data, queued work, or access only where it matters and is supported by evidence. Walk through the completed guide against the evidence and remove any step or claim the evidence cannot support.

## Constraints

- Keep the investigation read-only by default. A guide request authorizes documenting actions. Perform actions that change settings, send messages, or affect accounts only when the user has authorized that execution.
- Keep operator-only details such as internal flags, routes, and repository links in internal notes. Explain public availability in terms the reader can act on.
- Match the user's requested audience and destination. Update an existing guide in place when asked and when it is the maintained home for the topic. Publish or send a guide only when authorized.

## Failure handling

- If the product cannot be opened, use supplied material and current project evidence. Identify any consequential steps or outcomes that still need a walkthrough.
- If sources disagree, tie each path to its version, platform, or role where possible. Ask for the missing discriminator if it changes what the reader should do.
- If a setup path, permission, or outcome cannot be established, give the verified portion and identify the missing detail outside a public-facing draft.

## Output contract

Return the guide in chat by default or in the requested document. Honor the destination's format. For a standalone Markdown guide, use [the guide format](references/guide-format.md). Keep headings action-oriented and wording plain. Put verification limits and source links after the guide when they matter to the requester.
