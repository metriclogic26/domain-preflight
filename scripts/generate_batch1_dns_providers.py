#!/usr/bin/env python3
"""Generate dns/provider/* pages — Batch 1."""
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
DATE = "2026-03-19"


def strip_html(t: str) -> str:
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def escape_attr(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")

PROVIDERS = [
    {
        "id": "cloudflare-dns",
        "label": "Cloudflare DNS",
        "step1": "Open the Cloudflare Dashboard → <strong>DNS</strong> → <strong>Records</strong> → <strong>Add record</strong>.",
        "gotcha": "<strong>Proxy (orange cloud) must be grey (DNS only)</strong> for MX records, mail A records, and anything that must resolve exactly for mail. TXT for DMARC/SPF/DKIM should also use DNS-only — orange cloud can interfere with how some tools read mail DNS.",
        "name_hint": "Use the <strong>subdomain only</strong> in the Name field — e.g. <code>_dmarc</code> or <code>@</code> for apex, not the full hostname.",
        "propagation": "Usually <strong>minutes</strong> — Cloudflare is authoritative quickly; global resolver caches still respect TTL.",
    },
    {
        "id": "aws-route53",
        "label": "Amazon Route 53",
        "step1": "AWS Console → <strong>Route 53</strong> → <strong>Hosted zones</strong> → select your domain → <strong>Create record</strong>.",
        "gotcha": "<strong>TXT values must be wrapped in quotes</strong> in the value field. Multiple strings in one TXT are entered as separate quoted strings on one line.",
        "name_hint": "For apex SPF, leave the record name <strong>blank</strong> (not <code>@</code>). For DMARC use <code>_dmarc</code> in the name field.",
        "propagation": "Typically <strong>1–5 minutes</strong> to Route 53 authoritative data; resolvers cache per TTL.",
    },
    {
        "id": "google-cloud-dns",
        "label": "Google Cloud DNS",
        "step1": "Google Cloud Console → <strong>Network services</strong> → <strong>Cloud DNS</strong> → your <strong>zone</strong> → <strong>Add standard</strong> (or Add record set).",
        "gotcha": "The <strong>DNS name</strong> field for apex records must use a <strong>trailing dot</strong>: <code>example.com.</code> — FQDN form. Omitting the dot can create the wrong relative name.",
        "name_hint": "Use FQDN with trailing dot for clarity on apex; for <code>_dmarc</code> use <code>_dmarc.example.com.</code> in the name field.",
        "propagation": "Usually <strong>minutes</strong> once the zone is live at Google’s nameservers.",
    },
    {
        "id": "azure-dns",
        "label": "Azure DNS",
        "step1": "Azure Portal → your <strong>DNS zone</strong> → <strong>+ Record set</strong>.",
        "gotcha": "For apex records the <strong>name</strong> field uses <code>@</code>. TXT values go in the <strong>TXT Records</strong> box — <strong>one value per line</strong> if the UI splits long strings.",
        "name_hint": "SPF/DMARC/DKIM names are relative to the zone — e.g. <code>_dmarc</code> or <code>google._domainkey</code> for a selector.",
        "propagation": "<strong>Minutes to about an hour</strong> depending on TTL and downstream resolvers.",
    },
    {
        "id": "digitalocean-dns",
        "label": "DigitalOcean DNS",
        "step1": "DigitalOcean Control Panel → <strong>Networking</strong> → <strong>Domains</strong> → select your domain → <strong>Add record</strong>.",
        "gotcha": "For DKIM, the <strong>hostname</strong> field is only the left part — e.g. <code>google._domainkey</code> — <strong>not</strong> the full <code>google._domainkey.example.com</code>.",
        "name_hint": "Type <strong>TXT</strong>, enter the hostname fragment and paste the value. Apex often appears as <code>@</code>.",
        "propagation": "Usually <strong>minutes</strong>; TTL and recursive caches still apply.",
    },
]

TOPICS = ["dmarc-setup", "spf-record", "dkim-record", "propagation-times"]

TOPIC_META = {
    "dmarc-setup": {
        "title": "DMARC TXT — {provider}",
        "h1": "Add a DMARC record in {provider}",
        "desc": "Step-by-step: publish a DMARC TXT at _dmarc in {provider}, with exact field values and common mistakes.",
        "howto_name": "Add DMARC DNS in {provider}",
        "howto_desc": "Create a TXT at _dmarc with your DMARC policy and rua mailbox in {provider}.",
    },
    "spf-record": {
        "title": "SPF TXT — {provider}",
        "h1": "Add an SPF record in {provider}",
        "desc": "Publish a single SPF TXT for your domain in {provider} — name field, quoted values, and verification.",
        "howto_name": "Add SPF DNS in {provider}",
        "howto_desc": "Create one v=spf1 TXT at your sending domain in {provider}.",
    },
    "dkim-record": {
        "title": "DKIM TXT — {provider}",
        "h1": "Add a DKIM record in {provider}",
        "desc": "Publish selector._domainkey TXT in {provider} — hostname rules and full public key value.",
        "howto_name": "Add DKIM DNS in {provider}",
        "howto_desc": "Create TXT at your DKIM selector under _domainkey in {provider}.",
    },
    "propagation-times": {
        "title": "DNS propagation — {provider}",
        "h1": "DNS propagation in {provider}",
        "desc": "What to expect after you save records in {provider}, how TTL works, and how to verify globally.",
        "howto_name": "Verify DNS propagation from {provider}",
        "howto_desc": "Save changes in {provider}, wait for TTL, then confirm with Preflight and propagation checks.",
    },
}


def dmarc_txt_example() -> str:
    return "v=DMARC1; p=none; rua=mailto:dmarc@example.com; fo=1"


def spf_txt_example() -> str:
    return "v=spf1 include:_spf.google.com ~all"


def dkim_txt_example() -> str:
    return "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBA..."


def build_steps(provider: dict, topic: str) -> tuple[list[str], list[str], str]:
    """Returns step_names, step_texts (HTML fragments), intro_html."""
    p = provider["label"]
    sid = provider["id"]
    s1 = provider["step1"]
    gh = provider["gotcha"]
    nh = provider["name_hint"]
    prop = provider["propagation"]

    if topic == "dmarc-setup":
        names = [
            f"Open {p}",
            "Add a TXT record for DMARC",
            "Paste the DMARC value",
            "TTL and save",
            "Verify locally",
            "Confirm with DomainPreflight",
        ]
        block = dmarc_txt_example()
        if sid == "aws-route53":
            block = f'"{dmarc_txt_example()}"'
        texts = [
            s1,
            f"Choose <strong>TXT</strong>. In the name/host field enter <code>_dmarc</code> only ({nh}).",
            f"Paste this value in one piece (follow your provider’s quoting rules): <div class=\"dns-block\">{block}</div>",
            f"TTL: 1 hour is fine for rollout. Save. Remember: {gh}",
            "Query <code>_dmarc.yourdomain</code> with dig or use <a href=\"https://domainpreflight.dev/propagation/\">DNS Propagation</a> across resolvers.",
            "Run <a href=\"https://domainpreflight.dev/\">DNS Preflight</a> on the domain — DMARC policy and reporting should appear once TXT resolves.",
        ]
        intro = f"""      <p class="lead">DMARC lives at <code>_dmarc.yourdomain</code> as a TXT record. {p} is your control plane — one typo in the name field and receivers never see the record.</p>
      <div class="gotcha"><strong>Provider gotcha:</strong> {gh}</div>
      <p>See also <a href="/dns/dmarc-record/">DMARC record reference</a> and <a href="/learn/dmarc/">DMARC setup guide</a>.</p>"""

    elif topic == "spf-record":
        names = [
            f"Open {p}",
            "Add TXT at domain apex (or correct zone)",
            "Paste SPF",
            "Save",
            "Wait for TTL",
            "Verify with Preflight",
        ]
        block = spf_txt_example()
        if sid == "aws-route53":
            block = f'"{spf_txt_example()}"'
        elif sid == "google-cloud-dns":
            block = spf_txt_example()  # Google UI often one field
        texts = [
            s1,
            f"TXT record. For root domain SPF: {nh}.",
            f"Single SPF only — merge vendors into one string: <div class=\"dns-block\">{block}</div>",
            f"Save. {gh}",
            f"Propagation: {prop}",
            "Use <a href=\"https://domainpreflight.dev/\">DNS Preflight</a> — SPF tree shows lookup count. Link: <a href=\"/learn/spf/\">SPF guide</a>.",
        ]
        intro = f"""      <p class="lead">SPF must be a <strong>single</strong> TXT starting with <code>v=spf1</code> at the domain that sends mail. {p} will let you break this with duplicate TXT — don’t.</p>
      <div class="gotcha"><strong>Provider gotcha:</strong> {gh}</div>
      <p>Reference: <a href="/dns/spf-record/">SPF DNS</a>.</p>"""

    elif topic == "dkim-record":
        names = [
            f"Open {p}",
            "Create TXT for selector._domainkey",
            "Paste DKIM public key",
            "TTL / save",
            "Verify TXT length",
            "Test signing + Preflight",
        ]
        block = dkim_txt_example()
        if sid == "aws-route53":
            long_val = '"v=DKIM1; k=rsa; p=" "MIGfMA0GCSqGSIb3DQEBA..."'
            block = long_val
        texts = [
            s1,
            f"Name/host: your selector + <code>._domainkey</code> ({nh}).",
            f"Value from your ESP (often one long string): <div class=\"dns-block\">{block}</div>",
            f"Save. Truncated keys fail open verification. {gh}",
            "If the UI splits into 255-char chunks, that is normal for DNS — the full key must still be complete.",
            "Send test mail; run <a href=\"https://domainpreflight.dev/\">DNS Preflight</a> for DKIM strength. <a href=\"/learn/dkim/\">DKIM guide</a>.",
        ]
        intro = f"""      <p class="lead">DKIM publishes a public key at <code>selector._domainkey.yourdomain</code>. Copy the exact string your mail provider gives you.</p>
      <div class="gotcha"><strong>Provider gotcha:</strong> {gh}</div>
      <p>See <a href="/dns/dkim-record/">DKIM DNS</a>.</p>"""

    else:  # propagation-times
        names = [
            f"Open {p}",
            "Note TTL on changed records",
            "Save and timestamp",
            "Check authoritative NS first",
            "Use propagation checker",
            "Confirm in DNS Preflight",
        ]
        texts = [
            s1,
            "Lower TTL before big changes if your provider allows — then raise after stabilization.",
            "After save, wait at least one TTL cycle before assuming failure.",
            f"Query your zone’s authoritative nameservers directly. {nh}",
            f"Open <a href=\"https://domainpreflight.dev/propagation/\">DNS Propagation</a> to compare resolvers. Typical: {prop}",
            "Final check: <a href=\"https://domainpreflight.dev/\">DNS Preflight</a> for SPF/DKIM/DMARC together.",
        ]
        intro = f"""      <p class="lead">Saving in {p} updates your zone fast — the internet caches old answers until TTL expires.</p>
      <div class="gotcha"><strong>Provider gotcha:</strong> {gh}</div>
      <p>Read <a href="/dns/propagation/">DNS propagation</a> for background.</p>"""

    return names, texts, intro


def topic_faqs(provider: dict, topic: str) -> list[tuple[str, str]]:
    pl = provider["label"]
    if topic == "dmarc-setup":
        return [
            (f"Where do I add DMARC in {pl}?", f"In the DNS zone for your domain — TXT name _dmarc, value starting with v=DMARC1."),
            ("Why is my DMARC not visible yet?", "TTL on the old record, or wrong name (full FQDN vs relative). Check authoritative NS."),
            (f"Does {pl} proxy DMARC TXT?", "Treat mail-related DNS as DNS-only where applicable — follow the provider gotcha on this page."),
            ("What p= should I start with?", "p=none for monitoring — tighten after reports look clean."),
            ("How do I verify?", "DNS Preflight and the DMARC Report Analyzer after rua= receives XML."),
        ]
    if topic == "spf-record":
        return [
            ("Can I add two SPF TXT records?", "No — merge into one v=spf1 string or you get PermError."),
            (f"How does {pl} want SPF quoted?", "Follow the code block on this page; Route 53 requires quotes around the full TXT."),
            ("Why PermError after saving?", "Syntax error, duplicate SPF, or over 10 DNS lookups — use Preflight’s SPF tree."),
            ("Include SendGrid and Google?", "Yes in one record: v=spf1 include:... include:... ~all — watch lookup count."),
            ("How long until live?", provider["propagation"]),
        ]
    if topic == "dkim-record":
        return [
            ("What name do I enter for DKIM?", "selector._domainkey as your provider’s UI expects — see the gotcha on this page for your host."),
            ("Why dkim=fail?", "Truncated key, wrong selector, or signing with a different selector than DNS."),
            ("2048 vs 1024?", "Prefer 2048-bit keys; rotate 1024-bit legacy keys."),
            (f"Does {pl} split long TXT?", "Many providers auto-chunk; ensure the full key is present."),
            ("How to test?", "Send mail and check headers — then DNS Preflight for the published key."),
        ]
    return [
        ("What is DNS propagation?", "Delay while recursive resolvers cache old TTLs — not instant worldwide."),
        (f"How fast is {pl}?", provider["propagation"]),
        ("Why does dig show the new TXT but my tool doesn’t?", "Different resolver — use propagation checker and lower TTL next time."),
        ("What TTL should I use?", "300–3600s during changes; longer when stable."),
        ("Where to verify all records?", "DNS Preflight for SPF/DKIM/DMARC — Propagation tool for cross-resolver checks."),
    ]


def render_topic_page(provider: dict, topic: str) -> str:
    pid = provider["id"]
    pl = provider["label"]
    meta = TOPIC_META[topic]
    title = meta["title"].format(provider=pl)
    h1 = meta["h1"].format(provider=pl)
    desc = meta["desc"].format(provider=pl)
    canonical = f"{HOME}dns/provider/{pid}/{topic}/"
    step_names, step_texts, intro = build_steps(provider, topic)
    faqs = topic_faqs(provider, topic)

    crumbs = [
        ("Home", HOME),
        ("DNS Records", f"{HOME}dns/"),
        ("DNS Providers", f"{HOME}dns/provider/"),
        (pl, f"{HOME}dns/provider/{pid}/"),
        (title.split(" — ")[0], canonical),
    ]
    bc = breadcrumb_schema(crumbs)
    howto_name = meta["howto_name"].format(provider=pl)
    howto_desc = meta["howto_desc"].format(provider=pl)

    step_plain = [strip_html(t) for t in step_texts]
    ld = "\n".join(
        [
            json_ld_script(howto_schema(canonical, howto_name, howto_desc, step_names, step_plain)),
            json_ld_script(faq_schema(faqs)),
            json_ld_script(bc),
        ]
    )

    crumb_topic = {
        "dmarc-setup": "DMARC setup",
        "spf-record": "SPF record",
        "dkim-record": "DKIM record",
        "propagation-times": "Propagation times",
    }[topic]
    breadcrumb_html = f"""    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{HOME}">Home</a> <span aria-hidden="true">›</span> <a href="/dns/">DNS Records</a> <span aria-hidden="true">›</span> <a href="/dns/provider/">DNS Providers</a> <span aria-hidden="true">›</span> <a href="/dns/provider/{pid}/">{html_escape(pl)}</a> <span aria-hidden="true">›</span> {html_escape(crumb_topic)}</nav>"""

    body = f"""{intro}

{howto_steps_html(step_texts)}

      <div class="tool-cta">
        <p><strong>DNS Preflight</strong> — full auth check for your domain.</p>
        <p><a href="https://domainpreflight.dev/">Open DNS Preflight →</a></p>
        <p><strong>Propagation</strong> — compare resolvers.</p>
        <p><a href="https://domainpreflight.dev/propagation/">Open DNS Propagation →</a></p>
      </div>

{faq_section_html(faqs)}
      <div class="internal-links"><p><a href="/dns/provider/{pid}/">← {pl} hub</a> · <a href="/dns/provider/">All DNS providers</a></p></div>
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
{breadcrumb_html}
    <article>
      <p class="hero-label">DNS provider</p>
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


def render_provider_hub(provider: dict) -> str:
    pid = provider["id"]
    pl = provider["label"]
    canonical = f"{HOME}dns/provider/{pid}/"
    crumbs = breadcrumb_schema(
        [
            ("Home", HOME),
            ("DNS Records", f"{HOME}dns/"),
            ("DNS Providers", f"{HOME}dns/provider/"),
            (pl, canonical),
        ]
    )
    ld = json_ld_script(crumbs)
    cards = []
    labels = {
        "dmarc-setup": "DMARC setup",
        "spf-record": "SPF record",
        "dkim-record": "DKIM record",
        "propagation-times": "Propagation times",
    }
    for t in TOPICS:
        cards.append(
            f'      <a class="hub-card" href="/dns/provider/{pid}/{t}/"><div class="hub-card-title">{labels[t]}</div>'
            f'<div class="hub-card-desc">{TOPIC_META[t]["h1"].format(provider=pl)}</div></a>'
        )
    cards_html = "\n".join(cards)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{pl} — DNS Provider Guides — DomainPreflight</title>
  <meta name="description" content="Add DMARC, SPF, DKIM, and check propagation in {pl}.">
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
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{HOME}">Home</a> <span aria-hidden="true">›</span> <a href="/dns/">DNS Records</a> <span aria-hidden="true">›</span> <a href="/dns/provider/">DNS Providers</a> <span aria-hidden="true">›</span> {pl}</nav>
    <p class="hero-label">DNS provider</p>
    <h1>{pl}</h1>
    <p class="lead">Step-by-step guides for email authentication records in this DNS host.</p>
{cards_html}
    <p class="internal-links" style="margin-top:1.5rem"><a href="/dns/provider/">← All DNS providers</a></p>
  </main>
  <footer>
{FOOTER_INNER}
  </footer>
</body>
</html>
"""


def render_parent_hub() -> str:
    canonical = f"{HOME}dns/provider/"
    crumbs = breadcrumb_schema(
        [
            ("Home", HOME),
            ("DNS Records", f"{HOME}dns/"),
            ("DNS Providers", canonical),
        ]
    )
    items = []
    for p in PROVIDERS:
        items.append(
            f'      <a class="hub-card" href="/dns/provider/{p["id"]}/"><div class="hub-card-title">{p["label"]}</div>'
            f'<div class="hub-card-desc">DMARC, SPF, DKIM, propagation — {p["label"]}-specific steps.</div></a>'
        )
    ld = json_ld_script(crumbs)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DNS Providers — DomainPreflight</title>
  <meta name="description" content="How to add DMARC, SPF, DKIM, and verify propagation in Cloudflare, Route 53, Google Cloud DNS, Azure DNS, and DigitalOcean.">
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
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{HOME}">Home</a> <span aria-hidden="true">›</span> <a href="/dns/">DNS Records</a> <span aria-hidden="true">›</span> DNS Providers</nav>
    <p class="hero-label">DNS</p>
    <h1>DNS providers</h1>
    <p class="lead">Pick your DNS host — we show the exact UI path, field quirks, and copy-paste values.</p>
{chr(10).join(items)}
    <p class="internal-links" style="margin-top:1.5rem"><a href="/dns/">← DNS Records hub</a></p>
  </main>
  <footer>
{FOOTER_INNER}
  </footer>
</body>
</html>
"""


def main() -> None:
    base = ROOT / "dns" / "provider"
    base.mkdir(parents=True, exist_ok=True)
    (base / "index.html").write_text(render_parent_hub(), encoding="utf-8")
    print("Wrote", base / "index.html")
    for p in PROVIDERS:
        d = base / p["id"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(render_provider_hub(p), encoding="utf-8")
        print("Wrote", d / "index.html")
        for topic in TOPICS:
            td = d / topic
            td.mkdir(parents=True, exist_ok=True)
            (td / "index.html").write_text(render_topic_page(p, topic), encoding="utf-8")
            print("Wrote", td / "index.html")


if __name__ == "__main__":
    main()
