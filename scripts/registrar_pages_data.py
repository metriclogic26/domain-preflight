# -*- coding: utf-8 -*-
"""Content + build_all() for generate_registrar_guides.py."""

from __future__ import annotations

HOME = "https://domainpreflight.dev/"

# slug -> hub meta + topic slugs + one-line card for parent index
REGISTRARS: list[dict] = [
    {
        "slug": "cloudflare",
        "short": "Cloudflare",
        "parent_card": "Proxy toggle, fast DNS, registrar in same UI.",
        "hub_title": "Cloudflare DNS — Email Authentication Setup Guides",
        "hub_meta": "Set up SPF, DKIM, DMARC, and MX on Cloudflare — including grey-cloud rules for mail.",
        "hub_h1": "Email Authentication on Cloudflare",
        "hub_lead": "Cloudflare is the most popular DNS provider for developers. Here's how to set up SPF, DKIM, DMARC, and other email records correctly — including the proxy setting that breaks mail servers.",
        "hub_intro": "DNS, caching, and (if you use Cloudflare Registrar) renewal and lock all share one login. Each guide below matches the current Cloudflare record editor.",
        "collection_name": "Cloudflare DNS email guides",
        "topics": [
            "spf-record",
            "dkim",
            "dmarc-setup",
            "mx-record",
            "expiry-monitoring",
            "domain-lock",
        ],
    },
    {
        "slug": "namecheap",
        "short": "Namecheap",
        "parent_card": "Advanced DNS — host field, no proxy toggle.",
        "hub_title": "Namecheap DNS — Email Authentication Setup Guides",
        "hub_meta": "Add SPF, DKIM, DMARC, and MX in Namecheap Advanced DNS.",
        "hub_h1": "Email Authentication on Namecheap",
        "hub_lead": "Namecheap's Advanced DNS panel is where all email records live. Here's how to add SPF, DKIM, DMARC, and MX records correctly.",
        "hub_intro": "Everything lives under Domain List → Manage → Advanced DNS. Use the Host field: @ for root, subdomain only for DKIM, _dmarc for DMARC. TTL is usually Automatic — there's no orange cloud.",
        "collection_name": "Namecheap DNS email guides",
        "topics": ["spf-record", "dkim", "dmarc-setup", "mx-record", "expiry-monitoring", "domain-lock"],
    },
    {
        "slug": "godaddy",
        "short": "GoDaddy",
        "parent_card": "New vs legacy DNS — same records, different clicks.",
        "hub_title": "GoDaddy DNS — Email Authentication Setup Guides",
        "hub_meta": "SPF, DKIM, DMARC, and MX in GoDaddy DNS Manager.",
        "hub_h1": "Email Authentication on GoDaddy",
        "hub_lead": "GoDaddy's DNS Manager has both a new and legacy interface — steps differ slightly. Here's how to add email records in either.",
        "hub_intro": "Start at My Products → your domain → DNS (or Manage DNS). Use @ for the host on the root. TTL 1 hour (3600) is a sensible default while you're testing.",
        "collection_name": "GoDaddy DNS email guides",
        "topics": ["spf-record", "dkim", "dmarc-setup", "mx-record", "expiry-monitoring", "domain-lock"],
    },
    {
        "slug": "google-domains",
        "short": "Google Domains / Squarespace",
        "parent_card": "Squarespace domains UI — post-2023 migration.",
        "hub_title": "Google Domains / Squarespace — Email Authentication Setup",
        "hub_meta": "DNS at domains.squarespace.com for domains moved from Google Domains.",
        "hub_h1": "Email Authentication on Google Domains / Squarespace",
        "hub_lead": "Google Domains was acquired by Squarespace in 2023. If your domain was with Google Domains, it's now managed at domains.squarespace.com. DNS setup is similar but the interface has changed.",
        "hub_intro": "Open domains.squarespace.com → your domain → DNS. Google Workspace MX presets may appear if you're on Google — still verify TXT records manually.",
        "collection_name": "Squarespace Domains email guides",
        "topics": ["spf-record", "dkim", "dmarc-setup", "mx-record", "expiry-monitoring"],
    },
    {
        "slug": "porkbun",
        "short": "Porkbun",
        "parent_card": "Simple DNS — host field uses subdomain only.",
        "hub_title": "Porkbun DNS — Email Authentication Setup Guides",
        "hub_meta": "SPF, DKIM, DMARC, and MX in Porkbun DNS Records.",
        "hub_h1": "Email Authentication on Porkbun",
        "hub_lead": "Porkbun's DNS management is straightforward. Here's how to add SPF, DKIM, DMARC, and MX records in the Porkbun dashboard.",
        "hub_intro": "Go to Account → Domain Management → your domain → DNS Records. Porkbun appends your domain to the host — enter only @ or the subdomain portion.",
        "collection_name": "Porkbun DNS email guides",
        "topics": ["spf-record", "dkim", "dmarc-setup", "mx-record"],
    },
    {
        "slug": "aws-route53",
        "short": "AWS Route 53",
        "parent_card": "Quoted TXT values, blank apex, optional DNSSEC.",
        "hub_title": "AWS Route 53 — Email Authentication Setup Guides",
        "hub_meta": "SPF, DKIM, DMARC, MX, and DNSSEC in Route 53 hosted zones.",
        "hub_h1": "Email Authentication on AWS Route 53",
        "hub_lead": "Route 53 has a specific TXT record format — values must be wrapped in quotes. Here's how to add SPF, DKIM, DMARC, and MX records correctly.",
        "hub_intro": "Hosted zones live under Route 53 → Hosted Zones → your domain. Root is a blank record name — not @. Turn on DNSSEC from the hosted zone when you're ready.",
        "collection_name": "Route 53 email guides",
        "topics": ["spf-record", "dkim", "dmarc-setup", "mx-record", "dnssec"],
    },
    {
        "slug": "hover",
        "short": "Hover",
        "parent_card": "Minimal DNS editor — fixed TTL.",
        "hub_title": "Hover DNS — Email Authentication Setup Guides",
        "hub_meta": "SPF, DKIM, and DMARC in Hover DNS.",
        "hub_h1": "Email Authentication on Hover",
        "hub_lead": "Hover's DNS editor is clean and minimal. Here's how to add SPF, DKIM, and DMARC records for your email provider.",
        "hub_intro": "Hover account → your domain → DNS. You don't pick TTL — Hover sets it. There is no transfer-lock toggle in the UI; contact support for lock status.",
        "collection_name": "Hover DNS email guides",
        "topics": ["spf-record", "dkim", "dmarc-setup"],
    },
    {
        "slug": "gandi",
        "short": "Gandi",
        "parent_card": "LiveDNS — @ and _dmarc, renewal in domain settings.",
        "hub_title": "Gandi DNS — Email Authentication Setup Guides",
        "hub_meta": "SPF, DKIM, DMARC, and expiry in Gandi LiveDNS.",
        "hub_h1": "Email Authentication on Gandi",
        "hub_lead": "Gandi's DNS LiveDNS interface lets you add SPF, DKIM, and DMARC records for your domain. Here's how.",
        "hub_intro": "Most accounts use LiveDNS (not legacy DNS). Name field: @ for root, _dmarc for DMARC. Auto-renew lives in domain settings → renewal preferences.",
        "collection_name": "Gandi DNS email guides",
        "topics": ["spf-record", "dkim", "dmarc-setup", "expiry-monitoring"],
    },
    {
        "slug": "dynadot",
        "short": "Dynadot",
        "parent_card": "DNS Settings under Manage Domain.",
        "hub_title": "Dynadot DNS — Email Authentication Setup Guides",
        "hub_meta": "SPF, DKIM, DMARC, and renewal in Dynadot.",
        "hub_h1": "Email Authentication on Dynadot",
        "hub_lead": "Dynadot's DNS management is under Manage Domain → DNS Settings. Here's how to add SPF, DKIM, and DMARC records for your email provider.",
        "hub_intro": "My Domains → your domain → DNS Settings. Host @ for the root TXT. Renewal options are under domain settings if you need auto-renew.",
        "collection_name": "Dynadot DNS email guides",
        "topics": ["spf-record", "dkim", "dmarc-setup", "expiry-monitoring"],
    },
    {
        "slug": "name-com",
        "short": "Name.com",
        "parent_card": "Manage DNS — host @ for root TXT.",
        "hub_title": "Name.com DNS — Email Authentication Setup Guides",
        "hub_meta": "SPF, DKIM, DMARC, and MX in Name.com DNS Records.",
        "hub_h1": "Email Authentication on Name.com",
        "hub_lead": "Name.com's DNS management is under My Domains → DNS Records. Here's how to add SPF, DKIM, DMARC, and MX records.",
        "hub_intro": "My Domains → your domain → DNS Records → Manage DNS. Enter subdomain only in the host field — the UI shows the full hostname including your domain.",
        "collection_name": "Name.com DNS email guides",
        "topics": ["spf-record", "dkim", "dmarc-setup", "mx-record"],
    },
]

# Per-registrar DNS UI hints for templates
PROFILES: dict[str, dict] = {
    "cloudflare": {
        "dns_path": "Cloudflare Dashboard → select your domain → DNS → Records",
        "add_record": "Add record",
        "host_label": "Name",
        "root": "@",
        "quote_txt": False,
        "mx_proxy": "MX must be DNS-only (grey cloud). Never orange.",
        "txt_proxy": "TXT cannot be proxied — toggle stays grey.",
    },
    "namecheap": {
        "dns_path": "Domain List → Manage → Advanced DNS",
        "add_record": "Add New Record",
        "host_label": "Host",
        "root": "@",
        "quote_txt": False,
        "mx_proxy": "No proxy — MX is plain DNS.",
        "txt_proxy": "No Cloudflare-style proxy on Namecheap.",
    },
    "godaddy": {
        "dns_path": "My Products → your domain → DNS (Manage DNS)",
        "add_record": "Add (or Add Record)",
        "host_label": "Name / Host",
        "root": "@",
        "quote_txt": False,
        "mx_proxy": "GoDaddy does not proxy MX — standard DNS only.",
        "txt_proxy": "No proxy toggle for TXT.",
    },
    "google-domains": {
        "dns_path": "domains.squarespace.com → your domain → DNS",
        "add_record": "Add record",
        "host_label": "Host name",
        "root": "@",
        "quote_txt": False,
        "mx_proxy": "Squarespace DNS does not proxy MX.",
        "txt_proxy": "No proxy for email TXT.",
    },
    "porkbun": {
        "dns_path": "Account → Domain Management → your domain → DNS Records",
        "add_record": "Add Record",
        "host_label": "Host",
        "root": "@",
        "quote_txt": False,
        "mx_proxy": "Porkbun MX is standard DNS.",
        "txt_proxy": "No proxy toggle.",
    },
    "aws-route53": {
        "dns_path": "AWS Console → Route 53 → Hosted zones → your domain → Create record",
        "add_record": "Create record",
        "host_label": "Record name (blank = apex)",
        "root": "(leave blank for apex)",
        "quote_txt": True,
        "mx_proxy": "Route 53 does not proxy — MX is authoritative only.",
        "txt_proxy": "No proxy — enterprise DNS only.",
    },
    "hover": {
        "dns_path": "Hover → your domain → DNS",
        "add_record": "Add a record",
        "host_label": "Hostname",
        "root": "@",
        "quote_txt": False,
        "mx_proxy": "Hover does not offer orange-cloud style proxy.",
        "txt_proxy": "No proxy toggle.",
    },
    "gandi": {
        "dns_path": "Gandi → your domain → DNS Records (LiveDNS)",
        "add_record": "Add record",
        "host_label": "Name",
        "root": "@",
        "quote_txt": False,
        "mx_proxy": "Standard DNS — no proxy.",
        "txt_proxy": "No proxy.",
    },
    "dynadot": {
        "dns_path": "My Domains → your domain → DNS Settings",
        "add_record": "Add Record",
        "host_label": "Host",
        "root": "@",
        "quote_txt": False,
        "mx_proxy": "Standard MX records only.",
        "txt_proxy": "No proxy.",
    },
    "name-com": {
        "dns_path": "My Domains → your domain → DNS Records → Manage DNS",
        "add_record": "Add Record",
        "host_label": "Host",
        "root": "@",
        "quote_txt": False,
        "mx_proxy": "Standard DNS — no proxy.",
        "txt_proxy": "No proxy.",
    },
}

TOPIC_SHORT: dict[str, str] = {
    "spf-record": "SPF record",
    "dkim": "DKIM record",
    "dmarc-setup": "DMARC setup",
    "mx-record": "MX record",
    "expiry-monitoring": "Expiry monitoring",
    "domain-lock": "Domain lock",
    "dnssec": "DNSSEC",
}

TOPIC_CARDS: dict[str, tuple[str, str]] = {
    "spf-record": ("SPF record", "One v=spf1 TXT at root — merge providers."),
    "dkim": ("DKIM record", "TXT at selector._domainkey — paste full key."),
    "dmarc-setup": ("DMARC setup", "TXT at _dmarc — start with p=none."),
    "mx-record": ("MX record", "Priorities, hostnames, no proxy where applicable."),
    "expiry-monitoring": ("Expiry monitoring", "Auto-renew and WHOIS cross-check."),
    "domain-lock": ("Domain lock", "Transfer lock — verify before you move."),
    "dnssec": ("DNSSEC", "Signing keys in the hosted zone."),
}


def nav_topic(reg_slug: str, reg_short: str, topic_key: str) -> list[tuple[str, str | None]]:
    return [
        ("Home", HOME),
        ("Registrars", "/registrar/"),
        (reg_short, f"/registrar/{reg_slug}/"),
        (TOPIC_SHORT[topic_key], None),
    ]


def schema_topic(reg_slug: str, reg_short: str, topic_key: str, h1: str, rel: str) -> list[tuple[str, str]]:
    c = f"{HOME}registrar/{rel}/"
    return [
        ("Home", HOME),
        ("Registrars", f"{HOME}registrar/"),
        (reg_short, f"{HOME}registrar/{reg_slug}/"),
        (h1, c),
    ]


def import_cloudflare_pages() -> dict[str, dict]:
    from registrar_cloudflare_pages import CLOUDFLARE_TOPIC_PAGES  # noqa: PLC0415

    return {p["topic"]: p for p in CLOUDFLARE_TOPIC_PAGES}


def build_topic_payload(reg: dict, topic: str, p: dict) -> dict:
    """Common wrapper for emit_topic."""
    slug = reg["slug"]
    rel = f"{slug}/{topic}"
    back_href = f"/registrar/{slug}/"
    back_label = f"← {reg['short']} guides"
    return {
        "rel": rel,
        "title": p["title"],
        "meta": p["meta"],
        "h1": p["h1"],
        "subtitle": p["subtitle"],
        "hero": p.get("hero", "Registrar guide"),
        "bc_nav_segments": nav_topic(slug, reg["short"], topic),
        "bc_schema_trail": schema_topic(slug, reg["short"], topic, p["h1"], rel),
        "howto_name": p["howto_name"],
        "howto_desc": p["howto_desc"],
        "step_names": p["step_names"],
        "step_texts": p["step_texts"],
        "faqs": p["faqs"],
        "article": p["article"],
        "back_href": back_href,
        "back_label": back_label,
    }


def build_generic_topic(reg: dict, topic: str) -> dict:
    slug = reg["slug"]
    pr = PROFILES[slug]
    R = reg["short"]
    dns = pr["dns_path"]
    hl = pr["host_label"]
    root = pr["root"]
    ar = pr["add_record"]
    quote = pr["quote_txt"]

    def qv(s: str) -> str:
        return f'"{s}"' if quote else s

    if topic == "spf-record":
        block = f"""Type:    TXT
{hl}:    {root}
Value:   {qv("v=spf1 include:_spf.google.com ~all")}
TTL:     {"Automatic / Auto" if slug != "godaddy" else "1 hour (3600)"}"""
        return build_topic_payload(
            reg,
            topic,
            {
                "title": f"How to Add an SPF Record in {R}",
                "meta": f"Add SPF TXT at {R} — one v=spf1 record, merge includes. Verify in DNS Preflight.",
                "h1": f"Adding an SPF Record in {R} DNS",
                "subtitle": f"SPF belongs in a single TXT at your root. {R} uses “{hl}” for the left-hand field — use {root} for the apex. Never publish two SPF TXT records.",
                "howto_name": f"Add SPF TXT at {R}",
                "howto_desc": f"Open {R} DNS, add one TXT with your v=spf1 string, save, verify with DomainPreflight.",
                "step_names": [
                    f"Open {R} DNS",
                    "Add TXT record",
                    f"Set {hl} to root",
                    "Paste SPF value",
                    "Save",
                    "Verify in DNS Preflight",
                ],
                "step_texts": [
                    f"Navigate to {dns}.",
                    f"Click {ar} and choose type TXT.",
                    f"Set {hl} to {root} for the root domain.",
                    f"Paste your full SPF record starting with v=spf1 — merge with any existing SPF first.",
                    "Save the record. Wait a few minutes for the zone to update.",
                    "Run DNS Preflight to confirm SPF and lookup count.",
                ],
                "article": f"""
      <h2>Exact fields</h2>
      <div class="dns-block">{block}</div>
      <h2>The gotcha</h2>
      <p>Only one TXT may start with <code>v=spf1</code>. If you already have SPF, edit that row — do not add a second.</p>
      <p>{pr["txt_proxy"]}</p>
      <div class="tool-cta">
        <p>Verify SPF after you publish</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>
      <div class="glossary-links"><strong>See also:</strong>
        <a href="/dns/spf-record/">SPF record guide</a> ·
        <a href="/glossary/spf-record/">SPF glossary</a> ·
        <a href="/fix/spf/too-many-lookups/">Too many lookups</a>
      </div>
""",
                "faqs": [
                    (
                        f"How do I add a TXT record in {R}?",
                        f"{dns}. Then {ar} → TXT → set {hl} to {root} → paste value → save.",
                    ),
                    (
                        "Should I create a second SPF TXT if I use two senders?",
                        "No — merge includes into one v=spf1 string. Two SPF TXTs cause PermError.",
                    ),
                    (
                        f"How long until {R} SPF changes propagate?",
                        "Often minutes to a few hours. Confirm in DNS Preflight or the Propagation checker.",
                    ),
                    (
                        f"What if {R} splits my TXT into chunks?",
                        "Many panels split long strings — SPF usually fits. If something looks wrong, re-copy from your provider.",
                    ),
                    (
                        "Where does SPF go?",
                        "At the root of your domain — " + (f"blank apex name in Route 53" if slug == "aws-route53" else f'{hl} = {root}') + ".",
                    ),
                ],
            },
        )

    if topic == "dkim":
        dkim_block = f"""Type:    TXT
{hl}:    google._domainkey
Content: {qv("v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...")}
TTL:     Auto / Automatic"""
        if slug == "aws-route53":
            dkim_block = """Record name: google._domainkey
Type: TXT
Value: "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A..." """
        return build_topic_payload(
            reg,
            topic,
            {
                "title": f"How to Add a DKIM Record in {R}",
                "meta": f"DKIM TXT at selector._domainkey in {R} — subdomain only in {hl}.",
                "h1": f"Adding a DKIM Record in {R} DNS",
                "subtitle": f"DKIM is a TXT at [selector]._domainkey. In {R}, put only the subdomain part in {hl} — not the full FQDN — unless your panel says otherwise.",
                "howto_name": f"Publish DKIM TXT at {R}",
                "howto_desc": f"Get selector and value from your provider, add TXT in {R}, verify in DNS Preflight.",
                "step_names": [
                    "Copy DKIM from provider",
                    "Open DNS TXT form",
                    f"Set {hl} to selector._domainkey",
                    "Paste v=DKIM1 value",
                    "Save and wait",
                    "Verify in DNS Preflight",
                ],
                "step_texts": [
                    "Copy the hostname and TXT value from your email provider (Google, Microsoft, SendGrid, etc.).",
                    f"Go to " + dns + f" and click {ar} → TXT.",
                    f"Enter only the subdomain part in {hl} (e.g. google._domainkey). " + (
                        "Route 53: use google._domainkey as the record name relative to the zone."
                        if slug == "aws-route53"
                        else f"{R} usually appends your domain automatically."
                    ),
                    "Paste the full Content/value including v=DKIM1 and the long p= string.",
                    "Save. Wait a few minutes.",
                    "Run DNS Preflight to confirm DKIM passes and key strength looks sane.",
                ],
                "article": f"""
      <h2>Exact fields (example)</h2>
      <div class="dns-block">{dkim_block}</div>
      <h2>Name field</h2>
      <p>If the UI shows the full hostname preview, you still usually type only <code>google._domainkey</code> — not your registrable domain twice.</p>
      <div class="tool-cta">
        <p>Check DKIM after publish</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>
      <div class="glossary-links"><strong>See also:</strong>
        <a href="/dns/dkim-record/">DKIM setup guide</a> ·
        <a href="/glossary/dkim/">DKIM glossary</a> ·
        <a href="/fix/dkim/key-length/">Key length</a>
      </div>
""",
                "faqs": [
                    (
                        f"What goes in {hl} for DKIM?",
                        "Usually just the subdomain portion for that selector — e.g. google._domainkey. Your provider’s doc is authoritative.",
                    ),
                    (
                        f"Will {R} truncate long DKIM keys?",
                        "Most modern panels, including major registrars, handle long TXT. Paste the full p= value. If verification fails, re-paste without line breaks.",
                    ),
                    (
                        "Can I have multiple DKIM selectors?",
                        "Yes — different selectors are different hostnames. They don’t conflict.",
                    ),
                    (
                        "DNS Preflight shows pass but my dashboard says pending — why?",
                        "Providers poll on their schedule. If DNS answers look correct, give their checker time.",
                    ),
                    (
                        "Do I need CNAME instead of TXT?",
                        "Some hosts use CNAME for DKIM alignment — follow your provider. This guide covers TXT publication.",
                    ),
                ],
            },
        )

    if topic == "dmarc-setup":
        dmarc_block = f"""Type:    TXT
{hl}:    _dmarc
Content: {qv("v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com")}
TTL:     Auto / Automatic"""
        return build_topic_payload(
            reg,
            topic,
            {
                "title": f"How to Add a DMARC Record in {R}",
                "meta": f"DMARC TXT at _dmarc in {R} — start with p=none.",
                "h1": f"Adding a DMARC Record in {R} DNS",
                "subtitle": f"DMARC lives at _dmarc. In {R}, put _dmarc in {hl} — not _dmarc.yourdomain.com unless your UI asks for the full name.",
                "howto_name": f"Add DMARC at {R}",
                "howto_desc": f"Create TXT at _dmarc with v=DMARC1, confirm in DNS Preflight, tighten policy later.",
                "step_names": [
                    "Open DNS",
                    "Add TXT",
                    "Name _dmarc",
                    "Paste policy",
                    "Save",
                    "Verify and monitor",
                ],
                "step_texts": [
                    f"Go to {dns}.",
                    f"Add a TXT record ({ar}).",
                    f"Set {hl} to _dmarc.",
                    'Paste v=DMARC1; p=none; rua=mailto:you@yourdomain.com (adjust mailbox).',
                    "Save the record.",
                    "Run DNS Preflight. After reports arrive, consider p=quarantine then p=reject.",
                ],
                "article": f"""
      <h2>Exact fields</h2>
      <div class="dns-block">{dmarc_block}</div>
      <h2>Rollout</h2>
      <p>Start with <code>p=none</code>. Read aggregate reports, fix SPF/DKIM alignment, then tighten.</p>
      <div class="tool-cta">
        <p>Analyze DMARC XML</p>
        <a href="https://domainpreflight.dev/dmarc/">Open DMARC Report Analyzer →</a>
      </div>
      <div class="glossary-links"><strong>See also:</strong>
        <a href="/dns/dmarc-record/">DMARC setup guide</a> ·
        <a href="/glossary/dmarc/">DMARC glossary</a> ·
        <a href="/fix/dmarc/">DMARC fixes</a>
      </div>
""",
                "faqs": [
                    (
                        f"What {hl} do I use for DMARC?",
                        "_dmarc — the label for the DMARC policy host.",
                    ),
                    (
                        "SPF is also TXT — do they collide?",
                        "No. SPF sits at the root; DMARC sits at _dmarc. Different names.",
                    ),
                    (
                        "When do I move to p=reject?",
                        "After weeks of clean reports and no surprise mail sources — never on day one.",
                    ),
                    (
                        "Where do reports go?",
                        "Addresses in rua= (aggregate) and optionally ruf= (forensic). Use the analyzer to read XML.",
                    ),
                    (
                        f"Can I edit the same row later in {R}?",
                        "Yes — edit the existing TXT and save. DMARC updates are normal.",
                    ),
                ],
            },
        )

    if topic == "mx-record":
        mx_block = f"""Type:     MX
{hl}:     {root}
Mail server: aspmx.l.google.com
Priority: 1
TTL:      {"Auto" if slug != "godaddy" else "3600"}"""
        extra_mx = ""
        if slug == "cloudflare":
            extra_mx = """
      <h2>Cloudflare-specific</h2>
      <p><strong>MX must be DNS-only (grey cloud).</strong> Orange cloud on MX breaks mail — click the cloud until it’s grey.</p>"""
        return build_topic_payload(
            reg,
            topic,
            {
                "title": f"How to Add MX Records in {R}",
                "meta": f"Add MX at {R} — priorities, hostnames, {pr['mx_proxy']}",
                "h1": f"Adding MX Records in {R} DNS",
                "subtitle": f"MX points receiving mail servers. Use your provider’s exact hostnames and priorities. {pr['mx_proxy']}",
                "howto_name": f"Add MX records at {R}",
                "howto_desc": f"Create MX rows for each hostname your provider lists, verify with Propagation.",
                "step_names": [
                    "Open DNS",
                    "Add MX",
                    "Set root host",
                    "Enter mail server",
                    "Set priority",
                    "Save all MX rows",
                    "Verify propagation",
                ],
                "step_texts": [
                    f"Navigate to {dns}.",
                    f"Click {ar} → MX.",
                    f"Set {hl} to {root} for inbound mail to your domain.",
                    "Enter the mail server hostname from your provider (not an IP).",
                    "Set priority exactly as documented (lower number = higher preference where applicable).",
                    "Repeat for every MX your provider requires.",
                    "Use DomainPreflight Propagation — MX — to confirm all resolvers match.",
                ],
                "article": f"""
      <h2>Example row</h2>
      <div class="dns-block">{mx_block}</div>
      {extra_mx}
      <div class="tool-cta">
        <p>Check MX everywhere</p>
        <a href="https://domainpreflight.dev/propagation/">Open Propagation checker →</a>
      </div>
      <div class="glossary-links"><strong>See also:</strong>
        <a href="/dns/mx-record/">MX record guide</a> ·
        <a href="/glossary/mx-record/">MX glossary</a> ·
        <a href="/error/no-mx-record/">No MX error</a>
      </div>
""",
                "faqs": [
                    (
                        "How many MX rows do I need?",
                        "Whatever your provider documents — Google often lists five; Microsoft 365 might use one.",
                    ),
                    (
                        "What priority should I use?",
                        "Your provider’s numbers — don’t invent new priorities unless their docs say so.",
                    ),
                    (
                        f"My mail broke after editing MX in {R} — why?",
                        "Wrong hostnames, wrong priorities, or (on Cloudflare) orange-cloud proxy. Fix DNS-only for MX.",
                    ),
                    (
                        "MX hostname or IP?",
                        "Hostname — receivers expect a name that resolves in DNS.",
                    ),
                    (
                        "How do I verify?",
                        "DomainPreflight Propagation with type MX on your apex domain.",
                    ),
                ],
            },
        )

    if topic == "expiry-monitoring":
        return build_topic_payload(
            reg,
            topic,
            {
                "title": f"Domain Expiry Monitoring on {R}",
                "meta": f"Check renewal and auto-renew for domains at {R}. Cross-check with WHOIS.",
                "h1": f"Monitoring Domain Expiry — {R}",
                "subtitle": f"Know where renewal settings live for {R}, then cross-check the public expiry with WHOIS.",
                "howto_name": f"Verify expiry and auto-renew at {R}",
                "howto_desc": f"Open {R} account domain settings, confirm auto-renew, compare to DomainPreflight WHOIS.",
                "step_names": [
                    "Log into registrar",
                    "Open domain overview",
                    "Read expiry date",
                    "Enable auto-renew",
                    "Check billing",
                    "Cross-check WHOIS",
                ],
                "step_texts": [
                    f"Sign in to {R}.",
                    "Open your domain’s registration or overview page (path varies by brand).",
                    "Note the expiry / renewal date shown in the panel.",
                    "Turn on auto-renew if you want uninterrupted registration.",
                    "Ensure a valid payment method is on file.",
                    "Run DomainPreflight WHOIS to see registry-reported expiry and risk tier.",
                ],
                "article": f"""
      <h2>Where to look</h2>
      <p>{dns.split("→")[0] if "→" in dns else R} — most registrars show expiry on the domain dashboard. Names differ: Renew, Expires, Registration.</p>
      <div class="tool-cta">
        <p>Public expiry check</p>
        <a href="https://domainpreflight.dev/whois/">Open WHOIS →</a>
      </div>
      <div class="glossary-links"><strong>See also:</strong>
        <a href="/glossary/">Glossary</a>
      </div>
""",
                "faqs": [
                    (
                        "Why doesn’t the panel match WHOIS exactly?",
                        "Registry timing vs cache — WHOIS is authoritative for public expiry; the panel shows what the registrar plans.",
                    ),
                    (
                        "What if auto-renew fails?",
                        "Update billing early — some TLDs have short redemption windows.",
                    ),
                    (
                        f"Can I transfer away from {R} before expiry?",
                        "Usually yes — unlock / auth code steps depend on the registrar.",
                    ),
                    (
                        "Does DNS stop if the domain expires?",
                        "Eventually yes — the name leaves DNS when the registration lapses beyond grace.",
                    ),
                    (
                        "What is DomainPreflight risk tier?",
                        "A quick signal from WHOIS data — still verify in your registrar account.",
                    ),
                ],
            },
        )

    if topic == "domain-lock":
        return build_topic_payload(
            reg,
            topic,
            {
                "title": f"Domain Lock on {R}",
                "meta": f"Transfer lock at {R} — prevent unauthorised moves.",
                "h1": f"Domain Lock — {R}",
                "subtitle": f"Transfer lock stops surprise registrar moves. {R}'s UI label may say Transfer Lock, Lock, or similar.",
                "howto_name": f"Confirm transfer lock at {R}",
                "howto_desc": f"Find lock status in {R}, keep it on unless transferring.",
                "step_names": [
                    "Log in",
                    "Open domain security",
                    "Confirm lock on",
                    "Leave on until transfer",
                ],
                "step_texts": [
                    f"Sign in to {R}.",
                    "Open domain management → security / transfer settings.",
                    "Ensure transfer lock (or registrar lock) is enabled.",
                    "Disable only when you intentionally start an outbound transfer.",
                ],
                "article": f"""
      <h2>What lock does</h2>
      <p>Blocks unauthorised transfers — it does <strong>not</strong> replace renewal. Keep auto-renew on separately.</p>
      <p><strong>Hover note:</strong> lock controls may require support — check Hover’s current docs.</p>
      <div class="glossary-links"><strong>See also:</strong>
        <a href="/registrar/{slug}/expiry-monitoring/">Expiry monitoring</a>
      </div>
""",
                "faqs": [
                    (
                        "Does lock stop DNS edits?",
                        "No — you can still change records at your DNS host.",
                    ),
                    (
                        "How do I transfer out?",
                        "Unlock, request auth code, initiate transfer at the gaining registrar.",
                    ),
                    (
                        "Is lock default?",
                        "Often yes — verify periodically.",
                    ),
                    (
                        "Does lock prevent expiry?",
                        "No — renewal is separate.",
                    ),
                    (
                        f"Who do I contact if I can’t find lock in {R}?",
                        f"{R} support — panel labels move.",
                    ),
                ],
            },
        )

    if topic == "dnssec":
        # Only aws-route53 in our set
        return build_topic_payload(
            reg,
            topic,
            {
                "title": "Enable DNSSEC in AWS Route 53",
                "meta": "Turn on DNSSEC signing for a Route 53 hosted zone — then update DS at registrar.",
                "h1": "DNSSEC in Route 53",
                "subtitle": "Route 53 can sign your zone. After signing, you’ll add DS records at your registrar (or parent DNS) so resolvers can validate chains.",
                "howto_name": "Enable DNSSEC in Route 53",
                "howto_desc": "Open hosted zone, enable DNSSEC signing, copy DS data to registrar.",
                "step_names": [
                    "Open hosted zone",
                    "Enable DNSSEC signing",
                    "Copy DS digest",
                    "Add DS at registrar",
                    "Verify chain",
                ],
                "step_texts": [
                    "Route 53 → Hosted zones → select your zone.",
                    "Enable DNSSEC signing for the zone (follow AWS console prompts).",
                    "Copy the DS / DNSKEY details AWS provides for your registrar.",
                    "At your registrar (where the domain is registered), add the DS records they require.",
                    "Use external validators or dig + trusted tools to confirm the chain — mistakes break resolution.",
                ],
                "article": r"""
      <h2>Heads up</h2>
      <p>DNSSEC is easy to misconfigure — wrong DS at the parent means validation failures. Change during a maintenance window.</p>
      <div class="dns-block">Hosted zone → DNSSEC signing → ON
Registrar → add DS records (algorithm, digest type, digest from AWS)</div>
      <div class="glossary-links"><strong>See also:</strong>
        <a href="/dns/">DNS guides</a>
      </div>
""",
                "faqs": [
                    (
                        "Does Route 53 host my registration?",
                        "Not always — you often register elsewhere. DS goes where the domain is registered.",
                    ),
                    (
                        "Can I test before going live?",
                        "Use staging subdomains or lower TTL before cutover — DNSSEC errors are user-visible.",
                    ),
                    (
                        "Does DNSSEC fix email auth?",
                        "No — it validates DNS integrity. SPF/DKIM/DMARC are separate.",
                    ),
                    (
                        "What if email breaks after DS change?",
                        "Rollback DS at registrar or disable signing — diagnose with DNSSEC validators.",
                    ),
                    (
                        "Where is signing managed?",
                        "In the Route 53 hosted zone for authoritative DNS hosted at AWS.",
                    ),
                ],
            },
        )

    raise ValueError(f"unknown topic {topic}")


def build_all() -> list[tuple[str, dict]]:
    out: list[tuple[str, dict]] = []
    cf_pages = import_cloudflare_pages()
    for reg in REGISTRARS:
        slug = reg["slug"]
        for topic in reg["topics"]:
            if slug == "cloudflare" and topic in cf_pages:
                p = cf_pages[topic]
                rel = f"{slug}/{topic}"
                out.append(
                    (
                        "topic",
                        {
                            "rel": rel,
                            "title": p["title"],
                            "meta": p["meta"],
                            "h1": p["h1"],
                            "subtitle": p["subtitle"],
                            "hero": p.get("hero", "Registrar guide"),
                            "bc_nav_segments": nav_topic(slug, reg["short"], topic),
                            "bc_schema_trail": schema_topic(slug, reg["short"], topic, p["h1"], rel),
                            "howto_name": p["howto_name"],
                            "howto_desc": p["howto_desc"],
                            "step_names": p["step_names"],
                            "step_texts": p["step_texts"],
                            "faqs": p["faqs"],
                            "article": p["article"],
                            "back_href": f"/registrar/{slug}/",
                            "back_label": f"← {reg['short']} guides",
                        },
                    )
                )
            else:
                out.append(("topic", build_generic_topic(reg, topic)))

        cards = []
        for topic in reg["topics"]:
            ct, cd = TOPIC_CARDS[topic]
            cards.append((topic, ct, cd))
        out.append(
            (
                "hub",
                {
                    "rel": slug,
                    "title": reg["hub_title"],
                    "meta": reg["hub_meta"],
                    "h1": reg["hub_h1"],
                    "lead": reg["hub_lead"],
                    "intro": reg["hub_intro"],
                    "bc_nav": [
                        ("Home", HOME),
                        ("Registrars", "/registrar/"),
                        (reg["short"], None),
                    ],
                    "collection_name": reg["collection_name"],
                    "topic_cards": cards,
                    "breadcrumb_label": reg["short"],
                },
            )
        )
    return out
