#!/usr/bin/env python3
"""Generate batch 3 blog posts + rewrite blog index."""
from __future__ import annotations

import json
import sys
from html import escape as html_escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch3_blog_data import DATE, POSTS  # noqa: E402
from site_page_shell import article_schema, breadcrumb_schema, faq_schema, json_ld_script  # noqa: E402

HOME = "https://domainpreflight.dev/"

BLOG_CSS = """    :root { --bg: #0B0D14; --surface: #10131f; --bg3: #161924; --border: #1e2236; --purple: #6c63ff; --text: #e2e4f0; --text2: #8a8fb5; }
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
    main { max-width: 720px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }
    .breadcrumb { font-size: 0.8rem; color: var(--text2); margin-bottom: 1.25rem; line-height: 1.5; }
    .breadcrumb a { color: var(--purple); text-decoration: none; }
    .breadcrumb a:hover { text-decoration: underline; }
    .hero-label { font-size: 0.7rem; letter-spacing: 0.15em; font-weight: 600; text-transform: uppercase; color: var(--purple); margin-bottom: 0.5rem; }
    h1 { font-size: clamp(1.35rem, 3.5vw, 1.85rem); font-weight: 600; margin-bottom: 0.5rem; line-height: 1.3; }
    .post-date { color: var(--text2); font-size: 0.8rem; margin-bottom: 1.5rem; }
    article h2 { font-size: 1.05rem; font-weight: 600; margin: 2rem 0 0.75rem; color: var(--text); }
    article p, article li { color: var(--text2); font-size: 0.9rem; margin-bottom: 0.75rem; }
    article ul, article ol { margin: 0.5rem 0 1rem 1.25rem; color: var(--text2); font-size: 0.9rem; }
    pre.code-block { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 1rem 1.15rem; font-size: 0.78rem; line-height: 1.55; overflow-x: auto; white-space: pre-wrap; word-break: break-word; color: var(--text); margin: 0.75rem 0 1rem; }
    .tool-cta { margin: 2rem 0; padding: 1.25rem 1.5rem; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; border-left: 3px solid var(--purple); }
    .tool-cta p { margin-bottom: 0.5rem; color: var(--text); }
    .tool-cta a { color: var(--purple); font-weight: 600; text-decoration: none; }
    .tool-cta a:hover { text-decoration: underline; }
    .faq-section h2 { font-size: 1.05rem; margin-top: 2rem; }
    .faq-section h3 { font-size: 0.95rem; font-weight: 600; color: var(--text); margin: 1.5rem 0 0.4rem; }
    .faq-section p { margin-bottom: 0.5rem; color: var(--text2); font-size: 0.9rem; }
    .internal-links { margin-top: 2rem; padding-top: 1.25rem; border-top: 1px solid var(--border); font-size: 0.88rem; }
    .internal-links a { color: var(--purple); text-decoration: none; }
    footer { border-top: 1px solid var(--border); background: var(--surface); }
    .footer-inner { max-width: 1200px; margin: 0 auto; padding: 1.25rem 1.5rem; }
    .footer-disclaimer { color: var(--text2); font-size: 0.75rem; line-height: 1.5; margin-bottom: 1rem; }
    .footer-bar { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1rem; padding: 1rem 1.5rem; border-top: 1px solid var(--border); font-size: 0.8rem; color: var(--text2); max-width: 1200px; margin: 0 auto; }
    .footer-bar a { color: var(--text2); text-decoration: none; }
"""

NAV = """
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

FOOTER = """
    <div class="footer-inner"><p class="footer-disclaimer">This is a free sanity check — not legal or production advice. Verify DNS and mail in your own stack before you change anything.</p></div>
    <div class="footer-bar">
      <div><span>DomainPreflight by MetricLogic ·</span> <a href="https://configclarity.dev" target="_blank" rel="noopener">ConfigClarity</a> <span>·</span> <a href="https://domainpreflight.dev" target="_blank" rel="noopener">DomainPreflight</a> <span>·</span> <a href="https://packagefix.dev" target="_blank" rel="noopener">PackageFix</a> <span>·</span> <a href="/glossary/">Glossary</a></div>
      <div><a href="https://github.com/metriclogic26/domain-preflight" target="_blank" rel="noopener">Star on GitHub</a> <span> · </span> <span>MIT Licensed</span> <span> · </span> <a href="https://github.com/metriclogic26/domain-preflight/issues/new" target="_blank" rel="noopener">Report issue →</a></div>
    </div>
"""


def faq_html(faqs: list[tuple[str, str]]) -> str:
    lines = ['      <section class="faq-section" aria-label="FAQ">', "        <h2>FAQ</h2>"]
    for q, a in faqs:
        lines.append(f"        <h3>{html_escape(q)}</h3>")
        lines.append(f"        <p>{html_escape(a)}</p>")
    lines.append("      </section>")
    return "\n".join(lines)


def render_post(p: dict) -> str:
    slug = p["slug"]
    canonical = f"{HOME}blog/{slug}/"
    title = p["title"]
    faqs = p["faqs"]
    ld = "\n".join(
        [
            json_ld_script(article_schema(title, p["meta"], canonical, DATE)),
            json_ld_script(faq_schema(faqs)),
            json_ld_script(
                breadcrumb_schema(
                    [
                        ("Home", HOME),
                        ("Blog", f"{HOME}blog/"),
                        (title, canonical),
                    ]
                )
            ),
        ]
    )
    bc = f"""    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{HOME}">Home</a> <span aria-hidden="true">›</span> <a href="/blog/">Blog</a> <span aria-hidden="true">›</span> {html_escape(title)}</nav>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_escape(title)} | DomainPreflight</title>
  <meta name="description" content="{html_escape(p['meta'])}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
{ld}
  <script defer src="https://cloud.umami.is/script.js" data-website-id="27fc19d2-1ff5-4478-946a-b96cc7d5daf8"></script>
  <style>
{BLOG_CSS}
  </style>
  <link rel="icon" type="image/png" href="/favicon.png">
</head>
<body>
  <header>
    <div class="header-inner">
      <div class="logo"><a href="/">DomainPreflight.</a><span class="pill">BETA</span></div>
      <nav>
{NAV}
      </nav>
    </div>
  </header>
  <main>
{bc}
    <article>
      <p class="hero-label">Blog</p>
      <h1>{html_escape(title)}</h1>
      <p class="post-date"><time datetime="{DATE}">March 19, 2026</time></p>
{p["body"]}
{faq_html(faqs)}
      <div class="internal-links"><p><a href="/blog/">← All posts</a></p></div>
    </article>
  </main>
  <footer>
{FOOTER}
  </footer>
</body>
</html>
"""


# All 20 posts for index: 8 legacy + 12 new — titles and URLs for ItemList
LEGACY = [
    ("dmarc-p-none-still-a-problem", "Your DMARC Is Set to p=none. Here's Why That's Still a Problem.", "Green tick, zero blocking — spoofing still lands in inboxes. What to do next."),
    ("spf-lookup-limit", "The SPF Lookup Limit: Why You Hit 10 and How to Stay Under It", "Silent PermError when you stack one more SaaS on SPF — count and flatten."),
    ("dmarc-alignment-vs-dmarc-policy", "DMARC Alignment vs DMARC Policy — The Difference Most Guides Skip", "p=reject doesn't help if alignment never lines up. Here's the split."),
    ("spf-dkim-pass-dmarc-fails", "Why Your Emails Pass SPF and DKIM But Still Fail DMARC", "Two greens and a red — alignment is the missing piece."),
    ("sendgrid-cname-setup", "The SendGrid CNAME Setup Most People Miss", "SPF include alone won't align Return-Path — you need the three CNAMEs."),
    ("subdomain-takeover-dangling-cnames", "Subdomain Takeover: The Dangling CNAME Risk Nobody Checks", "Deleted the app, left the DNS — someone else can claim your hostname."),
    ("how-to-read-dmarc-report", "How to Read a DMARC Aggregate Report Without Losing Your Mind", "Zip, XML, pain — or paste into the analyzer and get a table."),
    ("domain-expiry-infrastructure-failure", "Domain Expiry: The Infrastructure Failure That Always Comes at the Worst Time", "NXDOMAIN Monday — auto-renew and WHOIS checks beat heroics."),
]


def write_blog_index() -> None:
    items = []
    cards = []
    for slug, title, desc in LEGACY:
        url = f"{HOME}blog/{slug}/"
        items.append({"@type": "ListItem", "position": len(items) + 1, "name": title, "url": url})
        cards.append(
            f'      <a class="post-card" href="/blog/{slug}/"><span class="post-card-arrow">→</span><div class="post-card-title">{html_escape(title)}</div><div class="post-card-meta">March 19, 2026</div><div class="post-card-desc">{html_escape(desc)}</div></a>'
        )
    for p in POSTS:
        slug = p["slug"]
        title = p["title"]
        url = f"{HOME}blog/{slug}/"
        items.append({"@type": "ListItem", "position": len(items) + 1, "name": title, "url": url})
        cards.append(
            f'      <a class="post-card" href="/blog/{slug}/"><span class="post-card-arrow">→</span><div class="post-card-title">{html_escape(title)}</div><div class="post-card-meta">March 19, 2026</div><div class="post-card-desc">{html_escape(p["meta"])}</div></a>'
        )
    blog_ld = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Email Deliverability & DNS Blog",
        "url": f"{HOME}blog/",
        "description": "DMARC, SPF, alignment, DNS — practical posts.",
        "publisher": {"@type": "Organization", "name": "MetricLogic"},
        "hasPart": {
            "@type": "ItemList",
            "name": "Blog posts",
            "numberOfItems": len(items),
            "itemListElement": items,
        },
    }
    idx = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Email Deliverability Blog — DomainPreflight</title>
  <meta name="description" content="DMARC, SPF, alignment, SendGrid setup, subdomain takeover, and domain expiry — short posts from the browser.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://domainpreflight.dev/blog/">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script defer src="https://cloud.umami.is/script.js" data-website-id="27fc19d2-1ff5-4478-946a-b96cc7d5daf8"></script>
  <script type="application/ld+json">
  {json.dumps(blog_ld, ensure_ascii=False)}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://domainpreflight.dev/"}},{{"@type":"ListItem","position":2,"name":"Blog","item":"https://domainpreflight.dev/blog/"}}]}}
  </script>
  <style>
    :root {{ --bg: #0B0D14; --surface: #10131f; --bg3: #161924; --border: #1e2236; --purple: #6c63ff; --text: #e2e4f0; --text2: #8a8fb5; }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'JetBrains Mono', monospace; background: var(--bg); color: var(--text); min-height: 100vh; line-height: 1.5; }}
    header {{ position: sticky; top: 0; z-index: 100; background: rgba(11, 13, 20, 0.7); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); padding: 0.75rem 1.5rem; }}
    .header-inner {{ max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem; }}
    .logo {{ display: flex; align-items: center; gap: 0.5rem; font-weight: 600; font-size: 1rem; }}
    .logo a {{ color: var(--purple); text-decoration: none; }}
    .pill {{ font-size: 0.65rem; padding: 0.2rem 0.5rem; border-radius: 999px; background: var(--bg3); border: 1px solid var(--border); margin-left: 0.5rem; color: var(--text2); }}
    nav {{ display: flex; gap: 0.85rem; align-items: center; flex-wrap: wrap; }}
    nav a {{ color: var(--text2); text-decoration: none; font-size: 0.78rem; }}
    nav a:hover {{ color: var(--text); }}
    main {{ max-width: 1000px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }}
    .breadcrumb {{ font-size: 0.8rem; color: var(--text2); margin-bottom: 1.25rem; }}
    .breadcrumb a {{ color: var(--purple); text-decoration: none; }}
    .breadcrumb a:hover {{ text-decoration: underline; }}
    .hero-label {{ font-size: 0.7rem; letter-spacing: 0.15em; font-weight: 600; text-transform: uppercase; color: var(--purple); margin-bottom: 0.5rem; }}
    h1 {{ font-size: clamp(1.5rem, 4vw, 2rem); font-weight: 600; margin-bottom: 0.75rem; }}
    .lead {{ color: var(--text2); font-size: 0.9rem; margin-bottom: 2rem; max-width: 640px; }}
    .card-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 0.85rem; }}
    .post-card {{ display: block; padding: 1.1rem 1.25rem; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; text-decoration: none; color: inherit; transition: border-color 0.2s, box-shadow 0.2s; }}
    .post-card:hover {{ border-color: var(--purple); box-shadow: 0 0 0 1px rgba(108, 99, 255, 0.25); }}
    .post-card-title {{ font-size: 0.95rem; font-weight: 600; color: var(--text); margin-bottom: 0.35rem; line-height: 1.35; }}
    .post-card-meta {{ font-size: 0.72rem; color: var(--text2); margin-bottom: 0.5rem; }}
    .post-card-desc {{ font-size: 0.78rem; color: var(--text2); line-height: 1.45; }}
    .post-card-arrow {{ color: var(--purple); float: right; font-size: 1.1rem; margin-left: 0.5rem; }}
    footer {{ border-top: 1px solid var(--border); background: var(--surface); }}
    .footer-inner {{ max-width: 1200px; margin: 0 auto; padding: 1.25rem 1.5rem; }}
    .footer-disclaimer {{ color: var(--text2); font-size: 0.75rem; line-height: 1.5; margin-bottom: 1rem; }}
    .footer-bar {{ display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1rem; padding: 1rem 1.5rem; border-top: 1px solid var(--border); font-size: 0.8rem; color: var(--text2); max-width: 1200px; margin: 0 auto; }}
    .footer-bar a {{ color: var(--text2); text-decoration: none; }}
    .footer-bar a:hover {{ color: var(--text); }}
  </style>
  <link rel="icon" type="image/png" href="/favicon.png">
</head>
<body>
  <header>
    <div class="header-inner">
      <div class="logo"><a href="/">DomainPreflight.</a><span class="pill">BETA</span></div>
      <nav>
{NAV}
      </nav>
    </div>
  </header>
  <main>
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="https://domainpreflight.dev/">Home</a> <span aria-hidden="true">›</span> Blog</nav>
    <p class="hero-label">Blog</p>
    <h1>Email Deliverability &amp; DNS Blog</h1>
    <p class="lead">Short posts — the stuff we wish someone had told us before a Friday outage.</p>

    <div class="card-grid">
{chr(10).join(cards)}
    </div>
  </main>
  <footer>
{FOOTER}
  </footer>
</body>
</html>
"""
    (ROOT / "blog" / "index.html").write_text(idx, encoding="utf-8")
    print("Wrote blog/index.html")


def main() -> None:
    for p in POSTS:
        out = ROOT / "blog" / p["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_post(p), encoding="utf-8")
        print("Wrote", out.relative_to(ROOT))
    write_blog_index()


if __name__ == "__main__":
    main()
