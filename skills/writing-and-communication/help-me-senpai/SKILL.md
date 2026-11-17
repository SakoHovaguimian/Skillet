---
name: help-me-senpai
description: Explain how a concept or behavior works in plain English with a concrete example. Use when asked what something means, why it behaves a certain way, or to walk through code or a process for a beginner. Do not use for setup guides or implementation requests.
disable-model-invocation: true
---

# Help Me Senpai

## Outcome

Give a first-time reader enough understanding to follow what happens and why in one read. Match any level of detail the user asks for.

## Inputs and preconditions

Use the topic named in the question and any relevant code, files, or examples the user refers to. Inspect the relevant excerpt if it is available. Ask a focused question only if the subject cannot be identified.

## Workflow

1. Answer the question in one plain-English sentence. Say what the thing does or why the behavior occurs before giving background.
2. Pick the smallest example that shows the behavior. For code, use a short snippet in the correct language and show the output beside it. If the example produces a type error, changes a value, or has another observable result, show that result. For other topics, use a familiar situation and say how it turns out.
3. If the user supplied or pointed to a real case, show the relevant excerpt and trace one concrete input or starting state. For code, walk through the relevant lines in execution order and say what each does. For other topics, show the steps that cause the outcome. Reuse one example when the actual case is already simple enough to teach from directly.
4. Define unfamiliar terms in a few words where they first matter. Keep any distinction the reader needs to predict the result, such as what a compiler checks versus what happens when the program runs. Cut background and edge cases that do not change the answer.

## Constraints

Quote the user's code or source material faithfully. If you simplify or change it for teaching, identify the result as an illustrative example.

## Failure handling

If the real case is unavailable, give the general explanation with a clearly identified example and say which missing detail prevents a specific walkthrough. Label expected results when behavior depends on an unverified assumption.

## Output contract

Return the direct answer, the example and its result, then the walkthrough when applicable. Use short paragraphs, small snippets, and only enough formatting to make the sequence easy to follow.
