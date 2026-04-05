# -*- coding: utf-8 -*-
"""Full Cloudflare topic pages — imported by registrar_pages_data.py."""

CLOUDFLARE_TOPIC_PAGES: list[dict] = [
    {
        "topic": "spf-record",
        "title": "How to Add an SPF Record in Cloudflare",
        "meta": "Add SPF TXT at Cloudflare — one v=spf1, merge includes. Grey cloud for mail hosts; verify in DNS Preflight.",
        "h1": "Adding an SPF Record in Cloudflare DNS",
        "subtitle": "Adding an SPF record in Cloudflare takes under 2 minutes. The key rule: never create two TXT records starting with v=spf1. Merge everything into one.",
        "hero": "Cloudflare",
        "howto_name": "Add SPF TXT in Cloudflare",
        "howto_desc": "Open DNS Records, add one TXT at @ with your v=spf1 string, save, verify SPF in DNS Preflight.",
        "step_names": [
            "Open DNS Records",
            "Add record",
            "Choose TXT and Name @",
            "Paste SPF Content",
            "TTL Auto and Save",
            "Verify in DNS Preflight",
        ],
        "step_texts": [
            "Cloudflare Dashboard → select your domain → DNS → Records.",
            "Click Add record.",
            "Type: TXT, Name: @",
            "Content: paste your full SPF record (v=spf1 ... ~all)",
            "TTL: Auto, Save",
            "Run DNS Preflight to verify SPF and lookup count",
        ],
        "article": r"""
      <h2>Exact fields in Cloudflare</h2>
      <div class="dns-block">DNS → Records → Add record
Type:    TXT
Name:    @
Content: v=spf1 include:_spf.google.com ~all
TTL:     Auto
Proxy:   DNS only (grey cloud) — TXT records cannot be proxied</div>
      <h2>The proxy warning</h2>
      <p>TXT records in Cloudflare are always DNS-only — the proxy toggle doesn’t apply. But <strong>MX records must also be DNS-only (grey)</strong>. Never proxy MX or mail-related A records.</p>
      <div class="tool-cta">
        <p>Verify SPF after publish</p>
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
                "How do I add a TXT record in Cloudflare?",
                "DNS → Records → Add record → Type: TXT → Name: @ → paste your SPF value → Save.",
            ),
            (
                "Should I proxy my SPF TXT record?",
                "TXT records can't be proxied — Cloudflare ignores the proxy toggle for TXT. Leave it grey.",
            ),
            (
                "I already have an SPF record — do I add another?",
                "No — merge both into one. Only one TXT record can start with v=spf1.",
            ),
            (
                "How long until Cloudflare SPF changes propagate?",
                "Usually minutes — Cloudflare's DNS is fast. Run DNS Preflight to confirm.",
            ),
            (
                "The Name field says @ — is that right?",
                "Yes. @ means your root domain. SPF always goes at the root.",
            ),
        ],
    },
    {
        "topic": "dkim",
        "title": "How to Add a DKIM Record in Cloudflare",
        "meta": "DKIM TXT at selector._domainkey in Cloudflare — Name field is subdomain only. Full key in Content.",
        "h1": "Adding a DKIM Record in Cloudflare DNS",
        "subtitle": "DKIM records in Cloudflare go at [selector]._domainkey.yourdomain.com. The most common mistake is using the wrong Name field — the subdomain part only, not the full hostname.",
        "hero": "Cloudflare",
        "howto_name": "Add DKIM TXT in Cloudflare",
        "howto_desc": "Copy DKIM from provider, add TXT with selector._domainkey in Name, paste v=DKIM1 value, verify in DNS Preflight.",
        "step_names": [
            "Get DKIM from provider",
            "Add TXT in Cloudflare",
            "Name: selector._domainkey",
            "Paste full v=DKIM1 value",
            "Save and wait",
            "Verify in DNS Preflight",
        ],
        "step_texts": [
            "Get your DKIM record from your email provider dashboard",
            "Cloudflare DNS → Add record → Type: TXT",
            "Name: [selector]._domainkey (e.g. google._domainkey) — do NOT include your domain name in the Name",
            "Content: paste the full v=DKIM1 value",
            "Save → wait 5 minutes",
            "Run DNS Preflight to confirm DKIM pass",
        ],
        "article": r"""
      <h2>Exact Cloudflare format</h2>
      <div class="dns-block">DNS → Records → Add record
Type:    TXT
Name:    google._domainkey
(NOT google._domainkey.yourdomain.com —
Cloudflare adds your domain automatically)
Content: "v=DKIM1; k=rsa; p=MIIBIjAN..."
TTL:     Auto</div>
      <div class="tool-cta">
        <p>Verify DKIM</p>
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
                "What do I put in the Name field for DKIM?",
                "Just the subdomain part — google._domainkey (not the full hostname). Cloudflare adds your domain automatically.",
            ),
            (
                "My DKIM record is very long — will Cloudflare truncate it?",
                "Cloudflare handles long TXT records correctly. Paste the full value — it won't be truncated.",
            ),
            (
                "How do I know which selector to use?",
                "Your email provider tells you. Google uses google, SendGrid uses s1 and s2, M365 uses selector1 and selector2.",
            ),
            (
                "DKIM shows as pass in DNS Preflight but my provider says pending — why?",
                "Providers cache verification. If DNS Preflight shows the record, propagation is done — your provider just needs time to check.",
            ),
            (
                "Can I add multiple DKIM records for different providers?",
                "Yes — each uses a different selector so they don't conflict. Add as many as you need.",
            ),
        ],
    },
    {
        "topic": "dmarc-setup",
        "title": "How to Add a DMARC Record in Cloudflare",
        "meta": "DMARC at _dmarc in Cloudflare — start p=none, add rua, verify in DNS Preflight.",
        "h1": "Adding a DMARC Record in Cloudflare DNS",
        "subtitle": "DMARC records in Cloudflare go at _dmarc as the Name. Start with p=none so you get reports without affecting delivery — then tighten the policy after reviewing the data.",
        "hero": "Cloudflare",
        "howto_name": "Add DMARC TXT in Cloudflare",
        "howto_desc": "Add TXT at _dmarc with v=DMARC1, confirm in DNS Preflight, upgrade policy after reports.",
        "step_names": [
            "Add TXT",
            "Name _dmarc",
            "Paste DMARC value",
            "Save",
            "Verify DMARC",
            "Plan policy upgrade",
        ],
        "step_texts": [
            "Cloudflare DNS → Add record → Type: TXT",
            "Name: _dmarc",
            "Content: paste your DMARC value starting with v=DMARC1",
            "Save",
            "Run DNS Preflight to confirm DMARC policy is live",
            "After 2-4 weeks of reports, upgrade from p=none to p=quarantine then p=reject",
        ],
        "article": r"""
      <h2>Exact Cloudflare format</h2>
      <div class="dns-block">DNS → Records → Add record
Type:    TXT
Name:    _dmarc
Content: "v=DMARC1; p=none;
rua=mailto:dmarc@yourdomain.com"
TTL:     Auto</div>
      <div class="tool-cta">
        <p>Read aggregate reports</p>
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
                "What Name do I use for DMARC in Cloudflare?",
                "_dmarc — not _dmarc.yourdomain.com. Cloudflare adds your domain automatically.",
            ),
            (
                "Should I start with p=none or p=reject?",
                "Always start with p=none. It monitors without affecting delivery. Only move to p=reject after reviewing reports.",
            ),
            (
                "Where do DMARC reports go?",
                "To the email in your rua= tag. Use DomainPreflight DMARC Report Analyzer to read them.",
            ),
            (
                "Can I have both SPF and DMARC TXT records in Cloudflare?",
                "Yes — they're at different Names. SPF is at @, DMARC is at _dmarc. No conflict.",
            ),
            (
                "How do I upgrade from p=none to p=reject?",
                "Edit the existing _dmarc record — change p=none to p=quarantine, save, monitor for a week, then change to p=reject.",
            ),
        ],
    },
    {
        "topic": "mx-record",
        "title": "How to Add MX Records in Cloudflare",
        "meta": "MX on Cloudflare must be DNS-only (grey cloud). Add provider MX hostnames and priorities — verify with Propagation.",
        "h1": "Adding MX Records in Cloudflare DNS",
        "subtitle": "The critical Cloudflare MX rule: MX records must NEVER be proxied (orange cloud). Set to DNS-only (grey cloud). Proxied MX records break email delivery.",
        "hero": "Cloudflare",
        "howto_name": "Add MX records in Cloudflare",
        "howto_desc": "Create MX rows at @, grey cloud only, match provider priorities, verify with Propagation.",
        "step_names": [
            "Add MX record",
            "Name @",
            "Mail server hostname",
            "Priority",
            "Grey cloud only",
            "Repeat for all MX",
            "Verify propagation",
        ],
        "step_texts": [
            "Cloudflare DNS → Add record → Type: MX",
            "Name: @",
            "Mail server: paste your provider's MX hostname",
            "Priority: set per your provider's instructions",
            "Confirm proxy is grey (DNS only) — never orange",
            "Repeat for each MX record your provider requires",
            "Verify with DomainPreflight Propagation — MX type",
        ],
        "article": r"""
      <h2>The critical Cloudflare MX rule</h2>
      <p>MX records must <strong>never</strong> be proxied (orange cloud). Set to <strong>DNS-only (grey cloud)</strong>. Proxied MX records break email delivery.</p>
      <div class="dns-block">DNS → Records → Add record
Type:     MX
Name:     @
Mail server: aspmx.l.google.com
Priority: 1
TTL:      Auto
Proxy:    DNS only (grey) — REQUIRED</div>
      <div class="tool-cta">
        <p>Check MX across resolvers</p>
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
                "Should Cloudflare MX records be proxied (orange) or DNS-only (grey)?",
                "Always DNS-only (grey). Proxied MX records break email delivery. This is the most common Cloudflare email mistake.",
            ),
            (
                "How many MX records do I need?",
                "Depends on your provider. Google Workspace needs 5. Microsoft 365 needs 1. Check your provider's docs.",
            ),
            (
                "What priority should I set?",
                "Use exactly what your provider specifies. Google uses 1, 5, 10. Microsoft uses 0.",
            ),
            (
                "My email stopped working after adding MX in Cloudflare — why?",
                "Check the proxy status. If it shows orange, click it to make it grey. Proxied MX breaks everything.",
            ),
            (
                "How do I verify MX records are propagated?",
                "DomainPreflight Propagation checker — select MX type, enter your domain.",
            ),
        ],
    },
    {
        "topic": "expiry-monitoring",
        "title": "Domain Expiry Monitoring with Cloudflare Registrar",
        "meta": "Check expiry and auto-renew for domains registered with Cloudflare Registrar — cross-check with WHOIS.",
        "h1": "Monitoring Domain Expiry on Cloudflare Registrar",
        "subtitle": "If your domain is registered with Cloudflare Registrar, expiry monitoring and auto-renew are in the same dashboard as your DNS. Here's how to check your expiry date and make sure auto-renew is enabled.",
        "hero": "Cloudflare",
        "howto_name": "Monitor domain expiry on Cloudflare Registrar",
        "howto_desc": "Open Domain Registration, confirm auto-renew and billing, cross-check expiry in WHOIS.",
        "step_names": [
            "Open Domain Registration",
            "Check expiry date",
            "Enable Auto-Renew",
            "Verify Billing",
            "Run WHOIS check",
        ],
        "step_texts": [
            "Cloudflare Dashboard → Domain Registration → your domain",
            "Check expiry date shown on the domain overview",
            "Confirm Auto-Renew is toggled ON",
            "Verify your payment method is current under Billing",
            "Run DomainPreflight WHOIS to see expiry with risk tier",
        ],
        "article": r"""
      <h2>DNS vs Registrar</h2>
      <p>Cloudflare DNS can be on any domain — expiry settings here apply when <strong>Cloudflare is also your registrar</strong> for that name.</p>
      <div class="tool-cta">
        <p>Public expiry lookup</p>
        <a href="https://domainpreflight.dev/whois/">Open WHOIS →</a>
      </div>
""",
        "faqs": [
            (
                "Where do I see my domain expiry in Cloudflare?",
                "Cloudflare Dashboard → Domain Registration → select your domain → expiry date shown on overview.",
            ),
            (
                "Does Cloudflare auto-renew domains?",
                "Yes — enable Auto-Renew in Domain Registration settings. Also verify your payment method is current.",
            ),
            (
                "How do I check expiry without logging into Cloudflare?",
                "Run DomainPreflight WHOIS — shows expiry date, registrar, and risk tier for any domain.",
            ),
            (
                "What happens if my Cloudflare domain expires?",
                "Cloudflare offers a grace period. After that, redemption fees apply. Enable auto-renew to avoid this.",
            ),
            (
                "Can I transfer my domain away from Cloudflare before it expires?",
                "Yes — unlock the domain in Domain Registration settings and request an auth code for transfer.",
            ),
        ],
    },
    {
        "topic": "domain-lock",
        "title": "Domain Lock on Cloudflare — Prevent Unauthorised Transfers",
        "meta": "Transfer lock on Cloudflare Registrar — on by default, verify in Domain Registration.",
        "h1": "Enabling Domain Lock on Cloudflare",
        "subtitle": "Domain lock (transfer lock) prevents your domain from being transferred to another registrar without your authorisation. Cloudflare enables it by default — here's how to verify it's on.",
        "hero": "Cloudflare",
        "howto_name": "Verify domain lock on Cloudflare",
        "howto_desc": "Open Domain Registration, confirm Transfer Lock is locked, leave on until intentional transfer.",
        "step_names": [
            "Open Domain Registration",
            "Find Transfer Lock",
            "Enable if unlocked",
            "Keep locked until transfer",
        ],
        "step_texts": [
            "Cloudflare → Domain Registration → your domain",
            "Look for Transfer Lock — confirm it shows Locked",
            "If unlocked → toggle to enable lock",
            "Lock stays on until you initiate a transfer",
        ],
        "article": r"""
      <h2>What lock does</h2>
      <p>Transfer lock blocks unauthorised moves to another registrar. It does not stop DNS edits or renewal — manage those separately.</p>
""",
        "faqs": [
            (
                "What is domain lock?",
                "A setting that prevents your domain from being transferred to another registrar without your explicit approval.",
            ),
            (
                "Is domain lock enabled by default in Cloudflare?",
                "Yes — Cloudflare locks domains by default. Verify it's still on in Domain Registration settings.",
            ),
            (
                "Does domain lock affect DNS changes?",
                "No. Lock only prevents transfers. You can still update DNS records, renew, and manage the domain normally.",
            ),
            (
                "How do I unlock for a transfer?",
                "Cloudflare → Domain Registration → your domain → disable Transfer Lock → request auth code.",
            ),
            (
                "Will domain lock prevent my domain from expiring?",
                "No — lock and renewal are separate. Enable Auto-Renew for expiry protection.",
            ),
        ],
    },
]
