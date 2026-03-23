"""Metadata, FAQs, and HowTo for learn/* guides. Bodies live in learn_guides_bodies."""
from __future__ import annotations

from learn_guides_bodies import BODIES

# Shared FAQ / HowTo builders — exact text matches user spec where provided.

_GUIDE_FAQS: dict[str, list[tuple[str, str]]] = {
    "dmarc": [
        (
            "What is DMARC?",
            "DMARC is an email authentication policy that tells receivers what to do with emails failing SPF and DKIM — monitor, quarantine, or reject them.",
        ),
        (
            "Do I need SPF and DKIM before setting up DMARC?",
            "Yes. DMARC builds on SPF and DKIM. Set up both first, then add DMARC to tie them together.",
        ),
        (
            "Will DMARC break my email?",
            "Not if you start with p=none. p=none monitors without affecting delivery. Only move to p=reject after confirming all senders are aligned.",
        ),
        (
            "How do I read DMARC reports?",
            "Use DomainPreflight DMARC Report Analyzer — paste the XML for a visual summary showing passing and failing senders.",
        ),
        (
            "How long does DMARC setup take?",
            "Adding the record takes 2 minutes. Safely reaching p=reject takes 4-8 weeks of monitoring reports and fixing alignment issues.",
        ),
    ],
    "spf": [
        (
            "What is an SPF record?",
            "A DNS TXT record that lists which servers are authorised to send email for your domain. Receivers check it to verify your email is legitimate.",
        ),
        (
            "How many DNS lookups can SPF use?",
            "Maximum 10. Exceeding this causes SPF PermError — receivers may reject your email. Use DomainPreflight to count your lookups.",
        ),
        (
            "Can I have two SPF records?",
            "No. Multiple TXT records starting with v=spf1 cause immediate PermError. Merge all senders into one record.",
        ),
        (
            "What does ~all mean?",
            "Softfail — unauthorised senders are marked suspicious but usually delivered. Start with ~all, move to -all once all senders are confirmed.",
        ),
        (
            "How do I add multiple email providers to SPF?",
            "Add all includes in a single TXT record: v=spf1 include:_spf.google.com include:sendgrid.net ~all. Watch the 10-lookup limit.",
        ),
    ],
    "dkim": [
        (
            "What is DKIM?",
            "An email authentication method that adds a digital signature to outgoing email. Receivers verify it using your public key in DNS.",
        ),
        (
            "What DKIM key size should I use?",
            "2048-bit minimum. 1024-bit is weak and should be rotated. DNS Preflight shows your current key strength.",
        ),
        (
            "What is a DKIM selector?",
            "A label identifying which DKIM key to use. Appears as s=[selector] in the DKIM-Signature header and must match a DNS TXT record.",
        ),
        (
            "How do I verify DKIM is working?",
            "Run DNS Preflight — it tries 14 common selectors and shows key strength for each one found.",
        ),
        (
            "Why does DKIM fail after working fine?",
            "Usually key rotation — old key in DNS, new key signing. Or message alteration by a mailing list. Check raw headers in DomainPreflight Email tool.",
        ),
    ],
    "email-deliverability": [
        (
            "What is email deliverability?",
            "The rate at which your emails reach the inbox rather than spam or being rejected. Determined by authentication, reputation, content, and engagement.",
        ),
        (
            "What is the difference between delivery and deliverability?",
            "Delivery means the email was accepted. Deliverability means it reached the inbox. An email can be delivered but still go to spam.",
        ),
        (
            "Why are my emails going to spam even though SPF and DKIM pass?",
            "Authentication passing is necessary but not sufficient. Check DMARC enforcement, IP reputation, PTR records, and content signals.",
        ),
        (
            "How do I check my email deliverability?",
            "Run DNS Preflight for authentication and DomainPreflight Email tool for IP reputation and blocklist checks.",
        ),
        (
            "How long does it take to improve deliverability?",
            "Authentication fixes take effect in 48 hours. Reputation takes weeks to months to rebuild. Start with authentication — it's the fastest win.",
        ),
    ],
    "dns-for-email": [
        (
            "What DNS records do I need for email?",
            "Five: MX (receive email), SPF (authorise senders), DKIM (sign messages), DMARC (enforce policy), and PTR (reverse DNS for your sending IP).",
        ),
        (
            "Which records are required vs optional?",
            "MX is required to receive email. SPF, DKIM, and DMARC are required for reliable delivery. PTR is required for self-hosted mail servers.",
        ),
        (
            "How do I check all my email DNS records at once?",
            "Run DNS Preflight — it checks all five in one pass with a health score.",
        ),
        (
            "Can I skip DMARC if I have SPF and DKIM?",
            "Not anymore. Google and Yahoo require DMARC for bulk senders. Even p=none is sufficient to meet the requirement.",
        ),
        (
            "What is the most important record to set up first?",
            "SPF — it's the fastest to add and blocks the most basic spoofing. Then DKIM, then DMARC.",
        ),
    ],
    "domain-security": [
        (
            "What is the biggest risk to my domain?",
            "Expiry — it takes down everything simultaneously and is completely preventable with auto-renew enabled.",
        ),
        (
            "What is domain transfer lock?",
            "A registrar setting that prevents your domain from being transferred without your explicit authorisation. Enable it and leave it on.",
        ),
        (
            "What does WHOIS privacy protect?",
            "Your personal name, address, phone, and email from being publicly visible in WHOIS lookups. Most registrars offer it free.",
        ),
        (
            "How do I check my domain expiry date?",
            "Run DomainPreflight WHOIS — shows exact expiry date, registrar, and risk tier.",
        ),
        (
            "What is an auth code?",
            "A code required to transfer your domain to another registrar. Keep it private — sharing it enables unauthorised transfers.",
        ),
    ],
    "subdomain-security": [
        (
            "What is subdomain takeover?",
            "When a CNAME points to a deleted external service, an attacker can claim that service and serve content on your subdomain.",
        ),
        (
            "Which cloud services are most vulnerable to subdomain takeover?",
            "GitHub Pages, AWS S3, Heroku, Netlify, and Azure are the most common targets.",
        ),
        (
            "How do I find my dangling DNS records?",
            "Run DomainPreflight Dangling Records — it discovers subdomains via certificate logs and checks each CNAME against known takeover fingerprints.",
        ),
        (
            "What should I do if I find a dangling record?",
            "Delete the DNS record immediately. If you still need the subdomain, recreate the service first.",
        ),
        (
            "How often should I audit my DNS for dangling records?",
            "Every 3-6 months, and every time you decommission a service or subdomain. Run Dangling Records as part of your offboarding checklist.",
        ),
    ],
    "dmarc-reporting": [
        (
            "What is a DMARC aggregate report?",
            "A daily XML file sent by major email providers showing every IP that sent email as your domain and whether SPF and DKIM passed.",
        ),
        (
            "How do I start receiving DMARC reports?",
            "Add rua=mailto:dmarc@yourdomain.com to your DMARC TXT record. Reports arrive within 24 hours.",
        ),
        (
            "How do I read DMARC XML reports?",
            "Use DomainPreflight DMARC Report Analyzer — paste the XML for a visual summary.",
        ),
        (
            "What should I do if I see a spoofing attempt in reports?",
            "Fix any alignment failures from legitimate senders first, then upgrade to p=reject to block spoofed email.",
        ),
        (
            "How long should I collect reports before upgrading to p=reject?",
            "Minimum 2-4 weeks of clean reports showing all legitimate senders aligned. Longer if you have complex email infrastructure.",
        ),
    ],
    "self-hosted-email": [
        (
            "What do I need for self-hosted email to reach inboxes?",
            "PTR record, SPF, DKIM, DMARC, and a clean sending IP. Miss any one and email lands in spam or gets rejected.",
        ),
        (
            "Which VPS providers allow port 25 for mail servers?",
            "Hetzner, DigitalOcean, Vultr, and Linode generally allow port 25. AWS and Google Cloud block it by default — requires a request to unblock.",
        ),
        (
            "How do I set up a PTR record for my mail server?",
            "In your hosting provider's control panel under Reverse DNS. Set it to your mail hostname and add a matching A record.",
        ),
        (
            "How do I warm up a new IP?",
            "Start with 50-100 emails/day. Double every few days if bounce rates stay low. Takes 2-4 weeks to build reputation.",
        ),
        (
            "How do I monitor my self-hosted mail server's reputation?",
            "Run DNS Preflight with your server's IP — checks PTR, blocklists, SPF, DKIM, and DMARC in one pass.",
        ),
    ],
    "brand-protection": [
        (
            "How do I stop attackers from spoofing my domain?",
            "Set DMARC to p=reject with proper SPF and DKIM alignment. This blocks spoofed emails from reaching inboxes.",
        ),
        (
            "How do I find domains impersonating my brand?",
            "Run DomainPreflight Typosquat Monitor — checks 30-50 lookalike variants via live DNS.",
        ),
        (
            "Should I register lookalike domains defensively?",
            "For high-risk variants — yes. Homoglyphs and common TLD swaps are worth the $10-15/year registration cost.",
        ),
        (
            "How do I prevent subdomain takeover?",
            "Run Dangling Records regularly. Delete DNS records when decommissioning services. Never leave CNAMEs pointing to deleted services.",
        ),
        (
            "What is the minimum brand protection setup?",
            "DMARC p=reject, regular typosquat monitoring, and periodic dangling record scans — all three are free with DomainPreflight.",
        ),
    ],
}

_HOWTOS: dict[str, dict] = {
    "dmarc": {
        "name": "Roll out DMARC safely",
        "desc": "Verify SPF and DKIM, publish DMARC at p=none, read reports, fix alignment, then tighten policy to quarantine and reject.",
        "step_names": [
            "Verify SPF and DKIM for every sender",
            "Publish a p=none DMARC TXT at _dmarc",
            "Confirm aggregate reports arrive at rua=",
            "Triage reports and fix alignment failures",
            "Move to p=quarantine with optional pct sampling",
            "Reach p=reject after sustained clean reports",
        ],
        "step_texts": [
            "Inventory Google, Microsoft, ESPs, and apps. Resolve spf/dkim failures before relying on DMARC policy.",
            "Use v=DMARC1; p=none; rua=mailto:... and optional fo=1. Document the record and TTL.",
            "Inbox or alias must accept mail from major receivers. Unzip a sample report to confirm parsing.",
            "Use the DMARC Report Analyzer and /fix/dmarc/ guides. One sender at a time until aligned.",
            "Increase pct gradually or set full quarantine once stakeholders agree on rollback.",
            "Keep rua= active. Revisit if new vendors onboard or domains are acquired.",
        ],
    },
    "spf": {
        "name": "Build and validate an SPF record",
        "desc": "Authorise senders in one TXT record, stay under ten DNS lookups, and test before hardfail.",
        "step_names": [
            "List every system that sends mail as your domain",
            "Draft v=spf1 with includes and ip4/ip6 as needed",
            "Merge into a single TXT; remove duplicate v=spf1",
            "Count lookups with DNS Preflight SPF tree",
            "Publish and wait for TTL",
            "Send test mail and verify Authentication-Results",
        ],
        "step_texts": [
            "Mailboxes, marketing, support tools, billing — each may need an include or dedicated envelope domain.",
            "Example: v=spf1 include:_spf.google.com include:sendgrid.net ~all — adjust to your stack.",
            "Multiple SPF TXT strings at the same owner break SPF; consolidate.",
            "Stay under 10 lookups to avoid PermError; trim unused vendors first.",
            "Query authoritative NS before declaring victory.",
            "Use headers or DNS Preflight to confirm spf=pass on each path.",
        ],
    },
    "dkim": {
        "name": "Publish and verify DKIM",
        "desc": "Generate a 2048-bit key, publish selector._domainkey TXT, verify signatures on live mail.",
        "step_names": [
            "Generate or export a 2048-bit key pair",
            "Choose a selector name for this key",
            "Publish the TXT at selector._domainkey",
            "Enable signing on the mail server or ESP",
            "Send a test message and read DKIM-Signature",
            "Confirm dkim=pass and align with DMARC",
        ],
        "step_texts": [
            "Use ESP UI or openssl — avoid 1024-bit for new deployments.",
            "Rotate by introducing selector2 while selector1 still verifies.",
            "Ensure the full p= base64 is present — truncation is a top failure mode.",
            "Match the selector in DNS to the s= value in headers.",
            "Confirm header exists and d= matches your branding domain.",
            "Layer DMARC to enforce alignment once signatures are stable.",
        ],
    },
    "email-deliverability": {
        "name": "Diagnose deliverability issues",
        "desc": "Check authentication first, then reputation, content, and engagement in that order.",
        "step_names": [
            "Run DNS Preflight on the sending domain",
            "Fix SPF, DKIM, DMARC failures and alignment",
            "Check IP reputation and blocklists",
            "Review content and link patterns",
            "Measure engagement and complaints",
            "Re-test with a small cohort before scaling",
        ],
        "step_texts": [
            "Capture baseline auth results before changing ESP settings.",
            "Use /learn/ guides for each protocol until reports are clean.",
            "Use the Email tool for IP signals if you send from dedicated IPs.",
            "Reduce URL shorteners and heavy attachments when filters bite.",
            "Suppress chronic non-openers and honour unsubscribes.",
            "Seed inboxes across providers to validate placement improvements.",
        ],
    },
    "dns-for-email": {
        "name": "Verify the five email DNS records",
        "desc": "Check MX, SPF, DKIM, DMARC, and PTR together so nothing hides in silos.",
        "step_names": [
            "Confirm MX points to live mail hosts",
            "Validate SPF TXT and lookup count",
            "Locate DKIM selectors and key strength",
            "Read DMARC policy and rua mailbox",
            "Check PTR for outbound sending IPs",
            "Run DNS Preflight for a combined health view",
        ],
        "step_texts": [
            "Test SMTP connectivity if you recently migrated.",
            "Single SPF string, under ten lookups.",
            "Match active selectors to your ESP documentation.",
            "Start at p=none if you are still aligning senders.",
            "Forward and reverse must agree for self-hosted SMTP.",
            "One dashboard beats five browser tabs during incidents.",
        ],
    },
    "domain-security": {
        "name": "Harden domain registration",
        "desc": "Enable renewals, transfer lock, privacy, and monitor expiry with WHOIS.",
        "step_names": [
            "Enable auto-renew and valid payment method",
            "Turn on registrar transfer lock",
            "Enable WHOIS privacy / redaction",
            "Protect auth codes like passwords",
            "Calendar external reminders before expiry",
            "Run DomainPreflight WHOIS on critical domains",
        ],
        "step_texts": [
            "Expiry takes DNS and mail offline — fix this first.",
            "Unlock only during intentional transfers.",
            "Reduces phishing against admins listed in WHOIS.",
            "Never paste codes into chat or unverified tickets.",
            "Registry reminders sometimes fail — own the date.",
            "Snapshot registrar, dates, and nameservers quarterly.",
        ],
    },
    "subdomain-security": {
        "name": "Find and remove dangling records",
        "desc": "Discover subdomains, inspect CNAME targets, delete or repoint risky records.",
        "step_names": [
            "Inventory subdomains from CT logs and configs",
            "Run Dangling Records for automated checks",
            "For each CNAME, confirm the target service is live and owned",
            "Delete DNS for decommissioned SaaS",
            "Re-create service before re-pointing if still needed",
            "Add a deprovisioning checklist to change management",
        ],
        "step_texts": [
            "Old marketing sites and POC apps are common culprits.",
            "Fingerprint known takeover patterns quickly.",
            "If NXDOMAIN or unclaimed bucket — you are exposed.",
            "Removing the CNAME removes attacker control.",
            "Avoid pointing names at resources you cannot claim.",
            "Quarterly audits catch drift between teams.",
        ],
    },
    "dmarc-reporting": {
        "name": "Operationalise DMARC aggregate reports",
        "desc": "Receive XML, parse with tooling, triage sources, then act on alignment and policy.",
        "step_names": [
            "Add rua= to your DMARC record",
            "Confirm gzip/XML attachments arrive",
            "Paste samples into the DMARC Report Analyzer",
            "Label each source IP as legit or suspicious",
            "Fix alignment for legitimate senders",
            "Adjust p= and pct based on clean data",
        ],
        "step_texts": [
            "Dedicated mailbox or alias — not a person who deletes attachments.",
            "Some providers batch daily; patience on day one.",
            "Tables beat raw XML for leadership updates.",
            "ASN and country often hint at ESP vs abuse.",
            "Use /fix/dmarc/ when a vendor misconfigures DKIM.",
            "Never jump to reject without this feedback loop.",
        ],
    },
    "self-hosted-email": {
        "name": "Stand up self-hosted SMTP with auth",
        "desc": "Set PTR, SPF, DKIM, DMARC, warm the IP, and monitor blocklists.",
        "step_names": [
            "Confirm outbound port 25 policy with your host",
            "Set PTR to your mail hostname and matching A record",
            "Publish SPF with your sending IP and relays",
            "Install DKIM signing (OpenDKIM/rspamd) and publish TXT",
            "Add DMARC p=none with rua=",
            "Warm IP volume and watch DMARC + blocklists",
        ],
        "step_texts": [
            "Without port 25 or relay, you are blocked before DNS matters.",
            "PTR mismatch is an instant spam signal.",
            "Include smart hosts if you relay outbound.",
            "2048-bit keys and documented selectors reduce surprises.",
            "Same DMARC story as hosted mail — start monitoring.",
            "Increase volume only when bounces and complaints stay low.",
        ],
    },
    "brand-protection": {
        "name": "Run a minimal brand protection program",
        "desc": "Enforce DMARC, monitor typosquats, scan dangling DNS, and keep WHOIS private.",
        "step_names": [
            "Reach DMARC p=reject with aligned SPF/DKIM",
            "Run Typosquat Monitor monthly",
            "Register critical homoglyph domains defensively",
            "Run Dangling Records after infra changes",
            "Enable WHOIS privacy on admin contacts",
            "Document owners and review quarterly",
        ],
        "step_texts": [
            "Stops naive spoofing at major receivers.",
            "Live DNS shows what attackers already registered.",
            "Cheap insurance for high-risk brands.",
            "Subdomain takeover abuses trust in your namespace.",
            "Shrinks social-engineering surface against teams.",
            "Security is a process — not a one-time checkbox.",
        ],
    },
}

_META: dict[str, tuple[str, str, str]] = {
    "dmarc": (
        "DMARC — The Complete Setup Guide",
        "How to Set Up DMARC: The Complete Guide",
        "DMARC tells receiving servers what to do when email fails authentication — monitor, quarantine, or reject. This guide covers everything from adding your first record to reaching p=reject safely.",
    ),
    "spf": (
        "SPF Record — The Complete Setup Guide",
        "How to Set Up an SPF Record: The Complete Guide",
        "SPF lists the servers authorised to send email for your domain. One wrong character or one too many includes breaks it silently. This guide covers building, testing, and maintaining your SPF record.",
    ),
    "dkim": (
        "DKIM — The Complete Setup Guide",
        "How to Set Up DKIM: The Complete Guide",
        "DKIM adds a cryptographic signature to every email you send. Receivers use your public key in DNS to verify the signature. This guide covers generating keys, publishing records, and troubleshooting common failures.",
    ),
    "email-deliverability": (
        "Email Deliverability — The Complete Guide",
        "Email Deliverability: Everything That Affects Whether Your Email Reaches the Inbox",
        "Email deliverability is not one thing — it's a stack of signals. Authentication, reputation, content, and engagement all play a role. This guide covers every layer and what to check when email starts going to spam.",
    ),
    "dns-for-email": (
        "DNS Records Every Email Sender Needs",
        "DNS Records Every Email Sender Needs",
        "Five DNS records control whether your email gets delivered. Miss one and email silently fails — often in ways that are hard to diagnose. Here's what each record does and how to verify it's correct.",
    ),
    "domain-security": (
        "Domain Security — Expiry, Registrar Lock, and WHOIS",
        "Domain Security: Expiry, Locks, and WHOIS Privacy",
        "Your domain is the foundation of your email, website, and every DNS-dependent service. Losing it — through expiry, hijacking, or transfer fraud — takes everything down simultaneously. Here's how to protect it.",
    ),
    "subdomain-security": (
        "Subdomain Security — Dangling Records and Takeover Prevention",
        "Subdomain Security: Dangling Records and Takeover Prevention",
        "Every subdomain you've ever created is a potential attack surface if you didn't clean up the DNS when you were done. Here's how subdomain takeover works, which services are vulnerable, and how to find your exposure.",
    ),
    "dmarc-reporting": (
        "DMARC Reporting — How to Use Aggregate Reports",
        "DMARC Reporting: How to Get, Read, and Act on Aggregate Reports",
        "DMARC aggregate reports are the most underused tool in email security. They show exactly who is sending email as your domain — legitimate senders and attackers alike. Here's how to use them.",
    ),
    "self-hosted-email": (
        "Self-Hosted Email Authentication — The Complete Guide",
        "Self-Hosted Email: SPF, DKIM, DMARC, and PTR Setup",
        "Running your own mail server is harder than it used to be. ISPs block port 25, major providers require PTR records, and DMARC is now mandatory for reliable delivery. This guide covers everything self-hosters need to configure.",
    ),
    "brand-protection": (
        "Email Brand Protection — DMARC, Typosquatting, and Domain Security",
        "Email Brand Protection: DMARC, Typosquats, and Subdomain Security",
        "Your domain is your brand's most important asset online. Attackers can spoof it for phishing, register lookalike domains, or take over subdomains. Here's how to protect all three attack surfaces.",
    ),
}

_SLUGS_ORDER = [
    "dmarc",
    "spf",
    "dkim",
    "email-deliverability",
    "dns-for-email",
    "domain-security",
    "subdomain-security",
    "dmarc-reporting",
    "self-hosted-email",
    "brand-protection",
]

_BREADCRUMB_LABELS = {
    "email-deliverability": "Email deliverability",
    "dns-for-email": "DNS records for email",
    "domain-security": "Domain security",
    "subdomain-security": "Subdomain security",
    "dmarc-reporting": "DMARC reporting",
    "self-hosted-email": "Self-hosted email",
    "brand-protection": "Brand protection",
}

_META_DESC = {
    "dmarc": "Complete DMARC setup: SPF, DKIM, first record, aggregate reports, alignment fixes, and a safe path from p=none to p=reject.",
    "spf": "Build a valid SPF record, stay under the 10-lookup limit, fix PermError, and test with DNS Preflight.",
    "dkim": "Generate 2048-bit DKIM keys, publish selector DNS, verify signatures, rotate safely, and pair with DMARC.",
    "email-deliverability": "Authentication, reputation, content, and engagement — how to diagnose inbox placement and fix root causes.",
    "dns-for-email": "MX, SPF, DKIM, DMARC, and PTR — what each record does and how to verify them together.",
    "domain-security": "Auto-renew, transfer lock, WHOIS privacy, auth codes, and monitoring to prevent loss or hijack.",
    "subdomain-security": "Dangling CNAMEs, takeover mechanics, cloud targets, and how to find and delete risky records.",
    "dmarc-reporting": "rua mailboxes, XML structure, triage with the Report Analyzer, and when to tighten DMARC policy.",
    "self-hosted-email": "PTR, SPF, DKIM, DMARC, IP warm-up, and monitoring for self-hosted MTAs in 2026.",
    "brand-protection": "DMARC enforcement, typosquat monitoring, dangling DNS, and a practical monthly checklist.",
}


def _build_guide(slug: str) -> dict:
    title, h1, subtitle = _META[slug]
    howto = _HOWTOS[slug]
    return {
        "slug": slug,
        "title": title,
        "h1": h1,
        "meta": _META_DESC[slug],
        "subtitle": subtitle,
        "breadcrumb_label": _BREADCRUMB_LABELS.get(slug, title.split("—")[0].strip()),
        "body": BODIES[slug],
        "faqs": _GUIDE_FAQS[slug],
        "howto": {
            "name": howto["name"],
            "desc": howto["desc"],
            "step_names": howto["step_names"],
            "step_texts": howto["step_texts"],
        },
    }


GUIDES: list[dict] = [_build_guide(s) for s in _SLUGS_ORDER]
