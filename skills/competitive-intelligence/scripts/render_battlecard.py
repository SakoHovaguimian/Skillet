#!/usr/bin/env python3
"""Render a self-contained competitive battlecard HTML file from JSON data."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from html import escape
from pathlib import Path
from typing import Any


def text(value: Any, default: str = "unknown") -> str:
    if value is None:
        return default
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    value = str(value).strip()
    return value if value else default


def e(value: Any, default: str = "unknown") -> str:
    return escape(text(value, default))


def slug(value: str) -> str:
    safe = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return safe or "item"


def list_items(items: list[Any], keys: tuple[str, ...] = ()) -> str:
    if not items:
        return '<p class="muted">No public data found.</p>'
    rendered: list[str] = []
    for item in items:
        if isinstance(item, dict):
            parts = []
            for key in keys or tuple(item.keys()):
                if key in item and item[key]:
                    label = key.replace("_", " ").title()
                    parts.append(f"<span><strong>{e(label)}:</strong> {e(item[key])}</span>")
            rendered.append(f"<li>{' '.join(parts) if parts else e(item)}</li>")
        else:
            rendered.append(f"<li>{e(item)}</li>")
    return f"<ul>{''.join(rendered)}</ul>"


def link(url: Any, label: Any | None = None) -> str:
    href = text(url, "")
    if not href:
        return e(label or "source")
    return f'<a href="{escape(href, quote=True)}" target="_blank" rel="noreferrer">{e(label or href)}</a>'


def render_sources(sources: list[dict[str, Any]]) -> str:
    if not sources:
        return '<p class="muted">No sources listed.</p>'
    rows = []
    for source in sources:
        rows.append(
            "<tr>"
            f"<td>{link(source.get('url'), source.get('label') or source.get('url'))}</td>"
            f"<td>{e(source.get('scope', ''))}</td>"
            f"<td>{e(source.get('date', ''))}</td>"
            "</tr>"
        )
    return (
        '<table class="compact"><thead><tr><th>Source</th><th>Scope</th><th>Date</th></tr></thead>'
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def render_matrix(data: dict[str, Any], competitor_names: list[str]) -> str:
    rows = []
    for row in data.get("matrix", []):
        winner = text(row.get("winner", "tie")).lower()
        cls = "you-win" if winner in {"you", "seller", "your_company"} else "they-win" if winner in [name.lower() for name in competitor_names] else "tie"
        competitor_cells = []
        competitor_values = row.get("competitors", {}) or {}
        for name in competitor_names:
            competitor_cells.append(f"<td>{e(competitor_values.get(name, 'unknown'))}</td>")
        rows.append(
            "<tr>"
            f"<td><span class=\"eyebrow\">{e(row.get('category', 'General'))}</span><strong>{e(row.get('criterion', 'Criterion'))}</strong><p>{e(row.get('detail', ''))}</p></td>"
            f"<td>{e(row.get('your_company', 'unknown'))}</td>"
            f"{''.join(competitor_cells)}"
            f"<td><span class=\"pill {cls}\">{e(row.get('winner', 'tie'))}</span></td>"
            "</tr>"
        )
    if not rows:
        colspan = 3 + len(competitor_names)
        return f'<table><tbody><tr><td colspan="{colspan}" class="muted">No matrix data provided.</td></tr></tbody></table>'
    headers = "".join(f"<th>{e(name)}</th>" for name in competitor_names)
    return (
        '<table class="comparison-matrix">'
        f"<thead><tr><th>Criterion</th><th>{e(data.get('your_company', {}).get('name', 'You'))}</th>{headers}<th>Winner</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def render_quick_guides(guides: list[dict[str, Any]]) -> str:
    if not guides:
        return '<p class="muted">No quick guides provided.</p>'
    cards = []
    for guide in guides:
        cards.append(
            '<article class="mini-card">'
            f"<h3>{e(guide.get('competitor', 'Competitor'))}</h3>"
            f"<p><strong>When you win:</strong> {e(guide.get('when_you_win', 'unknown'))}</p>"
            f"<p><strong>When they win:</strong> {e(guide.get('when_they_win', 'unknown'))}</p>"
            f"<p><strong>Watch out:</strong> {e(guide.get('watch_out', 'unknown'))}</p>"
            "</article>"
        )
    return f'<div class="win-loss-grid">{"".join(cards)}</div>'


def render_release_items(items: list[dict[str, Any]]) -> str:
    if not items:
        return '<p class="muted">No recent releases found.</p>'
    rendered = []
    for item in items:
        source = f" {link(item.get('source'), 'source')}" if item.get("source") else ""
        rendered.append(
            "<li>"
            f"<strong>{e(item.get('date', 'Date unknown'))}</strong> - {e(item.get('release', 'Release'))}"
            f"<p>{e(item.get('impact', ''))}{source}</p>"
            "</li>"
        )
    return f"<ul>{''.join(rendered)}</ul>"


def render_competitor(comp: dict[str, Any], your_name: str) -> str:
    profile = comp.get("profile", {}) or {}
    pricing = comp.get("pricing", {}) or {}
    talks = comp.get("talk_tracks", {}) or {}
    win_loss = comp.get("win_loss", {}) or {}
    return (
        '<div class="battlecard">'
        '<section class="panel profile">'
        f"<h2>{e(comp.get('name', 'Competitor'))}</h2>"
        f"<p class=\"lede\">{e(comp.get('what_they_sell', 'Product summary unavailable.'))}</p>"
        f"<p><strong>Positioning:</strong> {e(comp.get('their_positioning', 'unknown'))}</p>"
        '<div class="fact-grid">'
        f"<div><span>Website</span>{link(comp.get('website'), comp.get('website') or 'unknown')}</div>"
        f"<div><span>Founded</span>{e(profile.get('founded'))}</div>"
        f"<div><span>Funding</span>{e(profile.get('funding'))}</div>"
        f"<div><span>Employees</span>{e(profile.get('employees'))}</div>"
        f"<div><span>Target market</span>{e(profile.get('target_market'))}</div>"
        f"<div><span>Pricing model</span>{e(profile.get('pricing_model'))}</div>"
        f"<div><span>Market position</span>{e(profile.get('market_position'))}</div>"
        "</div></section>"
        '<section class="two-col">'
        '<details open><summary>Where They Win</summary>'
        f"{list_items(comp.get('where_they_win', []), ('area', 'advantage', 'how_to_handle'))}</details>"
        f'<details open><summary>Where {e(your_name)} Wins</summary>'
        f"{list_items(comp.get('where_you_win', []), ('area', 'advantage', 'proof_point'))}</details>"
        "</section>"
        '<section class="two-col">'
        '<details open><summary>Pricing Intelligence</summary>'
        f"<p><strong>Model:</strong> {e(pricing.get('model'))}</p>"
        f"<p><strong>Entry:</strong> {e(pricing.get('entry_price'))}</p>"
        f"<p><strong>Enterprise:</strong> {e(pricing.get('enterprise'))}</p>"
        f"<p><strong>Hidden costs:</strong> {e(pricing.get('hidden_costs'))}</p>"
        f"<p><strong>Talk track:</strong> {e(pricing.get('talk_track'))}</p>"
        "</details>"
        '<details open><summary>Recent Releases</summary>'
        f"{render_release_items(comp.get('recent_releases', []))}</details>"
        "</section>"
        '<section class="three-col">'
        f"<article><h3>Early Mention</h3><p>{e(talks.get('early_mention'))}</p></article>"
        f"<article><h3>Displacement</h3><p>{e(talks.get('displacement'))}</p></article>"
        f"<article><h3>Late Addition</h3><p>{e(talks.get('late_addition'))}</p></article>"
        "</section>"
        '<section class="two-col">'
        '<details open><summary>Objection Handling</summary>'
        f"{list_items(comp.get('objections', []), ('objection', 'response'))}</details>"
        '<details open><summary>Landmine Questions</summary>'
        f"{list_items(comp.get('landmines', []))}</details>"
        "</section>"
        '<section class="two-col">'
        '<details><summary>Win/Loss Signals</summary>'
        f"<p><strong>Win rate:</strong> {e(win_loss.get('win_rate'))}</p>"
        f"<p><strong>Common win factors:</strong> {e(win_loss.get('common_win_factors'))}</p>"
        f"<p><strong>Common loss factors:</strong> {e(win_loss.get('common_loss_factors'))}</p>"
        "</details>"
        '<details><summary>Sources</summary>'
        f"{render_sources(comp.get('sources', []))}</details>"
        "</section></div>"
    )


def render_html(data: dict[str, Any]) -> str:
    your = data.get("your_company", {}) or {}
    your_name = text(your.get("name"), "Your Company")
    competitors = data.get("competitors", []) or []
    competitor_names = [text(comp.get("name"), f"Competitor {idx + 1}") for idx, comp in enumerate(competitors)]
    generated_at = text(data.get("generated_at"), date.today().isoformat())
    source_categories = ", ".join(text(item) for item in data.get("source_categories", ["Web"]))
    tabs = ['<button class="tab active" data-tab="matrix">Comparison Matrix</button>', f'<button class="tab" data-tab="you">{e(your_name)}</button>']
    sections = []
    for comp, name in zip(competitors, competitor_names):
        tab_id = slug(name)
        tabs.append(f'<button class="tab" data-tab="{tab_id}">{e(name)}</button>')
        sections.append(f'<section id="{tab_id}" class="tab-content">{render_competitor(comp, your_name)}</section>')
    caveats = data.get("caveats", [])
    all_sources = data.get("sources", []) or []
    for comp in competitors:
        all_sources.extend(comp.get("sources", []) or [])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Battlecard: {e(your_name)} vs Competitors</title>
<style>
:root {{
  --bg-primary: #0a0d14;
  --bg-elevated: #0f131c;
  --bg-surface: #161b28;
  --bg-hover: #1e2536;
  --text-primary: #ffffff;
  --text-secondary: rgba(255,255,255,.72);
  --text-muted: rgba(255,255,255,.52);
  --accent: #3b82f6;
  --accent-hover: #2563eb;
  --you-win: #10b981;
  --they-win: #ef4444;
  --tie: #f59e0b;
  --border: rgba(255,255,255,.1);
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg-primary); color: var(--text-primary); font: 14px/1.55 Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; letter-spacing: 0; }}
a {{ color: #93c5fd; }}
header {{ padding: 32px clamp(18px, 4vw, 56px) 22px; border-bottom: 1px solid var(--border); background: linear-gradient(180deg, #101624 0%, var(--bg-primary) 100%); }}
h1 {{ margin: 0; font-size: clamp(28px, 4vw, 46px); line-height: 1.05; letter-spacing: 0; }}
h2 {{ margin: 0 0 14px; font-size: 22px; }}
h3 {{ margin: 0 0 8px; font-size: 16px; }}
p {{ color: var(--text-secondary); margin: 0 0 10px; }}
.meta {{ margin-top: 10px; color: var(--text-muted); }}
.tabs {{ position: sticky; top: 0; z-index: 5; display: flex; gap: 8px; overflow-x: auto; padding: 12px clamp(18px, 4vw, 56px); background: rgba(10,13,20,.92); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); }}
.tab {{ border: 1px solid var(--border); background: var(--bg-surface); color: var(--text-secondary); padding: 10px 14px; border-radius: 8px; cursor: pointer; white-space: nowrap; transition: .2s ease; }}
.tab:hover {{ background: var(--bg-hover); color: var(--text-primary); }}
.tab.active {{ background: var(--accent); border-color: var(--accent-hover); color: white; }}
main {{ padding: 24px clamp(18px, 4vw, 56px) 48px; }}
.tab-content {{ display: none; }}
.tab-content.active {{ display: block; }}
.panel, details, article.mini-card, .three-col article {{ background: var(--bg-elevated); border: 1px solid var(--border); border-radius: 12px; padding: 18px; box-shadow: 0 12px 30px rgba(0,0,0,.18); }}
.lede {{ max-width: 900px; font-size: 16px; color: rgba(255,255,255,.82); }}
.comparison-matrix, .compact {{ width: 100%; border-collapse: separate; border-spacing: 0; overflow: hidden; border: 1px solid var(--border); border-radius: 12px; background: var(--bg-elevated); }}
th, td {{ padding: 14px; border-bottom: 1px solid var(--border); border-right: 1px solid var(--border); vertical-align: top; min-width: 140px; }}
th {{ position: sticky; top: 58px; background: #111827; color: var(--text-primary); text-align: left; z-index: 2; }}
tr:last-child td {{ border-bottom: 0; }}
td:last-child, th:last-child {{ border-right: 0; }}
td strong {{ display: block; color: var(--text-primary); }}
.eyebrow {{ display: block; color: var(--text-muted); font-size: 12px; text-transform: uppercase; margin-bottom: 2px; }}
.pill {{ display: inline-flex; align-items: center; border-radius: 999px; padding: 4px 9px; font-size: 12px; font-weight: 700; }}
.you-win {{ background: rgba(16,185,129,.15); color: #6ee7b7; }}
.they-win {{ background: rgba(239,68,68,.15); color: #fca5a5; }}
.tie {{ background: rgba(245,158,11,.15); color: #fcd34d; }}
.win-loss-grid, .two-col, .three-col, .fact-grid {{ display: grid; gap: 14px; }}
.win-loss-grid {{ grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); margin-top: 18px; }}
.two-col {{ grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); margin-top: 14px; }}
.three-col {{ grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); margin-top: 14px; }}
.fact-grid {{ grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); margin-top: 16px; }}
.fact-grid div {{ padding: 12px; background: var(--bg-surface); border: 1px solid var(--border); border-radius: 8px; color: var(--text-secondary); overflow-wrap: anywhere; }}
.fact-grid span {{ display: block; color: var(--text-muted); font-size: 12px; text-transform: uppercase; margin-bottom: 4px; }}
summary {{ cursor: pointer; color: var(--text-primary); font-weight: 700; }}
ul {{ margin: 12px 0 0; padding-left: 18px; color: var(--text-secondary); }}
li {{ margin: 0 0 10px; }}
.muted {{ color: var(--text-muted); }}
.sources, .caveats {{ margin-top: 22px; }}
@media (max-width: 760px) {{
  main {{ padding-bottom: 28px; }}
  th {{ top: 54px; }}
  table {{ display: block; overflow-x: auto; }}
}}
</style>
</head>
<body>
<header>
  <h1>{e(your_name)} Competitive Battlecard</h1>
  <p class="meta">Generated: {e(generated_at)} | Competitors: {e(', '.join(competitor_names) or 'None')} | Sources: {e(source_categories)}</p>
</header>
<nav class="tabs">{''.join(tabs)}</nav>
<main>
  <section id="matrix" class="tab-content active">
    <h2>Head-to-Head Comparison</h2>
    {render_matrix(data, competitor_names)}
    <h2 style="margin-top:28px">Quick Win/Loss Guide</h2>
    {render_quick_guides(data.get('quick_guides', []))}
    <section class="caveats panel">
      <h2>Caveats</h2>
      {list_items(caveats)}
    </section>
    <section class="sources panel">
      <h2>Sources</h2>
      {render_sources(all_sources)}
    </section>
  </section>
  <section id="you" class="tab-content">
    <div class="battlecard">
      <section class="panel profile">
        <h2>{e(your_name)}</h2>
        <p class="lede">{e(your.get('product', 'Product summary unavailable.'))}</p>
        <p><strong>Positioning:</strong> {e(your.get('positioning'))}</p>
        <div class="fact-grid">
          <div><span>Website</span>{link(your.get('website'), your.get('website') or 'unknown')}</div>
          <div><span>Target market</span>{e((your.get('profile') or {}).get('target_market'))}</div>
          <div><span>Pricing model</span>{e((your.get('profile') or {}).get('pricing_model'))}</div>
          <div><span>Market position</span>{e((your.get('profile') or {}).get('market_position'))}</div>
        </div>
      </section>
      <section class="two-col">
        <details open><summary>Recent Releases</summary>{render_release_items(your.get('recent_releases', []))}</details>
        <details open><summary>Key Differentiators</summary>{list_items(your.get('differentiators', []), ('area', 'advantage', 'proof_point'))}</details>
      </section>
      <section class="panel" style="margin-top:14px">
        <h2>Proof Points</h2>
        {list_items(your.get('proof_points', []))}
      </section>
    </div>
  </section>
  {''.join(sections)}
</main>
<script>
document.querySelectorAll('.tab').forEach(button => {{
  button.addEventListener('click', () => {{
    const id = button.dataset.tab;
    document.querySelectorAll('.tab').forEach(tab => tab.classList.toggle('active', tab === button));
    document.querySelectorAll('.tab-content').forEach(section => section.classList.toggle('active', section.id === id));
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
  }});
}});
</script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Render an interactive competitive battlecard HTML artifact.")
    parser.add_argument("--input", required=True, type=Path, help="Path to battlecard JSON data.")
    parser.add_argument("--output", required=True, type=Path, help="Path for the generated HTML file.")
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    if "your_company" not in data:
        raise SystemExit("Input JSON must include 'your_company'.")
    if "competitors" not in data:
        raise SystemExit("Input JSON must include 'competitors'.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_html(data), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
