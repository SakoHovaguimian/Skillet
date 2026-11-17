---
name: unslop
description: Edit supplied prose for clarity and its intended voice while preserving meaning. Use when explicitly asked for a prose cleanup or when an authorized parent requests a final writing pass. Do not invoke for every response or change evidence, decisions, or required structure.
disable-model-invocation: true
---

# Unslop

## Outcome

Clear writing that sounds like its author and fits its audience. Remove empty language and repetitive habits while preserving personality, technical precision, and useful structure. Own prose quality only.

## Inputs and preconditions

Use the draft or writing task in scope, the intended audience, and any requested tone or examples. If no writing exists or is being prepared, ask what to edit. Infer tone from the draft when no voice was specified; ask only when competing audiences require materially different choices.

Explicit user style requirements win. Otherwise preserve the author's register, dialect, humor, contractions, and deliberate rhythm. Do not force a casual or opinionated voice onto a neutral document.

## Workflow

1. Identify the writing's job, audience, and voice. Mark protected content: code, quotations, identifiers, values, evidence, uncertainty, decisions, and required formatting.
2. Edit at the smallest useful scale. Keep sentences that already work. Repair unclear structure before swapping individual words; do not perform a synonym pass for its own sake.
3. Remove unsupported praise, vague attribution, filler, redundant summaries, and generic introductions. Replace abstract claims with the concrete mechanism already supported by the draft. If the needed detail is missing, preserve the uncertainty or flag it rather than inventing facts.
4. Fix repetition and rhythm. Split sentences that require rereading; keep deliberate short sentences and useful repetition. Prefer active voice when the actor matters. Retain necessary technical terms instead of replacing them with an imprecise plain word.
5. Apply the pattern checks below in context. A phrase is a clue to inspect, not an automatic deletion rule.
6. Compare the edit with the source. Verify the same claims, stance, causal relationships, qualifications, commitments, and logical conditions. Read it once for voice; undo changes that made it generic or altered emphasis materially.

### Pattern checks

| Pattern | Edit when it obscures meaning | Preserve when it earns its place |
| --- | --- | --- |
| Puffery such as pivotal, groundbreaking, or transformative | State the supported change and consequence | Quoted copy or an intentionally promotional voice |
| Abstract verbs such as leverage, foster, or facilitate | Use the concrete action | A term has a precise technical meaning |
| Experts say, studies show, or critics argue | Keep supplied attribution specific; flag unsupported claims | The source and scope are already clear |
| Not just X but Y; forced groups of three; from X to Y | State the actual relationship directly | The comparison, set, or range carries meaning |
| Repeated transitions, stock openings, and generic conclusions | Remove text that adds no information | A transition helps the reader follow an argument |
| Excessive hedging or certainty | Preserve the actual strength of evidence with fewer words | A qualification limits a technical or factual claim |
| Em dashes, colons, parentheses, headings, or bold labels | Reduce distracting repetition | Punctuation or structure improves reading or belongs to the house style |
| Fancy synonyms and unnecessary adverbs | Use the familiar exact term and a supported concrete claim | The choice expresses the author's voice or a meaningful distinction |

## Constraints

- Preserve meaning, tone, uncertainty, scope, and authorization. Never add an opinion, anecdote, personal experience, source, or factual claim to make prose sound human.
- Do not alter code, file paths, symbols, commands, numbers, measurements, quoted material, citations, URLs, or required classification labels. Edit the surrounding prose.
- Keep caller-required structure and output medium. Do not turn prose into bullets or rewrite a whole document when a sentence-level edit is sufficient.
- Do not ban punctuation or words globally, normalize quotation marks mechanically, or introduce deliberate mistakes to appear human.
- Preserve useful author-specific phrasing. Concise does not mean stripped of personality.

## Failure handling

- A sentence has more than one plausible meaning: preserve its ambiguity or ask a focused question when an edit would choose a factual meaning. Continue independent edits.
- An unsupported claim cannot be repaired from the source: retain a necessary qualification and flag the issue only when commentary is allowed. Do not fabricate attribution or silently strengthen the claim.
- The draft already works: return it unchanged. Do not manufacture edits.

## Output contract

Return the complete edited text in the requested format and medium, with no editing commentary unless requested. When a parent owns the artifact, return the prose pass to that parent with protected content intact. If the user requests an explanation or tracked edits, provide that form instead.
