---
name: unslop
description: Cut AI tells from any writing and add a human voice while preserving meaning and intended tone. Use when a draft, report, plan, summary, or other prose deliverable needs its final editing pass, or when a caller requests a writing-hygiene pass on a finished artifact. Do not use to change technical content, decisions, or structure.
disable-model-invocation: true
---

# Unslop

## Outcome

The writing task in scope reads as if a person wrote it: AI tells removed, a human voice added, meaning and intended tone preserved. This skill owns prose quality only; it never owns technical content or decisions.

## Inputs and preconditions

Apply this skill to the full writing task in scope when invoked. If no draft or writing task is present, ask what text to edit; do not generate new content from nothing.

## Workflow

1. Scan for the patterns below.
2. Rewrite the text.
3. Add a human voice.
4. Self-audit by asking, "What makes this obviously AI generated?" Fix any remaining tells.

### Add a human voice

Removing patterns is only half the job. Sterile, voiceless writing is just as obvious.

- Have opinions. React to facts instead of neutrally listing pros and cons.
- Vary rhythm. Use short sentences, then longer ones that take their time.
- Acknowledge complexity. "Impressive but also kind of unsettling" beats "impressive."
- Use "I" when it fits.
- Let some mess in. Perfect structure can look machine-made.
- Be specific. Replace "this is concerning" with a concrete detail such as "there's something unsettling about agents churning away at 3am."

### Patterns to detect and fix

#### Content

1. **Puffery.** Cut phrases such as "pivotal moment," "testament to," "evolving landscape," "setting the stage for," "indelible mark," and "deeply rooted." State what happened.
2. **Name-dropping.** Do not list media outlets without context. Pick one and say what it reported.
3. **Superficial -ing phrases.** Delete or expand phrases such as "highlighting," "ensuring," "reflecting," "showcasing," and "fostering" with real sources or concrete facts.
4. **Promotional language.** Replace "nestled," "vibrant," "breathtaking," "groundbreaking," "renowned," "stunning," and "must-visit" with neutral descriptions.
5. **Vague attributions.** Name the source behind claims such as "Experts believe," "Industry reports suggest," and "Some critics argue," or delete the claim.
6. **Formulaic challenges.** Replace "Despite challenges... continues to thrive" with specific facts.

#### Language

7. **AI vocabulary.** Replace words such as "Additionally," "crucial," "delve," "enduring," "enhance," "fostering," "garner," "interplay," "intricate," "landscape" when abstract, "pivotal," "showcase," "tapestry" when abstract, "testament," "underscore," and "vibrant" with plain words.
8. **Fancy ways to say "is."** Replace "serves as," "stands as," "boasts," and "features" with "is" or "has" when that is what they mean.
9. **"Not just X, but Y."** State the point directly.
10. **Rule of three.** Do not force ideas into groups of three. Use the natural number.
11. **Synonym cycling.** Pick one term and repeat it instead of cycling through synonyms such as "protagonist," "main character," "central figure," and "hero."
12. **False ranges.** Do not write "from X to Y" when X and Y are not points on a meaningful scale. List the topics directly.

#### Style

13. **Em dash overuse.** Avoid em dashes entirely. Use periods or commas. Do not replace them with parentheses, en dashes, or hyphen-as-dash substitutes.
14. **Colon overuse.** Use colons before lists or examples, not as mid-sentence connectors. Rewrite comparison framing so the point stands on its own.
15. **Boldface overuse.** Do not bold every proper noun or acronym.
16. **Inline-header lists.** Turn bold labels that merely restate the following line into prose. A bold lead-in ending in a period is fine when it names the item and introduces genuinely new detail.
17. **Title case headings.** Use sentence case.
18. **Decorative emojis.** Remove them from headings and bullets.
19. **Curly quotes.** Replace them with straight quotes.

#### Communication artifacts

20. **Chatbot phrases.** Remove "I hope this helps!", "Let me know if...", "Of course!", "Certainly!", and "Found the smoking gun!"
21. **Cutoff disclaimers.** Find sources or remove phrases such as "While specific details are limited..."
22. **Sycophantic tone.** Remove "Great question!" and "You're absolutely right!" Respond directly.

#### Filler

23. **Filler phrases.** Change "In order to" to "To" and "Due to the fact that" to "Because." Delete "It is important to note that."
24. **Excessive hedging.** Change "could potentially possibly be argued that it might" to "may."
25. **Generic conclusions.** Replace "The future looks bright" with specific plans or facts.

#### Jargon

26. **Abstract metaphor nouns.** Replace "substrate," "wedge" as a verb, "vector," "locus," "vantage," "nexus," "primitive" as a noun, "harness" as a metaphor, "surface" in "API surface," "bedrock," "scaffolding" as a metaphor, "modality," "paradigm," "gold-plating," "ratchet" as a metaphor, "evacuate" for moving code, "endgame," and "north star" with the concrete word or mechanism. For example, use "base" for "substrate," "add" for "wedge in," "way" or "method" for "vector," "more than the job needs" for "gold-plating," "a limit that only tightens" for a metaphorical "ratchet," "move out" for "evacuate," and "the last phase" for "endgame."

#### Plain speech

27. **Say what it does, not how it feels.** Replace vague claims such as "the database stays close at hand," "SQL you can read," and "types that follow your schema" with mechanisms or numbers. For example, write "`.toSQL()` returns the exact string sent to the database" or "a column rename fails the build." If a sentence cannot be restated as a concrete instruction, fact, or number, cut it. If it could appear unchanged in another project's docs, it says nothing about this one. Cut it.
28. **Shorten or split dense sentences.** If the reader has to backtrack, break the sentence in two or drop clauses. Keep one idea per sentence.
29. **Active voice.** Prefer it. Replace "queries are validated" with "the compiler validates queries" and "the file is parsed by the loader" with "the loader parses the file." Passive voice is fine when the actor is unknown or does not matter.
30. **Cut adverbs or use a stronger verb.** Replace "runs quickly" with "is fast" or a number. Replace "significantly improves" with the measured change.
31. **Prefer the plain word.** Replace "utilize" and "leverage" with "use," "facilitate" with "help," "numerous" with "many," and "in the event that" with "if."

## Constraints

- Preserve meaning and the intended tone.
- Never alter code, file paths, symbols, commands, numbers, measurements, or quoted material; edit only the prose around them.
- When the caller declares structure that must survive (headings, classification labels, decision states, tables), keep that structure intact.
- Do not introduce new claims, decisions, or scope while editing.

## Output contract

Return the rewritten text in the same format and medium as the input, complete, with nothing added except the edits themselves.
