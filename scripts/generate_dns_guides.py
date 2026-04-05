#!/usr/bin/env python3
"""Generate dns/[slug]/index.html guides — HowTo + FAQPage + BreadcrumbList."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DNS = ROOT / "dns"

STYLE_AND_SHELL = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__TITLE__ — DomainPreflight</title>
  <meta name="description" content="__META__">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="__CANON__">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script defer src="https://cloud.umami.is/script.js" data-website-id="27fc19d2-1ff5-4478-946a-b96cc7d5daf8"></script>
__LDJSON__
  <style>
    :root { --bg: #0B0D14; --surface: #10131f; --bg3: #161924; --border: #1e2236; --purple: #6c63ff; --text: #e2e4f0; --text2: #8a8fb5; }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'JetBrains Mono', monospace; background: var(--bg); color: var(--text); min-height: 100vh; line-height: 1.6; }
    header { position: sticky; top: 0; z-index: 100; background: rgba(11, 13, 20, 0.7); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); padding: 0.75rem 1.5rem; }
    .header-inner { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem; }
    .logo { display: flex; align-items: center; gap: 0.5rem; font-weight: 600; font-size: 1rem; }
    .logo a { color: var(--purple); text-decoration: none; }
    .pill { font-size: 0.65rem; padding: 0.2rem 0.5rem; border-radius: 999px; background: var(--bg3); border: 1px solid var(--border); margin-left: 0.5rem; color: var(--text2); }
    nav { display: flex; gap: 0.85rem; align-items: center; flex-wrap: wrap; }
    nav a { color: var(--text2); text-decoration: none; font-size: 0.78rem; }
    nav a:hover { color: var(--text); }
    main { max-width: 820px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }
    .breadcrumb { font-size: 0.8rem; color: var(--text2); margin-bottom: 1.25rem; line-height: 1.5; }
    .breadcrumb a { color: var(--purple); text-decoration: none; }
    .breadcrumb a:hover { text-decoration: underline; }
    .hero-label { font-size: 0.7rem; letter-spacing: 0.15em; font-weight: 600; text-transform: uppercase; color: var(--purple); margin-bottom: 0.5rem; }
    h1 { font-size: clamp(1.35rem, 3.5vw, 1.9rem); font-weight: 600; margin-bottom: 1rem; line-height: 1.3; }
    .subtitle { color: var(--text2); font-size: 0.95rem; margin-bottom: 2rem; }
    article h2 { font-size: 1.05rem; font-weight: 600; margin: 2rem 0 0.75rem; color: var(--text); }
    article p, article li { color: var(--text2); font-size: 0.9rem; margin-bottom: 0.75rem; }
    article ul { margin: 0.5rem 0 1rem 1.25rem; }
    .dns-block { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 1rem 1.15rem; font-size: 0.8rem; line-height: 1.55; overflow-x: auto; white-space: pre-wrap; word-break: break-word; color: var(--text); margin: 0.75rem 0 1rem; }
    .howto-step { margin-bottom: 1.35rem; padding: 0.85rem 0 0.85rem 1rem; border-left: 3px solid var(--purple); scroll-margin-top: 5rem; }
    .howto-step strong { color: var(--text); display: block; margin-bottom: 0.35rem; font-size: 0.9rem; }
    .tool-cta { margin: 2rem 0; padding: 1.25rem 1.5rem; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; border-left: 3px solid var(--purple); }
    .tool-cta p { color: var(--text); margin-bottom: 0.5rem !important; }
    .tool-cta a { color: var(--purple); font-weight: 600; text-decoration: none; }
    .tool-cta a:hover { text-decoration: underline; }
    .faq-section h3 { font-size: 0.95rem; font-weight: 600; color: var(--text); margin: 1.5rem 0 0.4rem; }
    .faq-section p { margin-bottom: 0.5rem; }
    .glossary-links { margin: 1.5rem 0; padding: 1rem 1.15rem; background: var(--surface); border: 1px solid var(--border); border-radius: 10px; font-size: 0.85rem; color: var(--text2); }
    .glossary-links a { color: var(--purple); text-decoration: none; }
    .glossary-links a:hover { text-decoration: underline; }
    .internal-links { margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border); font-size: 0.88rem; color: var(--text2); }
    .internal-links a { color: var(--purple); text-decoration: none; }
    .internal-links a:hover { text-decoration: underline; }
    footer { border-top: 1px solid var(--border); background: var(--surface); }
    .footer-inner { max-width: 1200px; margin: 0 auto; padding: 1.25rem 1.5rem; }
    .footer-disclaimer { color: var(--text2); font-size: 0.75rem; line-height: 1.5; margin-bottom: 1rem; }
    .footer-bar { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1rem; padding: 1rem 1.5rem; border-top: 1px solid var(--border); font-size: 0.8rem; color: var(--text2); max-width: 1200px; margin: 0 auto; }
    .footer-bar a { color: var(--text2); text-decoration: none; }
    .footer-bar a:hover { color: var(--text); }
  </style>
  <link rel="icon" type="image/png" href="/favicon.png">
</head>
<body>
  <header>
    <div class="header-inner">
      <div class="logo"><a href="/">DomainPreflight.</a><span class="pill">BETA</span></div>
      <nav>
        <a href="/">DNS Preflight</a>
        <a href="/email/">Email</a>
        <a href="/whois/">WHOIS</a>
        <a href="/dangling/">Dangling Records</a>
        <a href="/typosquat/">Typosquat</a>
        <a href="/propagation/">Propagation</a>
        <a href="/dmarc/">DMARC Report</a>
        <a href="/glossary/">Glossary</a>
        <a href="/dns/">DNS Records</a>
      </nav>
    </div>
  </header>
  <main>
__BREADCRUMB__
    <article>
      <p class="hero-label">__HERO__</p>
      <h1>__H1__</h1>
      <p class="subtitle">__SUB__</p>
__ARTICLE__
    </article>
  </main>
  <footer>
    <div class="footer-inner"><p class="footer-disclaimer">This is a free sanity check — not legal or production advice. Verify DNS and mail in your own stack before you change anything.</p></div>
    <div class="footer-bar">
      <div><span>DomainPreflight by MetricLogic ·</span> <a href="https://configclarity.dev" target="_blank" rel="noopener">ConfigClarity</a> <span>·</span> <a href="https://domainpreflight.dev" target="_blank" rel="noopener">DomainPreflight</a> <span>·</span> <a href="https://packagefix.dev" target="_blank" rel="noopener">PackageFix</a> <span>·</span> <a href="/glossary/">Glossary</a></div>
      <div><a href="https://github.com/metriclogic26/domain-preflight" target="_blank" rel="noopener">Star on GitHub</a> <span> · </span> <span>MIT Licensed</span> <span> · </span> <a href="https://github.com/metriclogic26/domain-preflight/issues/new" target="_blank" rel="noopener">Report issue →</a></div>
    </div>
  </footer>
</body>
</html>
"""


def faq_section(faqs: list[tuple[str, str]]) -> str:
    lines = ['      <section class="faq-section" aria-label="FAQ">', "        <h2>FAQ</h2>"]
    for q, a in faqs:
        lines.append(f"        <h3>{q}</h3>")
        lines.append(f"        <p>{a}</p>")
    lines.append("      </section>")
    return "\n".join(lines)


def howto_steps_html(step_texts: list[str]) -> str:
    out = ['      <h2>Step by step</h2>']
    for i, t in enumerate(step_texts, start=1):
        out.append(
            f'      <div class="howto-step" id="step{i}"><strong>Step {i}</strong> {t}</div>'
        )
    return "\n".join(out)


def build_ldjson(
    canonical: str,
    howto_name: str,
    howto_desc: str,
    step_names: list[str],
    step_texts: list[str],
    faqs: list[tuple[str, str]],
    breadcrumb_items: list[dict],
) -> str:
    steps = []
    for i, (sname, stext) in enumerate(zip(step_names, step_texts), start=1):
        steps.append(
            {
                "@type": "HowToStep",
                "position": i,
                "name": sname,
                "url": f"{canonical}#step{i}",
                "text": f"Step {i} {stext}",
            }
        )
    howto = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": howto_name,
        "description": howto_desc,
        "estimatedCost": {"@type": "MonetaryAmount", "currency": "USD", "value": "0"},
        "supply": {"@type": "HowToSupply", "name": "DNS access at your registrar or DNS host"},
        "tool": {"@type": "HowToTool", "name": "DomainPreflight", "url": "https://domainpreflight.dev/"},
        "step": steps,
    }
    faqpage = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": breadcrumb_items}
    parts = [
        '  <script type="application/ld+json">\n  '
        + json.dumps(howto, ensure_ascii=False, separators=(",", ":"))
        + "\n  </script>",
        '  <script type="application/ld+json">\n  '
        + json.dumps(faqpage, ensure_ascii=False, separators=(",", ":"))
        + "\n  </script>",
        '  <script type="application/ld+json">\n  '
        + json.dumps(crumbs, ensure_ascii=False, separators=(",", ":"))
        + "\n  </script>",
    ]
    return "\n".join(parts)


def breadcrumb_nav(segments: list[tuple[str, str | None]]) -> str:
    """(label, href) — last href None = current page text only."""
    parts = ['    <nav class="breadcrumb" aria-label="Breadcrumb">']
    bits = []
    for i, (label, href) in enumerate(segments):
        if href:
            bits.append(f'<a href="{href}">{label}</a>')
        else:
            bits.append(label)
    parts.append(' <span aria-hidden="true">›</span> '.join(bits))
    parts.append("</nav>")
    return "\n".join(parts)


def breadcrumb_schema(canonical: str, trail: list[tuple[str, str]]) -> list[dict]:
    """trail: (name, url) for each level including current — last uses canonical."""
    out = []
    for i, (name, url) in enumerate(trail, start=1):
        out.append({"@type": "ListItem", "position": i, "name": name, "item": url})
    out[-1]["item"] = canonical
    return out


def emit(
    rel: str,
    title: str,
    meta: str,
    h1: str,
    subtitle: str,
    hero: str,
    bc_nav_segments: list[tuple[str, str | None]],
    bc_schema_trail: list[tuple[str, str]],
    howto_name: str,
    howto_desc: str,
    step_names: list[str],
    step_texts: list[str],
    faqs: list[tuple[str, str]],
    article: str,
) -> None:
    canonical = f"https://domainpreflight.dev/dns/{rel}/"
    ld = build_ldjson(
        canonical,
        howto_name,
        howto_desc,
        step_names,
        step_texts,
        faqs,
        breadcrumb_schema(canonical, bc_schema_trail),
    )
    inner_steps = howto_steps_html(step_texts)

    full_article = article + "\n" + inner_steps + "\n" + faq_section(faqs) + """
      <div class="internal-links">
        <p><a href="/dns/">← All DNS record guides</a></p>
        <p><a href="https://domainpreflight.dev/">Open DomainPreflight →</a></p>
      </div>"""

    html = STYLE_AND_SHELL.replace("__TITLE__", title)
    html = html.replace("__META__", meta)
    html = html.replace("__CANON__", canonical)
    html = html.replace("__LDJSON__", ld)
    html = html.replace("__BREADCRUMB__", breadcrumb_nav(bc_nav_segments))
    html = html.replace("__HERO__", hero)
    html = html.replace("__H1__", h1)
    html = html.replace("__SUB__", subtitle)
    html = html.replace("__ARTICLE__", full_article)

    out = DNS / rel / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("Wrote", out.relative_to(ROOT))


def main() -> None:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from dns_pages_data import PAGES  # noqa: PLC0415

    for page in PAGES:
        emit(**page)


if __name__ == "__main__":
    main()
