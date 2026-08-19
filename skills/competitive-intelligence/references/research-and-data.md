# Competitive Intelligence Research And Data Guide

## Search Plan

Run focused searches for the seller and each competitor. Prefer official product, pricing, changelog, docs, blog, press, and investor pages for facts. Use review sites and communities for sentiment, and label sentiment as directional unless it is backed by multiple sources.

Seller searches:

- `[company] product`
- `[company] pricing`
- `[company] news`
- `[company] changelog OR release notes OR product updates`
- `[company] vs [competitor]`

Competitor searches:

- `[competitor] product features`
- `[competitor] pricing`
- `[competitor] news`
- `[competitor] changelog OR release notes OR product updates`
- `[competitor] reviews G2 OR Capterra OR TrustRadius`
- `[competitor] alternatives`
- `[competitor] customers`
- `[competitor] careers`

Use exact dates for "recent" findings. Treat "last 90 days" relative to the current date in the runtime environment.

## Battlecard Data Shape

Create a JSON file shaped like this. Missing fields are allowed; use `unknown` for notable gaps.

```json
{
  "generated_at": "YYYY-MM-DD",
  "source_categories": ["Web", "Docs"],
  "your_company": {
    "name": "Acme",
    "website": "https://example.com",
    "product": "One-line product summary",
    "positioning": "How the company describes itself",
    "profile": {
      "target_market": "Enterprise teams",
      "pricing_model": "Per seat",
      "market_position": "Challenger"
    },
    "recent_releases": [
      {
        "date": "YYYY-MM-DD",
        "release": "Feature or product",
        "impact": "Why it matters",
        "source": "https://example.com/release"
      }
    ],
    "differentiators": [
      {
        "area": "Implementation speed",
        "advantage": "Deploys faster for multi-team rollouts",
        "proof_point": "Customer proof or sourced evidence"
      }
    ],
    "proof_points": ["Customer quote or metric"]
  },
  "competitors": [
    {
      "name": "Competitor",
      "website": "https://competitor.example",
      "profile": {
        "founded": "2019",
        "funding": "Series B, amount unknown",
        "employees": "500-1000",
        "target_market": "Mid-market",
        "pricing_model": "Usage-based",
        "market_position": "Leader"
      },
      "what_they_sell": "Product summary",
      "their_positioning": "Positioning summary",
      "recent_releases": [
        {
          "date": "YYYY-MM-DD",
          "release": "Launch",
          "impact": "Strategic meaning",
          "source": "https://competitor.example/blog"
        }
      ],
      "where_they_win": [
        {
          "area": "Category",
          "advantage": "Their strength",
          "how_to_handle": "Counter-positioning"
        }
      ],
      "where_you_win": [
        {
          "area": "Category",
          "advantage": "Your strength",
          "proof_point": "Evidence"
        }
      ],
      "pricing": {
        "model": "Per seat",
        "entry_price": "$X/month",
        "enterprise": "Custom",
        "hidden_costs": "Implementation, add-ons, support",
        "talk_track": "How to discuss pricing"
      },
      "talk_tracks": {
        "early_mention": "What to say when they appear early",
        "displacement": "What to say when replacing them",
        "late_addition": "What to say when they enter late"
      },
      "objections": [
        {
          "objection": "Customer objection",
          "response": "Sales response"
        }
      ],
      "landmines": [
        "Question that exposes a trade-off without attacking the competitor"
      ],
      "win_loss": {
        "win_rate": "unknown",
        "common_win_factors": "Pattern from CRM or field intel",
        "common_loss_factors": "Pattern from CRM or field intel"
      },
      "sources": [
        {
          "label": "Pricing page",
          "url": "https://competitor.example/pricing",
          "date": "YYYY-MM-DD"
        }
      ]
    }
  ],
  "matrix": [
    {
      "category": "Positioning",
      "criterion": "Primary buyer",
      "your_company": "Enterprise platform teams",
      "competitors": {
        "Competitor": "Departmental teams"
      },
      "winner": "tie",
      "detail": "Depends on buyer profile."
    }
  ],
  "quick_guides": [
    {
      "competitor": "Competitor",
      "when_you_win": "Use when the customer values speed and governance.",
      "when_they_win": "They may win when the customer needs a narrow point solution.",
      "watch_out": "Procurement may anchor on lower entry price."
    }
  ],
  "sources": [
    {
      "label": "Company release notes",
      "url": "https://example.com/changelog",
      "scope": "seller",
      "date": "YYYY-MM-DD"
    }
  ],
  "caveats": [
    "Competitor enterprise pricing was not publicly available."
  ]
}
```

## Synthesis Rules

- Include where they win, where you win, and how to handle each competitor strength.
- Translate features into buyer outcomes.
- Avoid unsourced absolutes such as "best", "only", or "always" unless directly supported.
- Do not fabricate CRM, docs, chat, or transcript intel. If connectors are unavailable, say so.
- Keep landmine questions neutral: ask about integration effort, migration risk, time-to-value, admin burden, hidden add-ons, governance, data export, implementation services, support tiers, roadmap maturity, and vendor viability.
- Include exact dates for release recency and source freshness.
