# Glossary output template

Load for a new comprehensive document, or when an affected section needs a layout example. These rows are illustrative placeholders, not evidence about the repository. Replace them with supported findings and omit sections that do not apply. Preserve valid existing knowledge during scoped updates.

Write `docs/UBIQUITOUS_LANGUAGE.md` using the applicable sections below:

````md
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
````

## Final checks

Re-read the generated glossary before finishing.

- Ensure the file is saved strictly as `docs/UBIQUITOUS_LANGUAGE.md`.
- Ensure bounded contexts are explicit and defensible.
- Ensure the glossary snapshot gives readers a fast overview.
- Ensure the context map is present when there are multiple contexts.
- Ensure definitions are one sentence and domain-focused.
- Ensure the codebase evidence section only claims support that the search actually found.
- Ensure lifecycle/state sections appear only where states are real and supported by evidence.
- Include example dialogue only when it explains a real ambiguity or relationship from this repository.
- Ensure flagged ambiguities are actionable, not vague observations.
- Ensure retired terminology contains only terms the team should stop using.
- Ensure no term is treated as canonical solely because it appears in a DTO, payload, mapper, helper, or API wrapper.
