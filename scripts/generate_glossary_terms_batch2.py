#!/usr/bin/env python3
"""Generate 17 glossary term pages — batch 2."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOSS = ROOT / "glossary"

STYLE_EXTRA = """
    .breadcrumb { font-size: 0.8rem; color: var(--text2); margin-bottom: 1.25rem; line-height: 1.5; }
    .breadcrumb a { color: var(--purple); text-decoration: none; }
    .breadcrumb a:hover { text-decoration: underline; }
    .faq-section h3 { font-size: 0.95rem; font-weight: 600; color: var(--text); margin: 1.5rem 0 0.4rem; }
    .faq-section p { margin-bottom: 0.5rem; }
    .glossary-links { margin: 1.5rem 0; padding: 1rem 1.15rem; background: var(--bg2); border: 1px solid var(--border); border-radius: 10px; font-size: 0.85rem; color: var(--text2); }
    .glossary-links a { color: var(--purple); text-decoration: none; }
    .glossary-links a:hover { text-decoration: underline; }
    .internal-links { margin-top: 2rem; padding-top: 1.25rem; border-top: 1px solid var(--border); font-size: 0.88rem; }
    .internal-links a { color: var(--purple); text-decoration: none; }
    .internal-links a:hover { text-decoration: underline; }
"""

NAV = """      <nav>
        <a href="/">DNS Preflight</a>
        <a href="/email/">Email</a>
        <a href="/whois/">WHOIS</a>
        <a href="/dangling/">Dangling Records</a>
        <a href="/typosquat/">Typosquat</a>
        <a href="/propagation/">Propagation</a>
        <a href="/dmarc/">DMARC Report</a>
        <a href="/glossary/">Glossary</a>
      </nav>"""

FOOTER = """  <footer>
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
  </footer>"""


def page(
    slug: str,
    title: str,
    meta: str,
    term_name: str,
    first_p: str,
    body_html: str,
    faqs: list[tuple[str, str]],
    links_html: str | None = None,
) -> str:
    base = f"https://domainpreflight.dev/glossary/{slug}/"
    dt = {
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "name": term_name,
        "description": first_p,
        "inDefinedTermSet": "https://domainpreflight.dev/glossary/",
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
            {"@type": "ListItem", "position": 2, "name": "Glossary", "item": "https://domainpreflight.dev/glossary/"},
            {"@type": "ListItem", "position": 3, "name": term_name, "item": base},
        ],
    }
    faq_body = "\n".join(
        f'        <h3>{q}</h3>\n        <p>{a}</p>' for q, a in faqs
    )
    links_block = ""
    if links_html:
        links_block = f'\n      <div class="glossary-links"><strong>Also read:</strong> {links_html}</div>\n'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — DomainPreflight Glossary</title>
  <meta name="description" content="{meta}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{base}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script type="application/ld+json">
  {json.dumps(dt, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
  {json.dumps(faqpage, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
  {json.dumps(crumbs, ensure_ascii=False, separators=(",", ":"))}
  </script>
  <script defer src="https://cloud.umami.is/script.js" data-website-id="27fc19d2-1ff5-4478-946a-b96cc7d5daf8"></script>
  <style>
    :root {{
      --bg: #0B0D14;
      --bg2: #10131f;
      --bg3: #161924;
      --border: #1e2236;
      --purple: #6c63ff;
      --text: #e2e4f0;
      --text2: #8a8fb5;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'JetBrains Mono', monospace;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      line-height: 1.6;
    }}
    header {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(11, 13, 20, 0.7);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      padding: 0.75rem 1.5rem;
    }}
    .header-inner {{
      max-width: 1200px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.75rem;
    }}
    .logo {{ display: flex; align-items: center; gap: 0.5rem; font-weight: 600; font-size: 1rem; }}
    .logo a {{ color: var(--purple); text-decoration: none; }}
    .pill {{ font-size: 0.65rem; padding: 0.2rem 0.5rem; border-radius: 999px; background: var(--bg3); border: 1px solid var(--border); margin-left: 0.5rem; color: var(--text2); }}
    nav {{ display: flex; gap: 1rem; align-items: center; flex-wrap: wrap; }}
    nav a {{ color: var(--text2); text-decoration: none; font-size: 0.8rem; }}
    nav a:hover {{ color: var(--text); }}
    main {{ max-width: 760px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }}
    .hero-label {{ font-size: 0.7rem; letter-spacing: 0.15em; font-weight: 600; text-transform: uppercase; color: var(--purple); margin-bottom: 0.5rem; }}
    h1 {{ font-size: clamp(1.35rem, 3.5vw, 1.85rem); font-weight: 600; margin-bottom: 1rem; line-height: 1.3; }}
    article > p:first-of-type {{ color: var(--text2); font-size: 0.9rem; margin-bottom: 1.5rem; }}
    article h2 {{ font-size: 1.05rem; font-weight: 600; margin: 1.75rem 0 0.65rem; color: var(--text); }}
    article p {{ color: var(--text2); font-size: 0.9rem; margin-bottom: 0.75rem; }}
    article ul {{ color: var(--text2); font-size: 0.9rem; margin: 0.5rem 0 1rem 1.25rem; }}
    article li {{ margin-bottom: 0.35rem; }}
    .tool-cta {{
      margin-top: 2rem;
      padding: 1.25rem 1.5rem;
      background: var(--bg2);
      border: 1px solid var(--border);
      border-radius: 12px;
      border-left: 3px solid var(--purple);
    }}
    .tool-cta p {{ margin-bottom: 0.75rem; color: var(--text); }}
    .tool-cta a {{ color: var(--purple); font-weight: 600; text-decoration: none; }}
    .tool-cta a:hover {{ text-decoration: underline; }}
    footer {{
      border-top: 1px solid var(--border);
      padding: 0;
      background: var(--bg2);
    }}
    .footer-inner {{ max-width: 1200px; margin: 0 auto; padding: 1.25rem 1.5rem; }}
    .footer-disclaimer {{ color: var(--text2); font-size: 0.75rem; line-height: 1.5; margin-bottom: 1rem; }}
    .footer-bar {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 1rem;
      padding: 1rem 1.5rem;
      border-top: 1px solid var(--border);
      font-size: 0.8rem;
      color: var(--text2);
      max-width: 1200px;
      margin: 0 auto;
    }}
    .footer-bar a {{ color: var(--text2); text-decoration: none; }}
    .footer-bar a:hover {{ color: var(--text); }}
{STYLE_EXTRA}
  </style>
  <link rel="icon" type="image/png" href="/favicon.png">
</head>
<body>
  <header>
    <div class="header-inner">
      <div class="logo">
        <a href="/">DomainPreflight.</a>
        <span class="pill">BETA</span>
      </div>
{NAV}
    </div>
  </header>

  <main>
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="https://domainpreflight.dev/">Home</a> <span aria-hidden="true">›</span> <a href="/glossary/">Glossary</a> <span aria-hidden="true">›</span> {term_name}</nav>
    <article>
      <p class="hero-label">Glossary</p>
      <h1>{title}</h1>
      <p>{first_p}</p>
{body_html}{links_block}
      <section class="faq-section" aria-label="FAQ">
        <h2>FAQ</h2>
{faq_body}
      </section>

      <div class="internal-links">
        <p><a href="/glossary/">← All glossary terms</a></p>
      </div>
    </article>
  </main>

{FOOTER}
</body>
</html>
"""


def main():
    terms: list[dict] = [
        {
            "slug": "email-deliverability",
            "title": "Email Deliverability — What It Is and How to Improve It",
            "meta": "Email deliverability is whether mail reaches the inbox — not spam — based on auth, reputation, and content.",
            "term_name": "Email Deliverability",
            "first_p": "Email deliverability is the ability of an email to reach the recipient's inbox rather than their spam folder or being rejected entirely. It is determined by a combination of sender reputation, authentication records (SPF, DKIM, DMARC), IP reputation, content quality, and recipient engagement. High deliverability means your legitimate emails consistently reach inboxes.",
            "body": """      <h2>What Affects Email Deliverability</h2>
      <ul>
        <li><strong>Sender authentication:</strong> SPF, DKIM, DMARC</li>
        <li><strong>IP reputation:</strong> is your sending IP on blocklists</li>
        <li><strong>Domain reputation:</strong> how long you've been sending, bounce rates, spam complaints</li>
        <li><strong>Content:</strong> spam trigger words, HTML/text ratio</li>
        <li><strong>Engagement:</strong> open rates, click rates, unsubscribes</li>
      </ul>

      <h2>How to Check Your Deliverability</h2>
      <p>Run DNS Preflight with your sending IP and domain — it checks authentication records, IP reputation, and blocklist status in one pass.</p>

      <div class="tool-cta">
        <p>Run a full check on domainpreflight.dev</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>""",
            "links": '<a href="https://domainpreflight.dev/">DNS Preflight</a> · <a href="/glossary/dmarc/">DMARC</a> · <a href="/glossary/spf-record/">SPF record</a> · <a href="/glossary/dkim/">DKIM</a>',
            "faqs": [
                (
                    "What is email deliverability?",
                    "Email deliverability is the rate at which your emails successfully reach the inbox rather than spam folders or being rejected. It depends on authentication, reputation, and content.",
                ),
                (
                    "What is the difference between delivery and deliverability?",
                    "Delivery means the email was accepted by the receiving server. Deliverability means it reached the inbox. An email can be delivered (not bounced) but still go to spam.",
                ),
                (
                    "How do I improve email deliverability?",
                    "Set up SPF, DKIM, and DMARC correctly, ensure your sending IP has a PTR record, keep bounce rates under 2%, and warm up new IPs gradually.",
                ),
            ],
        },
        {
            "slug": "blacklist",
            "title": "Email Blacklist — What It Is and How to Get Delisted",
            "meta": "An email blacklist (DNSBL) lists IPs and domains known for spam — receivers may reject mail before SPF or DKIM.",
            "term_name": "Email Blacklist (Blocklist)",
            "first_p": "An email blacklist (also called a blocklist or DNSBL) is a real-time database of IP addresses and domains known to send spam. Mail servers query these lists when an email arrives — if your sending IP appears on a major blacklist like Spamhaus, your email may be rejected before SPF or DKIM is even checked.",
            "body": """      <h2>Major Email Blacklists</h2>
      <ul>
        <li><strong>Spamhaus ZEN</strong> — most widely used, covers multiple Spamhaus lists</li>
        <li><strong>SpamCop</strong> — crowd-sourced spam reports</li>
        <li><strong>Barracuda</strong> — used by many corporate mail servers</li>
        <li><strong>SORBS</strong> — aggregates multiple threat categories</li>
      </ul>

      <h2>How to Check If You're Blacklisted</h2>
      <p>Run DomainPreflight Email Deliverability with your sending IP — checks 10+ blacklists instantly.</p>

      <h2>How to Get Delisted</h2>
      <p>Fix the underlying issue first. Then submit a removal request at each list's website. Most removals take 24-72 hours.</p>

      <div class="tool-cta">
        <p>Check your IP against major lists</p>
        <a href="https://domainpreflight.dev/email/">Open Email Deliverability →</a>
      </div>""",
            "links": '<a href="https://domainpreflight.dev/email/">Email Deliverability</a> · <a href="/error/blacklisted-ip/">Blacklisted IP</a>',
            "faqs": [
                (
                    "What is an email blacklist?",
                    "A database of IP addresses and domains known to send spam. Mail servers check these lists to decide whether to accept or reject incoming email.",
                ),
                (
                    "How do I check if my IP is blacklisted?",
                    "Use DomainPreflight Email Deliverability — enter your sending IP and it checks 10+ major blacklists in seconds.",
                ),
                (
                    "How long does blacklist removal take?",
                    "Spamhaus: 24-48 hours. SpamCop: auto-expires in 24-48 hours when spam stops. Barracuda: 12-24 hours after delisting request.",
                ),
            ],
        },
        {
            "slug": "mx-record",
            "title": "MX Record — Mail Exchanger Explained",
            "meta": "An MX record tells the internet which server receives mail for your domain — without it, you can't receive email.",
            "term_name": "MX Record",
            "first_p": "An MX (Mail Exchanger) record is a DNS record that specifies which mail server is responsible for receiving email for a domain. When someone sends email to you@yourdomain.com, their mail server looks up the MX record for yourdomain.com to find where to deliver it. Without an MX record, your domain cannot receive any email.",
            "body": """      <h2>MX Record Priority</h2>
      <p>MX records have a priority value (preference number). Lower number = higher priority. When you have multiple mail servers, the lowest priority number is tried first.</p>

      <h2>Common MX Record Values</h2>
      <ul>
        <li><strong>Google Workspace:</strong> aspmx.l.google.com (1)</li>
        <li><strong>Microsoft 365:</strong> [tenant].mail.protection.outlook.com (0)</li>
        <li><strong>Fastmail:</strong> in1-smtp.messagingengine.com (10)</li>
        <li><strong>Zoho:</strong> mx.zoho.com (10)</li>
      </ul>

      <h2>How to Check Your MX Records</h2>
      <p>Run DNS Preflight on your domain — MX records appear in the DNS check results.</p>

      <div class="tool-cta">
        <p>Verify MX in seconds</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>""",
            "links": None,
            "faqs": [
                (
                    "What is an MX record?",
                    "An MX record tells other mail servers where to deliver email for your domain. Without one, your domain cannot receive email.",
                ),
                (
                    "What does MX record priority mean?",
                    "The priority number determines which mail server is tried first. Lower numbers have higher priority.",
                ),
                (
                    "Can I have multiple MX records?",
                    "Yes — multiple MX records provide redundancy. If the highest-priority server is unavailable, the next one is tried automatically.",
                ),
            ],
        },
        {
            "slug": "dmarc-policy",
            "title": "DMARC Policy — none, quarantine, reject Explained",
            "meta": "DMARC policy (p=) tells receivers whether to monitor, quarantine, or reject mail that fails DMARC — start at none, tighten over time.",
            "term_name": "DMARC Policy",
            "first_p": "A DMARC policy (the p= tag in your DMARC record) tells receiving mail servers what to do with emails that fail DMARC checks. There are three policy levels: p=none (monitor only, deliver everything), p=quarantine (send failures to spam), and p=reject (block failures entirely). Start with p=none and progressively tighten after reviewing aggregate reports.",
            "body": """      <h2>The Three Policy Levels</h2>
      <ul>
        <li><strong>p=none</strong> — monitoring mode. Failures are reported but all email is delivered. Safe starting point.</li>
        <li><strong>p=quarantine</strong> — failures go to spam folder. Partial protection.</li>
        <li><strong>p=reject</strong> — failures are blocked entirely. Full protection. Use only after confirming all legitimate senders are aligned.</li>
      </ul>

      <h2>Recommended Rollout</h2>
      <ul>
        <li>Week 1-4: p=none + rua= reporting</li>
        <li>Week 4-8: p=quarantine (review reports first)</li>
        <li>Week 8+: p=reject (once all senders clean)</li>
      </ul>

      <div class="tool-cta">
        <p>Check your live DMARC TXT</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>""",
            "links": '<a href="/glossary/dmarc/">DMARC</a> · <a href="/glossary/dmarc-alignment/">DMARC alignment</a> · <a href="https://domainpreflight.dev/">DNS Preflight</a>',
            "faqs": [
                (
                    "What is DMARC policy?",
                    "The p= tag in your DMARC record that tells receivers what to do with emails failing DMARC — monitor, quarantine, or reject.",
                ),
                (
                    "What is the safest DMARC policy to start with?",
                    "p=none — it collects reports without affecting delivery. Use it to identify all your legitimate senders before enforcing.",
                ),
                (
                    "When should I move to p=reject?",
                    "After at least 2-4 weeks of DMARC aggregate reports showing all legitimate senders are aligned with no failures.",
                ),
            ],
        },
        {
            "slug": "spf-permerror",
            "title": "SPF PermError — Cause and Fix",
            "meta": "SPF PermError means your SPF can't be evaluated — usually too many lookups or bad syntax. Many receivers treat it like a hard fail.",
            "term_name": "SPF PermError",
            "first_p": "SPF PermError (Permanent Error) is returned when an SPF record cannot be evaluated — most commonly because it exceeds the 10 DNS lookup limit or contains a syntax error. Unlike SoftFail or Fail, PermError means the SPF record is technically invalid. Many receiving servers treat PermError the same as a hard fail and reject or spam-folder the email.",
            "body": """      <h2>Common Causes</h2>
      <ul>
        <li>Too many include: statements (over 10 lookups)</li>
        <li>Multiple SPF records on the same domain</li>
        <li>Syntax error in the SPF record</li>
        <li>Circular include: references</li>
      </ul>

      <h2>How to Diagnose</h2>
      <p>Run DNS Preflight — the SPF recursive tree shows your lookup count and flags PermError causes immediately.</p>

      <div class="tool-cta">
        <p>Expand the SPF tree on domainpreflight.dev</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>""",
            "links": '<a href="/error/spf-permerror/">SPF PermError error page</a> · <a href="/fix/spf/too-many-lookups/">Too many lookups fix</a> · <a href="/glossary/spf-record/">SPF record</a>',
            "faqs": [
                (
                    "What is SPF PermError?",
                    "A permanent error meaning your SPF record is invalid — usually too many DNS lookups or a syntax error. Receivers may reject email when they see PermError.",
                ),
                (
                    "How do I fix SPF PermError?",
                    "Most commonly by reducing DNS lookups below 10 — either remove some include: statements or flatten them to IP addresses.",
                ),
                (
                    "Does SPF PermError affect DMARC?",
                    "Yes. SPF PermError means SPF alignment fails. DMARC can still pass if DKIM alignment passes independently.",
                ),
            ],
        },
        {
            "slug": "email-authentication",
            "title": "Email Authentication — SPF, DKIM, and DMARC Explained",
            "meta": "Email authentication uses SPF, DKIM, and DMARC in DNS to prove who sent mail — together they reduce spoofing.",
            "term_name": "Email Authentication",
            "first_p": "Email authentication is a set of DNS-based standards — SPF, DKIM, and DMARC — that verify an email was genuinely sent by the domain it claims to be from. Without authentication, anyone can forge the From: header and send email impersonating your domain. All three standards work together: SPF authorises sending servers, DKIM signs messages, and DMARC enforces policy and provides reporting.",
            "body": """      <h2>The Three Standards</h2>
      <ul>
        <li><strong>SPF</strong> — lists authorised sending servers in DNS</li>
        <li><strong>DKIM</strong> — adds cryptographic signatures to email</li>
        <li><strong>DMARC</strong> — enforces policy and ties SPF/DKIM to the From: domain</li>
      </ul>

      <h2>Why All Three Matter</h2>
      <p>SPF alone can be bypassed. DKIM alone doesn't prevent From: forgery. DMARC requires both to align with your From: domain — closing the gap.</p>

      <div class="tool-cta">
        <p>Check all three on your domain</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>""",
            "links": '<a href="/glossary/spf-record/">SPF record</a> · <a href="/glossary/dkim/">DKIM</a> · <a href="/glossary/dmarc/">DMARC</a> · <a href="https://domainpreflight.dev/">DNS Preflight</a>',
            "faqs": [
                (
                    "What is email authentication?",
                    "The set of DNS standards (SPF, DKIM, DMARC) that verify email was sent by an authorised server for the claimed domain.",
                ),
                (
                    "Do I need all three — SPF, DKIM, and DMARC?",
                    "Yes for full protection. SPF and DKIM alone have gaps. DMARC ties them together and provides reporting.",
                ),
                (
                    "Is email authentication required?",
                    "Gmail and Yahoo now require DMARC for bulk senders (February 2024). It is effectively mandatory for anyone sending significant email volume.",
                ),
            ],
        },
        {
            "slug": "dmarc-aggregate-report",
            "title": "DMARC Aggregate Report — How to Read It",
            "meta": "DMARC aggregate (RUA) reports are daily XML files showing who sent as your domain and whether SPF/DKIM passed.",
            "term_name": "DMARC Aggregate Report",
            "first_p": "A DMARC aggregate report (RUA report) is a daily XML file sent by receiving mail servers — Google, Microsoft, Yahoo — showing every IP address that sent email using your domain, and whether those emails passed SPF and DKIM. These reports are the primary tool for identifying unauthorised senders and verifying that legitimate senders are properly aligned before tightening your DMARC policy.",
            "body": """      <h2>How to Get Reports</h2>
      <p>Add <code>rua=mailto:dmarc@yourdomain.com</code> to your DMARC record. Reports arrive as .zip attachments containing XML files.</p>

      <h2>How to Read Reports</h2>
      <p>Use DomainPreflight DMARC Report Analyzer — paste the XML and get a visual summary showing passing and failing senders, spoofing detection, and policy upgrade recommendations.</p>

      <div class="tool-cta">
        <p>Paste aggregate XML into the analyzer</p>
        <a href="https://domainpreflight.dev/dmarc/">Open DMARC Report Analyzer →</a>
      </div>""",
            "links": '<a href="https://domainpreflight.dev/dmarc/">DMARC Report Analyzer</a> · <a href="/glossary/dmarc/">DMARC</a>',
            "faqs": [
                (
                    "What is a DMARC aggregate report?",
                    "A daily XML report from major mail providers showing every IP that sent email as your domain and whether SPF/DKIM passed.",
                ),
                (
                    "How do I receive DMARC reports?",
                    "Add rua=mailto:your@email.com to your DMARC TXT record. Reports arrive as .zip files containing XML.",
                ),
                (
                    "How do I read DMARC XML reports?",
                    "Use DomainPreflight's DMARC Report Analyzer — paste the XML for a visual summary of senders, pass/fail rates, and spoofing detection.",
                ),
            ],
        },
        {
            "slug": "rdns",
            "title": "Reverse DNS (rDNS) — What It Is and Why It Matters",
            "meta": "Reverse DNS maps an IP to a hostname (PTR). Mail servers use FCrDNS to validate sending infrastructure.",
            "term_name": "Reverse DNS (rDNS)",
            "first_p": "Reverse DNS (rDNS) is the process of resolving an IP address back to a hostname — the reverse of a standard DNS lookup. For email, receiving mail servers perform a reverse DNS lookup on your sending IP to verify it has a valid PTR record. An IP with no reverse DNS or with a PTR that doesn't forward-confirm is a common cause of email rejection and spam folder placement.",
            "body": """      <h2>Forward-Confirmed Reverse DNS (FCrDNS)</h2>
      <p>A valid reverse DNS setup requires both steps:</p>
      <ol style="color: var(--text2); font-size: 0.9rem; margin: 0.5rem 0 1rem 1.25rem;">
        <li>IP → PTR lookup → hostname</li>
        <li>Hostname → A lookup → same IP</li>
      </ol>
      <p>If step 2 returns a different IP, the check fails even though a PTR exists.</p>

      <h2>Who Controls rDNS</h2>
      <p>Your hosting provider or ISP — not your domain registrar. Set it in your VPS control panel.</p>

      <div class="tool-cta">
        <p>Check PTR with your sending IP</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>""",
            "links": '<a href="/glossary/ptr-record/">PTR record</a> · <a href="/error/ptr-mismatch/">PTR mismatch</a> · <a href="https://domainpreflight.dev/">DNS Preflight</a>',
            "faqs": [
                (
                    "What is reverse DNS?",
                    "The process of resolving an IP address back to a hostname using a PTR record. Mail servers use this to verify your sending infrastructure.",
                ),
                (
                    "Why does reverse DNS matter for email?",
                    "Many mail servers reject email from IPs with no PTR record or where the PTR hostname doesn't forward-resolve to the same IP.",
                ),
                (
                    "Who sets up reverse DNS?",
                    "Your hosting provider or ISP — not your domain registrar. Look for \"Reverse DNS\" in your VPS control panel.",
                ),
            ],
        },
        {
            "slug": "spf-softfail",
            "title": "SPF SoftFail (~all) — What It Means",
            "meta": "SPF SoftFail (~all) means the IP isn't in SPF but you asked receivers to treat it as suspicious, not always hard-fail.",
            "term_name": "SPF SoftFail",
            "first_p": "SPF SoftFail (~all) is a result returned when a sending IP is not listed in the SPF record, but the domain owner has indicated this should be treated as suspicious rather than a hard failure. Emails that trigger SoftFail are typically delivered but may be marked as suspicious or placed in spam, depending on the receiver's policy and the domain's DMARC configuration.",
            "body": """      <h2>SoftFail vs Fail vs Pass</h2>
      <ul>
        <li><strong>~all (softfail):</strong> not authorised, treat as suspicious</li>
        <li><strong>-all (hardfail/fail):</strong> not authorised, reject</li>
        <li><strong>+all (pass):</strong> everything passes — never use</li>
        <li><strong>?all (neutral):</strong> no policy — avoid</li>
      </ul>

      <h2>When to Use ~all</h2>
      <p>Use ~all while setting up email authentication and monitoring. Switch to -all once all legitimate senders are confirmed in your SPF.</p>

      <div class="tool-cta">
        <p>Validate your SPF TXT</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>""",
            "links": '<a href="/fix/spf/softfail-vs-hardfail/">SoftFail vs HardFail</a> · <a href="/glossary/spf-record/">SPF record</a>',
            "faqs": [
                (
                    "What does SPF SoftFail mean?",
                    "The sending IP isn't in your SPF record, but you've indicated failures should be treated as suspicious rather than hard failures. Email is usually delivered but may go to spam.",
                ),
                (
                    "Should I use ~all or -all?",
                    "Start with ~all while monitoring. Switch to -all once all your legitimate senders are in your SPF record and verified clean.",
                ),
                (
                    "Does SPF SoftFail affect DMARC?",
                    "SoftFail counts as SPF failure for DMARC alignment purposes. DMARC can still pass if DKIM alignment passes.",
                ),
            ],
        },
        {
            "slug": "dkim-selector",
            "title": "DKIM Selector — What It Is and How It Works",
            "meta": "A DKIM selector names which DNS key verifies a signature — it appears as s= in DKIM-Signature headers.",
            "term_name": "DKIM Selector",
            "first_p": "A DKIM selector is a string that identifies which DKIM public key to use when verifying an email's signature. It appears in the DKIM-Signature header as s=[selector] and must match a DNS TXT record published at [selector]._domainkey.yourdomain.com. Selectors allow a domain to have multiple DKIM keys — useful when using different sending providers or rotating keys.",
            "body": """      <h2>Common Selectors by Provider</h2>
      <ul>
        <li><strong>google</strong> — Google Workspace</li>
        <li><strong>selector1, selector2</strong> — Microsoft 365</li>
        <li><strong>s1, s2</strong> — SendGrid</li>
        <li><strong>k1</strong> — Mailgun</li>
        <li><strong>pm</strong> — Postmark</li>
        <li><strong>default, mail, dkim</strong> — common generic names</li>
      </ul>

      <h2>How to Find Your Selector</h2>
      <p>Check the DKIM-Signature header in a raw email. The s= tag shows which selector was used.</p>

      <div class="tool-cta">
        <p>Probe DKIM DNS in DNS Preflight</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>""",
            "links": '<a href="/fix/dkim/selector/">DKIM selector fix</a> · <a href="/glossary/dkim/">DKIM</a>',
            "faqs": [
                (
                    "What is a DKIM selector?",
                    "A label that identifies which DKIM public key to use for verification. It appears in the DKIM-Signature header and must match a DNS TXT record.",
                ),
                (
                    "Can I have multiple DKIM selectors?",
                    "Yes — each selector is independent. Multiple selectors are used when you have different sending providers or during key rotation.",
                ),
                (
                    "How do I find which selector my emails use?",
                    "Check the raw email headers — look for DKIM-Signature: s=[selector].",
                ),
            ],
        },
        {
            "slug": "cname-record",
            "title": "CNAME Record — What It Is and How to Use It",
            "meta": "A CNAME maps one hostname to another — ESPs use CNAMEs for DKIM alignment and branded sending.",
            "term_name": "CNAME Record",
            "first_p": "A CNAME (Canonical Name) record is a DNS record that maps one domain name to another. Instead of pointing to an IP address directly, a CNAME points to another hostname whose IP is resolved separately. Email providers like SendGrid and Microsoft 365 use CNAME records for DKIM alignment — your CNAME points to their servers, letting them sign email with your domain.",
            "body": """      <h2>CNAME vs A Record</h2>
      <ul>
        <li><strong>A record:</strong> hostname → IP address</li>
        <li><strong>CNAME record:</strong> hostname → another hostname</li>
      </ul>

      <h2>CNAME Restrictions</h2>
      <ul>
        <li>Cannot be used at root domain (@) — use A record or ALIAS/ANAME instead</li>
        <li>Cannot coexist with other record types at the same hostname</li>
        <li>Avoid CNAME chains (CNAME → CNAME → CNAME)</li>
      </ul>

      <div class="tool-cta">
        <p>Check DNS after you publish records</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>""",
            "links": '<a href="/glossary/subdomain-takeover/">Subdomain takeover</a> · <a href="/fix/dmarc/sendgrid/">SendGrid DMARC</a>',
            "faqs": [
                (
                    "What is a CNAME record?",
                    "A DNS record that maps one hostname to another hostname instead of directly to an IP address.",
                ),
                (
                    "Can I use a CNAME at my root domain?",
                    "No. CNAMEs cannot be used at the apex (root) domain because they would conflict with required SOA and NS records. Use an A record or ALIAS/ANAME instead.",
                ),
                (
                    "Why do email providers use CNAMEs for DKIM?",
                    "CNAMEs let providers control the DKIM key on their end — they can rotate keys without you updating DNS. Your CNAME always points to their current key.",
                ),
            ],
        },
        {
            "slug": "txt-record",
            "title": "TXT Record — DNS Text Records Explained",
            "meta": "TXT records store text in DNS — SPF, DKIM, DMARC, and verification tokens all use them.",
            "term_name": "TXT Record",
            "first_p": "A DNS TXT record stores arbitrary text data associated with a domain. TXT records are used for email authentication (SPF, DKIM, DMARC), domain verification (Google, Microsoft), and various security configurations. Most email authentication setup involves publishing TXT records — SPF lives entirely in a TXT record, DKIM public keys are published as TXT records, and DMARC policies are TXT records.",
            "body": """      <h2>Common TXT Record Uses</h2>
      <ul>
        <li><code>v=spf1 ... ~all</code> → SPF record</li>
        <li><code>v=DKIM1; k=rsa; p=...</code> → DKIM public key</li>
        <li><code>v=DMARC1; p=none; rua=...</code> → DMARC policy</li>
        <li><code>google-site-verification=...</code> → domain verification</li>
      </ul>

      <h2>TXT Record Limits</h2>
      <ul>
        <li>Single string: 255 characters max</li>
        <li>Multiple strings: combine in one record</li>
        <li>SPF: only ONE TXT record starting with v=spf1</li>
      </ul>

      <div class="tool-cta">
        <p>Read live TXT from DNS Preflight</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>""",
            "links": '<a href="/glossary/spf-record/">SPF record</a> · <a href="/glossary/dkim/">DKIM</a> · <a href="/glossary/dmarc/">DMARC</a>',
            "faqs": [
                (
                    "What is a DNS TXT record?",
                    "A DNS record that stores text data. Used for SPF, DKIM, DMARC, and domain verification.",
                ),
                (
                    "Can I have multiple TXT records?",
                    "Yes — except for SPF. You can have multiple TXT records but only one can start with v=spf1.",
                ),
                (
                    "Why is my TXT record not working?",
                    "Check for extra spaces, incorrect quote formatting, or truncation by your DNS provider. Long TXT records must be properly joined.",
                ),
            ],
        },
        {
            "slug": "whois",
            "title": "WHOIS — Domain Registration Lookup Explained",
            "meta": "WHOIS and RDAP return domain registration data — registrar, expiry, nameservers, and contacts.",
            "term_name": "WHOIS",
            "first_p": "WHOIS is a query protocol that returns registration information about a domain name — including the registrar, registration date, expiry date, name servers, and registrant contact details (where not privacy-protected). Modern WHOIS lookups use RDAP (Registration Data Access Protocol), a JSON-based successor that is more reliable and structured than the original port-43 WHOIS protocol.",
            "body": """      <h2>What WHOIS Shows</h2>
      <ul>
        <li>Registrar name and IANA ID</li>
        <li>Registration and expiry dates</li>
        <li>Name servers</li>
        <li>Domain status (active, locked, expired)</li>
        <li>Registrant contact (may be privacy-protected)</li>
      </ul>

      <h2>WHOIS Privacy</h2>
      <p>Most registrars offer WHOIS privacy (proxy registration) that replaces your personal details with the registrar's contact info.</p>

      <div class="tool-cta">
        <p>Lookup expiry and registrar via RDAP</p>
        <a href="https://domainpreflight.dev/whois/">Open WHOIS tool →</a>
      </div>""",
            "links": '<a href="https://domainpreflight.dev/whois/">WHOIS / RDAP</a>',
            "faqs": [
                (
                    "What is WHOIS?",
                    "A protocol for looking up domain registration information — registrar, expiry date, name servers, and owner details.",
                ),
                (
                    "What is RDAP vs WHOIS?",
                    "RDAP is the modern replacement for WHOIS. It returns structured JSON data and is more reliable across all TLDs. DomainPreflight uses RDAP.",
                ),
                (
                    "Can I hide my details from WHOIS?",
                    "Yes — most registrars offer WHOIS privacy that replaces your details with proxy contact information.",
                ),
            ],
        },
        {
            "slug": "domain-expiry",
            "title": "Domain Expiry — Risks and How to Monitor It",
            "meta": "When a domain expires it stops resolving — sites and email go down. Monitor expiry and enable auto-renew.",
            "term_name": "Domain Expiry",
            "first_p": "Domain expiry occurs when a registered domain name is not renewed before its expiry date, causing it to lapse and potentially become available for anyone to register. An expired domain immediately stops resolving — taking down your website, email, and all DNS-dependent services. Most registrars offer a grace period of 30-45 days, but email often fails before the domain officially expires.",
            "body": """      <h2>Expiry Risk Tiers</h2>
      <ul>
        <li><strong>Critical:</strong> under 30 days — act immediately</li>
        <li><strong>Warning:</strong> 30-60 days — schedule renewal</li>
        <li><strong>Safe:</strong> over 60 days — monitor regularly</li>
      </ul>

      <h2>How to Monitor Expiry</h2>
      <p>Use DomainPreflight WHOIS tool — shows exact expiry date and days remaining with colour-coded risk tier.</p>

      <div class="tool-cta">
        <p>Check expiry in one lookup</p>
        <a href="https://domainpreflight.dev/whois/">Open WHOIS tool →</a>
      </div>""",
            "links": '<a href="https://domainpreflight.dev/whois/">WHOIS tool</a> · <a href="/glossary/whois/">WHOIS</a>',
            "faqs": [
                (
                    "What happens when a domain expires?",
                    "It stops resolving — your website goes down, email stops working, and all DNS records become inaccessible. Most registrars offer a grace period but email often fails first.",
                ),
                (
                    "How much notice do I get before a domain expires?",
                    "Most registrars send emails at 90, 60, 30, and 7 days before expiry. Enable auto-renew to avoid expiry entirely.",
                ),
                (
                    "Can someone steal my domain when it expires?",
                    "Yes. After the grace period, expired domains enter a redemption phase and then become available for anyone to register — including domain squatters.",
                ),
            ],
        },
        {
            "slug": "dnssec",
            "title": "DNSSEC — DNS Security Extensions Explained",
            "meta": "DNSSEC signs DNS answers so resolvers can detect tampering — separate from SPF/DKIM/DMARC for email.",
            "term_name": "DNSSEC",
            "first_p": "DNSSEC (DNS Security Extensions) is a suite of protocols that add cryptographic signatures to DNS records, allowing resolvers to verify that DNS responses are authentic and have not been tampered with. DNSSEC protects against DNS cache poisoning and man-in-the-middle attacks on DNS queries. It requires coordination between your DNS hosting provider and your domain registrar.",
            "body": """      <h2>How DNSSEC Works</h2>
      <p>Your DNS zone is signed with a private key. The corresponding public key is published in DNS and linked to your registrar via DS records. Resolvers use the chain of trust to verify every DNS response.</p>

      <h2>DNSSEC vs Email Authentication</h2>
      <p>DNSSEC protects DNS queries themselves — not email content. SPF, DKIM, and DMARC authenticate email. Both are independent but complementary.</p>

      <div class="tool-cta">
        <p>Start with email auth on DNS Preflight</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>""",
            "links": None,
            "faqs": [
                (
                    "What is DNSSEC?",
                    "A DNS extension that adds cryptographic signatures to verify DNS responses are authentic and unmodified.",
                ),
                (
                    "Do I need DNSSEC for email security?",
                    "DNSSEC is separate from email authentication. SPF, DKIM, and DMARC protect email. DNSSEC protects DNS queries. Both are good practice but independent.",
                ),
                (
                    "How do I enable DNSSEC?",
                    "Enable it in your DNS provider's dashboard, then publish the DS record at your domain registrar. Both steps are required.",
                ),
            ],
        },
        {
            "slug": "catch-all-address",
            "title": "Catch-All Email Address — Risks and Best Practice",
            "meta": "A catch-all inbox accepts mail to any address at your domain — it attracts spam and can hurt reputation.",
            "term_name": "Catch-All Email Address",
            "first_p": "A catch-all email address receives all email sent to any address at your domain — even addresses that don't exist. While useful for not missing email, catch-all configurations attract enormous volumes of spam and dictionary attacks, inflate bounce rates when misused, and can negatively affect your domain's sending reputation if the same domain is used for outbound email.",
            "body": """      <h2>The Risk</h2>
      <p>Spammers probe catch-all domains with dictionary attacks — sending to thousands of random addresses. Your server accepts them all, creating backscatter and reputation damage.</p>

      <h2>When Catch-All Makes Sense</h2>
      <p>Single-person domains where you want to receive email regardless of typos. Not recommended for organisations.</p>

      <div class="tool-cta">
        <p>Audit outbound reputation with Email + DNS Preflight</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>""",
            "links": '<a href="/email/">Email tool</a>',
            "faqs": [
                (
                    "What is a catch-all email address?",
                    "An email configuration that accepts all incoming email regardless of whether the specific address exists.",
                ),
                (
                    "Does a catch-all affect email deliverability?",
                    "Yes. Catch-all domains receive spam probing which can inflate bounce rates and damage sending reputation if mishandled.",
                ),
                (
                    "Should I use a catch-all?",
                    "Only for single-person domains where you want to avoid missing email. For organisations, use specific addresses and aliases instead.",
                ),
            ],
        },
        {
            "slug": "mail-exchanger",
            "title": "Mail Exchanger (MX) — Deep Dive",
            "meta": "A mail exchanger is the server named by MX records that receives mail for your domain on port 25.",
            "term_name": "Mail Exchanger",
            "first_p": "A mail exchanger is the server responsible for receiving email on behalf of a domain, identified by its MX DNS record. When an email is sent to you@yourdomain.com, the sending server looks up the MX record for yourdomain.com to find the mail exchanger's hostname, then connects to it on port 25 to deliver the message. The mail exchanger hostname must have a valid A record and should have a PTR record for full deliverability compliance.",
            "body": """      <h2>MX Record Requirements</h2>
      <ul>
        <li>Must point to a hostname, never an IP</li>
        <li>Hostname must have an A record</li>
        <li>Should have a PTR record for the IP</li>
        <li>Priority value determines preference order</li>
      </ul>

      <h2>Multiple Mail Exchangers</h2>
      <p>Multiple MX records with different priorities provide redundancy. If the primary is down, sending servers try the next priority.</p>

      <div class="tool-cta">
        <p>Inspect MX and DNS in one run</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>""",
            "links": '<a href="/glossary/mx-record/">MX record</a> · <a href="/glossary/ptr-record/">PTR record</a> · <a href="https://domainpreflight.dev/">DNS Preflight</a>',
            "faqs": [
                (
                    "What is a mail exchanger?",
                    "The server that receives email for a domain, identified by its MX record. Sending servers connect to it to deliver email.",
                ),
                (
                    "Can an MX record point to an IP address?",
                    "No. MX records must point to a hostname (A record), not directly to an IP. This is an RFC requirement.",
                ),
                (
                    "What happens if my mail exchanger is down?",
                    "Sending servers retry for up to 5 days. If you have multiple MX records, the next priority server is tried automatically.",
                ),
            ],
        },
    ]

    for t in terms:
        html = page(
            slug=t["slug"],
            title=t["title"],
            meta=t["meta"],
            term_name=t["term_name"],
            first_p=t["first_p"],
            body_html=t["body"],
            faqs=t["faqs"],
            links_html=t.get("links"),
        )
        out = GLOSS / t["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print("Wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
