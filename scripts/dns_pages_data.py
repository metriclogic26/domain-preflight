# -*- coding: utf-8 -*-
"""Emit kwargs for generate_dns_guides.emit() — one dict per DNS guide page."""

HOME = "https://domainpreflight.dev/"


def bc2(name: str, rel: str):
    return [
        ("Home", HOME),
        ("DNS Records", "/dns/"),
        (name, None),
    ], [
        ("Home", HOME),
        ("DNS Records", f"{HOME}dns/"),
        (name, f"{HOME}dns/{rel}/"),
    ]


def bc_prop(page_title: str, rel: str):
    """Breadcrumb: Home > DNS Records > Propagation > page."""
    return [
        ("Home", HOME),
        ("DNS Records", "/dns/"),
        ("Propagation", "/dns/propagation/"),
        (page_title, None),
    ], [
        ("Home", HOME),
        ("DNS Records", f"{HOME}dns/"),
        ("Propagation", f"{HOME}dns/propagation/"),
        (page_title, f"{HOME}dns/{rel}/"),
    ]


PAGES: list[dict] = []

# ——— Page 1: MX ———
_nav, _sch = bc2("MX Record Setup Guide", "mx-record")
PAGES.append(
    {
        "rel": "mx-record",
        "title": "MX Record — How to Add and Verify Your Mail Exchanger",
        "meta": "Add MX records so mail servers know where to deliver email for your domain. Verify with DomainPreflight Propagation.",
        "h1": "MX Record Setup Guide",
        "subtitle": "An MX record tells other mail servers where to deliver email for your domain. Without one, your domain can't receive any email. Here's how to add the right MX records for your email provider and verify they're working.",
        "hero": "DNS guide",
        "bc_nav_segments": _nav,
        "bc_schema_trail": _sch,
        "howto_name": "Add and verify MX records for your domain",
        "howto_desc": "Log into DNS, remove old MX entries, add provider MX records with correct priority, wait for propagation, and verify with a propagation checker.",
        "step_names": [
            "Log into your DNS provider",
            "Remove old MX records",
            "Add provider MX records",
            "Set priority correctly",
            "Wait for DNS propagation",
            "Verify with Propagation checker",
        ],
        "step_texts": [
            "Log into your DNS provider (Cloudflare, Namecheap, etc.).",
            "Delete any existing MX records from a previous provider.",
            "Add the MX records your email provider specifies — get exact values from their setup docs.",
            "Set priority values correctly (lower number = higher priority).",
            "Wait up to 48 hours for DNS propagation.",
            "Run the DomainPreflight Propagation checker to confirm MX records are live across all resolvers.",
        ],
        "faqs": [
            (
                "What is an MX record?",
                "An MX record tells mail servers where to deliver email for your domain. Without one, your domain can't receive email.",
            ),
            (
                "Can I have multiple MX records?",
                "Yes — multiple MX records provide redundancy. Lower priority numbers are tried first. If the primary is down, the next is tried automatically.",
            ),
            (
                "What does MX priority mean?",
                "Lower number = higher priority. Priority 1 is tried before priority 5. If you have one server, use priority 10.",
            ),
            (
                "How long do MX record changes take?",
                "Up to 48 hours. Use DomainPreflight Propagation checker to see when all resolvers have the new record.",
            ),
            (
                "My MX records exist but email still bounces — why?",
                "Check that MX records point to a hostname (not an IP), the hostname has an A record, and your mail server is actually running.",
            ),
        ],
        "article": r"""
      <h2>Why it matters</h2>
      <p>When someone sends email to you@yourdomain.com, their server looks up your MX record to find your mail server. No MX = no delivery. Wrong MX = email going to the wrong server.</p>

      <h2>Common MX records by provider</h2>
      <p>Copy exact values from your provider’s docs — these are typical examples.</p>
      <h3>Google Workspace</h3>
      <div class="dns-block">@ MX 1  aspmx.l.google.com
@ MX 5  alt1.aspmx.l.google.com
@ MX 5  alt2.aspmx.l.google.com
@ MX 10 alt3.aspmx.l.google.com
@ MX 10 alt4.aspmx.l.google.com</div>
      <h3>Microsoft 365</h3>
      <div class="dns-block">@ MX 0  yourdomain-com.mail.protection.outlook.com</div>
      <h3>Fastmail</h3>
      <div class="dns-block">@ MX 10 in1-smtp.messagingengine.com
@ MX 20 in2-smtp.messagingengine.com</div>
      <h3>Zoho Mail</h3>
      <div class="dns-block">@ MX 10 mx.zoho.com
@ MX 20 mx2.zoho.com</div>

      <h2>How to verify</h2>
      <p>Run <strong>DomainPreflight Propagation</strong> — select MX record type, enter your domain, confirm all five resolvers show your records.</p>
      <div class="tool-cta">
        <p>Check MX across resolvers</p>
        <a href="https://domainpreflight.dev/propagation/">Open Propagation checker →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/glossary/mx-record/">MX record (glossary)</a> ·
        <a href="/error/no-mx-record/">No MX record error</a>
      </div>
""",
    }
)

# ——— Page 2: TXT ———
_nav, _sch = bc2("TXT Record Setup Guide", "txt-record")
PAGES.append(
    {
        "rel": "txt-record",
        "title": "TXT Record — How to Add SPF, DKIM, DMARC, and Verification Records",
        "meta": "Add TXT records for SPF, DKIM, DMARC, and domain verification. One SPF rule: only one v=spf1 record per domain.",
        "h1": "TXT Record Setup Guide",
        "subtitle": "TXT records store text data in DNS. They're how you add SPF, DKIM, DMARC, and domain verification records. Here's how to add them correctly — and the one rule that breaks most email setups.",
        "hero": "DNS guide",
        "bc_nav_segments": _nav,
        "bc_schema_trail": _sch,
        "howto_name": "Add TXT records for email authentication and verification",
        "howto_desc": "Identify needed TXT records, merge SPF instead of duplicating, add each record with correct host, avoid truncation, and verify.",
        "step_names": [
            "Identify TXT records you need",
            "Check existing SPF before adding",
            "Add each TXT with correct host",
            "Avoid truncation on long values",
            "Verify with Preflight or Propagation",
        ],
        "step_texts": [
            "Identify which TXT records you need (SPF, DMARC, DKIM, verification).",
            "Check for an existing SPF record before adding a new one — merge, don't duplicate.",
            "Add each TXT record with the correct name/host value (@ for root, _dmarc for DMARC).",
            "For long values (DKIM keys), ensure your DNS provider doesn't truncate the record.",
            "Verify with DNS Preflight or the Propagation checker.",
        ],
        "faqs": [
            (
                "What is a TXT record used for?",
                "Storing text data in DNS — mainly SPF, DKIM, DMARC, and domain verification for services like Google and Microsoft.",
            ),
            (
                "Can I have multiple TXT records?",
                "Yes — except for SPF. You can have multiple TXT records but only one can start with v=spf1.",
            ),
            (
                "What host value do I use for DMARC?",
                "_dmarc — the DMARC record always goes at _dmarc.yourdomain.com.",
            ),
            (
                "My DKIM key is too long — what do I do?",
                "Some DNS providers split long TXT records into 255-character chunks. DKIM keys must be properly formatted — check your provider's documentation for long TXT record handling.",
            ),
            (
                "How do I verify my TXT records are live?",
                "Use DomainPreflight Propagation checker — select TXT type, enter your domain, confirm the record appears.",
            ),
        ],
        "article": r"""
      <h2>The one rule</h2>
      <p>You can only have <strong>one</strong> SPF record. One TXT record starting with <code>v=spf1</code>. Two SPF records = immediate PermError. Every other TXT record can coexist.</p>

      <h2>Common TXT records</h2>
      <h3>SPF</h3>
      <div class="dns-block">@ TXT "v=spf1 include:_spf.google.com ~all"</div>
      <h3>DMARC</h3>
      <div class="dns-block">_dmarc TXT "v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com"</div>
      <h3>Google domain verification</h3>
      <div class="dns-block">@ TXT "google-site-verification=abc123..."</div>
      <h3>Microsoft domain verification</h3>
      <div class="dns-block">@ TXT "MS=ms12345678"</div>

      <div class="tool-cta">
        <p>Inspect DNS in the browser</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/glossary/txt-record/">TXT record</a> ·
        <a href="/glossary/spf-record/">SPF record</a>
      </div>
""",
    }
)

# ——— Page 3: CNAME ———
_nav, _sch = bc2("CNAME Record Setup Guide", "cname-record")
PAGES.append(
    {
        "rel": "cname-record",
        "title": "CNAME Record — Setup, Restrictions, and Common Uses",
        "meta": "CNAME maps one hostname to another. No CNAME at apex. Use Propagation checker to verify DKIM CNAMEs.",
        "h1": "CNAME Record Setup Guide",
        "subtitle": "A CNAME record maps one hostname to another. Email providers use CNAMEs for DKIM alignment. But CNAMEs have important restrictions — using them in the wrong place breaks email.",
        "hero": "DNS guide",
        "bc_nav_segments": _nav,
        "bc_schema_trail": _sch,
        "howto_name": "Add a CNAME record safely for email and services",
        "howto_desc": "Use a subdomain only, ensure no conflicting records, add source and target hostnames, verify with Propagation.",
        "step_names": [
            "Pick the hostname (subdomain only)",
            "Check for conflicting records",
            "Add CNAME source and target",
            "Verify with Propagation checker",
        ],
        "step_texts": [
            "Identify the hostname you need the CNAME on — must be a subdomain, never @.",
            "Check no other records exist at that hostname (A, MX, TXT) — CNAMEs can't coexist.",
            "Add the CNAME record with source hostname and target hostname.",
            "Verify with Propagation checker — select CNAME type.",
        ],
        "faqs": [
            (
                "What is a CNAME record?",
                "A DNS record that points one hostname to another hostname instead of directly to an IP address.",
            ),
            (
                "Can I use a CNAME at my root domain?",
                "No. CNAMEs cannot be at the apex (root) domain — they conflict with required records and break email. Use an A record or ALIAS/ANAME instead.",
            ),
            (
                "Can I have other records at the same hostname as a CNAME?",
                "No. A CNAME is exclusive — no other record types can exist at the same hostname.",
            ),
            (
                "Why do email providers use CNAMEs for DKIM?",
                "CNAMEs let the provider rotate DKIM keys without you updating DNS. Your CNAME always points to their current key.",
            ),
            (
                "How do I verify a CNAME is working?",
                "Use DomainPreflight Propagation checker — select CNAME, enter the full subdomain, confirm the target appears.",
            ),
        ],
        "article": r"""
      <h2>Key restriction</h2>
      <p>You cannot use a CNAME at your root domain (@). CNAMEs at the apex conflict with SOA and NS records — and would override your MX records, breaking email delivery entirely.</p>

      <h2>Common CNAME uses</h2>
      <h3>SendGrid DKIM alignment</h3>
      <div class="dns-block">s1._domainkey.yourdomain.com
CNAME s1.domainkey.u123.wl.sendgrid.net</div>
      <h3>Microsoft 365 DKIM</h3>
      <div class="dns-block">selector1._domainkey.yourdomain.com
CNAME selector1-yourdomain-com._domainkey.yourtenant.onmicrosoft.com</div>
      <h3>Subdomain to service</h3>
      <div class="dns-block">app.yourdomain.com
CNAME yourapp.herokuapp.com</div>

      <div class="tool-cta">
        <p>Verify CNAME propagation</p>
        <a href="https://domainpreflight.dev/propagation/">Open Propagation checker →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/glossary/cname-record/">CNAME record</a> ·
        <a href="/glossary/subdomain-takeover/">Subdomain takeover</a>
      </div>
""",
    }
)

# ——— Page 4: A ———
_nav, _sch = bc2("A Record Setup Guide", "a-record")
PAGES.append(
    {
        "rel": "a-record",
        "title": "A Record — How to Point Your Domain to an IP Address",
        "meta": "Map hostnames to IPv4 with A records. Mail hostnames need DNS-only in Cloudflare. Verify with Propagation.",
        "h1": "A Record Setup Guide",
        "subtitle": "An A record maps a hostname to an IPv4 address. It's how your domain resolves to your server. Most hosting setups, mail server PTR records, and custom DKIM hostnames need A records.",
        "hero": "DNS guide",
        "bc_nav_segments": _nav,
        "bc_schema_trail": _sch,
        "howto_name": "Add an A record to point a hostname to IPv4",
        "howto_desc": "Get your server IP, add A record at DNS, set Cloudflare proxy correctly for mail hosts, verify propagation.",
        "step_names": [
            "Get server IPv4 address",
            "Log into DNS provider",
            "Add A record",
            "Cloudflare: proxy vs DNS-only",
            "Verify with Propagation checker",
        ],
        "step_texts": [
            "Get your server's IP address from your hosting panel.",
            "Log into your DNS provider.",
            "Add A record — name: @ (or subdomain), value: IP.",
            "If on Cloudflare, decide proxy (orange cloud) vs DNS-only (grey cloud) — mail hostnames must be DNS-only.",
            "Verify with Propagation checker — select A type.",
        ],
        "faqs": [
            (
                "What is an A record?",
                "A DNS record that maps a hostname to an IPv4 address. Used to point your domain or subdomain to a server.",
            ),
            (
                "What is the difference between A and AAAA records?",
                "A records are for IPv4 addresses. AAAA records are for IPv6. Most setups need both.",
            ),
            (
                "Should I proxy my A record through Cloudflare?",
                "For websites — yes (orange cloud). For mail hostnames — no (grey cloud). Proxied mail hostnames break PTR forward confirmation.",
            ),
            (
                "How long do A record changes take?",
                "Up to 48 hours. Use DomainPreflight Propagation to check when all resolvers have the new IP.",
            ),
            (
                "My A record is correct but my site is still showing the old IP — why?",
                "Browser or ISP DNS cache. Force-refresh with Ctrl+Shift+R or check from a different network. DomainPreflight Propagation shows the live DNS state.",
            ),
        ],
        "article": r"""
      <h2>Common A record setup</h2>
      <h3>Root domain to server</h3>
      <div class="dns-block">@   A  203.0.113.10</div>
      <h3>WWW subdomain</h3>
      <div class="dns-block">www A  203.0.113.10</div>
      <h3>Mail hostname (for PTR/FCrDNS)</h3>
      <div class="dns-block">mail A  203.0.113.10</div>

      <h2>Important for email</h2>
      <p>Your mail hostname (e.g. mail.yourdomain.com) must have an A record for PTR forward confirmation to work. Set it to <strong>DNS-only</strong> in Cloudflare — proxied mail hostnames break email.</p>

      <div class="tool-cta">
        <p>Check A record propagation</p>
        <a href="https://domainpreflight.dev/propagation/">Open Propagation checker →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/glossary/ptr-record/">PTR record</a> ·
        <a href="/glossary/rdns/">Reverse DNS (rDNS)</a>
      </div>
""",
    }
)

# ——— Page 5: AAAA ———
_nav, _sch = bc2("AAAA Record Setup Guide", "aaaa-record")
PAGES.append(
    {
        "rel": "aaaa-record",
        "title": "AAAA Record — IPv6 DNS Setup Guide",
        "meta": "AAAA maps hostnames to IPv6. Add alongside A records for dual-stack. IPv6 mail needs IPv6 PTR too.",
        "h1": "AAAA Record Setup Guide",
        "subtitle": "An AAAA record maps a hostname to an IPv6 address — the IPv6 equivalent of an A record. Most modern servers support IPv6. Adding AAAA records alongside A records ensures your domain works for IPv6 clients.",
        "hero": "DNS guide",
        "bc_nav_segments": _nav,
        "bc_schema_trail": _sch,
        "howto_name": "Add an AAAA record for IPv6",
        "howto_desc": "Obtain IPv6 from hosting, add AAAA at @ or subdomain, verify with Propagation.",
        "step_names": [
            "Get server IPv6 address",
            "Add AAAA record",
            "Verify with Propagation checker",
        ],
        "step_texts": [
            "Get your server's IPv6 address from your hosting panel.",
            "Add AAAA record — name: @, value: full IPv6 address.",
            "Verify with Propagation checker — select AAAA type.",
        ],
        "faqs": [
            (
                "What is an AAAA record?",
                "A DNS record mapping a hostname to an IPv6 address. The IPv6 equivalent of an A record.",
            ),
            (
                "Do I need both A and AAAA records?",
                "Not required but recommended. A record covers IPv4 clients. AAAA covers IPv6. Most modern servers support both.",
            ),
            (
                "Does my mail server need an AAAA record?",
                "Only if it has an IPv6 address. If it does, also add a PTR record for the IPv6 address — some receivers check IPv6 PTR too.",
            ),
            (
                "How do I check my AAAA record is propagated?",
                "DomainPreflight Propagation checker — select AAAA type and enter your domain.",
            ),
            (
                "Will adding AAAA break my existing A record?",
                "No. A and AAAA records coexist at the same hostname without conflict.",
            ),
        ],
        "article": r"""
      <h2>Example</h2>
      <div class="dns-block">@ AAAA 2001:db8::1</div>

      <h2>Note for email</h2>
      <p>If your mail server has an IPv6 address, add a PTR record for the IPv6 address too. DomainPreflight DNS Preflight checks IPv6 PTR records — enter your IPv6 sending address in the IP field.</p>

      <div class="tool-cta">
        <p>Check AAAA propagation</p>
        <a href="https://domainpreflight.dev/propagation/">Open Propagation checker →</a>
      </div>
      <div class="tool-cta">
        <p>IPv6 PTR and full mail checks</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>
""",
    }
)

# ——— Page 6: PTR ———
_nav, _sch = bc2("PTR Record Setup Guide", "ptr-record")
PAGES.append(
    {
        "rel": "ptr-record",
        "title": "PTR Record — Reverse DNS Setup for Email Delivery",
        "meta": "PTR maps IP to hostname for reverse DNS. Set at your host, not registrar. Verify with DNS Preflight.",
        "h1": "PTR Record Setup Guide",
        "subtitle": "A PTR record maps your sending IP back to a hostname — reverse DNS. Mail servers check this when email arrives. No PTR record means many servers reject your email before even checking SPF or DKIM.",
        "hero": "DNS guide",
        "bc_nav_segments": _nav,
        "bc_schema_trail": _sch,
        "howto_name": "Configure PTR (reverse DNS) for your sending IP",
        "howto_desc": "Use hosting panel to set PTR hostname, add matching A record, verify with DNS Preflight.",
        "step_names": [
            "Open hosting control panel",
            "Find Reverse DNS or PTR",
            "Set PTR hostname you control",
            "Add matching A record",
            "Run DNS Preflight",
        ],
        "step_texts": [
            "Log into your hosting provider control panel.",
            "Find Reverse DNS or PTR settings for your IP.",
            "Set the PTR hostname to a hostname you control (e.g. mail.yourdomain.com).",
            "Add an A record for that hostname pointing back to the same IP.",
            "Run DNS Preflight with your sending IP to confirm the PTR check passes.",
        ],
        "faqs": [
            (
                "What is a PTR record?",
                "A DNS record that maps an IP address back to a hostname. Used by mail servers to verify your sending infrastructure.",
            ),
            (
                "Where do I set up a PTR record?",
                "At your hosting provider — not your domain registrar. Look for Reverse DNS in your VPS or server control panel.",
            ),
            (
                "What hostname should my PTR point to?",
                "A hostname you control that has an A record pointing back to the same IP. mail.yourdomain.com is the convention.",
            ),
            (
                "Does missing PTR cause email to bounce?",
                "It can. Many corporate mail servers reject email from IPs with no PTR. Others increase spam score. Always set a PTR for mail servers.",
            ),
            (
                "How do I verify my PTR is correct?",
                "Run DNS Preflight with your sending IP — it checks PTR existence and forward confirmation.",
            ),
        ],
        "article": r"""
      <h2>What forward-confirmed reverse DNS requires</h2>
      <p><strong>Step 1:</strong> IP → PTR lookup → mail.yourdomain.com<br><strong>Step 2:</strong> mail.yourdomain.com → A lookup → same IP. Both must match. If step 2 returns a different IP, the check fails.</p>

      <h2>How to set up</h2>
      <p>PTR records are controlled by your hosting provider — not your domain registrar. Look for Reverse DNS in your VPS control panel.</p>
      <ul>
        <li><strong>Hetzner:</strong> Server → Networking → Reverse DNS</li>
        <li><strong>DigitalOcean:</strong> Droplet → Networking → PTR</li>
        <li><strong>AWS:</strong> EC2 → Network Interfaces → Reverse DNS</li>
      </ul>

      <div class="tool-cta">
        <p>Check PTR and mail stack</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/glossary/ptr-record/">PTR record</a> ·
        <a href="/glossary/rdns/">Reverse DNS</a> ·
        <a href="/error/ptr-mismatch/">PTR mismatch error</a>
      </div>
""",
    }
)

# ——— Page 7: SPF ———
_nav, _sch = bc2("SPF Record Setup Guide", "spf-record")
PAGES.append(
    {
        "rel": "spf-record",
        "title": "SPF Record — How to Add and Verify Your Sender Policy",
        "meta": "One SPF TXT per domain. Merge includes, stay under 10 DNS lookups. Verify with DNS Preflight.",
        "h1": "SPF Record Setup Guide",
        "subtitle": "An SPF record lists the servers authorised to send email for your domain. Without one, any server can send email pretending to be from your domain. Here's how to build the right SPF record for your setup.",
        "hero": "DNS guide",
        "bc_nav_segments": _nav,
        "bc_schema_trail": _sch,
        "howto_name": "Publish and verify a correct SPF record",
        "howto_desc": "List senders, gather includes, merge into one TXT at @, verify SPF and lookup count in DNS Preflight.",
        "step_names": [
            "List all services that send mail",
            "Find each SPF include value",
            "Merge with existing SPF",
            "Publish single TXT at @",
            "Run DNS Preflight",
            "Confirm lookup count under 10",
        ],
        "step_texts": [
            "List all services that send email for your domain.",
            "Find each service's SPF include value.",
            "Check for existing SPF record — merge, don't duplicate.",
            "Publish as a single TXT record at @ with TTL: Auto.",
            "Run DNS Preflight to verify SPF and check lookup count.",
            "Check lookup count is under 10 — expand the SPF tree in DNS Preflight to see the count.",
        ],
        "faqs": [
            (
                "What is an SPF record?",
                "A TXT record that lists which servers are authorised to send email for your domain. Receivers check it to verify your email is legitimate.",
            ),
            (
                "What does ~all mean in SPF?",
                "Softfail — unauthorised servers are marked suspicious but email is usually delivered. Start with ~all, switch to -all once all senders are confirmed.",
            ),
            (
                "How many DNS lookups does my SPF use?",
                "Run DNS Preflight — the SPF tree shows each include expanded with a running count. Must stay under 10.",
            ),
            (
                "What if I need more than 10 lookups?",
                "Flatten high-lookup providers by replacing include: with their actual IP addresses. See the SPF too many lookups fix guide.",
            ),
            (
                "Do I need SPF if I have DKIM?",
                "Yes. SPF and DKIM serve different purposes. DMARC requires both to be configured for full protection.",
            ),
        ],
        "article": r"""
      <h2>The golden rule</h2>
      <p>One SPF record per domain. Only one TXT record can start with <code>v=spf1</code>. Two SPF records = immediate PermError.</p>

      <h2>Building your SPF record</h2>
      <h3>Google Workspace only</h3>
      <div class="dns-block">v=spf1 include:_spf.google.com ~all</div>
      <h3>Google + SendGrid</h3>
      <div class="dns-block">v=spf1 include:_spf.google.com include:sendgrid.net ~all</div>
      <h3>Google + SendGrid + Microsoft 365</h3>
      <div class="dns-block">v=spf1 include:_spf.google.com include:sendgrid.net include:spf.protection.outlook.com ~all</div>
      <h3>Self-hosted mail + Google</h3>
      <div class="dns-block">v=spf1 ip4:203.0.113.10 include:_spf.google.com ~all</div>

      <div class="tool-cta">
        <p>Verify SPF and lookup tree</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/glossary/spf-record/">SPF record</a> ·
        <a href="/fix/spf/too-many-lookups/">SPF too many lookups</a> ·
        <a href="/error/spf-permerror/">SPF PermError</a>
      </div>
""",
    }
)

# ——— Page 8: DKIM ———
_nav, _sch = bc2("DKIM Record Setup Guide", "dkim-record")
PAGES.append(
    {
        "rel": "dkim-record",
        "title": "DKIM Record — How to Publish Your Public Key",
        "meta": "Publish DKIM TXT at selector._domainkey. Avoid truncation. Verify key strength in DNS Preflight.",
        "h1": "DKIM Record Setup Guide",
        "subtitle": "A DKIM record publishes your public signing key in DNS. Mail servers use it to verify that your emails haven't been tampered with. Here's how to add it correctly and avoid the common truncation mistake.",
        "hero": "DNS guide",
        "bc_nav_segments": _nav,
        "bc_schema_trail": _sch,
        "howto_name": "Publish a DKIM TXT record correctly",
        "howto_desc": "Generate key in provider, copy full value, add at selector._domainkey, verify in DNS Preflight.",
        "step_names": [
            "Generate DKIM in provider",
            "Copy full TXT value",
            "Add TXT at selector._domainkey",
            "Confirm key not truncated",
            "Run DNS Preflight",
        ],
        "step_texts": [
            "Generate your DKIM key in your email provider's dashboard.",
            "Copy the full TXT record value — all of it, including the long p= string.",
            "Add the TXT record at [selector]._domainkey.yourdomain.com.",
            "Verify the full key is published — check it's not truncated.",
            "Run DNS Preflight to confirm DKIM pass and key strength.",
        ],
        "faqs": [
            (
                "What is a DKIM record?",
                "A TXT record that publishes your DKIM public key. Mail servers use it to verify your email signatures.",
            ),
            (
                "Where does the DKIM record go in DNS?",
                "At [selector]._domainkey.yourdomain.com — for example google._domainkey.yourdomain.com for Google Workspace.",
            ),
            (
                "What key size should I use?",
                "2048-bit minimum. 1024-bit is weak and should be rotated immediately. DNS Preflight shows your key strength.",
            ),
            (
                "Why does my DKIM record look wrong after adding it?",
                "Probably truncated by your DNS provider. DKIM keys are long — check that the full p= value is preserved in the record.",
            ),
            (
                "How do I verify my DKIM record works?",
                "Run DNS Preflight — it checks 14 common selectors and shows key strength for each one found.",
            ),
        ],
        "article": r"""
      <h2>What a DKIM record looks like</h2>
      <div class="dns-block">google._domainkey.yourdomain.com TXT
"v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA..."</div>
      <p><strong>Format:</strong> Name: <code>[selector]._domainkey.yourdomain.com</code> · Type: TXT · Value: <code>v=DKIM1; k=rsa; p=[public key]</code></p>

      <h2>The truncation trap</h2>
      <p>DKIM public keys are long. Some DNS providers split them incorrectly. The full key must be in one record. If it's split wrong, DKIM verification fails silently.</p>

      <div class="tool-cta">
        <p>Check DKIM selectors and strength</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/glossary/dkim/">DKIM</a> ·
        <a href="/fix/dkim/key-length/">DKIM key length</a> ·
        <a href="/error/dkim-signature-failed/">DKIM signature failed</a>
      </div>
""",
    }
)

# ——— Page 9: DMARC ———
_nav, _sch = bc2("DMARC Record Setup Guide", "dmarc-record")
PAGES.append(
    {
        "rel": "dmarc-record",
        "title": "DMARC Record — How to Add Your Policy and Start Getting Reports",
        "meta": "Add _dmarc TXT with p=none first, then tighten. Use DomainPreflight for policy checks and DMARC XML analyzer.",
        "h1": "DMARC Record Setup Guide",
        "subtitle": "A DMARC record sets your email authentication policy and tells receivers where to send failure reports. Here's how to add one, what each tag means, and the right rollout order to avoid blocking legitimate email.",
        "hero": "DNS guide",
        "bc_nav_segments": _nav,
        "bc_schema_trail": _sch,
        "howto_name": "Roll out DMARC safely",
        "howto_desc": "Start with monitoring, read reports, fix alignment, move to quarantine then reject, verify in DNS Preflight.",
        "step_names": [
            "Add _dmarc with p=none",
            "Wait and read reports",
            "Fix alignment failures",
            "Move to quarantine",
            "Monitor then reject",
            "Confirm policy in Preflight",
        ],
        "step_texts": [
            "Add _dmarc TXT record with p=none and rua= pointing to an email you check.",
            "Wait 2-4 weeks — read the aggregate reports.",
            "Fix any alignment failures shown in reports.",
            "Change to p=quarantine.",
            "Monitor for 1 week → change to p=reject.",
            "Run DNS Preflight to confirm new policy is live.",
        ],
        "faqs": [
            (
                "What is a DMARC record?",
                "A TXT record at _dmarc.yourdomain.com that sets your email authentication policy and enables aggregate reporting.",
            ),
            (
                "What is the minimum DMARC record?",
                "v=DMARC1; p=none — this is valid but provides no protection. Add rua= to get reports.",
            ),
            (
                "Will adding DMARC immediately block email?",
                "Only if you set p=reject from the start. Start with p=none — it monitors without affecting delivery.",
            ),
            (
                "How do I read DMARC reports?",
                "Use DomainPreflight DMARC Report Analyzer — paste the XML for a visual summary of passing and failing senders.",
            ),
            (
                "What is the pct= tag?",
                "Percentage of email to apply the policy to. pct=10 with p=quarantine affects 10% of failing emails — useful for gradual rollout.",
            ),
        ],
        "article": r"""
      <h2>DMARC record format</h2>
      <p><strong>Start here (monitoring only):</strong></p>
      <div class="dns-block">_dmarc.yourdomain.com TXT
"v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com"</div>
      <p><strong>After reviewing reports (partial enforcement):</strong></p>
      <div class="dns-block">"v=DMARC1; p=quarantine; pct=10; rua=mailto:dmarc@yourdomain.com"</div>
      <p><strong>Full enforcement:</strong></p>
      <div class="dns-block">"v=DMARC1; p=reject; rua=mailto:dmarc@yourdomain.com"</div>

      <h2>What each tag does</h2>
      <ul>
        <li><code>p=</code> — policy (none / quarantine / reject)</li>
        <li><code>rua=</code> — where to send aggregate reports</li>
        <li><code>pct=</code> — percentage of email to enforce on (gradual rollout)</li>
        <li><code>sp=</code> — policy for subdomains</li>
      </ul>

      <div class="tool-cta">
        <p>Check DMARC in DNS</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/glossary/dmarc/">DMARC</a> ·
        <a href="/glossary/dmarc-policy/">DMARC policy</a> ·
        <a href="/fix/dmarc/">DMARC fixes</a>
      </div>
""",
    }
)

# ——— Page 10: NS ———
_nav, _sch = bc2("NS Record — Nameserver Setup Guide", "ns-record")
PAGES.append(
    {
        "rel": "ns-record",
        "title": "NS Record — Nameserver Setup and Delegation",
        "meta": "NS records delegate DNS to your provider. Set at registrar. Plan 24-48h propagation for NS changes.",
        "h1": "NS Record — Nameserver Setup Guide",
        "subtitle": "NS records delegate your domain's DNS management to a specific DNS provider. They're set at your registrar and tell the internet which servers hold your DNS records. Changing them moves all your DNS.",
        "hero": "DNS guide",
        "bc_nav_segments": _nav,
        "bc_schema_trail": _sch,
        "howto_name": "Change nameservers at your registrar",
        "howto_desc": "Get NS from new DNS host, log into registrar, replace NS, wait for propagation.",
        "step_names": [
            "Get nameservers from DNS provider",
            "Log into registrar",
            "Find Custom Nameservers",
            "Replace NS with new values",
            "Wait 24-48 hours",
        ],
        "step_texts": [
            "Get the nameserver values from your new DNS provider.",
            "Log into your domain registrar.",
            "Find Custom Nameservers or DNS settings.",
            "Replace existing NS records with new values.",
            "Wait 24-48 hours — NS changes propagate slowly.",
        ],
        "faqs": [
            (
                "What is an NS record?",
                "A record that specifies which DNS servers are authoritative for your domain. Changed at your registrar.",
            ),
            (
                "How long do NS record changes take?",
                "24-48 hours. Slower than other DNS changes because registrars cache NS records longer.",
            ),
            (
                "Will changing NS records break my email?",
                "Temporarily — until the new DNS provider has all your records. Copy all existing DNS records to the new provider before switching NS.",
            ),
            (
                "Can I see my current NS records?",
                "Yes — run DomainPreflight Propagation checker and query NS type for your domain.",
            ),
            (
                "What if my NS records are wrong?",
                "Contact your registrar — NS records can only be changed there, not at the DNS provider level.",
            ),
        ],
        "article": r"""
      <h2>Example NS records</h2>
      <h3>Cloudflare</h3>
      <div class="dns-block">@ NS ns1.cloudflare.com
@ NS ns2.cloudflare.com</div>
      <h3>Route 53</h3>
      <div class="dns-block">@ NS ns-123.awsdns-45.com
@ NS ns-456.awsdns-67.net
@ NS ns-789.awsdns-89.org
@ NS ns-012.awsdns-01.co.uk</div>

      <h2>Key point</h2>
      <p>NS records are set at your registrar (Namecheap, GoDaddy, etc.) — not at your DNS provider. Changing NS records can take 24-48 hours and affects all DNS.</p>

      <div class="tool-cta">
        <p>Query NS across resolvers</p>
        <a href="https://domainpreflight.dev/propagation/">Open Propagation checker →</a>
      </div>
""",
    }
)

# ——— Page 11: Propagation hub ———
_nav, _sch = bc2("DNS Propagation", "propagation")
PAGES.append(
    {
        "rel": "propagation",
        "title": "DNS Propagation — How Long It Takes and How to Check It",
        "meta": "DNS changes spread as caches expire. Check Propagation checker for five resolvers at once. NS changes are slowest.",
        "h1": "DNS Propagation — How to Check If Your Changes Are Live",
        "subtitle": "DNS propagation is the time it takes for a DNS change to spread across the internet's resolvers. Most changes take minutes to hours — but some can take up to 48 hours. Here's how to check propagation status in real time.",
        "hero": "DNS guide",
        "bc_nav_segments": _nav,
        "bc_schema_trail": _sch,
        "howto_name": "Check DNS propagation after a change",
        "howto_desc": "Lower TTL before changes when possible, run Propagation checker, select record type, poll until all resolvers match.",
        "step_names": [
            "Make your DNS change",
            "Lower TTL before changes",
            "Run Propagation checker",
            "Select record type",
            "Poll until all resolvers match",
        ],
        "step_texts": [
            "Make your DNS change.",
            "Lower TTL to 300 seconds BEFORE making changes (if possible).",
            "After making the change, run Propagation checker immediately.",
            "Select the record type you changed.",
            "Check every 15-30 minutes until all five resolvers show the new record.",
        ],
        "faqs": [
            (
                "How long does DNS propagation take?",
                "Most changes: minutes to 4 hours. NS record changes: up to 48 hours. Lower your TTL before changing to speed it up.",
            ),
            (
                "Why does my DNS change show for me but not others?",
                "Different resolvers have different caches. Your ISP's resolver may have already updated while others haven't.",
            ),
            (
                "How do I speed up DNS propagation?",
                "Lower your TTL to 300 seconds (5 min) before making changes. After the change is live everywhere, raise TTL back to 3600.",
            ),
            (
                "How do I check if my DNS has propagated?",
                "Use DomainPreflight Propagation checker — it queries five different resolvers simultaneously and shows each result.",
            ),
            (
                "Is propagation complete when DomainPreflight shows all five green?",
                "That means the five major resolvers (Cloudflare, Google) have updated. Other resolvers worldwide may take longer but these cover the majority.",
            ),
        ],
        "article": r"""
      <h2>Why propagation takes time</h2>
      <p>DNS resolvers cache records for a period defined by the TTL (Time To Live) value. Until the cache expires, resolvers serve the old record. Lower TTL = faster propagation.</p>

      <h2>Typical propagation times</h2>
      <div class="dns-block">A record:     minutes to 4 hours
MX record:    1-4 hours
TXT record:   minutes to 4 hours
CNAME:        minutes to 4 hours
NS record:    24-48 hours (slowest)</div>

      <h2>How to check</h2>
      <p>Use DomainPreflight Propagation checker — enter your domain, select record type, see live results from five resolvers simultaneously.</p>

      <div class="tool-cta">
        <p>Check propagation now</p>
        <a href="https://domainpreflight.dev/propagation/">Open Propagation checker →</a>
      </div>
""",
    }
)


# ——— Page 12: A propagation ———
_nav, _sch = bc_prop("A Record Propagation", "propagation/a-record")
PAGES.append(
    {
        "rel": "propagation/a-record",
        "title": "A Record Propagation — How Long It Takes",
        "meta": "A record changes usually propagate in minutes to a few hours. TTL and caching explain the rest.",
        "h1": "A Record Propagation — How Long It Takes",
        "subtitle": "A record changes typically propagate in minutes to 4 hours. Here's what affects propagation speed and how to check.",
        "hero": "Propagation",
        "bc_nav_segments": _nav,
        "bc_schema_trail": _sch,
        "howto_name": "Track A record propagation",
        "howto_desc": "Understand TTL, expect typical windows, use Propagation checker, troubleshoot stuck caches.",
        "step_names": [
            "Note your old TTL",
            "Make the A change",
            "Run Propagation checker",
            "Compare all five resolvers",
            "Retry if caches linger",
        ],
        "step_texts": [
            "Before changing, note TTL — lower TTL speeds the next change.",
            "Publish the new A record at your DNS host.",
            "Open Propagation checker and select A.",
            "Wait until every resolver shows the new IP.",
            "If stuck, try another network or flush local DNS — Propagation shows authoritative state.",
        ],
        "faqs": [
            (
                "How long does A record propagation usually take?",
                "Minutes to four hours for most resolvers. NS or registrar issues can stretch longer.",
            ),
            (
                "How does TTL affect A record propagation?",
                "Resolvers keep the old answer until TTL expires. Lower TTL before a planned change so caches refresh faster.",
            ),
            (
                "Why do some resolvers lag behind others?",
                "Each resolver has its own cache and clock. Geographic and ISP differences are normal.",
            ),
            (
                "Does Cloudflare proxy vs DNS-only change propagation?",
                "Proxy only affects traffic path to Cloudflare — for raw DNS answers at your authoritative zone, still watch TTL and resolver cache.",
            ),
            (
                "How do I verify A propagation step by step?",
                "Use DomainPreflight Propagation — pick A, enter the hostname, confirm all five resolvers return the new IPv4.",
            ),
        ],
        "article": r"""
      <h2>What drives wait time</h2>
      <p>TTL tells resolvers how long they may cache your A record. Until it expires, some users still see the old IP — even when your authoritative DNS is already correct.</p>

      <h2>Typical timeline</h2>
      <p>Most A updates show up across major public resolvers within minutes to a few hours. Edge cases (stubborn caches, old TTL) can take longer.</p>

      <h2>If it looks stuck</h2>
      <p>Confirm the authoritative zone has the new record, then re-check Propagation. Try a different network or device to rule out local cache.</p>

      <div class="tool-cta">
        <p>Check A record propagation</p>
        <a href="https://domainpreflight.dev/propagation/">Open Propagation checker →</a>
      </div>
""",
    }
)

# ——— Page 13: MX propagation ———
_nav, _sch = bc_prop("MX Record Propagation", "propagation/mx-record")
PAGES.append(
    {
        "rel": "propagation/mx-record",
        "title": "MX Record Propagation — How Long It Takes",
        "meta": "MX changes often take 1-4 hours. Email may queue on old paths until caches refresh.",
        "h1": "MX Record Propagation — How Long It Takes",
        "subtitle": "MX record changes take 1-4 hours on average. Email delivery uses the old server until propagation completes — here's how to minimise disruption.",
        "hero": "Propagation",
        "bc_nav_segments": _nav,
        "bc_schema_trail": _sch,
        "howto_name": "Track MX record propagation",
        "howto_desc": "Plan the cutover, watch TTL, verify MX on all resolvers, understand queuing during change.",
        "step_names": [
            "Lower TTL ahead of time",
            "Publish new MX set",
            "Run Propagation for MX",
            "Confirm all priorities",
            "Watch inbound mail queues",
        ],
        "step_texts": [
            "If your DNS host allows it, drop TTL a day before the migration.",
            "Replace MX records with your provider's exact hostnames and priorities.",
            "Use Propagation checker with type MX and your apex domain.",
            "Ensure every resolver lists the same mail hosts and preference order.",
            "Senders may still use cached MX briefly — most queues retry automatically.",
        ],
        "faqs": [
            (
                "How long does MX propagation usually take?",
                "Often one to four hours; worst case up to 48 hours if TTLs were high or NS paths are involved.",
            ),
            (
                "What happens to email during MX changes?",
                "Sending servers cache MX. Until their cache expires, they may deliver to the previous mail infrastructure — queues usually retry.",
            ),
            (
                "Should I change TTL before switching MX?",
                "Yes — lower TTL first so resolver caches refresh faster after you publish new MX records.",
            ),
            (
                "How do I verify MX propagation?",
                "DomainPreflight Propagation — select MX, enter your domain, wait until all five resolvers match.",
            ),
            (
                "What if the old server still receives mail?",
                "Residual cache. Verify authoritative DNS, wait for TTL, check Propagation again — most stragglers clear within hours.",
            ),
        ],
        "article": r"""
      <h2>Email during propagation</h2>
      <p>MX is cached like any record. Senders don't all flip at once — that's normal. Good providers queue and retry.</p>

      <h2>TTL strategy</h2>
      <p>Lower TTL before the change. After everyone sees the new MX, you can raise TTL again for stability.</p>

      <div class="tool-cta">
        <p>Check MX propagation</p>
        <a href="https://domainpreflight.dev/propagation/">Open Propagation checker →</a>
      </div>
      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/dns/mx-record/">MX record setup guide</a>
      </div>
""",
    }
)

# ——— Page 14: TXT propagation ———
_nav, _sch = bc_prop("TXT Record Propagation", "propagation/txt-record")
PAGES.append(
    {
        "rel": "propagation/txt-record",
        "title": "TXT Record Propagation — SPF, DKIM, DMARC",
        "meta": "SPF, DKIM, and DMARC TXT records usually propagate in minutes to hours. Verify with Preflight and Propagation.",
        "h1": "TXT Record Propagation — SPF, DKIM, DMARC",
        "subtitle": "TXT record changes for SPF, DKIM, and DMARC typically propagate in minutes to 4 hours. Here's how to verify your email authentication records are live.",
        "hero": "Propagation",
        "bc_nav_segments": _nav,
        "bc_schema_trail": _sch,
        "howto_name": "Verify TXT propagation for email auth",
        "howto_desc": "Know record sensitivity, check SPF/DKIM/DMARC separately, combine DNS Preflight and Propagation.",
        "step_names": [
            "Publish one SPF change at a time",
            "Wait for TXT cache refresh",
            "Query TXT in Propagation",
            "Run DNS Preflight for auth",
            "Re-test sending mail",
        ],
        "step_texts": [
            "Avoid duplicate SPF — merge into a single v=spf1 TXT before expecting clean results.",
            "Give resolvers time; TXT TTL governs cache age.",
            "Use Propagation with type TXT on @ or _dmarc as needed.",
            "DNS Preflight validates SPF/DKIM/DMARC logic after DNS answers match.",
            "Send a test message and check headers once tools show green.",
        ],
        "faqs": [
            (
                "How long do TXT records take to propagate?",
                "Usually minutes to four hours for common public resolvers — same ballpark as other non-NS records.",
            ),
            (
                "Does email break while SPF TXT is propagating?",
                "Receivers may see mixed old/new SPF during cache overlap. Minimise TTL before changes and avoid duplicate SPF records.",
            ),
            (
                "How do I know DKIM TXT is live everywhere?",
                "Propagation for the DKIM host (selector._domainkey) plus DNS Preflight to confirm the key verifies.",
            ),
            (
                "How fast does DMARC at _dmarc update?",
                "Same TXT rules — check the _dmarc hostname in Propagation, then read aggregate reports after policy changes.",
            ),
            (
                "Which tools should I use together?",
                "Propagation for raw DNS agreement across resolvers; DNS Preflight for authentication semantics and alignment.",
            ),
        ],
        "article": r"""
      <h2>Different TXT, different sensitivity</h2>
      <p>SPF at apex, DKIM on _domainkey hosts, DMARC on <code>_dmarc</code> — each hostname caches independently.</p>

      <h2>SPF during propagation</h2>
      <p>Never publish two SPF TXT records. While caches mix, receivers can still PermError — merge first, then verify.</p>

      <h2>Verify end-to-end</h2>
      <p>Use Propagation for visibility across resolvers, then DNS Preflight for SPF/DKIM/DMARC checks against your live answers.</p>

      <div class="tool-cta">
        <p>Check TXT propagation</p>
        <a href="https://domainpreflight.dev/propagation/">Open Propagation checker →</a>
      </div>
      <div class="tool-cta">
        <p>Full auth check</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>
      <div class="glossary-links"><strong>Deep dives:</strong>
        <a href="/dns/spf-record/">SPF setup</a> ·
        <a href="/dns/dkim-record/">DKIM setup</a> ·
        <a href="/dns/dmarc-record/">DMARC setup</a>
      </div>
""",
    }
)

# ——— Page 15: CNAME propagation ———
_nav, _sch = bc_prop("CNAME Record Propagation", "propagation/cname")
PAGES.append(
    {
        "rel": "propagation/cname",
        "title": "CNAME Record Propagation — How Long It Takes",
        "meta": "CNAME updates usually propagate in minutes to hours. Long CNAME chains can add extra DNS hops.",
        "h1": "CNAME Record Propagation — How Long It Takes",
        "subtitle": "CNAME record changes propagate in minutes to 4 hours. Email provider CNAMEs for DKIM alignment take the same time — here's how to verify they're live.",
        "hero": "Propagation",
        "bc_nav_segments": _nav,
        "bc_schema_trail": _sch,
        "howto_name": "Track CNAME propagation for DKIM and apps",
        "howto_desc": "Publish CNAME, respect TTL, verify target in Propagation, understand chained lookups.",
        "step_names": [
            "Publish CNAME at subdomain",
            "Respect TTL between checks",
            "Run Propagation for CNAME",
            "Confirm final target host",
            "Retest DKIM after green",
        ],
        "step_texts": [
            "Add the CNAME on the exact host your provider lists (never at apex).",
            "Wait at least one TTL cycle before assuming failure.",
            "Select CNAME in Propagation and query the full hostname.",
            "Ensure the last hop in any chain matches the provider's current target.",
            "Send test mail and confirm DKIM passes once DNS converges.",
        ],
        "faqs": [
            (
                "How long does CNAME propagation take?",
                "Typically minutes to four hours on major resolvers — same class as A/TXT unless NS delegation is involved.",
            ),
            (
                "Do DKIM CNAMEs take longer?",
                "No special delay — they're normal CNAME RRs. The DKIM selector host must resolve everywhere receivers query.",
            ),
            (
                "How does TTL impact CNAME checks?",
                "Each resolver caches the CNAME answer for the TTL you set. Lower TTL before cutovers.",
            ),
            (
                "How do I verify a CNAME is live?",
                "Propagation checker with type CNAME on the full subdomain until all five resolvers show the expected target.",
            ),
            (
                "Can CNAME chains add delay?",
                "Extra hops mean more lookups, but propagation is still about cache expiry per label — watch TTL on each step.",
            ),
        ],
        "article": r"""
      <h2>CNAME for DKIM (SendGrid, M365, etc.)</h2>
      <p>Providers give you a host under your zone pointing at their rotating key. Your job is to publish the CNAME and wait for caches to agree.</p>

      <h2>TTL strategy</h2>
      <p>Lower TTL before you switch providers or selectors so the new target visible faster.</p>

      <h2>Chains</h2>
      <p>Some targets are themselves CNAMEs. All labels in the chain must resolve — if any hop is stale, DKIM can fail intermittently.</p>

      <div class="tool-cta">
        <p>Check CNAME propagation</p>
        <a href="https://domainpreflight.dev/propagation/">Open Propagation checker →</a>
      </div>
      <div class="glossary-links"><strong>Also read:</strong>
        <a href="/dns/cname-record/">CNAME setup guide</a> ·
        <a href="/fix/dmarc/sendgrid/">SendGrid DMARC fix</a>
      </div>
""",
    }
)
