# Business logic output template

Load for a new comprehensive document, or when an affected section needs a layout example. These rows are illustrative placeholders, not evidence about the repository. Replace them with supported findings and omit sections that do not apply. Preserve valid existing knowledge during scoped updates.

Write `docs/UBIQUITOUS_BUSINESS_LOGIC.md` using the applicable sections below:

````md
# Ubiquitous Business Logic

## How to Read This Document

This document captures business behavior as implemented in code, not just intended product behavior.

| Label | Meaning |
| --- | --- |
| Confirmed | Directly verified in code. |
| Partially confirmed | Some evidence found, but the full path is incomplete. |
| Contradicted | Existing docs or conversation claims conflict with current implementation. |
| Needs verification | Important claim exists, but code evidence was not found. |
| Retired | Evidence shows the system no longer enforces this logic. |

## System / Context Map

```text
[Add a compact map of the relevant bounded contexts, flows, routes, analytics, and integrations.]
```

## Bounded Context: [Context Name, e.g., Billing]

### Quick Mental Model

```text
[Summarize the context in 3-8 lines: inputs -> decisions -> outputs -> analytics/deeplinks if applicable.]
```

### Core Business Rules

| Rule | Description & Rationale | Enforced In | Status |
| --- | --- | --- | --- |
| **Proration on Downgrade** | When a user downgrades mid-cycle, the remaining balance is credited to their account, not refunded to their card. *Rationale: Reduces transaction fees and prevents refund abuse.* | `SubscriptionService.downgrade()` | Confirmed |
| **Minimum Charge** | Invoices under $0.50 are deferred to the next billing cycle. *Rationale: Stripe minimum processing fees.* | `InvoiceGenerator`, `Constants.MIN_CHARGE` | Confirmed |

### Rule Flow / Decision Points

| Flow Step | Decision / Branch | Outcome | Evidence |
| --- | --- | --- | --- |
| Downgrade request | User is mid-cycle | Credit remaining balance to account | `SubscriptionService.downgrade()` |
| Invoice generation | Invoice total is below minimum charge | Defer invoice to next billing cycle | `InvoiceGenerator`, `Constants.MIN_CHARGE` |

### Edge Cases & Oddities

| Oddity | Description & Rationale | Location / Workaround | Status |
| --- | --- | --- | --- |
| **Legacy Grandfathering** | Users created before Jan 1, 2022, bypass the `max_projects` limit. *Rationale: Promised unlimited projects in early beta.* | `PlanValidator.canCreateProject()` | Confirmed |
| **The "Acme Corp" Hack** | If `tenantId == 'acme-123'`, skip email verification. *Rationale: Enterprise client has strict firewall blocking our verification emails.* | `AuthService.register()` | Confirmed |

### Domain Constants & Magic Numbers

| Constant / Value | Meaning | Rationale | Evidence | Status |
| --- | --- | --- | --- | --- |
| `MAX_RETRY_ATTEMPTS = 3` | Number of retries before lockout. | Upstream API locks accounts after 4 failures. | `AuthConstants.MAX_RETRY_ATTEMPTS` | Confirmed |
| `DEFAULT_GRACE_PERIOD_DAYS = 7` | Days a user has to update an expired card before losing access. | Standard billing grace period. | `BillingConfig.DEFAULT_GRACE_PERIOD_DAYS` | Confirmed |

### Deeplinks & Routes

| Deeplink / Route | Destination Screen | Required Params | Optional Params | Guards / Fallbacks | Analytics | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `app://billing/invoice/:invoiceId` | Invoice Detail | `invoiceId` | `source` | Requires authenticated user; unauthorized users are redirected to login. | `deeplink_opened`, `invoice_viewed` | `linking.ts`, `InvoiceScreen` | Confirmed |

### Analytics Instrumentation

#### Screen Events

| Event | Screen / Source | Required Params | Optional Params | Fires When | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `billing_invoice_screen_viewed` | Invoice Detail | `invoice_id` | `source`, `deeplink` | Invoice screen mounts after invoice load succeeds. | `InvoiceScreen.trackView()` | Confirmed |

#### Error Events

| Event | Error / Failure State | Required Params | Optional Params | Fires When | User-Facing Outcome | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `billing_invoice_load_failed` | Invoice lookup fails | `invoice_id`, `error_code` | `source` | API returns not found or permission denied. | Shows invoice unavailable state. | `InvoiceScreen.loadInvoice()` | Confirmed |

#### Track Events

| Event | User / System Action | Required Params | Optional Params | Fires When | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `billing_downgrade_submitted` | User submits downgrade | `plan_id`, `account_id` | `coupon_id` | Downgrade CTA is submitted. | `BillingAnalytics.trackDowngradeSubmitted()` | Confirmed |

*(Repeat the Bounded Context block above for other contexts, e.g., Identity, Inventory, Scheduling, Eligibility, Navigation, Analytics, etc.)*

---

## Cross-Cutting Deeplink Inventory

| Deeplink / Route | Context | Destination | Required Params | Optional Params | Guards / Fallbacks | Related Events | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `app://billing/invoice/:invoiceId` | Billing | Invoice Detail | `invoiceId` | `source` | Login redirect when unauthenticated. | `deeplink_opened`, `invoice_viewed` | `linking.ts`, `InvoiceScreen` | Confirmed |

## Cross-Cutting Analytics Inventory

### Screen Events

| Event | Context | Screen / Source | Required Params | Optional Params | Fires When | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `billing_invoice_screen_viewed` | Billing | Invoice Detail | `invoice_id` | `source`, `deeplink` | Invoice screen mounts after invoice load succeeds. | `InvoiceScreen.trackView()` | Confirmed |

### Error Events

| Event | Context | Error / Failure State | Required Params | Optional Params | Fires When | User-Facing Outcome | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `billing_invoice_load_failed` | Billing | Invoice lookup fails | `invoice_id`, `error_code` | `source` | API returns not found or permission denied. | Shows invoice unavailable state. | `InvoiceScreen.loadInvoice()` | Confirmed |

### Track Events

| Event | Context | User / System Action | Required Params | Optional Params | Fires When | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `billing_downgrade_submitted` | Billing | User submits downgrade | `plan_id`, `account_id` | `coupon_id` | Downgrade CTA is submitted. | `BillingAnalytics.trackDowngradeSubmitted()` | Confirmed |

## Codebase Evidence & Verification

| Rule / Concept | Context | Primary Implementation | Supporting Evidence | Status |
| --- | --- | --- | --- | --- |
| Proration on Downgrade | Billing | `services/subscription.ts` | `SubscriptionService.downgrade()` credits account balance. | Confirmed |
| Legacy Grandfathering | Identity | `utils/legacy-checks.ts` | Hardcoded date `2022-01-01` found. | Confirmed |

## Discrepancies & Open Questions

| Claim / Expectation | What Code Does | Evidence | Recommended Follow-Up |
| --- | --- | --- | --- |
| [Conversation or existing doc claim] | [Actual implementation] | `[file/function]` | [Clarify, fix code, or update product expectation] |

## Retired Logic

| Legacy Rule | Replaced By / Removed Because | Evidence | Status |
| --- | --- | --- | --- |
| **Manual Invoice Approval** | Removed. All invoices are now auto-charged. | Code was stripped from `InvoiceService` in PR #402. | Retired |
````

## Final checks

Re-read the generated document before finishing.

- Ensure the file is saved strictly as `docs/UBIQUITOUS_BUSINESS_LOGIC.md`.
- Ensure generic technical details are omitted in favor of actual domain constraints.
- Ensure the `System / Context Map` and `Quick Mental Model` sections make the document easier to understand without simplifying away important details.
- Include deeplink and analytics tables when applicable; otherwise state their absence once in the coverage summary.
- Ensure deeplinks include destination, required params, optional params, guards/fallbacks, related analytics, evidence, and status.
- Ensure analytics are split into `Screen Events`, `Error Events`, and `Track Events`, with required and optional params documented separately.
- Ensure the `Edge Cases & Oddities` section is brutally honest about hacks and workarounds found in the code.
- Ensure the retired section contains only rules the system actively no longer enforces.
- Ensure every non-obvious claim has code evidence or is explicitly marked as needing verification.
