#!/usr/bin/env python3
"""Generate blog/[slug]/index.html posts."""
from __future__ import annotations

import html as html_module
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"
DATE_ISO = "2026-03-19"
DATE_DISPLAY = "March 19, 2026"

FOOTER = """  <footer>
    <div class="footer-inner"><p class="footer-disclaimer">This is a free sanity check — not legal or production advice. Verify DNS and mail in your own stack before you change anything.</p></div>
    <div class="footer-bar">
      <div><span>DomainPreflight by MetricLogic ·</span> <a href="https://configclarity.dev" target="_blank" rel="noopener">ConfigClarity</a> <span>·</span> <a href="https://domainpreflight.dev" target="_blank" rel="noopener">DomainPreflight</a> <span>·</span> <a href="https://packagefix.dev" target="_blank" rel="noopener">PackageFix</a> <span>·</span> <a href="/glossary/">Glossary</a></div>
      <div><a href="https://github.com/metriclogic26/domain-preflight" target="_blank" rel="noopener">Star on GitHub</a> <span> · </span> <span>MIT Licensed</span> <span> · </span> <a href="https://github.com/metriclogic26/domain-preflight/issues/new" target="_blank" rel="noopener">Report issue →</a></div>
    </div>
  </footer>"""


def faq_html(faqs: list[tuple[str, str]]) -> str:
    lines = []
    for q, a in faqs:
        lines.append(
            f"        <h3>{html_module.escape(q)}</h3>\n        <p>{html_module.escape(a)}</p>"
        )
    return "\n".join(lines)


def build_page(
    slug: str,
    page_title: str,
    meta: str,
    h1: str,
    crumb: str,
    body: str,
    faqs: list[tuple[str, str]],
) -> str:
    canonical = f"https://domainpreflight.dev/blog/{slug}/"
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": h1,
        "datePublished": DATE_ISO,
        "dateModified": DATE_ISO,
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
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://domainpreflight.dev/blog/"},
            {"@type": "ListItem", "position": 3, "name": crumb, "item": canonical},
        ],
    }
    article_j = json.dumps(article, ensure_ascii=False, indent=2)
    faq_j = json.dumps(faqpage, ensure_ascii=False, indent=2)
    crumb_j = json.dumps(crumbs, ensure_ascii=False, separators=(",", ":"))
    fq = faq_html(faqs)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_module.escape(page_title)} | DomainPreflight</title>
  <meta name="description" content="{html_module.escape(meta)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script type="application/ld+json">
  {article_j}
  </script>
  <script type="application/ld+json">
  {faq_j}
  </script>
  <script type="application/ld+json">
  {crumb_j}
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
    main {{ max-width: 720px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }}
    .breadcrumb {{ font-size: 0.8rem; color: var(--text2); margin-bottom: 1.25rem; line-height: 1.5; }}
    .breadcrumb a {{ color: var(--purple); text-decoration: none; }}
    .breadcrumb a:hover {{ text-decoration: underline; }}
    .hero-label {{ font-size: 0.7rem; letter-spacing: 0.15em; font-weight: 600; text-transform: uppercase; color: var(--purple); margin-bottom: 0.5rem; }}
    h1 {{ font-size: clamp(1.35rem, 3.5vw, 1.85rem); font-weight: 600; margin-bottom: 0.5rem; line-height: 1.3; }}
    .post-date {{ color: var(--text2); font-size: 0.8rem; margin-bottom: 1.5rem; }}
    article h2 {{ font-size: 1.05rem; font-weight: 600; margin: 2rem 0 0.75rem; color: var(--text); }}
    article p, article li {{ color: var(--text2); font-size: 0.9rem; margin-bottom: 0.75rem; }}
    article ul, article ol {{ margin: 0.5rem 0 1rem 1.25rem; color: var(--text2); font-size: 0.9rem; }}
    pre.code-block {{ background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 1rem 1.15rem; font-size: 0.78rem; line-height: 1.55; overflow-x: auto; white-space: pre-wrap; word-break: break-word; color: var(--text); margin: 0.75rem 0 1rem; }}
    .tool-cta {{ margin: 2rem 0; padding: 1.25rem 1.5rem; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; border-left: 3px solid var(--purple); }}
    .tool-cta p {{ margin-bottom: 0.5rem; color: var(--text); }}
    .tool-cta a {{ color: var(--purple); font-weight: 600; text-decoration: none; }}
    .tool-cta a:hover {{ text-decoration: underline; }}
    .glossary-links {{ margin: 1.5rem 0; padding: 1rem 1.15rem; background: var(--surface); border: 1px solid var(--border); border-radius: 10px; font-size: 0.85rem; color: var(--text2); }}
    .glossary-links a {{ color: var(--purple); text-decoration: none; }}
    .glossary-links a:hover {{ text-decoration: underline; }}
    .faq-section h2 {{ font-size: 1.05rem; margin-top: 2rem; }}
    .faq-section h3 {{ font-size: 0.95rem; font-weight: 600; color: var(--text); margin: 1.5rem 0 0.4rem; }}
    .faq-section p {{ margin-bottom: 0.5rem; color: var(--text2); font-size: 0.9rem; }}
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
        <a href="/blog/">Blog</a>
      </nav>
    </div>
  </header>
  <main>
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="https://domainpreflight.dev/">Home</a> <span aria-hidden="true">›</span> <a href="/blog/">Blog</a> <span aria-hidden="true">›</span> {html_module.escape(crumb)}</nav>
    <article>
      <p class="hero-label">Blog</p>
      <h1>{html_module.escape(h1)}</h1>
      <p class="post-date"><time datetime="{DATE_ISO}">{DATE_DISPLAY}</time></p>
{body}
      <section class="faq-section" aria-label="FAQ">
        <h2>FAQ</h2>
{fq}
      </section>
      <div class="internal-links">
        <p><a href="/blog/">← All posts</a></p>
      </div>
    </article>
  </main>
{FOOTER}
</body>
</html>
"""


def main():
    posts = [
        (
            "dmarc-p-none-still-a-problem",
            "Your DMARC Is Set to p=none. Here's Why That's Still a Problem.",
            "DMARC p=none monitors failures but blocks nothing. Attackers can still spoof your domain and hit inboxes. Here's what to do about it.",
            "Your DMARC Is Set to p=none. Here's Why That's Still a Problem.",
            "Your DMARC Is Set to p=none. Here's Why That's Still a Problem.",
            """      <p>You set up a DMARC record. It says p=none. Your DNS checker shows a green tick. And you're still getting spoofed.</p>
      <p>p=none is monitoring mode. It watches failures and reports them. It does not block anything.</p>
      <p>So your DMARC record exists — and spoofed emails from your domain still land in inboxes. That's the trap.</p>

      <h2>What p=none Actually Does</h2>
      <p>It tells receivers: "If this email fails DMARC, please send me a report about it."</p>
      <p>That's it. No quarantine. No rejection. Just a daily XML file to an email address most people never check.</p>
      <p>Meanwhile, phishing emails pretending to be from your domain keep getting delivered.</p>

      <h2>Why Everyone Starts Here (And Gets Stuck)</h2>
      <p>p=none is the right starting point. You need to see what's failing before you start blocking.</p>
      <p>The problem is staying there. Most teams set up p=none, see the green tick, and move on. The reports never get read. The policy never gets tightened.</p>
      <p>Months pass. Sometimes years.</p>

      <h2>What You Should Be Doing Instead</h2>
      <p><strong>Step 1:</strong> Add rua= to your DMARC record so you actually get reports.</p>
<pre class="code-block">v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com</pre>
      <p><strong>Step 2:</strong> Wait 2 weeks. Read the reports. Use DomainPreflight's DMARC Report Analyzer — paste the XML, see which senders are failing alignment.</p>
      <p><strong>Step 3:</strong> Fix the alignment failures. That usually means adding CNAME records for your third-party senders.</p>
      <p><strong>Step 4:</strong> Move to p=quarantine. Then p=reject.</p>

      <h2>How Long Should You Stay at p=none?</h2>
      <p>2-4 weeks if you're actively reading reports. Long enough to catch all your legitimate senders.</p>
      <p>Not 6 months. Not "indefinitely for safety." That's just leaving your domain unprotected.</p>

      <h2>The Fast Check</h2>
      <p>Run DNS Preflight on your domain. If DMARC shows p=none and you've had the record for more than a month — you need to act.</p>

      <div class="tool-cta">
        <p>Check your DMARC policy</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/glossary/dmarc-policy/">DMARC policy</a> ·
        <a href="/glossary/dmarc/">DMARC</a> ·
        <a href="/fix/dmarc/">DMARC fix guides</a> ·
        <a href="https://domainpreflight.dev/dmarc/">DMARC Report Analyzer</a>
      </div>""",
            [
                (
                    "Is DMARC p=none doing anything useful?",
                    "Yes — it collects reports showing who is sending as your domain. But it blocks nothing. Think of it as surveillance without enforcement.",
                ),
                (
                    "How do I know when it's safe to move to p=reject?",
                    "When your DMARC reports show all legitimate senders passing alignment for 2+ weeks with no unexplained failures.",
                ),
                (
                    "Will moving to p=reject break my email?",
                    "Only if some legitimate senders aren't aligned yet. Fix alignment failures first — then p=reject is safe.",
                ),
                (
                    "What if I never receive DMARC reports?",
                    "Check your rua= address. If it's missing or wrong, you're getting no data. Add rua=mailto:dmarc@yourdomain.com and wait 24 hours.",
                ),
                (
                    "Can attackers still spoof my domain with p=none?",
                    "Yes. p=none provides zero spoofing protection. Spoofed emails still reach inboxes. Only p=reject stops them.",
                ),
            ],
        ),
        (
            "spf-lookup-limit",
            "The SPF Lookup Limit: Why You Hit 10 and How to Stay Under It",
            "SPF allows exactly 10 DNS lookups. Most growing companies exceed this silently — and their emails start failing. Here's how to find and fix the problem.",
            "The SPF Lookup Limit: Why You Hit 10 and How to Stay Under It",
            "The SPF Lookup Limit: Why You Hit 10 and How to Stay Under It",
            """      <p>You didn't change anything. Your emails just started bouncing.</p>
      <p>The SPF lookup limit is one of the most common causes of silent email failure. You add one more email service — a CRM, a marketing tool, a transactional sender — and suddenly you're over 10 lookups.</p>
      <p>Receivers return PermError. Email gets rejected or lands in spam. Nothing in your dashboard tells you why.</p>

      <h2>Why 10 Lookups Is Less Than You Think</h2>
      <p>Every include: in your SPF record triggers a DNS lookup. And most providers nest their own includes inside.</p>
      <p>include:sendgrid.net doesn't use 1 lookup. It uses 3 or 4 — because SendGrid's SPF record has its own includes.</p>
      <p>Add Google Workspace, SendGrid, HubSpot, Mailgun, and a CRM — and you're at 12-15 lookups before you know it.</p>

      <h2>How to Check Your Count</h2>
      <p>Run DNS Preflight and expand the SPF lookup tree. It shows every include recursively with a running count.</p>
<pre class="code-block">v=spf1 include:amazonses.com          ← +1
include:_spf.google.com        ← +1
└─ include:_netblocks.google ← +1
include:sendgrid.net           ← +1
└─ include:u123.wl.sendgrid  ← +1
include:spf.hubspot.com        ← +1
Total: 8 lookups (you're getting close)</pre>

      <h2>The Fix — SPF Flattening</h2>
      <p>Replace include: statements with the actual IP addresses they resolve to.</p>
      <p><strong>Before:</strong></p>
<pre class="code-block">v=spf1 include:sendgrid.net ~all</pre>
      <p><strong>After:</strong></p>
<pre class="code-block">v=spf1 ip4:167.89.0.0/17
ip4:198.37.144.0/20 ~all</pre>
      <p>ip4: entries use zero lookups. Problem solved.</p>
      <p>The downside: you have to update your record when providers change their IPs. Set a calendar reminder every 6 months.</p>

      <h2>The Better Answer — Fewer Senders</h2>
      <p>The cleanest fix is sending through fewer services. If two tools both send email, route both through one provider.</p>
      <p>Fewer senders = fewer includes = fewer lookups = no problem.</p>

      <h2>What Counts Toward the Limit</h2>
      <p>include:, a:, mx:, ptr:, exists:, redirect= → each counts as one lookup</p>
      <p>ip4:, ip6:, ~all, -all, +all → zero lookups</p>

      <div class="tool-cta">
        <p>Count your SPF lookups</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/glossary/spf-record/">SPF record</a> ·
        <a href="/glossary/spf-permerror/">SPF PermError</a> ·
        <a href="/fix/spf/too-many-lookups/">Too many lookups fix</a> ·
        <a href="/error/spf-permerror/">SPF PermError error page</a>
      </div>""",
            [
                (
                    "What happens when you exceed 10 SPF lookups?",
                    "Receivers return SPF PermError. Depending on your DMARC policy, this can cause emails to be rejected or land in spam.",
                ),
                (
                    "How do I count my SPF lookups?",
                    "Run DNS Preflight — the SPF recursive tree expands every include and shows your running total.",
                ),
                (
                    "What is SPF flattening?",
                    "Replacing include: with the actual IP addresses they resolve to. Reduces lookup count to zero for those entries.",
                ),
                (
                    "Do ip4: entries count toward the limit?",
                    "No. ip4: and ip6: mechanisms don't trigger DNS lookups and don't count toward the 10-lookup limit.",
                ),
                (
                    "Will I get warned when I exceed 10 lookups?",
                    "No. SPF PermError happens silently. Emails fail without any obvious dashboard warning. Regular checks with DNS Preflight catch it early.",
                ),
            ],
        ),
        (
            "dmarc-alignment-vs-dmarc-policy",
            "DMARC Alignment vs DMARC Policy — The Difference Most Guides Skip",
            "DMARC policy and DMARC alignment are different things. Getting them confused is why most DMARC setups fail even when SPF and DKIM pass.",
            "DMARC Alignment vs DMARC Policy — The Difference Most Guides Skip",
            "DMARC Alignment vs DMARC Policy — The Difference Most Guides Skip",
            """      <p>You've read the DMARC guides. You set p=reject. SPF passes. DKIM passes.</p>
      <p>Emails still fail DMARC.</p>
      <p>The reason is usually alignment — and most guides explain policy without properly explaining alignment.</p>

      <h2>What Policy Does</h2>
      <p>Policy (the p= tag) tells receivers what to DO with emails that fail DMARC.</p>
      <p>p=none → deliver and report. p=quarantine → send to spam. p=reject → block entirely.</p>
      <p>That's it. Policy is enforcement.</p>

      <h2>What Alignment Does</h2>
      <p>Alignment checks whether SPF and DKIM are passing for YOUR domain — not just any domain.</p>
      <p>This is the part people miss.</p>
      <p>When you send through SendGrid, SendGrid signs your email with DKIM. The signature passes. But it's signed with sendgrid.net — not your domain.</p>
      <p>DMARC says: that doesn't count. The signing domain must match your From: domain.</p>

      <h2>The Exact Check</h2>
      <p>DMARC looks at two things:</p>
      <ol>
        <li>SPF: does the Return-Path domain match your From: domain?</li>
        <li>DKIM: does the d= tag in the DKIM signature match your From: domain?</li>
      </ol>
      <p>If either one matches → DMARC passes. If neither matches → DMARC fails. Regardless of your policy setting.</p>

      <h2>Why Third-Party Senders Break Alignment</h2>
      <p>SendGrid, Mailgun, HubSpot — by default they all send from their own domain.</p>
      <p>Your From: says you@yourdomain.com. The Return-Path says bounce@sendgrid.net.</p>
      <p>SPF passes for sendgrid.net. But that's not aligned with yourdomain.com.</p>
      <p>The fix is provider-specific CNAME records that let the provider sign with your domain.</p>

      <h2>How to Check Alignment</h2>
      <p>Run DNS Preflight. The alignment visual at the top of the results shows exactly what FROM domain is being compared against what Return-Path domain.</p>
      <p>Red arrow = misaligned. Green = passing.</p>

      <div class="tool-cta">
        <p>Check your alignment</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/glossary/dmarc-alignment/">DMARC alignment</a> ·
        <a href="/glossary/dmarc-policy/">DMARC policy</a> ·
        <a href="/fix/dmarc/">DMARC fix guides</a>
      </div>""",
            [
                (
                    "What is DMARC alignment?",
                    "The requirement that SPF or DKIM must pass for your From: domain specifically — not just any domain. Passing for sendgrid.net doesn't count as alignment for yourdomain.com.",
                ),
                (
                    "Can DMARC pass if only DKIM is aligned?",
                    "Yes. DMARC passes if either SPF or DKIM aligns with your From: domain. You don't need both.",
                ),
                (
                    "Why does SPF pass but DMARC still fail?",
                    "SPF may be passing for the Return-Path domain — but that domain doesn't match your From:. Alignment requires the domains to match.",
                ),
                (
                    "What is relaxed alignment?",
                    "Relaxed alignment (default) allows subdomains to match — mail.yourdomain.com aligns with yourdomain.com. Strict requires an exact match.",
                ),
                (
                    "How do I fix alignment for SendGrid?",
                    "Add SendGrid's three CNAME records to your DNS — they let SendGrid sign with your domain instead of theirs. See the SendGrid DMARC fix guide.",
                ),
            ],
        ),
        (
            "spf-dkim-pass-dmarc-fails",
            "Why Your Emails Pass SPF and DKIM But Still Fail DMARC",
            "SPF pass. DKIM pass. DMARC fail. It shouldn't be possible — but it happens constantly. Here's the exact reason and the fix.",
            "Why Your Emails Pass SPF and DKIM But Still Fail DMARC",
            "Why Your Emails Pass SPF and DKIM But Still Fail DMARC",
            """      <p>This is the most confusing thing in email authentication.</p>
      <p>SPF passes. DKIM passes. Your checker shows both green. And DMARC still fails.</p>
      <p>It feels like a bug. It's not.</p>

      <h2>The Problem Is Alignment</h2>
      <p>SPF and DKIM passing is not enough. They have to pass for the right domain.</p>
      <p>DMARC checks whether the SPF and DKIM domains match your From: header domain. This is called alignment.</p>
      <p>When you send through a third-party provider, they pass SPF and DKIM for their own domain — not yours.</p>

      <h2>A Real Example</h2>
      <p>You send email from you@yourdomain.com through SendGrid.</p>
      <p>SendGrid signs the email with DKIM. The signature passes verification.</p>
      <p>But the DKIM d= tag says sendgrid.net. Not yourdomain.com.</p>
      <p>SPF passes for the Return-Path — which is @sendgrid.net. Not @yourdomain.com.</p>
      <p>DMARC checks the From: domain (yourdomain.com) against the SPF and DKIM domains (sendgrid.net). They don't match. DMARC fails.</p>

      <h2>The Fix</h2>
      <p>You need provider-specific CNAME records that let the provider sign with YOUR domain.</p>
      <p>For SendGrid: add the three CNAME records from their Sender Authentication dashboard. After that, the DKIM d= tag shows yourdomain.com — and DMARC passes.</p>
      <p>Every major provider has the same pattern. See the DMARC provider fix guides.</p>

      <h2>How to Diagnose This Quickly</h2>
      <p>Run DNS Preflight. The alignment visual shows FROM domain vs Return-Path domain as two boxes with an arrow.</p>
      <p>Red arrow = not aligned. The provider detection card tells you exactly which CNAMEs are missing.</p>

      <div class="tool-cta">
        <p>Diagnose your alignment</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/glossary/dmarc-alignment/">DMARC alignment</a> ·
        <a href="/fix/dmarc/sendgrid/">SendGrid DMARC</a> ·
        <a href="/fix/dmarc/google-workspace/">Google Workspace</a> ·
        <a href="/fix/dmarc/microsoft-365/">Microsoft 365</a>
      </div>""",
            [
                (
                    "How can SPF and DKIM pass but DMARC still fail?",
                    "SPF and DKIM can pass for the provider's domain — but DMARC requires them to pass for YOUR From: domain. That's alignment.",
                ),
                (
                    "Which providers cause this most often?",
                    "SendGrid, Mailgun, HubSpot, Klaviyo — any provider that sends from their own infrastructure by default. All require specific CNAME setup.",
                ),
                (
                    "Is there a quick way to tell if I have an alignment problem?",
                    "Run DNS Preflight — the alignment visual shows the mismatch immediately. The provider detection card shows which CNAMEs to add.",
                ),
                (
                    "Do I need to fix both SPF and DKIM alignment?",
                    "No. DMARC passes if either SPF OR DKIM aligns. Fixing one is enough.",
                ),
                (
                    "Will fixing alignment affect my existing email delivery?",
                    "No. Adding CNAME records doesn't interrupt existing delivery. Alignment improves once the provider verifies the records.",
                ),
            ],
        ),
        (
            "sendgrid-cname-setup",
            "The SendGrid CNAME Setup Most People Miss (And Why DMARC Fails Without It)",
            "Most SendGrid users add an SPF include and call it done. But without the three CNAME records, DMARC alignment fails. Here's exactly what to add.",
            "The SendGrid CNAME Setup Most People Miss (And Why DMARC Fails Without It)",
            "The SendGrid CNAME Setup Most People Miss",
            """      <p>You added include:sendgrid.net to your SPF record. SPF passes.</p>
      <p>DMARC still fails.</p>
      <p>This is the most common SendGrid setup mistake. The SPF include is not enough for DMARC alignment.</p>

      <h2>Why the SPF Include Isn't Enough</h2>
      <p>The SPF include authorises SendGrid's servers to send as your domain. SPF passes. Good.</p>
      <p>But the Return-Path for your emails is still @sendgrid.net — not @yourdomain.com.</p>
      <p>DMARC alignment requires the Return-Path domain to match your From: domain. It doesn't. DMARC fails.</p>

      <h2>What You Actually Need</h2>
      <p>Three CNAME records from SendGrid's Sender Authentication dashboard.</p>
      <p>These records do two things: (1) let SendGrid sign email with your domain's DKIM key (DKIM alignment), and (2) route your Return-Path through your domain (SPF alignment).</p>
      <p>The exact records are account-specific — your account ID appears in the values. Get them from:</p>
      <p>SendGrid → Settings → Sender Authentication → Authenticate Your Domain</p>

      <h2>The Pattern (Replace [ID] with Your Account ID)</h2>
<pre class="code-block">em[ID].yourdomain.com
  CNAME → u[ID].wl.sendgrid.net

s1._domainkey.yourdomain.com
  CNAME → s1.domainkey.u[ID].wl.sendgrid.net

s2._domainkey.yourdomain.com
  CNAME → s2.domainkey.u[ID].wl.sendgrid.net</pre>
      <p>Add all three. Not just one.</p>

      <h2>After Adding the Records</h2>
      <p>Wait up to 48 hours for DNS propagation.</p>
      <p>Then return to SendGrid's Sender Authentication page and click Verify. SendGrid confirms the records are live.</p>
      <p>Run DNS Preflight after that to confirm the alignment visual shows green.</p>

      <h2>What If You're Already Sending</h2>
      <p>Adding these records doesn't break existing delivery. Email continues normally during the transition.</p>
      <p>After SendGrid verifies the records, new emails are signed with your domain and DMARC alignment passes.</p>

      <div class="tool-cta">
        <p>Check your SendGrid alignment</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/fix/dmarc/sendgrid/">SendGrid DMARC fix</a> ·
        <a href="/glossary/dmarc-alignment/">DMARC alignment</a> ·
        <a href="/glossary/dkim/">DKIM</a>
      </div>""",
            [
                (
                    "Why does SendGrid fail DMARC even with SPF configured?",
                    "The SPF include authorises SendGrid's servers but doesn't fix alignment. The Return-Path still comes from sendgrid.net, which doesn't match your From: domain.",
                ),
                (
                    "Do I need all three CNAME records?",
                    "Yes. The em[ID] record fixes SPF alignment. The s1 and s2 records fix DKIM alignment. All three are required.",
                ),
                (
                    "Where do I find my SendGrid account ID?",
                    "It appears in the CNAME values shown in the Sender Authentication dashboard — SendGrid generates them specifically for your account.",
                ),
                (
                    "Will adding these records break my current sending?",
                    "No. Adding DNS records doesn't interrupt delivery. Alignment improves after SendGrid verifies the records.",
                ),
                (
                    "How do I verify the setup is working?",
                    "Run DNS Preflight after 48 hours — the alignment visual should show green with SendGrid CNAME confirmed.",
                ),
            ],
        ),
        (
            "subdomain-takeover-dangling-cnames",
            "Subdomain Takeover: The Dangling CNAME Risk Nobody Checks",
            "Deleting a Heroku app without removing the CNAME lets attackers serve content on your subdomain. Here's how subdomain takeover works and how to find your dangling records.",
            "Subdomain Takeover: The Dangling CNAME Risk Nobody Checks",
            "Subdomain Takeover: The Dangling CNAME Risk Nobody Checks",
            """      <p>You deleted a staging app 18 months ago. You forgot to remove the DNS record.</p>
      <p>Someone else just claimed that app name on Heroku. They're now serving content on staging.yourdomain.com.</p>
      <p>That's a subdomain takeover. It's more common than most people think.</p>

      <h2>How It Happens</h2>
      <p>The pattern is always the same:</p>
      <ol>
        <li>You create a subdomain pointing to an external service (Heroku, GitHub Pages, S3, Netlify, Vercel, Azure)</li>
        <li>You delete the service or project</li>
        <li>You forget to delete the DNS record</li>
        <li>The CNAME is now pointing to an unclaimed name on that service</li>
        <li>An attacker claims the name</li>
        <li>Your subdomain now serves their content</li>
      </ol>

      <h2>Why This Is Serious</h2>
      <p>The content serves from your domain. Browsers show your domain in the URL bar. SSL certificates cover your subdomain.</p>
      <p>Users see your domain. They trust it. The attacker controls what they see.</p>
      <p>This is used for phishing, credential harvesting, and malware distribution — all under your brand.</p>

      <h2>The Services Most Exploited</h2>
      <ul>
        <li>GitHub Pages — most common</li>
        <li>AWS S3 — unclaimed buckets</li>
        <li>Heroku — deleted apps</li>
        <li>Netlify — deleted sites</li>
        <li>Azure Web Apps — deprovisioned apps</li>
        <li>Fastly — deleted services</li>
      </ul>

      <h2>How to Find Your Dangling Records</h2>
      <p>Run DomainPreflight Dangling Records on your domain.</p>
      <p>It scans certificate logs to discover your subdomains, then checks each CNAME against a feed of known takeover fingerprints.</p>
      <p>Any subdomain pointing to an unclaimed service shows as a risk — with a direct link to claim it or a fix recommendation.</p>

      <h2>The Fix</h2>
      <p>Delete the DNS record. That's it.</p>
      <p>If you still need the subdomain, recreate the service first. Then the CNAME points to something you own.</p>
      <p>If you're not sure whether the CNAME is still needed — delete it. DNS records are easy to add back. Subdomain takeovers are hard to recover from.</p>

      <div class="tool-cta">
        <p>Scan your subdomains</p>
        <a href="https://domainpreflight.dev/dangling/">Open Dangling Records →</a>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/glossary/subdomain-takeover/">Subdomain takeover</a> ·
        <a href="/glossary/cname-record/">CNAME record</a> ·
        <a href="https://domainpreflight.dev/dangling/">Dangling Records tool</a>
      </div>""",
            [
                (
                    "What is a subdomain takeover?",
                    "When a CNAME points to a deleted external service, an attacker can claim that service and serve content on your subdomain.",
                ),
                (
                    "How do I check if I have dangling DNS records?",
                    "Run DomainPreflight Dangling Records — it discovers your subdomains via certificate logs and checks each one for takeover risk.",
                ),
                (
                    "Which services are most commonly exploited?",
                    "GitHub Pages, AWS S3, Heroku, Netlify, and Azure are the most common targets for subdomain takeover.",
                ),
                (
                    "How do I fix a dangling CNAME?",
                    "Delete the DNS record. If you still need the subdomain, recreate the service first so the CNAME points to something you control.",
                ),
                (
                    "Can this happen to a root domain?",
                    "No — subdomain takeover requires a CNAME, which cannot be used at the root domain. Only subdomains are at risk.",
                ),
            ],
        ),
        (
            "how-to-read-dmarc-report",
            "How to Read a DMARC Aggregate Report Without Losing Your Mind",
            "DMARC aggregate reports arrive as zipped XML. Most people never open them. Here's what's actually in them and how to read them in under 5 minutes.",
            "How to Read a DMARC Aggregate Report Without Losing Your Mind",
            "How to Read a DMARC Aggregate Report Without Losing Your Mind",
            """      <p>Your DMARC record has rua= set. Reports are arriving.</p>
      <p>You open one. It's a zipped XML file that looks like this:</p>
<pre class="code-block">&lt;feedback&gt;
  &lt;report_metadata&gt;
    &lt;org_name&gt;Google Inc.&lt;/org_name&gt;
    ...
  &lt;/report_metadata&gt;
  &lt;record&gt;
    &lt;row&gt;
      &lt;source_ip&gt;209.85.220.41&lt;/source_ip&gt;
      &lt;count&gt;142&lt;/count&gt;
      &lt;policy_evaluated&gt;
        &lt;dkim&gt;pass&lt;/dkim&gt;
        &lt;spf&gt;pass&lt;/spf&gt;
      &lt;/policy_evaluated&gt;
    &lt;/row&gt;
  &lt;/record&gt;
&lt;/feedback&gt;</pre>
      <p>You close it and never look again.</p>
      <p>Here's how to actually read these.</p>

      <h2>What the Report Contains</h2>
      <p>Every DMARC report tells you three things:</p>
      <ol>
        <li>Who sent the report (Google, Microsoft, Yahoo)</li>
        <li>Which IPs sent email as your domain</li>
        <li>Whether those emails passed SPF and DKIM</li>
      </ol>
      <p>That's it. It's a list of sending IPs with pass/fail results.</p>

      <h2>The Three Things to Look For</h2>
      <p>Look for rows where both DKIM and SPF fail. That's either a misconfigured sender or someone spoofing your domain.</p>
      <p>Look for unfamiliar IPs. If you don't recognise the IP, find out what it is. Could be a service you forgot, or an attacker.</p>
      <p>Look for volume. A spoofing campaign shows up as high message count from an unknown IP. Even p=none lets you see this happening.</p>

      <h2>The Shortcut</h2>
      <p>Unzip the file. Paste the XML into DomainPreflight's DMARC Report Analyzer.</p>
      <p>It turns the XML into a table showing each sending IP, message count, DKIM result, SPF result, and risk level.</p>
      <p>Spoofing attempts show as red "Spoofing risk." Misaligned senders show as orange. Clean senders show as green "Aligned."</p>
      <p>5 minutes instead of decoding XML.</p>

      <h2>What to Do With What You Find</h2>
      <p>All green → you're clean. Consider moving to p=quarantine.</p>
      <p>Orange (partial failures) → fix alignment for the failing sender. Use the DMARC provider fix guides.</p>
      <p>Red (both fail) → investigate the IP. If it's not a sender you recognise, upgrade to p=reject to block it.</p>

      <div class="tool-cta">
        <p>Analyze your DMARC report</p>
        <a href="https://domainpreflight.dev/dmarc/">Open DMARC Report Analyzer →</a>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/glossary/dmarc-aggregate-report/">DMARC aggregate report</a> ·
        <a href="/glossary/dmarc-policy/">DMARC policy</a> ·
        <a href="https://domainpreflight.dev/dmarc/">DMARC Report Analyzer</a>
      </div>""",
            [
                (
                    "Where do DMARC aggregate reports come from?",
                    "Google, Microsoft, Yahoo, and other major receivers send daily XML reports to the email in your rua= tag.",
                ),
                (
                    "How do I get DMARC reports?",
                    "Add rua=mailto:dmarc@yourdomain.com to your DMARC TXT record. Reports arrive within 24 hours.",
                ),
                (
                    "What does a DMARC report actually show?",
                    "Which IPs sent email as your domain, how many messages, and whether SPF and DKIM passed for each one.",
                ),
                (
                    "How do I read DMARC XML?",
                    "Use DomainPreflight's DMARC Report Analyzer — paste the XML for a visual summary in seconds.",
                ),
                (
                    "What should I do if I see a spoofing attempt in the report?",
                    "Upgrade your DMARC policy to p=reject. That blocks the spoofed emails from reaching inboxes.",
                ),
            ],
        ),
        (
            "domain-expiry-infrastructure-failure",
            "Domain Expiry: The Infrastructure Failure That Always Comes at the Worst Time",
            "Domain expiry takes down your website, email, and every DNS-dependent service simultaneously. It's preventable in 5 minutes. Here's how.",
            "Domain Expiry: The Infrastructure Failure That Always Comes at the Worst Time",
            "Domain Expiry: The Infrastructure Failure That Always Comes at the Worst Time",
            """      <p>It's a Monday morning. Your website is down. Email is bouncing. Customers can't reach you.</p>
      <p>Someone checks the domain. It expired three days ago.</p>
      <p>This happens to companies of every size. The fix is five minutes of setup. The failure is weeks of damage.</p>

      <h2>What Actually Happens When a Domain Expires</h2>
      <p>Everything stops at once.</p>
      <p>Your website returns NXDOMAIN. Email bounces with "domain not found." SSL certificates break on the next renewal because the domain can't be verified.</p>
      <p>Subdomains, APIs, webhooks, SPF records, DKIM records — all gone. Everything that depends on DNS stops working.</p>

      <h2>The Danger Window</h2>
      <p>Most registrars send warning emails at 90, 60, 30, and 7 days before expiry.</p>
      <p>Those emails go to a billing address nobody checks. Or the inbox of someone who left the company three years ago.</p>
      <p>The domain expires. The grace period starts (usually 30-45 days). Then the redemption period. Then the domain is released to the public.</p>
      <p>Domain squatters watch expiry feeds. Valuable domains get snatched in minutes.</p>

      <h2>The Five-Minute Fix</h2>
      <p>Enable auto-renew on every domain you own. Not just your primary domain — all of them.</p>
      <p>Then check the expiry dates now. Use DomainPreflight WHOIS — it shows the exact expiry date, registrar, and a risk tier.</p>
      <p>Critical (under 30 days) → renew today. Warning (30-60 days) → renew this week. Safe (over 60 days) → enable auto-renew and forget about it.</p>

      <h2>Multiple Domains</h2>
      <p>If you manage more than a handful of domains, run each one through DomainPreflight WHOIS and note the expiry dates.</p>
      <p>Set calendar reminders 60 days before expiry as a backup — even with auto-renew enabled. Payment method expiry is the second most common cause of domain loss after just forgetting to renew.</p>

      <h2>If You've Already Expired</h2>
      <p>Contact your registrar immediately. Most offer a grace period where you can renew at normal cost.</p>
      <p>After the grace period, redemption fees kick in — often $100-200 to recover your own domain.</p>
      <p>After redemption, it's gone.</p>

      <div class="tool-cta">
        <p>Check your domain expiry</p>
        <a href="https://domainpreflight.dev/whois/">Open WHOIS →</a>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/glossary/domain-expiry/">Domain expiry</a> ·
        <a href="/glossary/whois/">WHOIS</a> ·
        <a href="https://domainpreflight.dev/whois/">WHOIS tool</a>
      </div>""",
            [
                (
                    "What happens when a domain expires?",
                    "Your website goes down, email stops working, and all DNS records become inaccessible. Everything that depends on your domain fails simultaneously.",
                ),
                (
                    "How much notice do I get before expiry?",
                    "Most registrars send emails at 90, 60, 30, and 7 days. These often go unread. Enable auto-renew and don't rely on email notices.",
                ),
                (
                    "Can I recover an expired domain?",
                    "Usually yes — during the grace period (30-45 days) at normal renewal cost. After that, redemption fees apply. After redemption, the domain is released.",
                ),
                (
                    "How do I check when my domain expires?",
                    "Run DomainPreflight WHOIS — it shows the exact expiry date, registrar, and days remaining with a risk tier.",
                ),
                (
                    "What if my domain was registered by someone who left the company?",
                    "Contact the registrar directly. Most require proof of ownership (company documents) to transfer or renew a domain under a departed registrant.",
                ),
            ],
        ),
    ]

    for row in posts:
        slug, page_title, meta, h1, crumb, body, faqs = row
        out_html = build_page(slug, page_title, meta, h1, crumb, body, faqs)
        out_path = BLOG / slug / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out_html, encoding="utf-8")
        print("Wrote", out_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
