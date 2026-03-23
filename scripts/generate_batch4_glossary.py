#!/usr/bin/env python3
"""Generate batch 4 glossary term pages + patch glossary index."""
from __future__ import annotations

import json
import sys
from html import escape as html_escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch4_glossary_data import TERMS  # noqa: E402
from site_page_shell import breadcrumb_schema, defined_term_schema, faq_schema, json_ld_script  # noqa: E402

HOME = "https://domainpreflight.dev/"

GLOSSARY_NAV = """
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

GLOSSARY_CSS = """    :root { --bg: #0B0D14; --bg2: #10131f; --bg3: #161924; --border: #1e2236; --purple: #6c63ff; --text: #e2e4f0; --text2: #8a8fb5; }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'JetBrains Mono', monospace; background: var(--bg); color: var(--text); min-height: 100vh; line-height: 1.6; }
    header { position: sticky; top: 0; z-index: 100; background: rgba(11, 13, 20, 0.7); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); padding: 0.75rem 1.5rem; }
    .header-inner { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem; }
    .logo { display: flex; align-items: center; gap: 0.5rem; font-weight: 600; font-size: 1rem; }
    .logo a { color: var(--purple); text-decoration: none; }
    .pill { font-size: 0.65rem; padding: 0.2rem 0.5rem; border-radius: 999px; background: var(--bg3); border: 1px solid var(--border); margin-left: 0.5rem; color: var(--text2); }
    nav { display: flex; gap: 1rem; align-items: center; flex-wrap: wrap; }
    nav a { color: var(--text2); text-decoration: none; font-size: 0.8rem; }
    nav a:hover { color: var(--text); }
    main { max-width: 760px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }
    .breadcrumb { font-size: 0.8rem; color: var(--text2); margin-bottom: 1.25rem; }
    .breadcrumb a { color: var(--purple); text-decoration: none; }
    .hero-label { font-size: 0.7rem; letter-spacing: 0.15em; font-weight: 600; text-transform: uppercase; color: var(--purple); margin-bottom: 0.5rem; }
    h1 { font-size: clamp(1.35rem, 3.5vw, 1.85rem); font-weight: 600; margin-bottom: 1rem; line-height: 1.3; }
    article > p:first-of-type { color: var(--text2); font-size: 0.9rem; margin-bottom: 1.5rem; }
    article h2 { font-size: 1.05rem; font-weight: 600; margin: 1.75rem 0 0.65rem; color: var(--text); }
    article p { color: var(--text2); font-size: 0.9rem; margin-bottom: 0.75rem; }
    article a { color: var(--purple); }
    .faq-section h2 { font-size: 1.05rem; margin-top: 2rem; }
    .faq-section h3 { font-size: 0.95rem; font-weight: 600; color: var(--text); margin: 1.35rem 0 0.4rem; }
    .faq-section p { margin-bottom: 0.5rem; color: var(--text2); font-size: 0.9rem; }
    .internal-links { margin-top: 1.5rem; font-size: 0.88rem; }
    .internal-links a { color: var(--purple); text-decoration: none; }
    footer { border-top: 1px solid var(--border); padding: 0; background: var(--bg2); }
    .footer-inner { max-width: 1200px; margin: 0 auto; padding: 1.25rem 1.5rem; }
    .footer-disclaimer { color: var(--text2); font-size: 0.75rem; line-height: 1.5; margin-bottom: 1rem; }
    .footer-bar { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1rem; padding: 1rem 1.5rem; border-top: 1px solid var(--border); font-size: 0.8rem; color: var(--text2); max-width: 1200px; margin: 0 auto; }
    .footer-bar a { color: var(--text2); text-decoration: none; }
"""

FOOTER = """
    <div class="footer-inner">
      <p class="footer-disclaimer">This is a free sanity check — not legal or production advice. Verify DNS and mail in your own stack before you change anything.</p>
    </div>
    <div class="footer-bar">
      <div>
        <span>DomainPreflight by MetricLogic ·</span>
        <a href="https://configclarity.dev" target="_blank" rel="noopener">ConfigClarity</a>
        <span>·</span>
        <a href="https://domainpreflight.dev" target="_blank" rel="noopener">DomainPreflight</a>
        <span>·</span>
        <a href="https://packagefix.dev" target="_blank" rel="noopener">PackageFix</a>
        <span>·</span>
        <a href="/glossary/">Glossary</a>
      </div>
      <div>
        <a href="https://github.com/metriclogic26/domain-preflight" target="_blank" rel="noopener">Star on GitHub</a>
        <span> · </span>
        <span>MIT Licensed</span>
        <span> · </span>
        <a href="https://github.com/metriclogic26/domain-preflight/issues/new" target="_blank" rel="noopener">Report issue →</a>
      </div>
    </div>
"""


def faq_html(faqs: list[tuple[str, str]]) -> str:
    lines = ['      <section class="faq-section" aria-label="FAQ">', "        <h2>FAQ</h2>"]
    for q, a in faqs:
        lines.append(f"        <h3>{html_escape(q)}</h3>")
        lines.append(f"        <p>{html_escape(a)}</p>")
    lines.append("      </section>")
    return "\n".join(lines)


def render_term(t: dict) -> str:
    slug = t["slug"]
    canonical = f"{HOME}glossary/{slug}/"
    name = t["name"]
    def_text = t["def_open"]
    # DefinedTerm description = first paragraph (plain for JSON)
    dt = defined_term_schema(name, def_text, canonical)
    fq = faq_schema(t["faqs"])
    bc = breadcrumb_schema(
        [
            ("Home", HOME),
            ("Glossary", f"{HOME}glossary/"),
            (name, canonical),
        ]
    )
    ld = "\n".join([json_ld_script(dt), json_ld_script(fq), json_ld_script(bc)])
    h1 = t["h1"]
    bc_nav = f"""    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{HOME}">Home</a> <span aria-hidden="true">›</span> <a href="/glossary/">Glossary</a> <span aria-hidden="true">›</span> {html_escape(name)}</nav>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_escape(name)} — DomainPreflight Glossary</title>
  <meta name="description" content="{html_escape(def_text[:300])}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
{ld}
  <script defer src="https://cloud.umami.is/script.js" data-website-id="27fc19d2-1ff5-4478-946a-b96cc7d5daf8"></script>
  <style>
{GLOSSARY_CSS}
  </style>
  <link rel="icon" type="image/png" href="/favicon.png">
</head>
<body>
  <header>
    <div class="header-inner">
      <div class="logo"><a href="/">DomainPreflight.</a><span class="pill">BETA</span></div>
      <nav>
{GLOSSARY_NAV}
      </nav>
    </div>
  </header>
  <main>
{bc_nav}
    <article>
      <p class="hero-label">Glossary</p>
      <h1>{html_escape(h1)}</h1>
      <p>{html_escape(def_text)}</p>
{t["extra"]}
{faq_html(t["faqs"])}
      <div class="internal-links"><p><a href="/glossary/">← All terms</a></p></div>
    </article>
  </main>
  <footer>
{FOOTER}
  </footer>
</body>
</html>
"""


def patch_glossary_index() -> None:
    path = ROOT / "glossary" / "index.html"
    text = path.read_text(encoding="utf-8")
    if "/glossary/bounce-rate/" in text:
        print("glossary index already lists new terms — skip patch")
        return
    old = """      <li>
        <a href="/glossary/mail-exchanger/">Mail Exchanger</a>
        <p>The server named by MX that receives SMTP on port 25 — needs A record and ideally matching PTR.</p>
      </li>
    </ul>"""
    insert = ""
    for t in TERMS:
        blurb = t["def_open"][:220] + ("…" if len(t["def_open"]) > 220 else "")
        insert += f"""      <li>
        <a href="/glossary/{t["slug"]}/">{html_escape(t["name"])}</a>
        <p>{html_escape(blurb)}</p>
      </li>
"""
    new = """      <li>
        <a href="/glossary/mail-exchanger/">Mail Exchanger</a>
        <p>The server named by MX that receives SMTP on port 25 — needs A record and ideally matching PTR.</p>
      </li>
""" + insert + """    </ul>"""
    if old not in text:
        raise SystemExit("glossary index needle not found — patch manually")
    text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print("Patched glossary/index.html")


def main() -> None:
    for t in TERMS:
        out = ROOT / "glossary" / t["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_term(t), encoding="utf-8")
        print("Wrote", out.relative_to(ROOT))
    patch_glossary_index()


if __name__ == "__main__":
    main()
