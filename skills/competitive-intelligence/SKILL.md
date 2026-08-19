---
name: competitive-intelligence
description: Research companies and competitors to create sales-ready competitive intelligence battlecards. Use when Codex is asked to compare a seller's company against competitors, build or refresh a competitive battlecard, prepare competitor talk tracks, research pricing/features/releases/reviews, generate landmine questions, synthesize win/loss positioning, or produce an interactive self-contained HTML comparison artifact for sales deals.
disable-model-invocation: true
---

# Competitive Intelligence

## Workflow

Create an evidence-backed, sales-usable battlecard. Browse the web unless the user explicitly forbids it, because pricing, positioning, releases, reviews, and news change frequently.

1. Gather context if missing:
   - Seller company and one-line product/service.
   - One to five competitors.
   - Optional focus competitor, deal context, heard objections, customer pain points, and preferred output folder.
   - If prior context is available, confirm it briefly before reusing it.
2. Research the seller company:
   - Product/offering, pricing, positioning, target market.
   - News, changelog, release notes, product updates, and launch posts from the last 90 days.
   - Existing "[seller] vs [competitor]" pages and credible customer proof.
3. Research each competitor:
   - Product features, pricing, packaging, positioning, target customers, customer logos.
   - News and releases from the last 90 days.
   - Reviews from sources such as G2, Capterra, TrustRadius, app stores, forums, and communities.
   - Hiring/careers signals that imply product or go-to-market investment areas.
4. Pull connected sources when available and authorized:
   - CRM: closed-won/lost deal patterns, competitor field history, win-rate signals.
   - Docs: existing battlecards, competitive playbooks, comparison docs.
   - Chat: field intel and recent mentions.
   - Transcripts: customer objections and competitor mentions.
5. Synthesize:
   - Be candid about where competitors win.
   - Prefer outcome-based differentiation over feature laundry lists.
   - Use landmine questions that reveal risk without badmouthing.
   - Mark unsupported claims as "unknown" or "not publicly found".
6. Build the HTML artifact using `scripts/render_battlecard.py`.

## Research Notes

Read `references/research-and-data.md` when planning searches, structuring the data JSON, or deciding what belongs in the battlecard.

For each important claim, preserve source URLs in the data. In the final user response, summarize sources used rather than dumping long source lists. The HTML should include a Sources tab or source section.

## Renderer

Use the bundled renderer after research and synthesis:

```bash
python3 <skill-directory>/scripts/render_battlecard.py \
  --input /path/to/battlecard-data.json \
  --output /path/to/Company-battlecard-YYYY-MM-DD.html
```

Resolve `<skill-directory>` from the location of this `SKILL.md` at runtime. Do
not assume the skill is installed under a particular agent home directory.

The JSON schema is flexible but should follow the structure in `references/research-and-data.md`. The renderer escapes content, creates clickable competitor tabs, builds an overview matrix, and emits a self-contained dark-theme HTML file.

## Delivery

After creating the artifact, respond with:

- A link to the HTML file.
- Seller company and competitors analyzed.
- Data source categories used: Web, CRM, Docs, Chat, Transcripts.
- Any major caveats such as missing pricing, stale release pages, or unavailable connectors.
- Practical usage notes: before-call review, live landmine questions, and post-win/loss updates.

Recommend refreshing monthly, before major deals, and after competitor announcements.
