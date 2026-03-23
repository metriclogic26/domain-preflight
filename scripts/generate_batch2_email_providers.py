#!/usr/bin/env python3
"""Generate email-providers/* pages — Batch 2."""
from __future__ import annotations

import re
import sys
from html import escape as html_escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_page_shell import (  # noqa: E402
    DOC_STYLES,
    FOOTER_INNER,
    NAV_LINKS,
    breadcrumb_schema,
    faq_schema,
    faq_section_html,
    howto_schema,
    howto_steps_html,
    json_ld_script,
)

HOME = "https://domainpreflight.dev/"


def strip_html(t: str) -> str:
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def escape_attr(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


EP = [
    {
        "id": "sendgrid",
        "label": "SendGrid",
        "dash": "SendGrid Dashboard → <strong>Settings</strong> → <strong>Sender Authentication</strong>.",
        "spf": "v=spf1 include:sendgrid.net ~all",
        "dkim": "CNAME records <code>s1.domainkey.uXXXXX.wl.sendgrid.net</code> and <code>s2.domainkey...</code> — exact targets shown in Sender Authentication after you add the domain.",
        "mistake": "Skipping branded link / CNAME authentication — DKIM won’t align to your domain until you complete the CNAME steps SendGrid shows.",
    },
    {
        "id": "mailgun",
        "label": "Mailgun",
        "dash": "Mailgun Control Panel → <strong>Sending</strong> → <strong>Domain settings</strong> → select your domain.",
        "spf": "v=spf1 include:mailgun.org ~all",
        "dkim": "TXT at <code>k1._domainkey</code> (or the selector Mailgun displays) with the public key value from the control panel.",
        "mistake": "Using the sandbox domain for production — SPF/DKIM must be on the domain you send from.",
    },
    {
        "id": "google-workspace",
        "label": "Google Workspace",
        "dash": "Google Admin console → <strong>Apps</strong> → <strong>Google Workspace</strong> → <strong>Gmail</strong> → <strong>Authenticate email</strong> (DKIM). SPF: no separate UI — publish TXT at your DNS host.",
        "spf": "v=spf1 include:_spf.google.com ~all",
        "dkim": "TXT at <code>google._domainkey</code> — value from Admin → Authenticate email → Generate / show DNS record.",
        "mistake": "Not turning DKIM on after publishing DNS — you must click Start authentication in Admin.",
    },
    {
        "id": "microsoft-365",
        "label": "Microsoft 365",
        "dash": "Microsoft 365 Defender portal → <strong>Email &amp; collaboration</strong> → <strong>Policies &amp; rules</strong> → <strong>DKIM</strong> — or Exchange admin center DKIM for the domain.",
        "spf": "v=spf1 include:spf.protection.outlook.com ~all",
        "dkim": "CNAME records <code>selector1._domainkey</code> → <code>selector1-domain-com._domainkey.*.onmicrosoft.com</code> (Microsoft shows exact FQDNs when you enable DKIM).",
        "mistake": "Expecting DKIM to work before the CNAMEs resolve — enable and wait for DNS.",
    },
    {
        "id": "postmark",
        "label": "Postmark",
        "dash": "Postmark → <strong>Sender signatures</strong> → your domain → <strong>DNS</strong> tab.",
        "spf": "v=spf1 include:spf.mtasv.net ~all",
        "dkim": "TXT at <code>pm._domainkey</code> with the value Postmark shows (often one TXT with k=rsa; p=...).",
        "mistake": "Adding SPF but not verifying the domain — Postmark requires verified sender signature before production sending.",
    },
    {
        "id": "amazon-ses",
        "label": "Amazon SES",
        "dash": "AWS Console → <strong>SES</strong> → <strong>Verified identities</strong> → your domain → <strong>DKIM</strong> → Easy DKIM.",
        "spf": "v=spf1 include:amazonses.com ~all",
        "dkim": "Three CNAME records (token-based) that SES displays — publish exactly as shown for Easy DKIM.",
        "mistake": "Verifying domain without enabling DKIM — Easy DKIM CNAMEs must be present and verified.",
    },
    {
        "id": "mailchimp",
        "label": "Mailchimp",
        "dash": "Mailchimp → <strong>Audience</strong> → <strong>Domains</strong> → authenticate domain (or Website → Domains depending on UI).",
        "spf": "v=spf1 include:servers.mcsv.net ~all",
        "dkim": "Mailchimp may show <code>k1._domainkey</code> TXT or CNAMEs — follow the records in the domain setup wizard.",
        "mistake": "Authenticating a different domain than your From address — alignment requires the From domain to match what you verified.",
    },
    {
        "id": "klaviyo",
        "label": "Klaviyo",
        "dash": "Klaviyo → <strong>Account</strong> → <strong>Settings</strong> → <strong>Domains</strong> → sending domain setup.",
        "spf": "v=spf1 include:klaviyomail.com ~all",
        "dkim": "CNAME records from Klaviyo’s sending domain setup — publish exactly as listed for your shop domain.",
        "mistake": "Partial setup — SPF without Klaviyo’s DKIM CNAMEs still fails DMARC alignment for marketing streams.",
    },
    {
        "id": "hubspot",
        "label": "HubSpot",
        "dash": "HubSpot → <strong>Settings</strong> → <strong>Website</strong> → <strong>Domains &amp; URLs</strong> → <strong>Email</strong> → connect / authenticate sending domain.",
        "spf": "v=spf1 include:_spf.hubspot.com ~all",
        "dkim": "CNAME records HubSpot provides under Email sending domains — add all host/target pairs.",
        "mistake": "Connecting CRM without completing DNS — HubSpot shows pending until TXT/CNAME checks pass.",
    },
    {
        "id": "brevo",
        "label": "Brevo",
        "dash": "Brevo → <strong>Senders &amp; IP</strong> → <strong>Domains</strong> → authenticate your domain.",
        "spf": "v=spf1 include:spf.sendinblue.com ~all",
        "dkim": "TXT at <code>mail._domainkey</code> (Brevo may also show a record name like <code>brevo._domainkey</code> — use their live values).",
        "mistake": "Old Sendinblue DNS snippets cached — always copy current records from Brevo’s domain authentication page.",
    },
]


def build_spf_steps(p: dict) -> tuple[list[str], list[str], str]:
    pl = p["label"]
    names = [
        f"Open {pl}",
        "Add or merge SPF TXT at your DNS host",
        "Use this SPF string",
        "Single record only",
        "Wait for DNS",
        "Verify with DNS Preflight",
    ]
    block = p["spf"]
    texts = [
        p["dash"],
        f"At Cloudflare, Route 53, or wherever your domain’s zone lives — not inside {pl}’s SPF editor if they don’t host DNS.",
        f"Merge with your other senders into <strong>one</strong> v=spf1 line. Example baseline including {pl}: <div class=\"dns-block\">{block}</div>",
        "If you already have SPF, add <code>include:...</code> before <code>~all</code> — never publish two SPF TXT records.",
        "TTL 300–3600s. Propagation: minutes to an hour depending on resolver.",
        "Run <a href=\"https://domainpreflight.dev/\">DNS Preflight</a> — confirm SPF resolves and lookup count stays under 10. DMARC alignment: <a href=\"/fix/dmarc/\">DMARC fixes</a>.",
    ]
    intro = f"""      <p class="lead">SPF authorises IPs and includes for your envelope sender. {pl} gives you the <code>include:</code> you must add to your domain’s single SPF TXT.</p>
      <div class="gotcha"><strong>Common mistake:</strong> {p["mistake"]}</div>"""
    return names, texts, intro


def build_dkim_steps(p: dict) -> tuple[list[str], list[str], str]:
    pl = p["label"]
    names = [
        f"Open {pl}",
        "Copy DKIM DNS records",
        "Publish at your DNS host",
        "Wait for resolution",
        "Enable signing in the provider if required",
        "Verify alignment",
    ]
    texts = [
        p["dash"],
        f"Copy the exact hostnames and values {pl} shows — do not invent selectors. Typical pattern: <div class=\"dns-block\">{p['dkim']}</div>",
        "Add TXT or CNAME at the DNS provider that hosts your domain. Truncated keys fail verification.",
        "Query the record from an authoritative resolver or use propagation checker.",
        "Google Workspace / some hosts require clicking “enable” after DNS is green.",
        "Send a test message; check <code>DKIM-Signature</code> and <code>d=</code>. Run <a href=\"https://domainpreflight.dev/\">DNS Preflight</a>. Align with DMARC: <a href=\"/fix/dmarc/\">/fix/dmarc/</a>.",
    ]
    intro = f"""      <p class="lead">DKIM proves message integrity. {pl} gives you a selector and key or CNAME targets — publish them exactly.</p>
      <div class="gotcha"><strong>Common mistake:</strong> {p["mistake"]}</div>"""
    return names, texts, intro


def spf_faqs(p: dict) -> list[tuple[str, str]]:
    pl = p["label"]
    return [
        (f"What SPF include does {pl} need?", f"Use the include string on this page — merge into your single SPF TXT with other mail sources."),
        ("Can I have two SPF records?", "No. Merge into one v=spf1 or receivers return PermError."),
        ("Where do I edit SPF?", "At your DNS host (Route 53, Cloudflare, etc.) — not always inside the email product."),
        ("How do I know it worked?", "DNS Preflight shows your SPF string and lookup count."),
        ("Why does DMARC still fail?", "SPF alone doesn’t align if Return-Path is different — you need DKIM alignment or aligned SPF. See /fix/dmarc/."),
    ]


def dkim_faqs(p: dict) -> list[tuple[str, str]]:
    pl = p["label"]
    return [
        (f"Where do I find {pl} DKIM records?", "In the provider’s domain authentication / sender settings — copy live values."),
        ("CNAME vs TXT?", "Use what the provider specifies — both are common."),
        ("Why dkim=fail?", "Wrong selector, truncated key, or signing not enabled after publish."),
        ("Does this fix DMARC?", "You need SPF + DKIM alignment for your From domain — DKIM is often the easier path for ESPs."),
        ("How to verify?", "DNS Preflight for the published key; send test mail for header verification."),
    ]


def render_topic(p: dict, topic: str) -> str:
    pid = p["id"]
    pl = p["label"]
    is_spf = topic == "spf-setup"
    canonical = f"{HOME}email-providers/{pid}/{topic}/"
    if is_spf:
        step_names, step_texts, intro = build_spf_steps(p)
        h1 = f"SPF setup for {pl}"
        title = f"SPF setup — {pl}"
        desc = f"Add {pl} to your SPF TXT: include string, one record, verify with DNS Preflight."
        howto_name = f"Add {pl} SPF"
        howto_desc = f"Publish SPF include for {pl} at your DNS host and verify."
        faqs = spf_faqs(p)
    else:
        step_names, step_texts, intro = build_dkim_steps(p)
        h1 = f"DKIM setup for {pl}"
        title = f"DKIM setup — {pl}"
        desc = f"Publish {pl} DKIM DNS records and verify signing for DMARC alignment."
        howto_name = f"Add {pl} DKIM"
        howto_desc = f"Create DKIM TXT or CNAME records for {pl} at your DNS host."
        faqs = dkim_faqs(p)

    crumbs = [
        ("Home", HOME),
        ("Email Providers", f"{HOME}email-providers/"),
        (pl, f"{HOME}email-providers/{pid}/"),
        ("SPF setup" if is_spf else "DKIM setup", canonical),
    ]
    step_plain = [strip_html(t) for t in step_texts]
    ld = "\n".join(
        [
            json_ld_script(howto_schema(canonical, howto_name, howto_desc, step_names, step_plain)),
            json_ld_script(faq_schema(faqs)),
            json_ld_script(breadcrumb_schema(crumbs)),
        ]
    )
    crumb = "SPF setup" if is_spf else "DKIM setup"
    bc = f"""    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{HOME}">Home</a> <span aria-hidden="true">›</span> <a href="/email-providers/">Email Providers</a> <span aria-hidden="true">›</span> <a href="/email-providers/{pid}/">{html_escape(pl)}</a> <span aria-hidden="true">›</span> {html_escape(crumb)}</nav>"""

    body = f"""{intro}

{howto_steps_html(step_texts)}

      <div class="tool-cta">
        <p><strong>DNS Preflight</strong> — verify SPF, DKIM, DMARC in one pass.</p>
        <p><a href="https://domainpreflight.dev/">Open DNS Preflight →</a></p>
        <p><strong>DMARC alignment</strong> — fixes when reports show failures.</p>
        <p><a href="/fix/dmarc/">DMARC fix guides →</a></p>
      </div>

{faq_section_html(faqs)}
      <div class="internal-links"><p><a href="/email-providers/{pid}/">← {html_escape(pl)} hub</a> · <a href="/email-providers/">All email providers</a></p></div>
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_escape(title)} — DomainPreflight</title>
  <meta name="description" content="{escape_attr(desc)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script defer src="https://cloud.umami.is/script.js" data-website-id="27fc19d2-1ff5-4478-946a-b96cc7d5daf8"></script>
{ld}
  <style>
{DOC_STYLES}
  </style>
  <link rel="icon" type="image/png" href="/favicon.png">
</head>
<body>
  <header>
    <div class="header-inner">
      <div class="logo"><a href="/">DomainPreflight.</a><span class="pill">BETA</span></div>
      <nav>
{NAV_LINKS}
      </nav>
    </div>
  </header>
  <main>
{bc}
    <article>
      <p class="hero-label">Email provider</p>
      <h1>{html_escape(h1)}</h1>
{body}
    </article>
  </main>
  <footer>
{FOOTER_INNER}
  </footer>
</body>
</html>
"""


def render_hub(p: dict) -> str:
    pid = p["id"]
    pl = p["label"]
    canonical = f"{HOME}email-providers/{pid}/"
    crumbs = breadcrumb_schema(
        [
            ("Home", HOME),
            ("Email Providers", f"{HOME}email-providers/"),
            (pl, canonical),
        ]
    )
    ld = json_ld_script(crumbs)
    cards = f"""      <a class="hub-card" href="/email-providers/{pid}/spf-setup/"><div class="hub-card-title">SPF setup</div><div class="hub-card-desc">Include string and merge rules for {pl}.</div></a>
      <a class="hub-card" href="/email-providers/{pid}/dkim-setup/"><div class="hub-card-title">DKIM setup</div><div class="hub-card-desc">TXT/CNAME records and verification.</div></a>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_escape(pl)} — Email Provider — DomainPreflight</title>
  <meta name="description" content="SPF and DKIM DNS setup for {pl}: records, gotchas, DMARC alignment.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script defer src="https://cloud.umami.is/script.js" data-website-id="27fc19d2-1ff5-4478-946a-b96cc7d5daf8"></script>
{ld}
  <style>
{DOC_STYLES}
  </style>
  <link rel="icon" type="image/png" href="/favicon.png">
</head>
<body>
  <header>
    <div class="header-inner">
      <div class="logo"><a href="/">DomainPreflight.</a><span class="pill">BETA</span></div>
      <nav>
{NAV_LINKS}
      </nav>
    </div>
  </header>
  <main>
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{HOME}">Home</a> <span aria-hidden="true">›</span> <a href="/email-providers/">Email Providers</a> <span aria-hidden="true">›</span> {html_escape(pl)}</nav>
    <p class="hero-label">Email provider</p>
    <h1>{html_escape(pl)}</h1>
    <p class="lead">SPF and DKIM for this sender — copy the includes and records, then verify with DNS Preflight.</p>
{cards}
    <p class="internal-links" style="margin-top:1.5rem"><a href="/email-providers/">← All email providers</a></p>
  </main>
  <footer>
{FOOTER_INNER}
  </footer>
</body>
</html>
"""


def render_parent() -> str:
    canonical = f"{HOME}email-providers/"
    crumbs = breadcrumb_schema([("Home", HOME), ("Email Providers", canonical)])
    items = "\n".join(
        f'      <a class="hub-card" href="/email-providers/{p["id"]}/"><div class="hub-card-title">{html_escape(p["label"])}</div><div class="hub-card-desc">SPF + DKIM guides</div></a>'
        for p in EP
    )
    ld = json_ld_script(crumbs)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Email Providers — SPF &amp; DKIM — DomainPreflight</title>
  <meta name="description" content="SPF and DKIM DNS setup for SendGrid, Mailgun, Google Workspace, Microsoft 365, SES, marketing tools, and more.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script defer src="https://cloud.umami.is/script.js" data-website-id="27fc19d2-1ff5-4478-946a-b96cc7d5daf8"></script>
{ld}
  <style>
{DOC_STYLES}
  </style>
  <link rel="icon" type="image/png" href="/favicon.png">
</head>
<body>
  <header>
    <div class="header-inner">
      <div class="logo"><a href="/">DomainPreflight.</a><span class="pill">BETA</span></div>
      <nav>
{NAV_LINKS}
      </nav>
    </div>
  </header>
  <main>
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{HOME}">Home</a> <span aria-hidden="true">›</span> Email Providers</nav>
    <p class="hero-label">Email</p>
    <h1>Email providers</h1>
    <p class="lead">Transactional and marketing ESPs — SPF include strings and DKIM records with DMARC alignment in mind.</p>
{items}
  </main>
  <footer>
{FOOTER_INNER}
  </footer>
</body>
</html>
"""


def main() -> None:
    base = ROOT / "email-providers"
    base.mkdir(parents=True, exist_ok=True)
    (base / "index.html").write_text(render_parent(), encoding="utf-8")
    print("Wrote", base / "index.html")
    for p in EP:
        d = base / p["id"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(render_hub(p), encoding="utf-8")
        print("Wrote", d / "index.html")
        for topic in ("spf-setup", "dkim-setup"):
            td = d / topic
            td.mkdir(parents=True, exist_ok=True)
            (td / "index.html").write_text(render_topic(p, topic), encoding="utf-8")
            print("Wrote", td / "index.html")


if __name__ == "__main__":
    main()
