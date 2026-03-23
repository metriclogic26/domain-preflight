"""Batch 4 glossary terms — slug, display name, opening definition, extra sections HTML, 3 FAQs."""
from __future__ import annotations

TERMS: list[dict] = [
    {
        "slug": "bounce-rate",
        "name": "Bounce Rate",
        "h1": "Bounce Rate — Hard vs Soft Bounces",
        "def_open": "Bounce rate is the percentage of emails that could not be delivered — split into hard bounces (permanent: bad address, domain doesn’t exist) and soft bounces (temporary: mailbox full, server timeout). High bounce rates damage sender reputation and can trigger blacklistings.",
        "extra": """      <h2>Why operators track it</h2>
      <p>Mailbox providers use bounce rate as a hygiene signal. A sudden spike in hard bounces often means a scraped or purchased list — not an accident.</p>
      <h2>What to do</h2>
      <p>Suppress hard-bounce addresses immediately. Retry soft bounces per ESP policy — then remove chronic soft bounces.</p>""",
        "faqs": [
            ("What is a hard bounce?", "A permanent failure — invalid recipient, unknown domain, or policy block. Remove the address from your list."),
            ("What is a soft bounce?", "Temporary — full mailbox, greylisting, or server busy. May retry; suppress if it persists."),
            ("How does bounce rate affect deliverability?", "High hard bounces hurt IP and domain reputation — receivers may throttle or block you."),
        ],
    },
    {
        "slug": "spam-trap",
        "name": "Spam Trap",
        "h1": "Spam Trap — Pristine and Recycled",
        "def_open": "A spam trap is an email address used to identify senders who use bad lists. Pristine traps were never real addresses — hitting one means you bought, scraped, or generated addresses. Recycled traps were once real addresses that bounced for years — mailing them means you didn’t process bounces. Both damage sender reputation.",
        "extra": """      <h2>How to avoid traps</h2>
      <p>Double opt-in, remove bounces, never buy lists. Traps are designed to catch bad actors — legitimate senders hit them only through hygiene failure.</p>""",
        "faqs": [
            ("What is a pristine spam trap?", "An address never used for real mail — any hit is a strong spam signal."),
            ("What is a recycled trap?", "An abandoned address that bounced long-term — then reactivated as a trap."),
            ("Will providers tell me which address was a trap?", "Usually not — you infer from sudden reputation drops and list audits."),
        ],
    },
    {
        "slug": "email-header",
        "name": "Email Header",
        "h1": "Email Header — Metadata Behind Every Message",
        "def_open": "Email headers are metadata attached to every message: delivery path, authentication results (SPF, DKIM, DMARC), timestamps, and Received hops. Recipients rarely see them — “Show original” in Gmail exposes the full chain.",
        "extra": """      <h2>What to look for</h2>
      <p><code>Authentication-Results</code>, <code>DKIM-Signature</code>, <code>Return-Path</code>, and <code>Received-SPF</code> tell you why mail passed or failed filters.</p>""",
        "faqs": [
            ("What header shows DMARC results?", "Often Authentication-Results at major providers — plus per-hop SPF/DKIM in chain."),
            ("Can headers be forged?", "Some fields can be spoofed — SPF/DKIM/DMARC exist to make spoofing detectable."),
            ("Where do I paste headers for analysis?", "DomainPreflight Email tool — or read raw in your client’s “Show original”."),
        ],
    },
    {
        "slug": "return-path",
        "name": "Return-Path",
        "h1": "Return-Path — The Envelope Sender",
        "def_open": "Return-Path is the envelope sender used for bounces — separate from the visible From: header. SPF checks the Return-Path domain (or HELO/EHLO context). DMARC alignment compares Return-Path domain to the From: domain for SPF alignment.",
        "extra": """      <h2>Why ESPs use their own domain</h2>
      <p>Many ESPs set Return-Path to bounce domains they control — so DKIM alignment to your brand domain becomes critical for DMARC.</p>""",
        "faqs": [
            ("Is Return-Path the same as From?", "No — From is what users see; Return-Path is the SMTP bounce address."),
            ("Why does SPF use Return-Path?", "SPF checks the envelope — not the header From:."),
            ("How do I align DMARC with ESP mail?", "SPF aligned Return-Path or DKIM d= aligned to From — see DMARC alignment."),
        ],
    },
    {
        "slug": "dkim-signature",
        "name": "DKIM Signature",
        "h1": "DKIM Signature Header",
        "def_open": "A DKIM signature is a cryptographic hash of the body and selected headers, signed with the sender’s private key. It appears in the DKIM-Signature header. Receivers verify using the public key at selector._domainkey.domain.",
        "extra": """      <h2>What breaks verification</h2>
      <p>Key rotation without DNS update, mailing lists that mutate content, or truncated DNS keys.</p>""",
        "faqs": [
            ("What is d= in DKIM-Signature?", "The signing domain — must align with From for DMARC (relaxed or strict)."),
            ("What is s=?", "The selector — points to DNS TXT at s._domainkey.d."),
            ("Can one message have multiple DKIM signatures?", "Yes — common when multiple systems touch the message."),
        ],
    },
    {
        "slug": "smtp",
        "name": "SMTP",
        "h1": "SMTP — Simple Mail Transfer Protocol",
        "def_open": "SMTP is the standard protocol for sending email between servers — typically port 25 for server-to-server relay and port 587 (or 465) for authenticated submission. SMTP alone does not authenticate senders — SPF, DKIM, and DMARC provide that layer.",
        "extra": """      <h2>Ports at a glance</h2>
      <p>25: MTA to MTA. 587: submission with STARTTLS. 465: implicit TLS (legacy). Blocking outbound 25 is common on consumer and some cloud networks.</p>""",
        "faqs": [
            ("Is SMTP encrypted?", "Often STARTTLS opportunistically — not required by the original protocol."),
            ("Who speaks SMTP?", "Your mail client to your provider; your provider to the recipient’s MX."),
            ("Does SMTP validate identity?", "No — that’s SPF/DKIM/DMARC on the message path."),
        ],
    },
    {
        "slug": "email-spoofing-vs-phishing",
        "name": "Email Spoofing vs Phishing",
        "h1": "Email Spoofing vs Phishing",
        "def_open": "Spoofing is forging the From: header (and related envelope data) to impersonate a domain. Phishing is using deceptive email to steal credentials or install malware. Spoofing is a technical technique; phishing is the attack goal. DMARC p=reject stops spoofing of your domain at participating receivers — it does not stop phishing from lookalike domains.",
        "extra": """      <h2>Defense in depth</h2>
      <p>Combine DMARC with typosquat monitoring, user training, and browser protections — lookalikes bypass your exact domain.</p>""",
        "faqs": [
            ("Does DMARC stop all phishing?", "No — only misaligned use of domains you control. Homoglyph domains need brand monitoring."),
            ("Can spoofing happen without phishing?", "Yes — spam and reputation attacks may spoof without credential forms."),
            ("What stops lookalike domains?", "Registration monitoring, Safe Browsing, and user awareness — not DMARC alone."),
        ],
    },
    {
        "slug": "dnsbl",
        "name": "DNSBL (DNS Blacklist)",
        "h1": "DNSBL — DNS-Based Blocklists",
        "def_open": "A DNSBL is a DNS-based blocklist: mail servers query a special DNS zone with a reversed IP embedded in the query. Example: for 1.2.3.4, query 4.3.2.1.zen.spamhaus.org — NXDOMAIN means not listed; an A record response means listed. Queries happen in real time during SMTP acceptance.",
        "extra": """      <h2>Delisting</h2>
      <p>Fix the cause (spam, compromised app, open relay) — then request delist per provider policy. Repeated listings hurt harder.</p>""",
        "faqs": [
            ("Are DNSBLs the same as SPF?", "No — DNSBL checks IP reputation; SPF checks authorised senders for a domain."),
            ("Why was my IP listed?", "Spam complaints, spam trap hits, compromised hosts, or neighbors on bad ranges."),
            ("How do I check listings?", "DNS Preflight Email tool and multi-DNSBL lookups."),
        ],
    },
    {
        "slug": "email-warm-up",
        "name": "Email Warm-Up",
        "h1": "Email Warm-Up",
        "def_open": "Email warm-up is gradually increasing send volume from a new IP address so mailbox providers build positive reputation instead of flagging a sudden spike as abuse. Cold IPs with high volume trigger spam filters — warm-up typically spans 2–4 weeks depending on engagement and list quality.",
        "extra": """      <h2>Practical pattern</h2>
      <p>Start with low daily volume to engaged recipients; double cadence only when bounces and complaints stay flat.</p>""",
        "faqs": [
            ("Do marketing automation tools replace warm-up?", "They schedule volume — they don’t replace good lists and PTR/auth hygiene."),
            ("Does shared ESP IP need warm-up?", "Usually no — ESP pools already carry reputation; dedicated IPs do."),
            ("What metrics matter during warm-up?", "Bounces, complaints, deferrals — stop ramping if they spike."),
        ],
    },
    {
        "slug": "list-unsubscribe",
        "name": "List-Unsubscribe Header",
        "h1": "List-Unsubscribe Header",
        "def_open": "The List-Unsubscribe header (RFC 2369, extended by RFC 8058) lets mail clients show an unsubscribe button next to the message. Bulk senders to Google and Yahoo require one-click unsubscribe support — List-Unsubscribe-Post enables one-click HTTP without a landing page in compliant clients.",
        "extra": """      <h2>Implementation</h2>
      <p>ESP dashboards often toggle this — your job is DNS/auth alignment for the sending domain, not the header syntax alone.</p>""",
        "faqs": [
            ("Is List-Unsubscribe required?", "For bulk marketing to major providers — yes, as part of bulk sender requirements."),
            ("What’s the difference between mailto and https?", "mailto: opens a client; https: + POST enables one-click in supporting clients."),
            ("Does unsubscribe affect deliverability?", "High complaint rates hurt — easy unsubscribe reduces “report spam” clicks."),
        ],
    },
    {
        "slug": "spf-alignment",
        "name": "SPF Alignment",
        "h1": "SPF Alignment (DMARC)",
        "def_open": "SPF alignment is the DMARC check that the Return-Path domain matches the From: header’s organizational domain. Relaxed alignment allows subdomain matches; strict requires exact host match. SPF alignment fails when ESPs use their own bounce domain unless you align via DKIM instead.",
        "extra": """      <h2>Typical fix</h2>
      <p>Branded bounce domains or DKIM d= aligned to your From domain — see <a href="/glossary/dkim-alignment/">DKIM alignment</a>.</p>""",
        "faqs": [
            ("Does SPF pass imply alignment?", "No — pass on the wrong domain still fails DMARC alignment."),
            ("What is relaxed vs strict?", "Controlled by aspf= in DMARC — relaxed is default for most setups."),
            ("Can I align SPF for all ESPs?", "Only if Return-Path is under your domain or you rely on DKIM alignment."),
        ],
    },
    {
        "slug": "dkim-alignment",
        "name": "DKIM Alignment",
        "h1": "DKIM Alignment (DMARC)",
        "def_open": "DKIM alignment verifies the d= domain in the DKIM-Signature matches the From: header’s organizational domain. Relaxed alignment allows subdomain relationships; strict requires exact match. Most ESPs achieve alignment via CNAME or TXT DKIM on your domain.",
        "extra": """      <h2>When DKIM saves DMARC</h2>
      <p>If Return-Path is on the ESP’s domain, aligned DKIM to your brand domain still satisfies DMARC when SPF alignment fails.</p>""",
        "faqs": [
            ("What if I have multiple DKIM signatures?", "DMARC can pass if any signature aligns — policy-dependent."),
            ("Does mailing list break DKIM?", "Often yes — body changes break the signature unless the list re-signs."),
            ("What is adkim=?", "DMARC tag for strict vs relaxed DKIM alignment."),
        ],
    },
    {
        "slug": "ip-reputation",
        "name": "IP Reputation",
        "h1": "IP Reputation",
        "def_open": "IP reputation is a trust score mailbox providers assign to a sending IP based on history: bounces, spam complaints, spam trap hits, and blocklist appearances. It affects delivery independently of domain reputation — a bad IP can drag down good domains.",
        "extra": """      <h2>Shared vs dedicated</h2>
      <p>Shared ESP pools share reputation — dedicated IPs start cold and need warm-up.</p>""",
        "faqs": [
            ("How is IP reputation different from domain reputation?", "IP is tied to the sending machine; domain is tied to From: and auth history."),
            ("Can I check IP reputation?", "Google Postmaster for Google; blocklist queries; provider dashboards."),
            ("Does IPv6 work the same?", "Yes — same concepts, ensure PTR and auth for the IP you actually send from."),
        ],
    },
    {
        "slug": "envelope-sender",
        "name": "Envelope Sender",
        "h1": "Envelope Sender (MAIL FROM)",
        "def_open": "The envelope sender is the address in the SMTP MAIL FROM command — also called Return-Path or bounce address. It is separate from the visible From: header. SPF validates against the envelope domain — DMARC alignment requires envelope domain to match From: for SPF alignment.",
        "extra": """      <h2>Why it confuses people</h2>
      <p>Users only see From: — receivers see both. Misalignment is invisible in the inbox until DMARC fails.</p>""",
        "faqs": [
            ("Where do I see envelope sender?", "In raw headers as Return-Path — often after delivery."),
            ("Can envelope and From differ?", "Yes — common for ESPs — that’s why DKIM alignment matters."),
            ("Does SRS change the envelope?", "Yes — forwarding can rewrite envelope for deliverability."),
        ],
    },
    {
        "slug": "feedback-loop",
        "name": "Feedback Loop (FBL)",
        "h1": "Feedback Loop (FBL)",
        "def_open": "A feedback loop is a service where mailbox providers forward spam complaints (FBL reports) to the sender when users click “Report spam.” Registered senders receive complaint notifications so they can remove complainers and fix content. FBLs reduce future reputation damage.",
        "extra": """      <h2>Signup</h2>
      <p>Major providers run FBL programs — usually via Postmaster tools or ESP integration. Not all mail generates FBL events.</p>""",
        "faqs": [
            ("Is FBL the same as DMARC rua?", "No — rua is aggregate auth; FBL is complaint forwarding."),
            ("What should I do with an FBL complaint?", "Remove the subscriber and review content/frequency."),
            ("Do all ISPs offer FBL?", "No — large ones often do; coverage varies by region."),
        ],
    },
]
