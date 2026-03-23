#!/usr/bin/env python3
"""Generate error/[slug]/index.html — do not run from fix/ directory."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERROR = ROOT / "error"

STYLE = """  <style>
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
      </nav>
    </div>
  </header>
"""

FOOTER = """  <footer>
    <div class="footer-inner"><p class="footer-disclaimer">This is a free sanity check — not legal or production advice. Verify DNS and mail in your own stack before you change anything.</p></div>
    <div class="footer-bar">
      <div><span>DomainPreflight by MetricLogic ·</span> <a href="https://configclarity.dev" target="_blank" rel="noopener">ConfigClarity</a> <span>·</span> <a href="https://domainpreflight.dev" target="_blank" rel="noopener">DomainPreflight</a> <span>·</span> <a href="https://packagefix.dev" target="_blank" rel="noopener">PackageFix</a> <span>·</span> <a href="/glossary/">Glossary</a></div>
      <div><a href="https://github.com/metriclogic26/domain-preflight" target="_blank" rel="noopener">Star on GitHub</a> <span> · </span> <span>MIT Licensed</span> <span> · </span> <a href="https://github.com/metriclogic26/domain-preflight/issues/new" target="_blank" rel="noopener">Report issue →</a></div>
    </div>
  </footer>
</body>
</html>
"""

UMAMI = '  <script defer src="https://cloud.umami.is/script.js" data-website-id="27fc19d2-1ff5-4478-946a-b96cc7d5daf8"></script>\n'


def build(
    slug: str,
    title: str,
    meta: str,
    h1: str,
    subtitle: str,
    crumb_last: str,
    howto_name: str,
    howto_desc: str,
    step_names: list[str],
    step_texts: list[str],
    faqs: list[tuple[str, str]],
    article_body: str,
) -> str:
    base = f"https://domainpreflight.dev/error/{slug}/"
    steps = []
    for i, (sname, stext) in enumerate(zip(step_names, step_texts), start=1):
        steps.append(
            {
                "@type": "HowToStep",
                "position": i,
                "name": sname,
                "url": f"{base}#step{i}",
                "text": stext,
            }
        )
    howto = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": howto_name,
        "description": howto_desc,
        "estimatedCost": {"@type": "MonetaryAmount", "currency": "USD", "value": "0"},
        "supply": {"@type": "HowToSupply", "name": "Browser and DNS access"},
        "tool": {"@type": "HowToTool", "name": "DomainPreflight DNS Preflight", "url": "https://domainpreflight.dev/"},
        "step": steps,
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
            {"@type": "ListItem", "position": 2, "name": "Errors", "item": "https://domainpreflight.dev/error/"},
            {"@type": "ListItem", "position": 3, "name": crumb_last, "item": base},
        ],
    }
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — DomainPreflight</title>
  <meta name="description" content="{meta}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{base}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
{UMAMI}  <script type="application/ld+json">
  {json.dumps(howto, ensure_ascii=False, separators=(",", ":"))}
  </script>
  <script type="application/ld+json">
  {json.dumps(faqpage, ensure_ascii=False, separators=(",", ":"))}
  </script>
  <script type="application/ld+json">
  {json.dumps(crumbs, ensure_ascii=False, separators=(",", ":"))}
  </script>
{STYLE}
  <main>
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="https://domainpreflight.dev/">Home</a> <span aria-hidden="true">›</span> <a href="/error/">Errors</a> <span aria-hidden="true">›</span> {crumb_last}</nav>
    <article>
      <p class="hero-label">Errors</p>
      <h1>{h1}</h1>
      <p class="subtitle">{subtitle}</p>
{article_body}
    </article>
  </main>
{FOOTER}
"""


def main():
    pages = [
        # slug, title, meta, h1, subtitle, crumb_last, howto_name, howto_desc, step_names, step_texts, faqs, body
        (
            "spf-permerror",
            "SPF PermError: Too Many DNS Lookups — Fix",
            "SPF PermError means your SPF record exceeded the 10 DNS lookup limit. Receivers may reject mail or send it to spam — flatten includes to IP ranges.",
            "SPF PermError — Your SPF Record Has Too Many Lookups",
            "SPF PermError means your SPF record exceeded the 10 DNS lookup limit. Receiving servers treat this as a hard failure — your legitimate emails may be rejected or land in spam. The fix is to reduce your lookups by flattening includes into IP addresses.",
            "SPF PermError",
            "Fix SPF PermError from too many DNS lookups",
            "SPF stops at 10 DNS lookups. Exceeding that yields PermError; flattening swaps include: for ip4/ip6 to cut lookups.",
            [
                "Run DNS Preflight and note lookup count",
                "Find heavy includes",
                "Get IP ranges from providers",
                "Replace include: with ip4:",
                "Confirm under 10 lookups",
                "Publish TXT and verify",
            ],
            [
                "Step 1 Run DNS Preflight → expand SPF tree → note total lookup count",
                "Step 2 Identify which includes consume the most lookups",
                "Step 3 For each high-lookup provider, get current IP ranges from their documentation",
                "Step 4 Replace include: with ip4: and ip6: entries in your SPF TXT",
                "Step 5 Re-run DNS Preflight → confirm count is under 10",
                "Step 6 Publish updated TXT record and verify SPF passes",
            ],
            [
                ("What causes SPF PermError?", "Too many DNS lookups or invalid SPF syntax. Too many include: statements is the usual cause."),
                ("Will SPF PermError make my email bounce?", "Depends on the receiver. Many treat PermError as fail and reject or spam-folder the mail."),
                ("What is SPF flattening?", "Replacing include: with the actual IP ranges they resolve to — those hops then cost zero lookups."),
                ("How do I check my SPF lookup count?", "Run DNS Preflight — the SPF tree expands includes and shows a running total."),
                ("Does SPF PermError affect DMARC?", "Yes — SPF alignment fails on PermError. DMARC can still pass if DKIM aligns."),
            ],
            """      <h2>What this error means</h2>
      <p>SPF allows exactly 10 DNS lookups to evaluate your record. Add too many email providers — SendGrid, Mailgun, Google, HubSpot — and each one adds lookups. Go over 10 and receivers return PermError. They may reject the mail outright.</p>

      <h2>How to diagnose</h2>
      <p>Run <strong>DNS Preflight</strong> on your domain. Expand the SPF lookup tree — it shows exactly which provider burns each lookup and your running total.</p>

      <h2>The fix</h2>
      <p>Replace <code>include:</code> statements with the IP ranges they resolve to. You trade zero lookups for keeping the list updated when vendors move subnets.</p>
      <div class="dns-block">Before: v=spf1 include:sendgrid.net ~all
After:  v=spf1 ip4:167.89.0.0/17 ip4:198.37.144.0/20 ~all</div>

      <h2>Fix it step by step</h2>
      <div class="howto-step" id="step1"><strong>Step 1</strong> Run DNS Preflight → expand SPF tree → note total lookup count</div>
      <div class="howto-step" id="step2"><strong>Step 2</strong> Identify which includes consume the most lookups</div>
      <div class="howto-step" id="step3"><strong>Step 3</strong> For each high-lookup provider, get current IP ranges from their documentation</div>
      <div class="howto-step" id="step4"><strong>Step 4</strong> Replace <code>include:</code> with <code>ip4:</code> / <code>ip6:</code> entries in your SPF record</div>
      <div class="howto-step" id="step5"><strong>Step 5</strong> Re-run DNS Preflight → confirm count is under 10</div>
      <div class="howto-step" id="step6"><strong>Step 6</strong> Publish updated TXT record and verify SPF passes</div>

      <div class="tool-cta">
        <p>Run DNS Preflight to count SPF lookups</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/fix/spf/too-many-lookups/">SPF too many lookups fix</a> ·
        <a href="/glossary/spf-record/">SPF record</a>
      </div>

      <section class="faq-section" aria-label="FAQ">
        <h2>FAQ</h2>
        <h3>What causes SPF PermError?</h3>
        <p>Too many DNS lookups or invalid SPF syntax. Too many include: statements is the usual cause.</p>
        <h3>Will SPF PermError make my email bounce?</h3>
        <p>Depends on the receiver. Many treat PermError as fail and reject or spam-folder the mail.</p>
        <h3>What is SPF flattening?</h3>
        <p>Replacing include: with the actual IP ranges they resolve to — those hops then cost zero lookups.</p>
        <h3>How do I check my SPF lookup count?</h3>
        <p>Run DNS Preflight — the SPF tree expands includes and shows a running total.</p>
        <h3>Does SPF PermError affect DMARC?</h3>
        <p>Yes — SPF alignment fails on PermError. DMARC can still pass if DKIM aligns.</p>
      </section>

      <div class="internal-links">
        <p><a href="/error/">← All error fixes</a></p>
        <p><a href="https://domainpreflight.dev/">Open DNS Preflight and re-check your zone →</a></p>
      </div>""",
        ),
        (
            "dmarc-alignment-failed",
            "Messages Failing DMARC Alignment — Fix Guide",
            "DMARC alignment fails when From: doesn’t match SPF or DKIM domains — common with ESPs until you add their CNAMEs.",
            "DMARC Alignment Failing — Why and How to Fix It",
            "DMARC alignment fails when your From: domain doesn’t match the domain used for SPF or DKIM. Third-party senders often need their CNAME bundle — not just your SPF TXT.",
            "DMARC alignment",
            "Fix DMARC alignment failures",
            "Alignment requires From: to match Return-Path (SPF) or DKIM d=; ESPs need branded DNS.",
            [
                "Check alignment in Preflight",
                "Find the mismatching provider",
                "Open provider fix guide",
                "Add CNAME records",
                "Wait and re-check",
                "Confirm green alignment",
            ],
            [
                "Step 1 Run DNS Preflight → check alignment at the top of ACTIONS — does From match Return-Path?",
                "Step 2 Identify which provider is causing the mismatch (provider detection cards)",
                "Step 3 Open the provider-specific fix guide for your sender",
                "Step 4 Add the required CNAME records to your DNS",
                "Step 5 Wait up to 48 hours for propagation then re-run DNS Preflight",
                "Step 6 Confirm alignment shows green → ✓",
            ],
            [
                ("Why does DMARC fail even when SPF and DKIM both pass?", "DMARC needs alignment — passes must be for your domain, not sendgrid.net. A pass on the wrong domain doesn’t count."),
                ("How do I know which provider is causing the failure?", "DNS Preflight detects your sender and shows which CNAMEs or records are missing."),
                ("Can DMARC pass with only DKIM alignment?", "Yes — either SPF or DKIM alignment is enough. You don’t need both."),
                ("What is relaxed vs strict DMARC alignment?", "Relaxed (default) lets subdomains align with the org domain. Strict needs an exact domain match."),
                ("How long after fixing CNAMEs will DMARC pass?", "DNS can take up to 48 hours. Re-run Preflight then watch aggregate reports."),
            ],
            """      <h2>What this error means</h2>
      <p>DMARC doesn’t stop at SPF/DKIM pass — the domain in From: must match the domain that passed SPF (Return-Path) or DKIM (<code>d=</code>). SendGrid signing as <code>sendgrid.net</code> is a DKIM pass — but not aligned with your brand.</p>

      <h2>Common causes</h2>
      <ul>
        <li>ESP not set up for branded sending (missing CNAMEs)</li>
        <li>Return-Path doesn’t match your From: domain</li>
        <li>DKIM selector missing or pointing at the provider’s domain only</li>
      </ul>

      <h2>Fix it step by step</h2>
      <div class="howto-step" id="step1"><strong>Step 1</strong> Run DNS Preflight → check alignment at the top of ACTIONS — does From match Return-Path?</div>
      <div class="howto-step" id="step2"><strong>Step 2</strong> Identify which provider is causing the mismatch (provider detection cards)</div>
      <div class="howto-step" id="step3"><strong>Step 3</strong> Open the provider-specific fix guide for your sender</div>
      <div class="howto-step" id="step4"><strong>Step 4</strong> Add the required CNAME records to your DNS</div>
      <div class="howto-step" id="step5"><strong>Step 5</strong> Wait up to 48 hours for propagation then re-run DNS Preflight</div>
      <div class="howto-step" id="step6"><strong>Step 6</strong> Confirm alignment shows green → ✓</div>

      <div class="tool-cta">
        <p>Run DNS Preflight to see alignment and missing DNS</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/fix/dmarc/">DMARC fix guides by provider</a> ·
        <a href="/glossary/dmarc-alignment/">DMARC alignment</a> ·
        <a href="/glossary/dmarc/">DMARC</a>
      </div>

      <section class="faq-section" aria-label="FAQ">
        <h2>FAQ</h2>
        <h3>Why does DMARC fail even when SPF and DKIM both pass?</h3>
        <p>DMARC needs alignment — passes must be for your domain, not sendgrid.net. A pass on the wrong domain doesn’t count.</p>
        <h3>How do I know which provider is causing the failure?</h3>
        <p>DNS Preflight detects your sender and shows which CNAMEs or records are missing.</p>
        <h3>Can DMARC pass with only DKIM alignment?</h3>
        <p>Yes — either SPF or DKIM alignment is enough. You don’t need both.</p>
        <h3>What is relaxed vs strict DMARC alignment?</h3>
        <p>Relaxed (default) lets subdomains align with the org domain. Strict needs an exact domain match.</p>
        <h3>How long after fixing CNAMEs will DMARC pass?</h3>
        <p>DNS can take up to 48 hours. Re-run Preflight then watch aggregate reports.</p>
      </section>

      <div class="internal-links">
        <p><a href="/error/">← All error fixes</a></p>
        <p><a href="https://domainpreflight.dev/">Open DNS Preflight and re-check your zone →</a></p>
      </div>""",
        ),
        (
            "dkim-signature-failed",
            "DKIM Signature Verification Failed — Fix",
            "DKIM verification failed — key mismatch, body changed in transit, wrong selector, or truncated TXT. Fix headers and DNS.",
            "DKIM Signature Verification Failed — Causes and Fixes",
            "Verification fails when DNS’s public key doesn’t match the signer, the body changed in flight, or the selector TXT is missing or wrong. Headers tell you which one.",
            "DKIM signature failed",
            "Fix DKIM signature verification failures",
            "DKIM fails when keys mismatch, selectors don’t resolve, or mailing lists rewrite content.",
            [
                "Get raw headers",
                "Paste into Email tool",
                "Read selector from s=",
                "Check DNS TXT",
                "Fix key mismatch",
                "Check body alteration",
            ],
            [
                "Step 1 Get raw email headers — Gmail: ⋮ → Show original | Outlook: File → Properties",
                "Step 2 Paste into DomainPreflight Email header analyzer",
                "Step 3 Find the s= tag in DKIM-Signature — that’s your selector",
                "Step 4 Check that selector._domainkey.yourdomain.com exists in DNS",
                "Step 5 If key mismatch → regenerate and republish the DKIM record",
                "Step 6 If body alteration → check if a mailing list or forwarder modified the message",
            ],
            [
                ("What does DKIM signature verification failed mean?", "The receiver checked your DKIM signature against DNS and it didn’t verify — or no key was found at the selector."),
                ("Can forwarded emails fail DKIM?", "Yes — forwarding often rewrites headers or body. That’s expected; not always your DNS."),
                ("How do I find which DKIM selector was used?", "Read the DKIM-Signature header — the s= tag is the selector name."),
                ("My DKIM TXT exists but verification still fails — why?", "Truncated or split TXT is a common culprit. The full public key must be published correctly."),
                ("Does DKIM failure always bounce email?", "No — DMARC can still pass on SPF alignment. DKIM fail alone often means spam folder, not always hard bounce."),
            ],
            """      <h2>Common causes</h2>
      <ol style="color: var(--text2); font-size: 0.9rem; margin: 0.5rem 0 1rem 1.25rem;">
        <li><strong>Key mismatch</strong> — you rotated keys but DNS still has the old one (or the opposite)</li>
        <li><strong>Message altered</strong> — lists and some forwarders change the body</li>
        <li><strong>Wrong selector</strong> — <code>s=</code> in the message doesn’t match a TXT</li>
        <li><strong>Truncated TXT</strong> — long keys split wrong at the DNS host</li>
      </ol>

      <h2>How to diagnose</h2>
      <p>Paste raw headers into <strong>DomainPreflight Email</strong> — it surfaces DKIM-Signature, selector, and whether things line up.</p>

      <h2>Fix it step by step</h2>
      <div class="howto-step" id="step1"><strong>Step 1</strong> Get raw email headers — Gmail: ⋮ → Show original | Outlook: File → Properties</div>
      <div class="howto-step" id="step2"><strong>Step 2</strong> Paste into DomainPreflight Email header analyzer</div>
      <div class="howto-step" id="step3"><strong>Step 3</strong> Find the <code>s=</code> tag in DKIM-Signature — that’s your selector</div>
      <div class="howto-step" id="step4"><strong>Step 4</strong> Check that <code>selector._domainkey.yourdomain.com</code> exists in DNS</div>
      <div class="howto-step" id="step5"><strong>Step 5</strong> If key mismatch → regenerate and republish the DKIM record</div>
      <div class="howto-step" id="step6"><strong>Step 6</strong> If body alteration → check if a mailing list or forwarder modified the message</div>

      <div class="tool-cta">
        <p>Open the Email tool to parse headers</p>
        <p><a href="/email/">Open Email tool →</a> · <a href="https://domainpreflight.dev/">DNS Preflight</a></p>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/fix/dkim/signature-failed/">DKIM signature failed fix</a> ·
        <a href="/fix/dkim/selector/">DKIM selectors</a> ·
        <a href="/fix/dkim/rotate-keys/">Key rotation</a> ·
        <a href="/glossary/dkim/">DKIM</a>
      </div>

      <section class="faq-section" aria-label="FAQ">
        <h2>FAQ</h2>
        <h3>What does DKIM signature verification failed mean?</h3>
        <p>The receiver checked your DKIM signature against DNS and it didn’t verify — or no key was found at the selector.</p>
        <h3>Can forwarded emails fail DKIM?</h3>
        <p>Yes — forwarding often rewrites headers or body. That’s expected; not always your DNS.</p>
        <h3>How do I find which DKIM selector was used?</h3>
        <p>Read the DKIM-Signature header — the s= tag is the selector name.</p>
        <h3>My DKIM TXT exists but verification still fails — why?</h3>
        <p>Truncated or split TXT is a common culprit. The full public key must be published correctly.</p>
        <h3>Does DKIM failure always bounce email?</h3>
        <p>No — DMARC can still pass on SPF alignment. DKIM fail alone often means spam folder, not always hard bounce.</p>
      </section>

      <div class="internal-links">
        <p><a href="/error/">← All error fixes</a></p>
        <p><a href="https://domainpreflight.dev/">Open DNS Preflight and re-check your zone →</a></p>
      </div>""",
        ),
        (
            "emails-going-to-spam",
            "Emails Going to Spam Despite SPF and DKIM Passing",
            "Spam folder with SPF/DKIM pass — check DMARC enforcement, PTR, reputation, blocklists, and content.",
            "Emails Landing in Spam — Why and How to Fix It",
            "SPF and DKIM passing only means you’re authenticated — not trusted. DMARC at none, bad PTR, blocklists, content, or cold IP still land you in spam.",
            "Spam folder",
            "Reduce spam-folder placement when auth passes",
            "Check DMARC policy, PTR, lists, content, and IP warmup.",
            [
                "Run full Preflight check",
                "Tighten DMARC if none",
                "Fix PTR",
                "Delist if blocked",
                "Review content",
                "Warm new IP",
            ],
            [
                "Step 1 Run DNS Preflight → check health score and all cards",
                "Step 2 If DMARC shows p=none → plan upgrade to p=quarantine",
                "Step 3 If PTR missing → contact your host to add reverse DNS",
                "Step 4 If IP on blocklist → follow /error/blacklisted-ip/ for delisting",
                "Step 5 Check content — test with mail-tester.com alongside DomainPreflight",
                "Step 6 If new IP → warm gradually with low volume",
            ],
            [
                ("SPF and DKIM pass — why am I still in spam?", "Auth proves identity — not trust. Reputation, DMARC enforcement, PTR, lists, and content all move the inbox needle."),
                ("What’s the fastest fix?", "Fix missing PTR, move DMARC toward quarantine/reject when safe, and clear blocklists — big impact fast."),
                ("How do I check blocklists?", "Use DomainPreflight Email — enter your sending IP and we check major lists."),
                ("Does DMARC p=none help spam placement?", "No — none only reports. It doesn’t block spoofing or fix reputation."),
                ("How long to build IP reputation?", "Often 2–4 weeks of consistent, low-bounce sending. Ramp volume slowly."),
            ],
            """      <h2>Common causes (rough order)</h2>
      <ol style="color: var(--text2); font-size: 0.9rem; margin: 0.5rem 0 1rem 1.25rem;">
        <li>DMARC at <code>p=none</code> — no enforcement</li>
        <li>No PTR or PTR doesn’t forward-resolve</li>
        <li>IP on a blocklist</li>
        <li>New IP with no history</li>
        <li>Content triggers — spammy words, bad HTML/text ratio, no unsubscribe</li>
        <li>Low engagement — people mark spam or never open</li>
      </ol>

      <h2>How to diagnose</h2>
      <p>Run <strong>DNS Preflight</strong> with your sending IP — PTR, lists, SPF, DKIM, DMARC in one pass.</p>

      <h2>Fix it step by step</h2>
      <div class="howto-step" id="step1"><strong>Step 1</strong> Run DNS Preflight → check health score and all cards</div>
      <div class="howto-step" id="step2"><strong>Step 2</strong> If DMARC shows <code>p=none</code> → plan upgrade to <code>p=quarantine</code></div>
      <div class="howto-step" id="step3"><strong>Step 3</strong> If PTR missing → contact your host to add reverse DNS</div>
      <div class="howto-step" id="step4"><strong>Step 4</strong> If IP on blocklist → follow <a href="/error/blacklisted-ip/">blacklisted IP</a> for delisting</div>
      <div class="howto-step" id="step5"><strong>Step 5</strong> Check content — test with mail-tester.com alongside DomainPreflight</div>
      <div class="howto-step" id="step6"><strong>Step 6</strong> If new IP → warm gradually with low volume</div>

      <div class="tool-cta">
        <p>Run DNS Preflight and the Email IP checker</p>
        <p><a href="https://domainpreflight.dev/">DNS Preflight →</a> · <a href="/email/">Email tool</a></p>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/error/blacklisted-ip/">Blacklisted IP</a> ·
        <a href="/glossary/dmarc/">DMARC</a> ·
        <a href="/glossary/ptr-record/">PTR record</a>
      </div>

      <section class="faq-section" aria-label="FAQ">
        <h2>FAQ</h2>
        <h3>SPF and DKIM pass — why am I still in spam?</h3>
        <p>Auth proves identity — not trust. Reputation, DMARC enforcement, PTR, lists, and content all move the inbox needle.</p>
        <h3>What’s the fastest fix?</h3>
        <p>Fix missing PTR, move DMARC toward quarantine/reject when safe, and clear blocklists — big impact fast.</p>
        <h3>How do I check blocklists?</h3>
        <p>Use DomainPreflight Email — enter your sending IP and we check major lists.</p>
        <h3>Does DMARC p=none help spam placement?</h3>
        <p>No — none only reports. It doesn’t block spoofing or fix reputation.</p>
        <h3>How long to build IP reputation?</h3>
        <p>Often 2–4 weeks of consistent, low-bounce sending. Ramp volume slowly.</p>
      </section>

      <div class="internal-links">
        <p><a href="/error/">← All error fixes</a></p>
        <p><a href="https://domainpreflight.dev/">Open DNS Preflight and re-check your zone →</a></p>
      </div>""",
        ),
        (
            "blacklisted-ip",
            "Email Server IP on Blacklist — Delisting Guide",
            "Your sending IP is on a blocklist — fix the cause and request delisting. Check lists with the Email tool.",
            "Your Sending IP Is Blacklisted — How to Get Delisted",
            "Blocklists flag IPs that sent spam. Receivers may reject mail before SPF/DKIM. Fix the root cause — then request removal.",
            "Blacklisted IP",
            "Delist a blacklisted sending IP",
            "Identify lists, fix compromise or hygiene, submit removals, re-check.",
            [
                "Identify lists",
                "Fix root cause",
                "Submit removals",
                "Wait for removal",
                "Re-check lists",
                "Monitor bounces",
            ],
            [
                "Step 1 Run DomainPreflight Email → see which lists you’re on",
                "Step 2 Fix the cause — compromised host, open relay, high bounces",
                "Step 3 Go to each blacklist removal page and submit a request",
                "Step 4 Wait — most removals take 24–72 hours",
                "Step 5 Re-run DomainPreflight to confirm removal",
                "Step 6 Monitor sending — keep bounce rate under ~2%",
            ],
            [
                ("How do I know if my IP is blacklisted?", "Run DomainPreflight Email with your sending IP — we check many major lists at once."),
                ("How long does delisting take?", "Spamhaus often 24–48h after request. SpamCop can auto-expire in 24–48h. Barracuda often 12–24h — varies by list."),
                ("Can I send while blacklisted?", "Some mail still slips through — not every receiver checks every list. Fix it anyway."),
                ("I didn’t send spam — why am I listed?", "Often a compromised account, bad script, shared IP, or a neighbor on shared hosting."),
                ("Will delisting fix spam folder issues?", "Yes if the list was the main driver. If not, check PTR, DMARC, and content next."),
            ],
            """      <h2>How to see which lists you’re on</h2>
      <p>Run <strong>DomainPreflight Email</strong> with your sending IP — Spamhaus, SpamCop, Barracuda, and more in one pass.</p>

      <h2>Why IPs get listed</h2>
      <ul>
        <li>Compromised server blasting spam</li>
        <li>High bounces</li>
        <li>Spam trap hits</li>
        <li>Sudden volume spike</li>
        <li>Shared IP with a bad neighbor</li>
      </ul>

      <h2>Delisting quick refs</h2>
      <p><strong>Spamhaus:</strong> spamhaus.org/removal — fix first, then request.<br /><strong>SpamCop:</strong> often auto-expires 24–48h after spam stops.<br /><strong>Barracuda:</strong> barracudacentral.org/lookups → request removal.</p>

      <h2>Fix it step by step</h2>
      <div class="howto-step" id="step1"><strong>Step 1</strong> Run DomainPreflight Email → see which lists you’re on</div>
      <div class="howto-step" id="step2"><strong>Step 2</strong> Fix the cause — compromised host, open relay, high bounces</div>
      <div class="howto-step" id="step3"><strong>Step 3</strong> Go to each blacklist removal page and submit a request</div>
      <div class="howto-step" id="step4"><strong>Step 4</strong> Wait — most removals take 24–72 hours</div>
      <div class="howto-step" id="step5"><strong>Step 5</strong> Re-run DomainPreflight to confirm removal</div>
      <div class="howto-step" id="step6"><strong>Step 6</strong> Monitor sending — keep bounce rate under ~2%</div>

      <div class="tool-cta">
        <p>Check your IP against blocklists</p>
        <p><a href="/email/">Open Email tool →</a></p>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/error/emails-going-to-spam/">Emails going to spam</a> ·
        <a href="/glossary/email-spoofing/">Email spoofing</a>
      </div>

      <section class="faq-section" aria-label="FAQ">
        <h2>FAQ</h2>
        <h3>How do I know if my IP is blacklisted?</h3>
        <p>Run DomainPreflight Email with your sending IP — we check many major lists at once.</p>
        <h3>How long does delisting take?</h3>
        <p>Spamhaus often 24–48h after request. SpamCop can auto-expire in 24–48h. Barracuda often 12–24h — varies by list.</p>
        <h3>Can I send while blacklisted?</h3>
        <p>Some mail still slips through — not every receiver checks every list. Fix it anyway.</p>
        <h3>I didn’t send spam — why am I listed?</h3>
        <p>Often a compromised account, bad script, shared IP, or a neighbor on shared hosting.</p>
        <h3>Will delisting fix spam folder issues?</h3>
        <p>Yes if the list was the main driver. If not, check PTR, DMARC, and content next.</p>
      </section>

      <div class="internal-links">
        <p><a href="/error/">← All error fixes</a></p>
        <p><a href="https://domainpreflight.dev/">Open DNS Preflight and re-check your zone →</a></p>
        <p><a href="https://domainpreflight.dev/email/">Email Deliverability (IP &amp; lists) →</a></p>
      </div>""",
        ),
        (
            "550-rejected",
            "550 5.7.1 Email Rejected — Fix Guide",
            "550 5.7.1 means policy rejection — SPF, DKIM, DMARC, or reputation. Read the bounce text and fix DNS or IP.",
            "550 5.7.1 Email Rejected Due to Security Policies",
            "550 5.7.1 is a policy block — SPF, DKIM, DMARC, or IP rep. The bounce text usually says which. Most fixes are DNS or hygiene.",
            "550 5.7.1 rejected",
            "Fix 550 5.7.1 SMTP rejections",
            "Read bounce, run Preflight, fix failing check, retest.",
            [
                "Read full bounce",
                "Run DNS Preflight",
                "Fix failing check",
                "Check IP lists",
                "Resend test",
                "Gmail 5.7.26 and DMARC",
            ],
            [
                "Step 1 Read the full bounce message — the 550 subcode tells you which check failed",
                "Step 2 Run DNS Preflight on your domain with your sending IP",
                "Step 3 Fix the failing SPF, DKIM, or DMARC issue",
                "Step 4 If IP reputation → check blacklists in Email tool",
                "Step 5 Re-send a test after changes",
                "Step 6 If Gmail 5.7.26 → add a DMARC record (even p=none) for bulk senders",
            ],
            [
                ("What does 550 5.7.1 mean?", "Policy rejection — SPF, DKIM, DMARC, or reputation. The text after 5.7.1 usually names the failure."),
                ("How do I fix 550 5.7.26 from Gmail?", "Add a DMARC TXT record — Gmail requires DMARC for bulk senders. Even p=none is often enough to stop that rejection."),
                ("SPF and DKIM pass but I still get 550 — why?", "Check alignment — passes on the wrong domain still fail DMARC. Preflight shows alignment."),
                ("Will DNS fixes stop 550s immediately?", "DNS can take up to 48 hours to propagate. Re-test after TTL settles."),
                ("I only email one person — can it still be DNS?", "Yes — corporate gateways can enforce strict DMARC regardless of volume."),
            ],
            """      <h2>Common 550 variants</h2>
      <ul>
        <li><strong>SPF failed</strong> — your IP isn’t authorized in SPF</li>
        <li><strong>DKIM failed</strong> — key mismatch or missing TXT</li>
        <li><strong>DMARC rejected</strong> — <code>p=reject</code> and alignment failed</li>
        <li><strong>5.7.26 unauthenticated</strong> (Gmail) — bulk path without DMARC</li>
      </ul>

      <h2>Fix it step by step</h2>
      <div class="howto-step" id="step1"><strong>Step 1</strong> Read the full bounce message — the 550 subcode tells you which check failed</div>
      <div class="howto-step" id="step2"><strong>Step 2</strong> Run DNS Preflight on your domain with your sending IP</div>
      <div class="howto-step" id="step3"><strong>Step 3</strong> Fix the failing SPF, DKIM, or DMARC issue</div>
      <div class="howto-step" id="step4"><strong>Step 4</strong> If IP reputation → check blacklists in Email tool</div>
      <div class="howto-step" id="step5"><strong>Step 5</strong> Re-send a test after changes</div>
      <div class="howto-step" id="step6"><strong>Step 6</strong> If Gmail 5.7.26 → add a DMARC record (even p=none) for bulk senders</div>

      <div class="tool-cta">
        <p>Run DNS Preflight to see what’s failing</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>

      <div class="glossary-links"><strong>Related errors:</strong>
        <a href="/error/spf-permerror/">SPF PermError</a> ·
        <a href="/error/dkim-signature-failed/">DKIM signature failed</a> ·
        <a href="/error/dmarc-alignment-failed/">DMARC alignment</a> ·
        <a href="/error/blacklisted-ip/">Blacklisted IP</a>
      </div>

      <section class="faq-section" aria-label="FAQ">
        <h2>FAQ</h2>
        <h3>What does 550 5.7.1 mean?</h3>
        <p>Policy rejection — SPF, DKIM, DMARC, or reputation. The text after 5.7.1 usually names the failure.</p>
        <h3>How do I fix 550 5.7.26 from Gmail?</h3>
        <p>Add a DMARC TXT record — Gmail requires DMARC for bulk senders. Even p=none is often enough to stop that rejection.</p>
        <h3>SPF and DKIM pass but I still get 550 — why?</h3>
        <p>Check alignment — passes on the wrong domain still fail DMARC. Preflight shows alignment.</p>
        <h3>Will DNS fixes stop 550s immediately?</h3>
        <p>DNS can take up to 48 hours to propagate. Re-test after TTL settles.</p>
        <h3>I only email one person — can it still be DNS?</h3>
        <p>Yes — corporate gateways can enforce strict DMARC regardless of volume.</p>
      </section>

      <div class="internal-links">
        <p><a href="/error/">← All error fixes</a></p>
        <p><a href="https://domainpreflight.dev/">Open DNS Preflight and re-check your zone →</a></p>
      </div>""",
        ),
        (
            "dkim-none",
            "DKIM Status None — No Signature on Email",
            "DKIM none means no signature on the message — enable signing at your provider and publish selector._domainkey TXT.",
            "DKIM Status None — Your Emails Aren't Being Signed",
            "DKIM “none” means no signature at all — not a bad signature. Turn on signing and publish the TXT. Usually easier than “fail.”",
            "DKIM none",
            "Fix DKIM none — enable signing and DNS",
            "Enable DKIM in provider, publish TXT, wait for DNS, verify in Preflight.",
            [
                "Check Preflight DKIM card",
                "Identify provider",
                "Enable signing",
                "Publish TXT",
                "Wait and re-check",
                "Confirm with a test send",
            ],
            [
                "Step 1 Run DNS Preflight → does the DKIM card show none or no record?",
                "Step 2 Identify your sending provider (alignment engine)",
                "Step 3 Enable DKIM signing in your provider dashboard",
                "Step 4 Publish the DKIM TXT record to your DNS",
                "Step 5 Wait up to 48 hours → re-run DNS Preflight → confirm DKIM pass",
                "Step 6 Send a test email and confirm DKIM-Signature appears in headers",
            ],
            [
                ("What does DKIM none mean?", "No DKIM signature on the message — nothing to verify at the receiver."),
                ("Is none worse than fail?", "Both hurt DMARC. None means signing wasn’t on. Fail means DNS didn’t match. None is often easier to fix."),
                ("How do I enable DKIM signing?", "Use your provider’s domain authentication or sender authentication flow — pick the fix guide for your ESP."),
                ("Provider says enabled but Preflight shows none — why?", "You still need the TXT in DNS — dashboard + DNS are two steps."),
                ("Does DKIM none hurt inbox placement?", "Yes — big inboxes use DKIM as a trust signal. No DKIM plus weak DMARC raises spam risk."),
            ],
            """      <h2>none vs fail vs pass</h2>
      <p><strong>none</strong> — no signature. <strong>fail</strong> — signature didn’t verify. <strong>pass</strong> — good. none is fixable — flip signing on and publish DNS.</p>

      <h2>Common causes</h2>
      <ul>
        <li>DKIM not enabled in the provider</li>
        <li>New ESP without domain authentication</li>
        <li>Subdomain sending with no DKIM row</li>
        <li>Wrong selector — DNS doesn’t match what signs</li>
      </ul>

      <h2>Fix it step by step</h2>
      <div class="howto-step" id="step1"><strong>Step 1</strong> Run DNS Preflight → does the DKIM card show none or no record?</div>
      <div class="howto-step" id="step2"><strong>Step 2</strong> Identify your sending provider (alignment engine)</div>
      <div class="howto-step" id="step3"><strong>Step 3</strong> Enable DKIM signing in your provider dashboard</div>
      <div class="howto-step" id="step4"><strong>Step 4</strong> Publish the DKIM TXT record to your DNS</div>
      <div class="howto-step" id="step5"><strong>Step 5</strong> Wait up to 48 hours → re-run DNS Preflight → confirm DKIM pass</div>
      <div class="howto-step" id="step6"><strong>Step 6</strong> Send a test email and confirm DKIM-Signature appears in headers</div>

      <div class="tool-cta">
        <p>Run DNS Preflight to confirm DKIM DNS</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>

      <div class="glossary-links"><strong>Provider guides:</strong>
        <a href="/fix/dkim/sendgrid/">SendGrid DKIM</a> ·
        <a href="/fix/dkim/google-workspace/">Google Workspace</a> ·
        <a href="/fix/dkim/microsoft-365/">Microsoft 365</a> ·
        <a href="/glossary/dkim/">DKIM</a>
      </div>

      <section class="faq-section" aria-label="FAQ">
        <h2>FAQ</h2>
        <h3>What does DKIM none mean?</h3>
        <p>No DKIM signature on the message — nothing to verify at the receiver.</p>
        <h3>Is none worse than fail?</h3>
        <p>Both hurt DMARC. None means signing wasn’t on. Fail means DNS didn’t match. None is often easier to fix.</p>
        <h3>How do I enable DKIM signing?</h3>
        <p>Use your provider’s domain authentication or sender authentication flow — pick the fix guide for your ESP.</p>
        <h3>Provider says enabled but Preflight shows none — why?</h3>
        <p>You still need the TXT in DNS — dashboard + DNS are two steps.</p>
        <h3>Does DKIM none hurt inbox placement?</h3>
        <p>Yes — big inboxes use DKIM as a trust signal. No DKIM plus weak DMARC raises spam risk.</p>
      </section>

      <div class="internal-links">
        <p><a href="/error/">← All error fixes</a></p>
        <p><a href="https://domainpreflight.dev/">Open DNS Preflight and re-check your zone →</a></p>
      </div>""",
        ),
        (
            "ptr-mismatch",
            "PTR Record Mismatch — Reverse DNS Fix Guide",
            "PTR mismatch — reverse DNS hostname doesn’t forward-resolve to your IP. Fix rDNS and matching A record.",
            "PTR Record Mismatch — Your Reverse DNS Is Wrong",
            "A PTR mismatch means your IP’s hostname doesn’t round-trip to the same IP. FCrDNS fails — many servers junk or reject on that.",
            "PTR mismatch",
            "Fix PTR / FCrDNS mismatch",
            "Check PTR, verify A record back to IP, fix at host.",
            [
                "Preflight PTR card",
                "Note PTR hostname",
                "Verify A record",
                "Fix at hosting panel",
                "Add matching A",
                "Re-check Preflight",
            ],
            [
                "Step 1 Run DNS Preflight with your sending IP → check PTR card",
                "Step 2 Note the hostname PTR returns",
                "Step 3 Check that hostname’s A record points back to your IP",
                "Step 4 If mismatch → log into your hosting provider control panel",
                "Step 5 Set reverse DNS to a hostname whose A points to your IP (e.g. mail.yourdomain.com)",
                "Step 6 Add the A record if missing → re-run DNS Preflight",
            ],
            [
                ("What is a PTR mismatch?", "PTR returns a hostname, but that hostname’s A doesn’t point back to your sending IP — FCrDNS fails."),
                ("Who fixes PTR?", "Your host or ISP — not the domain registrar. Look for reverse DNS in the VPS panel."),
                ("Does PTR mismatch bounce mail?", "Sometimes — more often it raises spam score."),
                ("What PTR hostname should I use?", "A name you control — mail.yourdomain.com — with an A record to the same IP."),
                ("Panel says PTR is right but Preflight disagrees?", "Propagation can take 24–48h. Double-check the A record for the PTR name."),
            ],
            """      <h2>What FCrDNS means</h2>
      <p>Receiver does PTR on your IP → gets <code>mail.example.com</code>. Then A on <code>mail.example.com</code> must return your IP. Different IP → mismatch.</p>

      <h2>Who controls PTR</h2>
      <p>Your cloud or ISP — set rDNS in the panel (Hetzner, DO, AWS, etc.). Not your registrar’s MX screen.</p>

      <h2>Fix it step by step</h2>
      <div class="howto-step" id="step1"><strong>Step 1</strong> Run DNS Preflight with your sending IP → check PTR card</div>
      <div class="howto-step" id="step2"><strong>Step 2</strong> Note the hostname PTR returns</div>
      <div class="howto-step" id="step3"><strong>Step 3</strong> Check that hostname’s A record points back to your IP</div>
      <div class="howto-step" id="step4"><strong>Step 4</strong> If mismatch → log into your hosting provider control panel</div>
      <div class="howto-step" id="step5"><strong>Step 5</strong> Set reverse DNS to a hostname whose A points to your IP (e.g. mail.yourdomain.com)</div>
      <div class="howto-step" id="step6"><strong>Step 6</strong> Add the A record if missing → re-run DNS Preflight</div>

      <div class="tool-cta">
        <p>Run DNS Preflight with your sending IP</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/glossary/ptr-record/">PTR record</a> ·
        <a href="/error/emails-going-to-spam/">Emails going to spam</a>
      </div>

      <section class="faq-section" aria-label="FAQ">
        <h2>FAQ</h2>
        <h3>What is a PTR mismatch?</h3>
        <p>PTR returns a hostname, but that hostname’s A doesn’t point back to your sending IP — FCrDNS fails.</p>
        <h3>Who fixes PTR?</h3>
        <p>Your host or ISP — not the domain registrar. Look for reverse DNS in the VPS panel.</p>
        <h3>Does PTR mismatch bounce mail?</h3>
        <p>Sometimes — more often it raises spam score.</p>
        <h3>What PTR hostname should I use?</h3>
        <p>A name you control — mail.yourdomain.com — with an A record to the same IP.</p>
        <h3>Panel says PTR is right but Preflight disagrees?</h3>
        <p>Propagation can take 24–48h. Double-check the A record for the PTR name.</p>
      </section>

      <div class="internal-links">
        <p><a href="/error/">← All error fixes</a></p>
        <p><a href="https://domainpreflight.dev/">Open DNS Preflight and re-check your zone →</a></p>
      </div>""",
        ),
        (
            "no-mx-record",
            "Domain Has No MX Record — Fix Guide",
            "No MX record — your domain can’t receive mail. Add MX from your email provider at your DNS host.",
            "No MX Record Found — Your Domain Can't Receive Email",
            "MX tells the world where to deliver mail for your domain. No MX = bounces. Sending outbound still works — only inbound breaks.",
            "No MX record",
            "Add MX records to receive email",
            "Verify in Preflight, add MX at DNS, set priorities, wait, re-check.",
            [
                "Check Preflight MX card",
                "Open DNS host",
                "Add MX from provider",
                "Set priorities",
                "Wait for propagation",
                "Confirm MX live",
            ],
            [
                "Step 1 Run DNS Preflight → does the MX card show records?",
                "Step 2 Log into your DNS provider (Cloudflare, Namecheap, etc.)",
                "Step 3 Add MX records from your email provider’s setup docs",
                "Step 4 Set lower number = higher priority for multiple MX",
                "Step 5 Wait up to 48 hours for propagation",
                "Step 6 Re-run DNS Preflight → confirm MX records appear",
            ],
            [
                ("What happens with no MX record?", "Inbound mail to your domain bounces — there’s nowhere to deliver."),
                ("Does missing MX affect sending?", "No — MX is inbound only. You can still send — replies won’t reach you if MX is missing."),
                ("What priority should I use?", "Lower number = higher priority. Single server often 10; multiple use 10, 20, …"),
                ("MX exists but mail still bounces — why?", "MX must point to a hostname with an A record. The server must accept SMTP on 25."),
                ("I deleted MX by accident — will mail queue?", "Senders retry for days — restore MX fast and most queued mail can still arrive."),
            ],
            """      <h2>What MX does</h2>
      <p>Other servers look up MX for <code>yourdomain.com</code> to find where to deliver mail. No MX — no delivery.</p>

      <h2>Examples (verify with your provider)</h2>
      <div class="dns-block">Google Workspace: aspmx.l.google.com (priority 1)
Microsoft 365: yourdomain-com.mail.protection.outlook.com
Fastmail: in1-smtp.messagingengine.com (priority 10)
Zoho: mx.zoho.com (priority 10)</div>

      <h2>Fix it step by step</h2>
      <div class="howto-step" id="step1"><strong>Step 1</strong> Run DNS Preflight → does the MX card show records?</div>
      <div class="howto-step" id="step2"><strong>Step 2</strong> Log into your DNS provider (Cloudflare, Namecheap, etc.)</div>
      <div class="howto-step" id="step3"><strong>Step 3</strong> Add MX records from your email provider’s setup docs</div>
      <div class="howto-step" id="step4"><strong>Step 4</strong> Set lower number = higher priority for multiple MX</div>
      <div class="howto-step" id="step5"><strong>Step 5</strong> Wait up to 48 hours for propagation</div>
      <div class="howto-step" id="step6"><strong>Step 6</strong> Re-run DNS Preflight → confirm MX records appear</div>

      <div class="tool-cta">
        <p>Run DNS Preflight to verify MX</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/glossary/dmarc/">DMARC</a> ·
        <a href="/fix/spf/google-workspace/">Google Workspace SPF</a>
      </div>

      <section class="faq-section" aria-label="FAQ">
        <h2>FAQ</h2>
        <h3>What happens with no MX record?</h3>
        <p>Inbound mail to your domain bounces — there’s nowhere to deliver.</p>
        <h3>Does missing MX affect sending?</h3>
        <p>No — MX is inbound only. You can still send — replies won’t reach you if MX is missing.</p>
        <h3>What priority should I use?</h3>
        <p>Lower number = higher priority. Single server often 10; multiple use 10, 20, …</p>
        <h3>MX exists but mail still bounces — why?</h3>
        <p>MX must point to a hostname with an A record. The server must accept SMTP on 25.</p>
        <h3>I deleted MX by accident — will mail queue?</h3>
        <p>Senders retry for days — restore MX fast and most queued mail can still arrive.</p>
      </section>

      <div class="internal-links">
        <p><a href="/error/">← All error fixes</a></p>
        <p><a href="https://domainpreflight.dev/">Open DNS Preflight and re-check your zone →</a></p>
      </div>""",
        ),
        (
            "dmarc-policy-none",
            "DMARC Policy Set to None — What It Means",
            "DMARC p=none monitors but doesn’t block — move to quarantine or reject after you read reports.",
            "DMARC p=none — You're Monitoring But Not Protected",
            "p=none means you’re collecting reports — not blocking spoofed mail. Start here — then move to quarantine or reject after you trust your senders.",
            "DMARC p=none",
            "Move from DMARC p=none to enforcement",
            "Add rua, read reports, fix senders, then tighten policy.",
            [
                "Add rua if missing",
                "Read reports in analyzer",
                "Fix failing senders",
                "Move to quarantine",
                "Monitor then reject",
                "Confirm in Preflight",
            ],
            [
                "Step 1 Add rua=mailto:… to your DMARC record if missing — you need reports before upgrading",
                "Step 2 Paste aggregate XML into DomainPreflight DMARC Report Analyzer",
                "Step 3 Fix any senders failing alignment before you enforce",
                "Step 4 After 2–4 weeks of clean reports → change p=none to p=quarantine",
                "Step 5 Monitor for a week → if clean, move toward p=reject",
                "Step 6 Run DNS Preflight to confirm the new policy is live",
            ],
            [
                ("Is DMARC p=none bad?", "Not for the first weeks — it’s the right starting point. Bad if you stay forever with no enforcement."),
                ("Can attackers spoof me with p=none?", "Yes — none doesn’t block. Reports show abuse — they don’t stop it."),
                ("How do I get aggregate reports?", "Add rua=mailto:dmarc@yourdomain.com to DMARC — big providers send daily XML zips."),
                ("When is it safe to move to p=reject?", "After weeks of reports showing legit senders aligned — use the analyzer to verify."),
                ("Will p=reject break my mail?", "Only if you still have unaligned legit senders. Fix alignment at none first — then enforce."),
            ],
            """      <h2>What p=none does</h2>
      <p>Collects aggregate reports so you see who sends as you. Doesn’t block or quarantine — visibility without risk.</p>

      <h2>When to stay vs move</h2>
      <p>Stay on none for 2–4 weeks while you learn your traffic. Move to <code>p=quarantine</code> when reports look clean — then <code>p=reject</code> when you’re brave.</p>

      <h2>Fix it step by step</h2>
      <div class="howto-step" id="step1"><strong>Step 1</strong> Add <code>rua=mailto:…</code> to your DMARC record if missing — you need reports before upgrading</div>
      <div class="howto-step" id="step2"><strong>Step 2</strong> Paste aggregate XML into DomainPreflight DMARC Report Analyzer</div>
      <div class="howto-step" id="step3"><strong>Step 3</strong> Fix any senders failing alignment before you enforce</div>
      <div class="howto-step" id="step4"><strong>Step 4</strong> After 2–4 weeks of clean reports → change <code>p=none</code> to <code>p=quarantine</code></div>
      <div class="howto-step" id="step5"><strong>Step 5</strong> Monitor for a week → if clean, move toward <code>p=reject</code></div>
      <div class="howto-step" id="step6"><strong>Step 6</strong> Run DNS Preflight to confirm the new policy is live</div>

      <div class="tool-cta">
        <p>Open the DMARC Report Analyzer</p>
        <a href="https://domainpreflight.dev/dmarc/">DMARC Report Analyzer →</a>
      </div>

      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/glossary/dmarc/">DMARC</a> ·
        <a href="/glossary/dmarc-alignment/">DMARC alignment</a>
      </div>

      <section class="faq-section" aria-label="FAQ">
        <h2>FAQ</h2>
        <h3>Is DMARC p=none bad?</h3>
        <p>Not for the first weeks — it’s the right starting point. Bad if you stay forever with no enforcement.</p>
        <h3>Can attackers spoof me with p=none?</h3>
        <p>Yes — none doesn’t block. Reports show abuse — they don’t stop it.</p>
        <h3>How do I get aggregate reports?</h3>
        <p>Add rua=mailto:dmarc@yourdomain.com to DMARC — big providers send daily XML zips.</p>
        <h3>When is it safe to move to p=reject?</h3>
        <p>After weeks of reports showing legit senders aligned — use the analyzer to verify.</p>
        <h3>Will p=reject break my mail?</h3>
        <p>Only if you still have unaligned legit senders. Fix alignment at none first — then enforce.</p>
      </section>

      <div class="internal-links">
        <p><a href="/error/">← All error fixes</a></p>
        <p><a href="https://domainpreflight.dev/">Open DNS Preflight and re-check your zone →</a></p>
      </div>""",
        ),
    ]

    for p in pages:
        slug = p[0]
        html = build(*p)
        out = ERROR / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print("Wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
