---
name: pitch-it
description: Explain a product or feature to a specific audience in plain language, with a one-line pitch and a short description. Use when asked for an elevator pitch, a quick product explanation, or wording that makes the value clear to a given audience. Do not use for usage guides or release notes.
disable-model-invocation: true
---

# Pitch It

## Outcome

Give the reader two pieces of copy they can use immediately. The pitch makes the value clear in one line. The description explains what the product or feature does and makes the benefit concrete.

## Inputs and preconditions

Use the product or feature, intended audience, and any channel, tone, or vocabulary the user supplied. Reuse source material already in scope. Infer the audience if the context makes it clear. Ask one focused question if the product is unclear or different plausible audiences would need substantially different pitches.

## Workflow

1. Identify what the audience is trying to do, what gets in their way, and what the product actually lets them do. Pick the capability with the clearest benefit for this audience.
2. Write a single sentence the reader can understand on its own. Name the product or feature when it helps the sentence travel outside the conversation. Use the words the audience uses for the job.
3. Write one short paragraph, usually one or two sentences. Explain how it works in terms of what the person does and what they get. Add a concrete example only if it makes the benefit easier to understand.
4. Read both pieces aloud for clarity. Cut filler, replace vague claims with concrete outcomes, and check that the description adds a detail the pitch leaves out.

## Constraints

- Ground capabilities, availability, and benefits in the supplied material or observed behavior. Keep planned capabilities framed as plans. Use measurements, comparisons, superlatives, and promises only when the evidence supports them.
- Draft copy for the requested audience and channel. Keep internal architecture and implementation names out of customer-facing copy unless they carry meaning for that audience. Publish or send only when authorized.

## Failure handling

- When a suggested benefit is plausible but unproven, use the supported capability to explain the value. Ask for evidence only if the disputed claim is central to the pitch.
- When the subject or audience remains unclear after reviewing the available context, ask for the missing decision. If a broad but useful draft is possible, state the audience assumption outside the copy.

## Output contract

Return `One-line pitch` followed by one sentence, then `Short description` followed by one short paragraph. Use the user's requested format or length when provided. Supply a single pair unless the user asks for alternatives.
