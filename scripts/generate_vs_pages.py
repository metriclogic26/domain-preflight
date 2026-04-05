#!/usr/bin/env python3
"""Generate vs/[slug]/index.html comparison pages."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VS = ROOT / "vs"
DATE_PUBLISHED = "2026-03-12"

SHELL_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | DomainPreflight</title>
  <meta name="description" content="{meta}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script type="application/ld+json">
  {article_json}
  </script>
  <script type="application/ld+json">
  {faq_json}
  </script>
  <script type="application/ld+json">
  {breadcrumb_json}
  </script>
  <script defer src="https://cloud.umami.is/script.js" data-website-id="27fc19d2-1ff5-4478-946a-b96cc7d5daf8"></script>
  <style>
    :root {{ --bg: #0B0D14; --surface: #10131f; --bg3: #161924; --border: #1e2236; --purple: #6c63ff; --text: #e2e4f0; --text2: #8a8fb5; }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'JetBrains Mono', monospace; background: var(--bg); color: var(--text); min-height: 100vh; line-height: 1.6; }}
    header {{ position: sticky; top: 0; z-index: 100; background: rgba(11, 13, 20, 0.7); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); padding: 0.75rem 1.5rem; }}
    .header-inner {{ max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem; }}
    .logo {{ display: flex; align-items: center; gap: 0.5rem; font-weight: 600; font-size: 1rem; }}
    .logo a {{ color: var(--purple); text-decoration: none; }}
    .pill {{ font-size: 0.65rem; padding: 0.2rem 0.5rem; border-radius: 999px; background: var(--bg3); border: 1px solid var(--border); margin-left: 0.5rem; color: var(--text2); }}
    nav {{ display: flex; gap: 0.85rem; align-items: center; flex-wrap: wrap; }}
    nav a {{ color: var(--text2); text-decoration: none; font-size: 0.78rem; }}
    nav a:hover {{ color: var(--text); }}
    main {{ max-width: 820px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }}
    .breadcrumb {{ font-size: 0.8rem; color: var(--text2); margin-bottom: 1.25rem; line-height: 1.5; }}
    .breadcrumb a {{ color: var(--purple); text-decoration: none; }}
    .breadcrumb a:hover {{ text-decoration: underline; }}
    .hero-label {{ font-size: 0.7rem; letter-spacing: 0.15em; font-weight: 600; text-transform: uppercase; color: var(--purple); margin-bottom: 0.5rem; }}
    h1 {{ font-size: clamp(1.35rem, 3.5vw, 1.9rem); font-weight: 600; margin-bottom: 1rem; line-height: 1.3; }}
    .subtitle {{ color: var(--text2); font-size: 0.95rem; margin-bottom: 1.75rem; }}
    article h2 {{ font-size: 1.05rem; font-weight: 600; margin: 2rem 0 0.75rem; color: var(--text); }}
    article p, article li {{ color: var(--text2); font-size: 0.9rem; margin-bottom: 0.75rem; }}
    article ul {{ margin: 0.5rem 0 1rem 1.25rem; }}
    .compare-wrap {{ overflow-x: auto; margin: 1.25rem 0; -webkit-overflow-scrolling: touch; }}
    .compare-table {{ width: 100%; border-collapse: collapse; font-size: 0.78rem; }}
    .compare-table th, .compare-table td {{ border: 1px solid var(--border); padding: 0.5rem 0.65rem; text-align: left; vertical-align: top; }}
    .compare-table th {{ background: var(--surface); color: var(--text); font-weight: 600; }}
    .tool-cta {{ margin: 2rem 0; padding: 1.25rem 1.5rem; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; border-left: 3px solid var(--purple); }}
    .tool-cta p {{ margin-bottom: 0.5rem; color: var(--text); }}
    .tool-cta a {{ color: var(--purple); font-weight: 600; text-decoration: none; }}
    .tool-cta a:hover {{ text-decoration: underline; }}
    .faq-section h3 {{ font-size: 0.95rem; font-weight: 600; color: var(--text); margin: 1.5rem 0 0.4rem; }}
    .faq-section p {{ margin-bottom: 0.5rem; }}
    .internal-links {{ margin-top: 2rem; padding-top: 1.25rem; border-top: 1px solid var(--border); font-size: 0.88rem; }}
    .internal-links a {{ color: var(--purple); text-decoration: none; }}
    .internal-links a:hover {{ text-decoration: underline; }}
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
        <a href="/">DNS Preflight</a>
        <a href="/email/">Email</a>
        <a href="/whois/">WHOIS</a>
        <a href="/dangling/">Dangling Records</a>
        <a href="/typosquat/">Typosquat</a>
        <a href="/propagation/">Propagation</a>
        <a href="/dmarc/">DMARC Report</a>
        <a href="/glossary/">Glossary</a>
      </nav>
    </div>
  </header>
  <main>
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="https://domainpreflight.dev/">Home</a> <span aria-hidden="true">›</span> <a href="/vs/">Comparisons</a> <span aria-hidden="true">›</span> {crumb_title}</nav>
    <article>
      <p class="hero-label">Compare</p>
      <h1>{h1}</h1>
      <p class="subtitle">{subtitle}</p>
{body}
      <section class="faq-section" aria-label="FAQ">
        <h2>FAQ</h2>
{faq_html}
      </section>
      <div class="internal-links">
        <p><a href="/vs/">← All comparisons</a></p>
      </div>
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


def faq_block(faqs: list[tuple[str, str]]) -> str:
    lines = []
    for q, a in faqs:
        lines.append(f"        <h3>{q}</h3>\n        <p>{a}</p>")
    return "\n".join(lines)


def build(
    slug: str,
    title: str,
    meta: str,
    h1: str,
    crumb_title: str,
    subtitle: str,
    body: str,
    faqs: list[tuple[str, str]],
) -> str:
    canonical = f"https://domainpreflight.dev/vs/{slug}/"
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": h1,
        "datePublished": DATE_PUBLISHED,
        "dateModified": DATE_PUBLISHED,
        "author": {"@type": "Organization", "name": "MetricLogic"},
        "publisher": {
            "@type": "Organization",
            "name": "DomainPreflight",
            "url": "https://domainpreflight.dev/",
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
    }
    faq_entities = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ]
    faqpage = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_entities}
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://domainpreflight.dev/"},
            {"@type": "ListItem", "position": 2, "name": "Comparisons", "item": "https://domainpreflight.dev/vs/"},
            {"@type": "ListItem", "position": 3, "name": crumb_title, "item": canonical},
        ],
    }
    return SHELL_HEAD.format(
        title=title,
        meta=meta,
        canonical=canonical,
        article_json=json.dumps(article, ensure_ascii=False, indent=2),
        faq_json=json.dumps(faqpage, ensure_ascii=False, indent=2),
        breadcrumb_json=json.dumps(crumbs, ensure_ascii=False, separators=(",", ":")),
        crumb_title=crumb_title,
        h1=h1,
        subtitle=subtitle,
        body=body,
        faq_html=faq_block(faqs),
    )


def main():
    pages: list[tuple[str, str, str, str, str, str, str, list[tuple[str, str]]]] = [
        (
            "mxtoolbox",
            "DomainPreflight vs MXToolbox — Comparison",
            "Honest comparison: MXToolbox flags issues; DomainPreflight adds alignment fixes, copy-paste DNS, no account, open source.",
            "DomainPreflight vs MXToolbox",
            "DomainPreflight vs MXToolbox",
            "MXToolbox tells you what's wrong. DomainPreflight tells you how to fix it — with copy-paste DNS records, provider-specific alignment detection, and no account required.",
            """      <h2>Comparison</h2>
      <div class="compare-wrap">
        <table class="compare-table">
          <thead>
            <tr><th>Feature</th><th>MXToolbox</th><th>DomainPreflight</th></tr>
          </thead>
          <tbody>
            <tr><td>DMARC alignment check</td><td>Basic</td><td>Deep — detects per-provider CNAME gaps</td></tr>
            <tr><td>Copy-paste DNS fix</td><td>❌</td><td>✅</td></tr>
            <tr><td>No signup required</td><td>⚠️ Partial</td><td>✅ Always</td></tr>
            <tr><td>Client-side only</td><td>❌</td><td>✅</td></tr>
            <tr><td>DMARC XML analyzer</td><td>❌</td><td>✅</td></tr>
            <tr><td>Typosquat monitor</td><td>❌</td><td>✅</td></tr>
            <tr><td>Dangling record scan</td><td>❌</td><td>✅</td></tr>
            <tr><td>DNS propagation check</td><td>✅</td><td>✅</td></tr>
            <tr><td>Pricing</td><td>Freemium ($19/mo)</td><td>Free always</td></tr>
            <tr><td>Open source</td><td>❌</td><td>✅ MIT</td></tr>
          </tbody>
        </table>
      </div>

      <h2>Where MXToolbox wins</h2>
      <ul>
        <li>Brand recognition and trust (20+ years)</li>
        <li>Monitoring alerts (paid tier)</li>
        <li>Broader tool coverage (HTTP checks, etc.)</li>
        <li>Larger historical database</li>
      </ul>

      <h2>Where DomainPreflight wins</h2>
      <ul>
        <li><strong>Alignment engine:</strong> detects provider-specific CNAME issues MXToolbox misses</li>
        <li><strong>Copy-paste fixes:</strong> not just flags — actual DNS records to paste</li>
        <li><strong>No account ever:</strong> nothing stored, nothing tracked</li>
        <li><strong>DMARC XML analysis:</strong> paste your report, see what's failing</li>
        <li><strong>Open source:</strong> inspect every check</li>
      </ul>

      <div class="tool-cta">
        <p>Run DNS Preflight — alignment, SPF tree, and more</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>""",
            [
                (
                    "Is DomainPreflight a free alternative to MXToolbox?",
                    "Yes — all DomainPreflight tools are free with no account required. MXToolbox has a free tier but limits lookups and requires signup for full access.",
                ),
                (
                    "What does DomainPreflight do that MXToolbox doesn't?",
                    "The alignment engine detects provider-specific CNAME gaps — MXToolbox tells you DMARC fails but not why SendGrid specifically is breaking alignment.",
                ),
                (
                    "Does MXToolbox have monitoring alerts?",
                    "Yes — MXToolbox charges $19/mo for scheduled monitoring. DomainPreflight is manual scan only currently.",
                ),
                (
                    "Which tool should I use first?",
                    "Run DomainPreflight first — it gives you actionable fixes, not just flags. If you need ongoing monitoring, consider MXToolbox's paid tier later.",
                ),
                (
                    "Is DomainPreflight open source?",
                    "Yes — MIT licensed at https://github.com/metriclogic26/domain-preflight. MXToolbox is proprietary.",
                ),
            ],
        ),
        (
            "easydmarc",
            "DomainPreflight vs EasyDMARC — Comparison",
            "EasyDMARC is paid DMARC monitoring; DomainPreflight is a free browser pre-flight checker with alignment fixes.",
            "DomainPreflight vs EasyDMARC",
            "DomainPreflight vs EasyDMARC",
            "EasyDMARC is a paid DMARC monitoring platform. DomainPreflight is a free pre-flight checker with no account. They solve different problems — EasyDMARC for ongoing monitoring, DomainPreflight for diagnosing and fixing alignment before you send.",
            """      <h2>Where EasyDMARC wins</h2>
      <ul>
        <li>Ongoing DMARC reporting and monitoring</li>
        <li>Visual reporting dashboards</li>
        <li>Managed DMARC service option</li>
        <li>BIMI setup assistance</li>
      </ul>

      <h2>Where DomainPreflight wins</h2>
      <ul>
        <li>Free, no account ever</li>
        <li>Alignment engine with provider-specific fixes</li>
        <li>Copy-paste DNS records</li>
        <li>Client-side only — nothing stored</li>
        <li>Broader tool set (WHOIS, dangling records, typosquat, propagation)</li>
      </ul>

      <div class="tool-cta">
        <p>Fix alignment, then paste DMARC XML when you have it</p>
        <p><a href="https://domainpreflight.dev/">DNS Preflight →</a> · <a href="https://domainpreflight.dev/dmarc/">DMARC Report Analyzer →</a></p>
      </div>""",
            [
                (
                    "Is DomainPreflight a free alternative to EasyDMARC?",
                    "For pre-flight checking and fixing alignment — yes. For ongoing DMARC report monitoring — EasyDMARC does more.",
                ),
                (
                    "Does DomainPreflight have DMARC reporting?",
                    "Yes — paste your DMARC XML report into the DMARC Report Analyzer for a visual summary. Not ongoing automated monitoring.",
                ),
                (
                    "What does EasyDMARC cost?",
                    "EasyDMARC starts at around $7-24/mo depending on plan. DomainPreflight is free.",
                ),
                (
                    "Which should I use to set up DMARC for the first time?",
                    "DomainPreflight — it detects your provider and shows exactly which CNAMEs to add. Use EasyDMARC if you want ongoing monitoring after.",
                ),
                (
                    "Can I use both together?",
                    "Yes. Use DomainPreflight to fix alignment issues and diagnose problems. Use EasyDMARC for ongoing aggregate report monitoring.",
                ),
            ],
        ),
        (
            "dmarcian",
            "DomainPreflight vs dmarcian — Comparison",
            "dmarcian is enterprise DMARC reporting; DomainPreflight is a free browser tool for alignment diagnosis and fixes.",
            "DomainPreflight vs dmarcian",
            "DomainPreflight vs dmarcian",
            "dmarcian specialises in DMARC reporting and policy management for enterprises. DomainPreflight is a free browser tool for diagnosing and fixing DNS and email issues with no account required.",
            """      <h2>Where dmarcian wins</h2>
      <ul>
        <li>Deep DMARC aggregate report analysis</li>
        <li>Policy management workflow</li>
        <li>Enterprise support</li>
        <li>Historical data and trends</li>
      </ul>

      <h2>Where DomainPreflight wins</h2>
      <ul>
        <li>Free, no account</li>
        <li>Alignment diagnosis with fix output</li>
        <li>Broader tool set beyond DMARC</li>
        <li>Client-side, nothing stored</li>
      </ul>

      <div class="tool-cta">
        <p>Diagnose alignment and paste aggregate XML</p>
        <p><a href="https://domainpreflight.dev/">DNS Preflight →</a> · <a href="https://domainpreflight.dev/dmarc/">DMARC Report Analyzer →</a></p>
      </div>""",
            [
                (
                    "Is DomainPreflight a free dmarcian alternative?",
                    "For diagnosing DMARC alignment failures — yes. For enterprise DMARC management and reporting — dmarcian does more.",
                ),
                (
                    "What does dmarcian cost?",
                    "dmarcian pricing starts at $14-24/mo. DomainPreflight is free.",
                ),
                (
                    "Does DomainPreflight analyze DMARC reports?",
                    "Yes — paste your XML report into the DMARC Report Analyzer. Not automated monitoring.",
                ),
                (
                    "Who is DomainPreflight for vs dmarcian?",
                    "DomainPreflight is for developers and sysadmins diagnosing and fixing issues. dmarcian is for organisations that need ongoing policy management.",
                ),
                (
                    "Can I fix my DMARC alignment using DomainPreflight before switching to dmarcian?",
                    "Yes — that's the ideal workflow. Fix alignment with DomainPreflight, then use dmarcian for monitoring.",
                ),
            ],
        ),
        (
            "powerdmarc",
            "DomainPreflight vs PowerDMARC — Comparison",
            "PowerDMARC is enterprise AI-backed DMARC; DomainPreflight is free pre-flight alignment and copy-paste fixes.",
            "DomainPreflight vs PowerDMARC",
            "DomainPreflight vs PowerDMARC",
            "PowerDMARC is an enterprise DMARC platform with AI-powered reporting. DomainPreflight is a free pre-flight checker with alignment detection and copy-paste fixes.",
            """      <h2>Key differences</h2>
      <ul>
        <li><strong>PowerDMARC:</strong> enterprise, paid, ongoing monitoring and AI reporting</li>
        <li><strong>DomainPreflight:</strong> free, pre-flight scans, fix-oriented output, no account</li>
      </ul>

      <h2>Where PowerDMARC wins</h2>
      <ul>
        <li>Enterprise dashboards and SLA-style support</li>
        <li>Continuous aggregate reporting and alerting</li>
        <li>Policy workflow for large teams</li>
      </ul>

      <h2>Where DomainPreflight wins</h2>
      <ul>
        <li>Zero cost — no trial wall</li>
        <li>Alignment engine with provider-specific fixes</li>
        <li>WHOIS, typosquat, dangling, propagation — same session</li>
        <li>Open source — MIT</li>
      </ul>

      <div class="tool-cta">
        <p>Start with DNS Preflight + DMARC XML paste</p>
        <p><a href="https://domainpreflight.dev/">DNS Preflight →</a> · <a href="https://domainpreflight.dev/dmarc/">DMARC Report Analyzer →</a></p>
      </div>""",
            [
                (
                    "Is DomainPreflight a free alternative to PowerDMARC?",
                    "For diagnosing and fixing alignment before enforcement — yes. For enterprise DMARC operations with AI dashboards — PowerDMARC is built for that.",
                ),
                (
                    "What does PowerDMARC cost?",
                    "PowerDMARC is a paid enterprise platform (contact sales / tiered pricing). DomainPreflight is free.",
                ),
                (
                    "Does DomainPreflight analyze DMARC reports?",
                    "Yes — paste aggregate XML into the DMARC Report Analyzer. It's manual, not a 24/7 hosted inbox.",
                ),
                (
                    "Who should use PowerDMARC vs DomainPreflight?",
                    "Use DomainPreflight when you need fast fixes and proof in the browser. Use PowerDMARC when you need ongoing org-wide monitoring and workflows.",
                ),
                (
                    "Can I use both together?",
                    "Yes — fix alignment and validate DNS in DomainPreflight, then route reports to a commercial platform if your org needs it.",
                ),
            ],
        ),
        (
            "intodns",
            "DomainPreflight vs intoDNS — Comparison",
            "intoDNS is broad DNS health; DomainPreflight adds email deliverability, alignment, blocklists, and copy-paste fixes.",
            "DomainPreflight vs intoDNS",
            "DomainPreflight vs intoDNS",
            "intoDNS checks DNS health and configuration. DomainPreflight focuses on email deliverability — adding DMARC alignment detection, IP reputation, blocklist checks, and copy-paste fixes that intoDNS doesn't have.",
            """      <h2>Key differences</h2>
      <ul>
        <li><strong>intoDNS:</strong> broader DNS health (NS, SOA, glue, recursion)</li>
        <li><strong>DomainPreflight:</strong> email-focused stack — alignment, DMARC, lists, fixes</li>
      </ul>

      <h2>Overlap</h2>
      <p>Both can surface MX and SPF basics. DomainPreflight adds alignment scoring, DMARC XML, blocklists, typosquat, dangling records, and fix output.</p>

      <h2>Where intoDNS wins</h2>
      <ul>
        <li>Classic DNS sanity checklist in one page</li>
        <li>Familiar to ops teams for non-mail DNS review</li>
      </ul>

      <h2>Where DomainPreflight wins</h2>
      <ul>
        <li>Alignment engine with provider gaps</li>
        <li>Email + IP reputation tooling in one place</li>
        <li>Copy-paste DNS rows, not just pass/fail</li>
      </ul>

      <div class="tool-cta">
        <p>Run DNS Preflight for mail — use Propagation for resolver agreement</p>
        <p><a href="https://domainpreflight.dev/">DNS Preflight →</a> · <a href="/propagation/">Propagation check →</a></p>
      </div>""",
            [
                (
                    "What's the difference between intoDNS and DomainPreflight?",
                    "intoDNS is general DNS health. DomainPreflight is built around email authentication, alignment, reputation, and actionable fixes.",
                ),
                (
                    "Do both check MX and SPF?",
                    "Yes — there's overlap on basics. DomainPreflight goes deeper on DMARC alignment, DKIM, IP lists, and deliverability context.",
                ),
                (
                    "Does DomainPreflight give copy-paste DNS fixes?",
                    "Yes — where the tool can infer provider-specific records, you get copy-paste guidance. intoDNS is mostly diagnostic labels.",
                ),
                (
                    "Are both free?",
                    "Both are free to use in the browser for typical checks. DomainPreflight requires no account.",
                ),
                (
                    "Which should I run first for email issues?",
                    "DomainPreflight — you'll get alignment and blocklist signal in one pass. Use intoDNS when you want a broad DNS checklist outside mail.",
                ),
            ],
        ),
        (
            "spftoolbox",
            "DomainPreflight vs SPFToolbox — Comparison",
            "SPFToolbox focuses on SPF/WHOIS; DomainPreflight covers the full mail stack with alignment and open source.",
            "DomainPreflight vs SPFToolbox",
            "DomainPreflight vs SPFToolbox",
            "SPFToolbox handles SPF lookups and WHOIS. DomainPreflight covers the full email authentication stack — SPF, DKIM, DMARC alignment, IP reputation, dangling records, and typosquat monitoring — in one browser tool.",
            """      <h2>Key differences</h2>
      <ul>
        <li><strong>SPFToolbox:</strong> SPF / MX / WHOIS focus</li>
        <li><strong>DomainPreflight:</strong> full stack + alignment + deliverability extras</li>
      </ul>

      <h2>Both open source</h2>
      <p>SPFToolbox and DomainPreflight are open-source friendly. You can read the checks and run them locally.</p>

      <h2>Where SPFToolbox wins</h2>
      <ul>
        <li>Single-purpose SPF lookup depth</li>
        <li>Lightweight if you only care about SPF strings</li>
      </ul>

      <h2>Where DomainPreflight wins</h2>
      <ul>
        <li>DMARC alignment and provider detection</li>
        <li>DKIM probes, blocklists, typosquat, dangling records</li>
        <li>One workflow for “why is mail failing?”</li>
      </ul>

      <div class="tool-cta">
        <p>Walk the full SPF tree + alignment in Preflight</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>""",
            [
                (
                    "How do features overlap?",
                    "Both help with SPF. DomainPreflight adds DKIM, DMARC alignment, IP reputation, and non-SPF DNS tools in the same UI.",
                ),
                (
                    "Does SPFToolbox cover DMARC alignment?",
                    "It doesn't focus on alignment scoring — DomainPreflight does, including provider-specific CNAME gaps.",
                ),
                (
                    "Are both open source?",
                    "Yes — DomainPreflight is MIT on GitHub. SPFToolbox is open source in spirit; verify its license on the project page.",
                ),
                (
                    "Which tool should I use for SPF flattening?",
                    "Use SPF lookup depth to see includes — DomainPreflight's tree helps you see lookup count before you flatten. Pair with vendor IP docs.",
                ),
                (
                    "Should I use both?",
                    "If you want a second opinion on raw SPF text, sure. For most teams, DomainPreflight alone covers SPF plus the rest of the stack.",
                ),
            ],
        ),
        (
            "dnschecker",
            "DomainPreflight vs DNSChecker — Comparison",
            "DNSChecker maps global propagation; DomainPreflight adds email auth, alignment, and a 5-resolver propagation view.",
            "DomainPreflight vs DNSChecker",
            "DomainPreflight vs DNSChecker",
            "DNSChecker shows DNS propagation across global servers. DomainPreflight's propagation tool checks across 5 resolvers and adds email-specific checks — SPF, DKIM, DMARC, alignment — that DNSChecker doesn't cover.",
            """      <h2>Key differences</h2>
      <ul>
        <li><strong>DNSChecker:</strong> propagation focus, many resolvers worldwide</li>
        <li><strong>DomainPreflight:</strong> email-focused stack + propagation across 5 resolvers</li>
      </ul>

      <h2>Where DNSChecker wins</h2>
      <ul>
        <li>More global resolver coverage for pure propagation maps</li>
        <li>Great when you only care “is it visible everywhere yet?”</li>
      </ul>

      <h2>Where DomainPreflight wins</h2>
      <ul>
        <li>DMARC alignment and mail auth context after propagation</li>
        <li>Typosquat, dangling, WHOIS — launch-week toolkit</li>
      </ul>

      <div class="tool-cta">
        <p>Check propagation, then validate mail auth</p>
        <p><a href="/propagation/">Propagation (5 resolvers) →</a> · <a href="https://domainpreflight.dev/">DNS Preflight →</a></p>
      </div>""",
            [
                (
                    "How does propagation checking compare?",
                    "DNSChecker often shows more geographic resolver dots. DomainPreflight uses five resolvers and pairs results with email-specific follow-up checks.",
                ),
                (
                    "Does DNSChecker check DMARC alignment?",
                    "It doesn't specialise in alignment — DomainPreflight does, including provider-specific gaps.",
                ),
                (
                    "Which is better for global DNS propagation?",
                    "DNSChecker if you want a wide map of resolvers. DomainPreflight if you want propagation plus mail auth in one project.",
                ),
                (
                    "Which is better for email setup?",
                    "DomainPreflight — it interprets SPF/DKIM/DMARC for deliverability, not just raw TXT strings.",
                ),
                (
                    "Can I use both on launch day?",
                    "Yes — use DNSChecker for worldwide visibility, DomainPreflight to confirm mail auth and alignment after TTLs settle.",
                ),
            ],
        ),
        (
            "dmarc-analyzer",
            "DomainPreflight vs DMARC Analyzer — Comparison",
            "Validity's DMARC Analyzer is paid monitoring; DomainPreflight is free pre-flight plus XML paste analysis.",
            "DomainPreflight vs DMARC Analyzer",
            "DomainPreflight vs DMARC Analyzer",
            "DMARC Analyzer (by Validity) is a paid DMARC reporting platform. DomainPreflight is a free pre-flight tool with alignment detection and a built-in DMARC XML report analyzer.",
            """      <h2>Key differences</h2>
      <ul>
        <li><strong>DMARC Analyzer:</strong> ongoing monitoring, paid tiers, enterprise reporting</li>
        <li><strong>DomainPreflight:</strong> free pre-flight checks + manual XML analysis, no account</li>
      </ul>

      <h2>Where DMARC Analyzer wins</h2>
      <ul>
        <li>Hosted continuous aggregate ingestion</li>
        <li>Team workflows and vendor-style support</li>
      </ul>

      <h2>Where DomainPreflight wins</h2>
      <ul>
        <li>Alignment engine with provider fixes before you pay</li>
        <li>Paste XML when you have it — no subscription</li>
        <li>Full DNS + mail stack beyond DMARC alone</li>
      </ul>

      <div class="tool-cta">
        <p>Fix alignment first — paste XML in the analyzer</p>
        <p><a href="https://domainpreflight.dev/">DNS Preflight →</a> · <a href="https://domainpreflight.dev/dmarc/">DMARC Report Analyzer →</a></p>
      </div>""",
            [
                (
                    "Is DMARC Analyzer free?",
                    "It's a commercial platform with paid plans for ongoing monitoring. DomainPreflight's browser tools are free.",
                ),
                (
                    "Does DomainPreflight replace DMARC Analyzer?",
                    "Not for hosted 24/7 monitoring — it replaces the need for expensive tools if you only need diagnosis, fixes, and occasional XML analysis.",
                ),
                (
                    "How does DMARC XML analysis compare?",
                    "DomainPreflight's analyzer lets you paste aggregate XML for a visual summary. DMARC Analyzer is built around continuous ingestion.",
                ),
                (
                    "Which is better for ongoing monitoring?",
                    "DMARC Analyzer or similar paid platforms. DomainPreflight is manual scan + paste today.",
                ),
                (
                    "Which should I use for first-time DMARC setup?",
                    "DomainPreflight — it shows alignment gaps and copy-paste paths. Add paid monitoring later if your org needs it.",
                ),
            ],
        ),
    ]

    for row in pages:
        slug, title, meta, h1, crumb, sub, body, faqs = row
        html = build(slug, title, meta, h1, crumb, sub, body, faqs)
        out = VS / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print("Wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
