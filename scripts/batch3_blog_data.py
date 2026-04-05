"""Content for batch 3 blog posts — used by generate_batch3_blog.py."""
from __future__ import annotations

DATE = "2026-03-19"

# slug, title, meta, faqs (5), body_html (no FAQ section)
POSTS: list[dict] = [
    {
        "slug": "dmarc-reject-safe",
        "title": "When Is It Safe to Set DMARC to p=reject?",
        "meta": "You need clean aggregate reports for 2-4 weeks before p=reject is safe — here's exactly what to check.",
        "faqs": [
            ("How long should I wait before p=reject?", "At least 2-4 weeks of reports showing all legitimate mail aligned — longer if you have many ESPs."),
            ("What must be true in reports?", "No unexplained high-volume sources; SPF/DKIM pass and align for known senders."),
            ("Can I use pct to sample reject?", "Yes — pct=25 then ramp; reduces blast radius if something breaks."),
            ("What if marketing uses a new ESP mid-rollout?", "Pause policy changes until the new sender is aligned and visible in reports."),
            ("Where do I verify alignment?", "DomainPreflight DMARC Report Analyzer and DNS Preflight for live DNS."),
        ],
        "body": r"""
      <p>p=reject is the point where spoofed mail should stop reaching inboxes. It is also the point where a forgotten newsletter tool can silently die. Safety is a data problem — not a calendar problem.</p>
      <h2>What “clean” means</h2>
      <p>You want aggregate XML showing <strong>only</strong> sources you can explain: your MX, Google or Microsoft, each ESP, each app. Random ASNs with volume need investigation before reject.</p>
      <p>Alignment matters more than pass. SPF can pass for bounces.example.com while DMARC fails — fix Return-Path and DKIM until <a href="/glossary/dmarc-alignment/">alignment</a> holds. Read <a href="/learn/dmarc/">the DMARC guide</a> for the rollout ladder.</p>
      <h2>Minimum window</h2>
      <p>Two weeks is a floor for simple stacks. Four to eight weeks is normal for enterprises. Acquisitions and seasonal tools extend the window.</p>
      <h2>Rollback plan</h2>
      <p>Keep screenshots of your DMARC TXT. If reject causes legitimate loss, revert to quarantine or none, fix the sender, re-validate reports, then try again.</p>
      <div class="tool-cta"><p>Validate before you tighten</p><a href="https://domainpreflight.dev/dmarc/">DMARC Report Analyzer →</a></div>
""",
    },
    {
        "slug": "ptr-record-email-delivery",
        "title": "Why Your PTR Record Is Killing Your Email Delivery",
        "meta": "No PTR record = many mail servers reject you before checking SPF. Here's how to add one.",
        "faqs": [
            ("What is PTR?", "Reverse DNS: IP resolves to a hostname — filters expect it to match your sending identity."),
            ("Who sets PTR?", "Usually your hosting provider or ISP for the IP — not your domain registrar’s DNS."),
            ("Does SaaS mail need PTR?", "The ESP’s IPs are already configured — self-hosted and dedicated IPs need PTR most."),
            ("What is FCrDNS?", "Forward-confirmed reverse DNS: PTR hostname resolves back to the same IP."),
            ("How do I test?", "DNS Preflight checks PTR path; dig -x for the IP from your laptop."),
        ],
        "body": r"""
      <p>SPF and DKIM can pass — and mail still gets deferred or spam-foldered because the connecting IP has no PTR or a generic hostname. Many receivers treat that as sloppy or hostile.</p>
      <h2>What breaks</h2>
      <p>Self-hosted Postfix on a VPS: you need PTR pointing to <code>mail.example.com</code> and an A record back. Cloud IPs without PTR are a common “everything worked in Mailgun” moment when you migrate.</p>
      <p>See <a href="/glossary/ptr-record/">PTR</a> and <a href="/learn/self-hosted-email/">self-hosted email</a>.</p>
      <h2>Fix path</h2>
      <p>Open a ticket with whoever owns the IP (AWS, Hetzner, etc.). Set PTR to your mail hostname. Wait for propagation — then verify FCrDNS.</p>
<pre class="code-block">dig +short -x YOUR.SENDING.IP</pre>
      <div class="tool-cta"><p>Check PTR + blocklists</p><a href="https://domainpreflight.dev/">DNS Preflight →</a></div>
""",
    },
    {
        "slug": "dmarc-mailchimp-setup",
        "title": "How to Set Up DMARC Alignment for Mailchimp",
        "meta": "Mailchimp's domain verification is not the same as DMARC alignment — here's what's missing.",
        "faqs": [
            ("Does verifying my domain in Mailchimp equal DMARC pass?", "No — verification proves control of DNS; alignment still needs SPF/DKIM matching your From domain."),
            ("What record does Mailchimp need?", "Follow their wizard — usually SPF include and DKIM TXT/CNAME — merged into your single SPF."),
            ("Why dmarc=fail with green Mailchimp?", "From domain mismatch or Return-Path on a different domain — check Authentication-Results."),
            ("Where is Mailchimp Return-Path?", "Often on a Mailchimp bounce domain — DKIM d= must align to your brand domain."),
            ("What policy should I use?", "Start p=none with rua= — tighten after reports are clean."),
        ],
        "body": r"""
      <p>Mailchimp’s UI says “authenticated” — DMARC still fails if the <code>From:</code> domain does not align with SPF or DKIM per your relaxed/strict settings. Verification tokens and marketing alignment are different jobs.</p>
      <h2>What to publish</h2>
      <p>Merge <code>include:servers.mcsv.net</code> into one SPF. Complete DKIM keys Mailchimp shows. Publish DMARC at <code>_dmarc</code>. Use <a href="/email-providers/mailchimp/spf-setup/">Mailchimp SPF</a> and <a href="/email-providers/mailchimp/dkim-setup/">DKIM</a> pages.</p>
      <h2>Read the headers</h2>
      <p>Send a campaign to yourself. In “Show original,” confirm <code>spf=pass</code>, <code>dkim=pass</code>, and aligned domains. If not, fix DNS before blaming content.</p>
""",
    },
    {
        "slug": "spf-include-explained",
        "title": "SPF include: Explained — What It Does and When to Use It",
        "meta": "Every include: costs one DNS lookup. Here's what include: actually does and how to use it without hitting the limit.",
        "faqs": [
            ("Does include pull IPs automatically at send time?", "No — receivers resolve the included SPF record at lookup time; nested includes chain."),
            ("Why is nested include expensive?", "Each include: can add more lookups — SendGrid’s record includes more includes."),
            ("What is the limit?", "10 DNS lookups total for SPF evaluation — see the SPF lookup limit post on this blog."),
            ("Can I replace include with ip4?", "Yes — flattening — trades operational pain for fewer lookups."),
            ("How do I count?", "DNS Preflight SPF tree shows the running total."),
        ],
        "body": r"""
      <p><code>include:vendor.net</code> tells the receiver: “also evaluate that domain’s SPF.” It is indirection — not a magic CC list.</p>
      <h2>Lookup math</h2>
      <p>Each mechanism that triggers DNS counts. Nested includes multiply pain. That is why stacks with six SaaS tools blow past ten without anyone editing a character.</p>
<pre class="code-block">v=spf1 include:_spf.google.com include:sendgrid.net ~all</pre>
      <p>Learn more: <a href="/glossary/spf-record/">SPF record</a>, <a href="/learn/spf/">SPF guide</a>.</p>
""",
    },
    {
        "slug": "email-authentication-checklist",
        "title": "The Email Authentication Checklist — SPF, DKIM, DMARC Before You Send",
        "meta": "Five checks to run before sending from a new domain — and the order that matters.",
        "faqs": [
            ("What order should I fix things?", "SPF/DKIM first — then DMARC reporting — then policy."),
            ("Do I need all three?", "For modern inbox placement at scale — yes. DMARC can be p=none initially."),
            ("What tool runs the checks?", "<a href=\"https://domainpreflight.dev/\">DNS Preflight</a> for DNS-side authentication."),
            ("What about PTR?", "Required for dedicated/self-hosted IPs — less relevant for pure ESP sending."),
            ("How do I track drift?", "DMARC aggregate reports to rua= — see <a href=\"/learn/dmarc-reporting/\">reporting guide</a>."),
        ],
        "body": r"""
      <p>Order: <strong>inventory senders → publish SPF → enable DKIM → add DMARC p=none with rua → read reports → tighten</strong>. Skipping inventory means surprise sources when you go to quarantine.</p>
      <ol>
        <li>SPF: one TXT, under 10 lookups.</li>
        <li>DKIM: 2048-bit key live at selector._domainkey.</li>
        <li>DMARC: v=DMARC1; p=none; rua=mailto:you@domain.</li>
        <li>Test mail + headers.</li>
        <li>DMARC XML in inbox within 24-48h.</li>
      </ol>
      <p>Deep dives: <a href="/learn/dns-for-email/">DNS records for email</a>.</p>
""",
    },
    {
        "slug": "dmarc-subdomain-policy",
        "title": "DMARC Subdomain Policy (sp=) — When You Need It",
        "meta": "Your DMARC record covers your root domain — but what about mail.yourdomain.com? Here's when sp= matters.",
        "faqs": [
            ("What does sp= do?", "Sets policy for subdomains separately from the organizational domain’s p=."),
            ("When is it needed?", "When subdomains send mail with different risk — e.g. looser sandbox vs strict root."),
            ("Does the root DMARC apply to subdomains?", "Often by inheritance — sp= overrides subdomain policy explicitly."),
            ("Is strict alignment related?", "Separate — adkim/aspf control alignment strictness."),
            ("Example?", "v=DMARC1; p=reject; sp=quarantine for stricter root than marketing subdomains."),
        ],
        "body": r"""
      <p>Most teams only set <code>p=</code>. Subdomains that send mail (<code>mail.example.com</code>) inherit policy context — but acquisitions and marketing sandboxes sometimes need different enforcement.</p>
      <h2>When to set sp=</h2>
      <p>Use <code>sp=</code> when a subdomain is less trusted or still warming up — quarantine there while root is reject. Document the decision — future you will not remember why.</p>
      <p>Read <a href="/glossary/dmarc-policy/">DMARC policy</a> and <a href="/learn/dmarc/">DMARC setup</a>.</p>
""",
    },
    {
        "slug": "ip-warmup-guide",
        "title": "IP Warm-Up for New Sending IPs — The Right Way",
        "meta": "Sending high volume from a new IP immediately is the fastest way to get blacklisted. Here's the right warm-up approach.",
        "faqs": [
            ("How long does warm-up take?", "Often 2-4 weeks to stable reputation — varies by volume and list quality."),
            ("What volume day one?", "Start tiny — tens to low hundreds — double only when bounces and complaints stay low."),
            ("Does dedicated IP matter for ESPs?", "ESP shared pools already have reputation — dedicated IPs start cold."),
            ("What metrics watch?", "Bounce rate, spam complaints, deferrals — stop ramping if they spike."),
            ("PTR required?", "Yes for SMTP IPs — align with <a href=\"/blog/ptr-record-email-delivery/\">PTR guidance</a>."),
        ],
        "body": r"""
      <p>Cold IPs have no history — receivers assume worst. Volume spikes look like botnets. Warm-up is proving you are boring and legitimate.</p>
      <h2>Pattern</h2>
      <p>Day 1-3: seed inboxes + real engaged users. Ramp slowly. If metrics wobble, hold steady — do not “catch up” with a blast.</p>
      <p>Related: <a href="/learn/email-deliverability/">email deliverability</a> and <a href="/error/blacklisted-ip/">blacklisted IP</a>.</p>
""",
    },
    {
        "slug": "check-dmarc-from-terminal",
        "title": "How to Check DMARC, SPF, and DKIM from the Terminal",
        "meta": "dig and nslookup commands to verify your email authentication records without opening a browser.",
        "faqs": [
            ("Which record for DMARC?", "TXT at _dmarc.domain — dig TXT _dmarc.example.com +short"),
            ("SPF?", "TXT at apex or sending domain — often dig TXT example.com +short | grep spf"),
            ("DKIM without knowing selector?", "You must know selector — or use DNS Preflight’s probe — dig TXT selector._domainkey.example.com"),
            ("Why two answers?", "Split TXT strings — DNS concatenates; both are normal."),
            ("Faster than dig?", "DNS Preflight does it in the browser — <a href=\"https://domainpreflight.dev/\">open tool</a>."),
        ],
        "body": r"""
      <p>Quick checks from macOS/Linux — no dashboard, no cache confusion if you query authoritative NS.</p>
<pre class="code-block">dig TXT _dmarc.example.com +short
dig TXT example.com +short | grep spf
dig TXT google._domainkey.example.com +short</pre>
      <p>For recursive-only checks, specify <code>@1.1.1.1</code> or <code>@8.8.8.8</code>.</p>
""",
    },
    {
        "slug": "google-postmaster-tools",
        "title": "Google Postmaster Tools — What It Shows and How to Use It",
        "meta": "Postmaster Tools shows your domain and IP reputation at Google. Here's how to read it.",
        "faqs": [
            ("Do I need to verify?", "Yes — add DNS token or file to prove domain ownership."),
            ("What is IP reputation vs domain?", "IP history for your sending IPs vs authentication + spam rate for the domain."),
            ("Does it fix delivery?", "It diagnoses — fixes are still SPF/DKIM/DMARC and list hygiene."),
            ("Free?", "Yes for qualified senders — volume thresholds apply."),
            ("Yahoo equivalent?", "No single clone — use DMARC reports and seed inboxes."),
        ],
        "body": r"""
      <p>Postmaster is Google’s side of the story: authentication pass rates, encryption, spam rate — for domains you verify. It does not replace DMARC XML — it complements it.</p>
      <h2>What to watch</h2>
      <p>Sudden drops in domain reputation correlate with list purchases or auth breakage. Cross-check DNS changes with the timeline.</p>
""",
    },
    {
        "slug": "bulk-sender-requirements-2024",
        "title": "Bulk Sender Requirements in 2024 — Google, Yahoo, and What's Coming",
        "meta": "Both Google and Yahoo now require DMARC, SPF, DKIM, and unsubscribe compliance. Here's the full list.",
        "faqs": [
            ("Is p=none enough for DMARC?", "For many bulk requirements — yes — but you must publish a record and align mail."),
            ("List-Unsubscribe?", "One-click headers required for bulk — RFC 8058 style."),
            ("Spam rate threshold?", "Keep spam complaints low — check Postmaster and internal metrics."),
            ("Applies to small senders?", "Volume thresholds — transactional-only may differ — read current provider docs."),
            ("What about February 2024?", "That was the major deadline — requirements evolve — monitor Postmaster + Yahoo sender hub."),
        ],
        "body": r"""
      <p>2024 shifted “nice to have” to “blocked if missing” for high-volume senders: authenticate your domain, keep spam low, make unsub easy. The details moved twice — treat vendor blogs as source of truth.</p>
      <p>Your stack: <a href="/learn/email-deliverability/">deliverability guide</a>, <a href="/glossary/list-unsubscribe/">List-Unsubscribe</a> (glossary), DMARC aggregate monitoring.</p>
""",
    },
    {
        "slug": "dkim-rotation-guide",
        "title": "DKIM Key Rotation — How to Rotate Without Breaking Email",
        "meta": "Rotating DKIM keys without downtime requires publishing the new key before switching. Here's the exact sequence.",
        "faqs": [
            ("Publish new or delete old first?", "Publish new selector — overlap — then remove old after TTL + send volume."),
            ("How long overlap?", "Often 48-168 hours depending on mail volume and ESP defaults."),
            ("1024 to 2048?", "Generate 2048 — publish new selector — flip signing — retire 1024."),
            ("What if I delete old first?", "Instant dkim=fail for in-flight mail."),
            ("Where documented?", "<a href=\"/fix/dkim/rotate-keys/\">Rotate DKIM keys</a> fix page."),
        ],
        "body": r"""
      <p>Rotation is a two-key problem: receivers must find a valid key while signers might still use the old one for minutes.</p>
      <ol>
        <li>Create new selector in ESP / mail server.</li>
        <li>Publish new DNS TXT (or CNAME).</li>
        <li>Verify with dig / Preflight.</li>
        <li>Switch signing to new selector in app.</li>
        <li>Monitor — then remove old DNS.</li>
      </ol>
      <p><a href="/learn/dkim/">DKIM guide</a> · <a href="/fix/dkim/rotate-keys/">rotate fix</a></p>
""",
    },
    {
        "slug": "domain-registrar-comparison",
        "title": "Choosing a Domain Registrar for Email — What to Look For",
        "meta": "Not all registrars make DNS management easy. Here's what matters for email authentication setup.",
        "faqs": [
            ("API vs UI?", "If you automate DNS — API and audit logs matter."),
            ("DNS hosting included?", "Some registrars are terrible at TXT chunking — third-party DNS is OK."),
            ("WHOIS privacy?", "Most offer free privacy — reduces admin phishing."),
            ("Transfer lock?", "Enable by default — see <a href=\"/learn/domain-security/\">domain security</a>."),
            ("Expiry alerts?", "Auto-renew + calendar — expiry kills mail instantly."),
        ],
        "body": r"""
      <p>The registrar is not the mail server — but it is often where DNS lives. Painful TXT UIs mean slower DKIM rollout and more typos.</p>
      <h2>Checklist</h2>
      <ul>
        <li>Easy multi-string TXT entry</li>
        <li>Low TTL when you need fast rollback</li>
        <li>2FA on account</li>
        <li>Lock + auth code hygiene</li>
      </ul>
      <p>We also cover <a href="/registrar/">registrar hubs</a> for step-by-step SPF/DKIM per host.</p>
""",
    },
]
