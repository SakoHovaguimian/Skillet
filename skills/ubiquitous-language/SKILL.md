---
name: ubiquitous-language
description: Build or update a DDD-style ubiquitous language glossary by analyzing the current conversation and codebase. Use when Codex needs to define domain terms, group language by bounded context, compare domain language against implementation naming, identify ambiguities or synonym drift, document actors, relationships, lifecycle states, commands, events, and write or refresh `docs/UBIQUITOUS_LANGUAGE.md` grounded in real model usage.
disable-model-invocation: true
---

# Ubiquitous Language

Build and maintain a DDD-style glossary that is grounded in both domain discussion and implementation reality. The goal is to make the team's language easier to understand, easier to search, and harder to misuse.

## Operating Principles

- Preserve information. Merge forward from any existing glossary instead of replacing it wholesale.
- Make language visual and navigable. Prefer maps, tables, lifecycle flows, and relationship bullets over long prose.
- Be opinionated. Pick canonical terms when evidence supports a recommendation.
- Be honest about drift. Flag overloaded terms, aliases, UI/backend mismatch, and implementation names that mislead domain discussion.
- Separate domain language from technical wrappers. DTOs, schemas, mappers, API responses, and UI helper objects can be evidence, but they are not automatically domain terms.
- Ground claims in codebase evidence. Include files, types, functions, routes, screens, or tests wherever possible.

## Workflow Map

```text
Conversation language
        ↓
Existing docs/UBIQUITOUS_LANGUAGE.md
        ↓
Codebase vocabulary scan
        ↓
Model + usage tracing
        ↓
Bounded context grouping
        ↓
Ambiguity + synonym analysis
        ↓
Canonical glossary + maps
        ↓
Evidence verification + summary
```

## Workflow

1. Scan the current conversation.
   Extract domain nouns, verbs, actors, states, workflows, overloaded terms, synonym clusters, and phrases the user uses with strong intent. Capture how the user talks about the domain before checking whether the code agrees.

2. Read the existing `docs/UBIQUITOUS_LANGUAGE.md` if it exists.
   Merge forward instead of restarting blindly. Keep stable terms when possible. Move dropped or actively discouraged terms to the retired section only when conversation or code evidence supports the change.

3. Inspect the codebase, starting with domain-shaped folders.
   Prioritize searches in:
   - `models`
   - `entities`
   - `domain`
   - `use-cases` / `usecases`
   - `services`
   - `repositories`
   - `controllers`
   - `routes`
   - `schemas`
   - `views` / `screens` / `features`
   - `copy`, `i18n`, `locales`, or text resources when UI language matters
   - tests and fixtures when they reveal expected language or lifecycle examples

4. Trace primary model usages outward from the strongest domain nouns.
   Focus on where important models are created, mutated, read, persisted, exposed, and presented. Prefer major usages over weak or incidental references.

5. Build a terminology inventory.
   For each important term, capture:
   - canonical candidate
   - bounded context
   - definition in one sentence
   - aliases and synonyms found
   - code names found
   - UI labels or route names found
   - lifecycle states or enum values
   - commands/actions/events that mutate it
   - confidence level based on evidence

6. Identify terminology problems explicitly.
   Flag:
   - one word used for multiple concepts
   - multiple words used for the same concept
   - vague or overloaded names
   - technical wrappers posing as domain terms
   - UI language that drifts from backend or model language
   - route or screen names that imply a different domain concept than the model
   - enum/state names that hide important business meaning
   - actor names that blur permissions, ownership, or lifecycle responsibility

7. Propose canonical terms grouped by bounded context.
   For each important concept, pick one best term, define it in one sentence, list aliases to avoid, and tie the recommendation back to codebase evidence.

8. Map relationships, states, and domain events.
   Describe how the core terms relate, which actions or events drive state changes, and which lifecycle states matter. Use simple visual flows when useful.

9. Write or rewrite `docs/UBIQUITOUS_LANGUAGE.md`.
   Ensure a `docs` directory exists in the root of the project, creating it if needed. Use the exact output structure below. Preserve prior decisions when they still fit; move deprecated language to the retired section.

10. Return a short inline summary after writing the file.
    Include terminology clusters found, biggest ambiguities, strongest canonical recommendations, and whether codebase naming and domain language are aligned.

## Investigation Heuristics

### Start Points

- Start from model names; they usually reveal the strongest candidate nouns.
- Use use-case, service, and repository names to find verbs, actions, and ownership boundaries.
- Use routes, controllers, screens, and UI copy to detect public-facing terminology drift.
- Read enum definitions, state machines, reducers, workflow steps, and validation schemas for lifecycle vocabulary.
- Check tests and fixtures for realistic domain examples and expected terminology.

### Evidence Weighting

Use this evidence hierarchy when deciding whether a term is canonical:

| Evidence type | Weight | Why it matters |
| --- | --- | --- |
| Domain model/entity/value object | High | Usually represents core concepts. |
| Use case/command/event names | High | Reveals meaningful domain actions. |
| Service/repository methods | Medium-high | Shows operational language and lifecycle changes. |
| Routes/screens/UI copy | Medium | Shows language exposed to users or operators. |
| Schemas/DTOs/API payloads | Medium-low | Useful evidence, but can be transport-oriented. |
| Helpers/mappers/wrappers | Low | Often technical, not domain language. |
| Comments/TODOs/HACKs | Contextual | Useful for intent and known naming problems. |

### Drift Signals

Treat these as strong signals that the glossary needs a note or recommendation:

- A model has one name but the UI consistently uses another.
- A term means different things in different bounded contexts.
- A route, screen, or API endpoint uses a broad word such as `account`, `item`, `record`, `session`, or `status` without a domain qualifier.
- A state enum contains vague values such as `active`, `inactive`, `done`, `pending`, or `failed` without domain-specific explanation.
- A technical object such as `Payload`, `DTO`, `Response`, `Config`, or `Wrapper` is used as if it were a domain concept.

## Visual Documentation Rules

Use visual aids in markdown when they make the glossary easier to understand. Keep them text-based so the file remains portable.

### Context Map

Add a context map near the top when there are multiple bounded contexts:

```text
[Identity] User authenticates → owns → [Account]
[Billing] Customer subscribes → receives → [Invoice]
[Inventory] Product is allocated → into → [Order]
```

### Lifecycle Flow

Use lifecycle flows for terms with important states:

```text
OrderDraft → OrderPlaced → OrderFulfilled → OrderCancelled
```

### Relationship Bullets

Prefer precise relationship bullets:

- A **Customer** can place many **Orders**.
- An **Order** can produce zero or more **Invoices** until fulfillment is confirmed.
- An **Invoice** belongs to exactly one **Customer**.

### Naming Drift Notes

Use explicit callouts for confusing terms:

```md
> **Naming drift:** The UI says "Bill", but backend services use `Invoice`. Use **Invoice** as the canonical term and reserve "bill" only when quoting legacy UI copy.
```

## Writing Rules

- Keep definitions tight: one sentence that says what the thing is, not how the code implements it.
- Include only domain-relevant concepts.
- Define the same word separately when it means different things in different bounded contexts.
- Distinguish domain concepts from transport objects, technical wrappers, and UI helper types.
- Flag contested or misleading names directly and recommend better canonical terms.
- Rewrite the example dialogue so it resolves a real ambiguity or clarifies a real relationship found in the codebase.
- Use evidence status labels: `Confirmed`, `Likely`, `Conflicting`, `Missing evidence`, or `Retired`.
- Do not invent business meaning from file names alone. File names are leads, not proof.
- If the conversation and code disagree, document both and recommend the term that best supports domain clarity.

## Output Structure

Write `docs/UBIQUITOUS_LANGUAGE.md` with exactly this structure:

```md
# Ubiquitous Language

## Glossary Snapshot

| Area | Canonical terms | Key ambiguity | Alignment |
| --- | --- | --- | --- |
| Billing | **Customer**, **Order**, **Invoice** | "Account" overlaps with Identity | Partial alignment |

## Context Map

```text
[Context A] TermOne action → TermTwo
[Context B] Actor command → DomainEvent → State
```

## Bounded Context: [Context Name, e.g., Billing]

### Core Terms
| Term | Definition | Aliases to avoid | Evidence |
| --- | --- | --- | --- |
| **Order** | A customer's request to purchase one or more items. | Purchase, transaction | `Order`, `CreateOrder`, `orders/:id` |
| **Invoice** | A request for payment tied to fulfilled value. | Bill, payment request | `Invoice`, `InvoicingService` |

### Actors
| Term | Definition | Aliases to avoid | Evidence |
| --- | --- | --- | --- |
| **Customer** | A person or organization that places orders. | Client, buyer | `Customer`, `customerId` |

### Domain Events & Actions
| Action / Event | Definition | Triggers / State Change | Evidence |
| --- | --- | --- | --- |
| **FulfillOrder** | The act of successfully delivering the requested items. | Transitions Order to `Fulfilled`; generates `Invoice`. | `FulfillOrder`, `OrderService.fulfill()` |

### Lifecycle & States
```text
OrderDraft → OrderPlaced → OrderFulfilled → OrderCancelled
```

| State | Meaning | Entered by | Exited by / Terminal? |
| --- | --- | --- | --- |
| `OrderDraft` | The order is being prepared and has not been placed. | `CreateOrderDraft` | `PlaceOrder`; not terminal |

### Relationships
- An **Invoice** belongs to exactly one **Customer**.
- An **Order** can produce one or more **Invoices**.

### Naming Drift & Recommendations
| Issue | Recommendation | Rationale / Evidence | Status |
| --- | --- | --- | --- |
| UI uses "Bill" while backend uses `Invoice`. | Use **Invoice** as canonical. | `InvoicingService` owns payment request lifecycle. | Confirmed |

*(Repeat the Bounded Context block above for other contexts, e.g., Identity, Inventory, etc.)*

---

## Codebase Evidence

| Term | Context | Model / Type | Primary usages | UI / Route language | Notes | Status |
| --- | --- | --- | --- | --- | --- | --- |
| **Order** | Billing | `Order` | `CreateOrder`, `FulfillOrder`, `CancelOrder` | `/orders`, "Order details" | Canonical term is mostly consistent across layers. | Confirmed |
| **Account** | Multiple | `Account`, `UserAccount` | `LoginUser`, `AttachCustomerAccount` | `/account`, "Account settings" | Ambiguous across Auth and Billing contexts. | Conflicting |

## Synonym & Ambiguity Matrix

| Word / Phrase | Meanings found | Contexts | Recommendation | Evidence |
| --- | --- | --- | --- | --- |
| Account | Login identity; billing customer container | Identity, Billing | Qualify as **User Account** or **Customer Account**. | `UserAccount`, `customer.accountId` |

## Example Dialogue

> **Dev:** "In the Billing context, when a **Customer** places an **Order**, do we create the **Invoice** immediately?"
>
> **Domain expert:** "No. The **Invoice** is generated only after the **FulfillOrder** action is confirmed."
>
> **Dev:** "So an **Order** and an **Invoice** are not the same lifecycle concept?"
>
> **Domain expert:** "Exactly. The **Order** captures intent. The **Invoice** captures billable fulfillment."

## Flagged Ambiguities

- "account" was used to mean both **Customer** in Billing and **User** in Identity. These are distinct concepts across bounded contexts and should not share the same canonical name in discussions.

## Retired Terminology

| Legacy Term | Replaced By | Reason | Evidence |
| --- | --- | --- | --- |
| **Bill** | **Invoice** | "Bill" was used inconsistently in the UI. Standardized on Invoice to match the `InvoicingService`. | `InvoicingService`, legacy copy |
```

## Final Checks

Re-read the generated glossary before finishing.

- Ensure the file is saved strictly as `docs/UBIQUITOUS_LANGUAGE.md`.
- Ensure bounded contexts are explicit and defensible.
- Ensure the glossary snapshot gives readers a fast overview.
- Ensure the context map is present when there are multiple contexts.
- Ensure definitions are one sentence and domain-focused.
- Ensure the codebase evidence section only claims support that the search actually found.
- Ensure lifecycle/state sections appear only where states are real and supported by evidence.
- Ensure the example dialogue reflects a real ambiguity or relationship from this repository.
- Ensure flagged ambiguities are actionable, not vague observations.
- Ensure retired terminology contains only terms the team should stop using.
- Ensure no term is treated as canonical solely because it appears in a DTO, payload, mapper, helper, or API wrapper.
