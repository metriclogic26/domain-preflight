"""Shared nav, footer, and styles for static doc pages."""
from __future__ import annotations

import json
from html import escape

HOME = "https://domainpreflight.dev/"

NAV_LINKS = """
        <a href="/">DNS Preflight</a>
        <a href="/email/">Email</a>
        <a href="/whois/">WHOIS</a>
        <a href="/dangling/">Dangling Records</a>
        <a href="/typosquat/">Typosquat</a>
        <a href="/propagation/">Propagation</a>
        <a href="/dmarc/">DMARC Report</a>
        <a href="/glossary/">Glossary</a>
        <a href="/dns/">DNS Records</a>
        <a href="/blog/">Blog</a>
        <a href="/learn/">Learn</a>
"""

FOOTER_INNER = """
    <div class="footer-inner"><p class="footer-disclaimer">This is a free sanity check — not legal or production advice. Verify DNS and mail in your own stack before you change anything.</p></div>
    <div class="footer-bar">
      <div><span>DomainPreflight by MetricLogic ·</span> <a href="https://configclarity.dev" target="_blank" rel="noopener">ConfigClarity</a> <span>·</span> <a href="https://domainpreflight.dev" target="_blank" rel="noopener">DomainPreflight</a> <span>·</span> <a href="https://packagefix.dev" target="_blank" rel="noopener">PackageFix</a> <span>·</span> <a href="/glossary/">Glossary</a></div>
      <div><a href="https://github.com/metriclogic26/domain-preflight" target="_blank" rel="noopener">Star on GitHub</a> <span> · </span> <span>MIT Licensed</span> <span> · </span> <a href="https://github.com/metriclogic26/domain-preflight/issues/new" target="_blank" rel="noopener">Report issue →</a></div>
    </div>
"""

DOC_STYLES = """
    :root { --bg: #0B0D14; --surface: #10131f; --bg3: #161924; --border: #1e2236; --purple: #6c63ff; --text: #e2e4f0; --text2: #8a8fb5; --warn: #f0a030; }
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
    main { max-width: 760px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }
    .breadcrumb { font-size: 0.8rem; color: var(--text2); margin-bottom: 1.25rem; line-height: 1.5; }
    .breadcrumb a { color: var(--purple); text-decoration: none; }
    .breadcrumb a:hover { text-decoration: underline; }
    .hero-label { font-size: 0.7rem; letter-spacing: 0.15em; font-weight: 600; text-transform: uppercase; color: var(--purple); margin-bottom: 0.5rem; }
    h1 { font-size: clamp(1.25rem, 3.2vw, 1.75rem); font-weight: 600; margin-bottom: 0.75rem; line-height: 1.3; }
    .lead { color: var(--text2); font-size: 0.92rem; margin-bottom: 1.25rem; }
    article h2 { font-size: 1.05rem; font-weight: 600; margin: 1.75rem 0 0.65rem; color: var(--text); }
    article p, article li { color: var(--text2); font-size: 0.9rem; margin-bottom: 0.75rem; }
    .gotcha { margin: 1rem 0 1.25rem; padding: 1rem 1.15rem; background: rgba(240, 160, 48, 0.08); border: 1px solid rgba(240, 160, 48, 0.35); border-radius: 10px; font-size: 0.88rem; color: var(--text); }
    .gotcha strong { color: var(--warn); }
    .dns-block, pre.code-block { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 1rem 1.15rem; font-size: 0.78rem; line-height: 1.55; overflow-x: auto; white-space: pre-wrap; word-break: break-word; color: var(--text); margin: 0.65rem 0 1rem; }
    .howto-step { margin-bottom: 1.25rem; padding: 0.75rem 0 0.75rem 1rem; border-left: 3px solid var(--purple); scroll-margin-top: 5rem; }
    .howto-step strong { color: var(--text); display: block; margin-bottom: 0.35rem; font-size: 0.88rem; }
    .tool-cta { margin: 1.75rem 0; padding: 1.15rem 1.35rem; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; border-left: 3px solid var(--purple); }
    .tool-cta p { color: var(--text); margin-bottom: 0.45rem !important; font-size: 0.9rem; }
    .tool-cta a { color: var(--purple); font-weight: 600; text-decoration: none; }
    .tool-cta a:hover { text-decoration: underline; }
    .faq-section h2 { font-size: 1.05rem; margin-top: 2rem; }
    .faq-section h3 { font-size: 0.95rem; font-weight: 600; color: var(--text); margin: 1.35rem 0 0.4rem; }
    .faq-section p { margin-bottom: 0.5rem; color: var(--text2); font-size: 0.9rem; }
    .internal-links { margin-top: 1.75rem; padding-top: 1.25rem; border-top: 1px solid var(--border); font-size: 0.86rem; }
    .internal-links a { color: var(--purple); text-decoration: none; }
    .hub-card { display: block; padding: 1rem 1.15rem; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; text-decoration: none; color: inherit; margin-bottom: 0.65rem; transition: border-color 0.2s; }
    .hub-card:hover { border-color: var(--purple); }
    .hub-card-title { font-weight: 600; color: var(--text); font-size: 0.92rem; }
    .hub-card-desc { font-size: 0.78rem; color: var(--text2); margin-top: 0.35rem; }
    footer { border-top: 1px solid var(--border); background: var(--surface); }
"""


def json_ld_script(obj: dict) -> str:
    return (
        '  <script type="application/ld+json">\n  '
        + json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
        + "\n  </script>"
    )


def howto_schema(
    canonical: str,
    name: str,
    description: str,
    step_names: list[str],
    step_texts: list[str],
) -> dict:
    steps = []
    for i, (sn, st) in enumerate(zip(step_names, step_texts, strict=True), start=1):
        steps.append(
            {
                "@type": "HowToStep",
                "position": i,
                "name": sn,
                "url": f"{canonical}#step{i}",
                "text": f"Step {i} {st}",
            }
        )
    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": name,
        "description": description,
        "estimatedCost": {"@type": "MonetaryAmount", "currency": "USD", "value": "0"},
        "supply": {"@type": "HowToSupply", "name": "DNS admin access"},
        "tool": {"@type": "HowToTool", "name": "DomainPreflight", "url": "https://domainpreflight.dev/"},
        "step": steps,
    }


def faq_schema(questions: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in questions
        ],
    }


def breadcrumb_schema(items: list[tuple[str, str]]) -> dict:
    """items: (name, url) — last url should be canonical of current page."""
    out = []
    for i, (name, url) in enumerate(items, start=1):
        out.append({"@type": "ListItem", "position": i, "name": name, "item": url})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": out}


def article_schema(
    headline: str,
    description: str,
    canonical: str,
    date_published: str = "2026-03-19",
) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": description,
        "datePublished": date_published,
        "dateModified": date_published,
        "author": {"@type": "Organization", "name": "MetricLogic"},
        "publisher": {
            "@type": "Organization",
            "name": "DomainPreflight",
            "url": "https://domainpreflight.dev/",
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
    }


def defined_term_schema(name: str, description: str, canonical: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "name": name,
        "description": description,
        "inDefinedTermSet": "https://domainpreflight.dev/glossary/",
        "url": canonical,
    }


def howto_steps_html(step_texts: list[str]) -> str:
    lines = ['      <h2>Step by step</h2>']
    for i, t in enumerate(step_texts, start=1):
        lines.append(
            f'      <div class="howto-step" id="step{i}"><strong>Step {i}</strong> {t}</div>'
        )
    return "\n".join(lines)


def faq_section_html(faqs: list[tuple[str, str]]) -> str:
    lines = ['      <section class="faq-section" aria-label="FAQ">', '        <h2>FAQ</h2>']
    for q, a in faqs:
        lines.append(f"        <h3>{escape(q)}</h3>")
        lines.append(f"        <p>{escape(a)}</p>")
    lines.append("      </section>")
    return "\n".join(lines)
