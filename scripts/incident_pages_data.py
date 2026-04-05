# -*- coding: utf-8 -*-
"""Incident page definitions for generate_incident_pages.py."""

INCIDENTS: list[dict] = [
    {
        "slug": "google-dmarc-enforcement-2024",
        "title": "Google and Yahoo DMARC Enforcement — February 2024",
        "meta": "In Feb 2024 Google and Yahoo began enforcing DMARC, SPF, and DKIM for bulk senders — 550 5.7.26 bounces spiked worldwide.",
        "h1": "Google and Yahoo DMARC Enforcement: What Changed in February 2024",
        "subtitle": "In February 2024, Google and Yahoo began rejecting bulk email from senders without DMARC, SPF, and DKIM properly configured. This was the biggest change to email deliverability in years — and it caught thousands of senders off guard.",
        "breadcrumb_label": "Google & Yahoo DMARC (2024)",
        "body": r"""
      <p>In February 2024, Google and Yahoo turned on strict authentication for bulk traffic to their users — and overnight, senders without DMARC (and aligned SPF/DKIM) started seeing hard bounces and spam placement at scale. If you send marketing or transactional mail at volume, this was the line in the sand.</p>

      <h2>What happened</h2>
      <p>Google and Yahoo announced new requirements for bulk senders (5,000+ emails/day to Gmail):</p>
      <ol>
        <li>Valid SPF or DKIM authentication required</li>
        <li>DMARC record required (p=none is sufficient)</li>
        <li>One-click unsubscribe required for marketing email</li>
        <li>Spam rate must stay below 0.3%</li>
      </ol>
      <p>The deadline was February 1, 2024. Senders who didn't comply saw emails rejected or routed to spam.</p>

      <h2>Why it mattered</h2>
      <p>Before this, many businesses sent email with no DMARC record and minimal SPF configuration. It worked because major providers were lenient. February 2024 ended that leniency. Google's <strong>550 5.7.26</strong> error code started appearing in bounce logs worldwide — "Unauthenticated email from [domain] is not accepted due to domain's DMARC policy."</p>

      <h2>Who was affected</h2>
      <ul>
        <li>Marketing platforms without domain authentication configured</li>
        <li>Transactional email senders without DMARC</li>
        <li>Self-hosted mail servers with weak SPF</li>
        <li>Anyone using shared hosting email with default configuration</li>
      </ul>

      <h2>The 5.7.26 error</h2>
      <div class="dns-block">550-5.7.26 This message does not have
authentication information or fails to
pass authentication checks. To best
protect our users from spam, the message
has been blocked.</div>
      <p>This error means no DMARC record exists or the DMARC record has no policy that satisfies Google's requirements.</p>

      <h2>What to do now</h2>
      <ol>
        <li>Add a DMARC record if you don't have one — even <code>p=none</code> satisfies Google's requirement</li>
        <li>Verify SPF covers all your sending IPs</li>
        <li>Enable DKIM for your sending domain</li>
        <li>Run DNS Preflight to check all three</li>
      </ol>
      <p>Minimum DMARC to satisfy Google:</p>
      <div class="dns-block">_dmarc TXT "v=DMARC1; p=none;
rua=mailto:dmarc@yourdomain.com"</div>
      <div class="tool-cta">
        <p>Check your DMARC compliance</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/glossary/dmarc/">DMARC</a> ·
        <a href="/glossary/dmarc-policy/">DMARC policy</a> ·
        <a href="/dns/dmarc-record/">DMARC record guide</a>
      </div>
""",
        "faqs": [
            (
                "What did Google change in February 2024?",
                "Google started rejecting bulk email from senders without a DMARC record, valid SPF, and DKIM. The change affected anyone sending 5,000+ emails/day to Gmail addresses.",
            ),
            (
                "What is the 550 5.7.26 error?",
                "Google's rejection code for email failing authentication requirements. Usually means no DMARC record or DMARC failing on the sending domain.",
            ),
            (
                "Does p=none DMARC satisfy Google's requirement?",
                "Yes — Google requires a DMARC record to exist, not p=reject. Even p=none satisfies the February 2024 requirement.",
            ),
            (
                "Does this affect low-volume senders?",
                "The 5,000/day threshold applies to bulk requirements. But Google applies authentication checks to all senders — low-volume senders should still have SPF, DKIM, and DMARC.",
            ),
            (
                "How do I check if I'm compliant?",
                "Run DNS Preflight — it checks SPF, DKIM, and DMARC in one pass and shows exactly what's missing.",
            ),
        ],
    },
    {
        "slug": "yahoo-bulk-sender-requirements",
        "title": "Yahoo Bulk Sender Requirements — 2024 Changes",
        "meta": "Yahoo aligned with Google in 2024: DMARC, SPF/DKIM, one-click unsubscribe, and spam-rate limits for bulk senders.",
        "h1": "Yahoo Bulk Sender Requirements: What Changed",
        "subtitle": "Yahoo announced the same bulk sender requirements as Google in 2024 — SPF or DKIM, DMARC, one-click unsubscribe, and spam rate limits. Yahoo's enforcement has been progressively tightening since the announcement.",
        "breadcrumb_label": "Yahoo bulk senders (2024)",
        "body": r"""
      <p>Yahoo rolled out the same bulk-sender playbook as Gmail in 2024: authenticate your mail, publish DMARC, honour unsubscribe, and keep complaints under the line. If you only tuned Gmail, you still needed to pass Yahoo's checks — especially PTR, bounce behaviour, and reputation signals.</p>

      <h2>What Yahoo requires</h2>
      <p>Same core requirements as Google:</p>
      <ol>
        <li>Valid DKIM or SPF (preferably both)</li>
        <li>DMARC policy (p=none acceptable)</li>
        <li>One-click unsubscribe (RFC 8058)</li>
        <li>Spam complaint rate under 0.3%</li>
      </ol>
      <p>Yahoo also checks:</p>
      <ul>
        <li>Valid PTR records for sending IPs</li>
        <li>Low bounce rates</li>
        <li>Consistent sending volumes (sudden spikes trigger spam filters)</li>
      </ul>

      <h2>Yahoo vs Gmail enforcement</h2>
      <p>Yahoo has been somewhat less aggressive than Gmail on hard rejections, but this is tightening. Failing authentication on Yahoo increasingly means spam folder or rejection rather than delivery.</p>

      <h2>What to do</h2>
      <p>Same as Google — SPF, DKIM, DMARC minimum. Run DNS Preflight to check your setup.</p>
      <div class="tool-cta">
        <p>Verify authentication</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/incidents/google-dmarc-enforcement-2024/">Google &amp; Yahoo DMARC (2024)</a> ·
        <a href="/glossary/dmarc/">DMARC</a>
      </div>
""",
        "faqs": [
            (
                "Are Yahoo's requirements the same as Google's?",
                "Essentially yes — both require DMARC, valid SPF/DKIM, one-click unsubscribe, and low spam rates for bulk senders.",
            ),
            (
                "When did Yahoo start enforcing these?",
                "Yahoo announced requirements alongside Google in late 2023 with enforcement starting February 2024. Tightening has continued since.",
            ),
            (
                "Does Yahoo enforce p=reject?",
                "Yahoo honours DMARC p=reject policies and applies its own filtering on top. Having any DMARC record is the minimum requirement.",
            ),
            (
                "How do I check my Yahoo deliverability?",
                "Run DNS Preflight for authentication checks. Yahoo Postmaster Tools (postmaster.yahooinc.com) provides reputation data for your domain.",
            ),
            (
                "What is one-click unsubscribe?",
                "RFC 8058 — a List-Unsubscribe header that lets email clients show a one-click unsubscribe button without sending the user to a landing page.",
            ),
        ],
    },
    {
        "slug": "spamhaus-public-mirror-sunset",
        "title": "Spamhaus Public DNS Mirror Sunset — April 2026",
        "meta": "Spamhaus ends public DNS mirrors April 8, 2026 — use a free DQS key or blocklist queries return NXDOMAIN. DomainPreflight already uses DQS.",
        "h1": "Spamhaus Sunsetting Public DNS Mirrors: What to Do Before April 8, 2026",
        "subtitle": "Spamhaus is sunsetting its public DNS mirrors on April 8, 2026. Mail servers using public DNS resolvers (8.8.8.8, 1.1.1.1) to query Spamhaus blocklists will stop getting valid responses. The fix is to register for a free Spamhaus DQS key.",
        "breadcrumb_label": "Spamhaus mirror sunset",
        "body": r"""
      <p>On April 8, 2026, Spamhaus flips off public DNS mirror answers — queries that used to return blocklist data via resolvers like 8.8.8.8 will come back as NXDOMAIN. If your Postfix or RBL still points at zen.spamhaus.org without DQS, your spam filter quietly stops working.</p>

      <h2>What is changing</h2>
      <p>Spamhaus has always provided blocklist queries via DNS. Anyone could query zen.spamhaus.org using public resolvers. From April 8, 2026: queries via public resolvers return NXDOMAIN instead of blocklist results. Only queries from registered DQS (Data Query Service) accounts will continue to work.</p>

      <h2>Who is affected</h2>
      <ul>
        <li>Self-hosted mail servers (Postfix, Exim, Dovecot) querying Spamhaus directly</li>
        <li>Custom spam filters using Spamhaus DNS</li>
        <li>Any tool that queries zen.spamhaus.org without a DQS key</li>
      </ul>
      <p><strong>DomainPreflight uses Spamhaus DQS</strong> — the IP blocklist check on the Email Deliverability tool is not affected.</p>

      <h2>The fix</h2>
      <p>Register for a free Spamhaus DQS account at spamhaus.org/dqs. Free tier covers self-hosted mail servers.</p>
      <p>Update your mail server config:</p>
      <div class="dns-block">Before April 8:
reject_rbl_client zen.spamhaus.org

After April 8 (with DQS key):
reject_rbl_client [key].zen.dq.spamhaus.net</div>

      <h2>Migration steps</h2>
      <div class="howto-step" id="step1"><strong>Step 1</strong> Go to spamhaus.org/dqs and register for a free account</div>
      <div class="howto-step" id="step2"><strong>Step 2</strong> Get your DQS API key from the dashboard</div>
      <div class="howto-step" id="step3"><strong>Step 3</strong> Update your mail server config to use the DQS hostname format: [key].zen.dq.spamhaus.net</div>
      <div class="howto-step" id="step4"><strong>Step 4</strong> Test the new config before April 8 — don't wait</div>
      <div class="howto-step" id="step5"><strong>Step 5</strong> Run DomainPreflight Email Deliverability to verify blocklist checks still work</div>

      <div class="tool-cta">
        <p>Email Deliverability (blocklists)</p>
        <a href="https://domainpreflight.dev/email/">Open Email tool →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/glossary/blacklist/">Blacklist</a> ·
        <a href="/error/blacklisted-ip/">Blacklisted IP</a>
      </div>
""",
        "faqs": [
            (
                "What is Spamhaus sunsetting?",
                "Spamhaus is ending public DNS mirror access on April 8, 2026. Queries via public resolvers (8.8.8.8, 1.1.1.1) will return NXDOMAIN instead of blocklist results.",
            ),
            (
                "How do I fix this before April 8?",
                "Register for a free Spamhaus DQS account at spamhaus.org/dqs, get your API key, and update your mail server to use the DQS hostname format.",
            ),
            (
                "Is DomainPreflight affected?",
                "No — DomainPreflight already uses Spamhaus DQS. The Email Deliverability blocklist checks continue working.",
            ),
            (
                "What happens if I do nothing by April 8?",
                "Your mail server's Spamhaus blocklist checks will stop working — returning NXDOMAIN for all queries. This effectively disables that spam check.",
            ),
            (
                "Is the Spamhaus DQS free?",
                "Yes for self-hosted mail servers with low query volume. Commercial use requires a paid plan.",
            ),
        ],
    },
    {
        "slug": "microsoft-365-spf-changes",
        "title": "Microsoft 365 SPF and DKIM Configuration Changes",
        "meta": "Microsoft 365 now expects DKIM on custom domains — SPF alone isn't enough; selector CNAMEs and Defender DKIM signing are required for alignment.",
        "h1": "Microsoft 365 Email Authentication: What's Changed and What to Check",
        "subtitle": "Microsoft has progressively tightened email authentication requirements for Microsoft 365. DKIM is now effectively required for custom domains — and SPF alone is no longer sufficient for reliable inbox delivery.",
        "breadcrumb_label": "Microsoft 365 auth",
        "body": r"""
      <p>Microsoft 365 has been tightening how it treats custom-domain senders: SPF alone no longer reliably lands in the inbox — you need DKIM keys published and signing enabled, or DMARC alignment breaks and mail junked or rejected.</p>

      <h2>What changed</h2>
      <p>Microsoft 365 now strongly enforces DKIM alignment for custom domains. Emails without DKIM configured are increasingly landing in Junk or being rejected.</p>
      <p>The key change many missed: adding <code>include:spf.protection.outlook.com</code> to your SPF record is not enough. You also need:</p>
      <ol>
        <li>selector1 and selector2 CNAME records published in your DNS</li>
        <li>DKIM signing enabled in Microsoft 365 Defender</li>
      </ol>
      <p>Without these, M365 signs email with Microsoft's domain — not yours. DMARC alignment fails.</p>

      <h2>The error in bounce logs</h2>
      <div class="dns-block">550 5.7.509 Access denied, sending domain
[domain] does not pass DMARC verification
and has a DMARC policy of reject.</div>

      <h2>What to do</h2>
      <div class="howto-step" id="step1"><strong>Step 1</strong> Microsoft 365 Defender → Email &amp; collaboration → Policies → DKIM</div>
      <div class="howto-step" id="step2"><strong>Step 2</strong> Select your domain → Create DKIM keys</div>
      <div class="howto-step" id="step3"><strong>Step 3</strong> Add selector1 and selector2 CNAMEs to your DNS</div>
      <div class="howto-step" id="step4"><strong>Step 4</strong> Enable DKIM signing in Defender</div>
      <div class="howto-step" id="step5"><strong>Step 5</strong> Run DNS Preflight to confirm alignment</div>

      <div class="tool-cta">
        <p>Check alignment</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/fix/dmarc/microsoft-365/">DMARC fix for Microsoft 365</a> ·
        <a href="/fix/dkim/microsoft-365/">DKIM fix for Microsoft 365</a>
      </div>
""",
        "faqs": [
            (
                "Is SPF alone enough for Microsoft 365?",
                "No longer. Microsoft now expects DKIM configured for custom domains. SPF + DKIM + DMARC is the required setup.",
            ),
            (
                "What are the selector1 and selector2 CNAMEs?",
                "Two CNAME records that let Microsoft sign email with your domain's DKIM key instead of Microsoft's. Required for DMARC alignment. Get exact values from Defender → DKIM settings.",
            ),
            (
                "My M365 email was working fine without DKIM — why is it failing now?",
                "Microsoft has been tightening enforcement progressively. What worked a year ago may now trigger spam filtering or rejection.",
            ),
            (
                "Does this affect all M365 customers?",
                "All customers with custom domains should configure DKIM. @outlook.com/@hotmail.com addresses are handled automatically.",
            ),
            (
                "How do I verify M365 DKIM is working?",
                "Run DNS Preflight — the alignment engine checks selector1 and selector2 CNAMEs and shows pass/fail.",
            ),
        ],
    },
    {
        "slug": "subdomain-takeover-cases",
        "title": "Subdomain Takeover: Real Cases and How to Prevent Them",
        "meta": "Dangling CNAMEs to GitHub, S3, Heroku, and more — how takeovers happen and how to scan with Dangling Records.",
        "h1": "Real Subdomain Takeover Cases — and How to Find Your Risk",
        "subtitle": "Subdomain takeovers have affected companies of all sizes — including major brands. Here are documented cases showing how dangling CNAMEs get exploited and what the attackers actually do with them.",
        "breadcrumb_label": "Subdomain takeovers",
        "body": r"""
      <p>Attackers don't need your API keys — they need a forgotten CNAME pointing at a cloud hostname you no longer control. When the service is gone but DNS stays, the next person who claims that name owns your subdomain.</p>

      <h2>Why this happens so often</h2>
      <p>Development teams spin up subdomains constantly — for staging, testing, feature branches, marketing campaigns. When the service is deprovisioned, the DNS record stays. Over time, every company accumulates dangling CNAMEs. Most don't know they have them until someone reports a problem.</p>

      <h2>Documented takeover patterns</h2>
      <p><strong>GitHub Pages:</strong> A subdomain points to username.github.io — the user deletes the repo or account. An attacker creates a GitHub account with the same username and publishes a page. Your subdomain now serves their content.</p>
      <p><strong>AWS S3:</strong> A subdomain points to bucket.s3.amazonaws.com. The bucket is deleted. An attacker creates a bucket with the same name in the same region. Your subdomain serves their files.</p>
      <p><strong>Heroku:</strong> A subdomain points to appname.herokuapp.com. The Heroku app is deleted. An attacker creates an app with the same name. Your subdomain shows their app.</p>

      <h2>What attackers do with taken subdomains</h2>
      <ul>
        <li>Host phishing pages under your domain</li>
        <li>Serve malware downloads under your trusted domain</li>
        <li>Harvest credentials from users who trust your brand</li>
        <li>Send email from the subdomain (bypasses some filters)</li>
      </ul>

      <h2>What to do</h2>
      <p>Run DomainPreflight Dangling Records — it discovers your subdomains via certificate logs and checks each CNAME against known takeover fingerprints. The fix is always the same: delete the DNS record if the service is gone.</p>
      <div class="tool-cta">
        <p>Scan for dangling records</p>
        <a href="https://domainpreflight.dev/dangling/">Open Dangling Records →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/glossary/subdomain-takeover/">Subdomain takeover</a> ·
        <a href="/glossary/cname-record/">CNAME record</a>
      </div>
""",
        "faqs": [
            (
                "How common are subdomain takeovers?",
                "Very — security researchers regularly find vulnerable subdomains on Fortune 500 companies. Any organisation that uses cloud services and doesn't audit DNS is likely exposed.",
            ),
            (
                "What do attackers actually do with a taken subdomain?",
                "Phishing pages, malware distribution, credential harvesting — all served under your trusted domain. Some attackers hold them and notify you for a bug bounty.",
            ),
            (
                "How do I find my dangling CNAMEs?",
                "Run DomainPreflight Dangling Records — it discovers subdomains via certificate logs and checks each against known takeover fingerprints.",
            ),
            (
                "Which services are most commonly exploited?",
                "GitHub Pages, AWS S3, Heroku, Netlify, and Azure are the most common targets.",
            ),
            (
                "Is there a responsible disclosure process for subdomain takeovers?",
                "Most companies have a security@ email or bug bounty program. Researchers who find takeovers typically report them before exploiting.",
            ),
        ],
    },
    {
        "slug": "domain-expiry-outages",
        "title": "Domain Expiry Outages — Real Cases and Prevention",
        "meta": "When a domain expires, DNS stops — sites go NXDOMAIN, mail bounces, APIs die. Auto-renew and WHOIS monitoring prevent process failures.",
        "h1": "Domain Expiry Outages: What Happens and How to Prevent Them",
        "subtitle": "Domain expiry has taken down major services — including Microsoft, Foursquare, and various payment processors. The pattern is always the same: auto-renew was off, or the payment method expired.",
        "breadcrumb_label": "Domain expiry outages",
        "body": r"""
      <p>When a domain expires, everything that depends on the name stops — not gradually. DNS disappears, so your site, mail, APIs, and cert renewals all fail together. Big companies hit this through process failure, not ignorance.</p>

      <h2>Why expiry happens to serious companies</h2>
      <p>It's never negligence at the technical level. It's process failure:</p>
      <ul>
        <li>Domain registered by someone who left</li>
        <li>Payment card expired and nobody noticed</li>
        <li>Auto-renew was off on a "secondary" domain that turned out to be critical</li>
        <li>Acquisition: new team didn't know which domains mattered</li>
      </ul>

      <h2>What the outage looks like</h2>
      <p>At expiry, DNS resolution fails for the domain. Everything that depends on it stops at once — not gracefully, not with a warning message. Just stops.</p>
      <ul>
        <li>Website: NXDOMAIN</li>
        <li>Email: immediate bounce</li>
        <li>APIs: connection refused</li>
        <li>SSL renewal: fails (domain can't be verified)</li>
        <li>CDN: origin resolution fails</li>
      </ul>

      <h2>Recovery timeline</h2>
      <p><strong>Grace period (0-30 days):</strong> renew at normal price<br><strong>Redemption period (30-75 days):</strong> renew at $100-200 redemption fee<br><strong>After redemption:</strong> domain released to public</p>

      <h2>What to do</h2>
      <ol>
        <li>Enable auto-renew on every domain</li>
        <li>Use a payment method that doesn't expire (virtual card with no expiry, or update annually)</li>
        <li>Add a calendar reminder 60 days before expiry as backup</li>
        <li>Monitor expiry dates with DomainPreflight WHOIS</li>
      </ol>
      <div class="tool-cta">
        <p>Check your domain expiry</p>
        <a href="https://domainpreflight.dev/whois/">Open WHOIS →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/glossary/domain-expiry/">Domain expiry</a> ·
        <a href="/glossary/whois/">WHOIS</a> ·
        <a href="/blog/domain-expiry-infrastructure-failure/">Blog: infra failure</a>
      </div>
""",
        "faqs": [
            (
                "Has domain expiry really affected major companies?",
                "Yes — Microsoft accidentally let hotmail.co.uk expire, Foursquare had an expiry incident, and many payment processors have had outages from domain lapses.",
            ),
            (
                "What is the redemption period?",
                "After the grace period (30-45 days), domains enter redemption — usually 30-45 more days at $100-200 fee. After that, the domain is released.",
            ),
            (
                "Can I recover my domain after it expires?",
                "Yes during the grace and redemption periods. After redemption, the domain becomes available to anyone.",
            ),
            (
                "How do I monitor domain expiry?",
                "Run DomainPreflight WHOIS — shows exact expiry date with risk tier. Set up auto-renew at your registrar as the primary protection.",
            ),
            (
                "What if the domain was registered by someone who left the company?",
                "Contact the registrar with proof of company ownership. Most registrars have a process for this — act before expiry, not after.",
            ),
        ],
    },
    {
        "slug": "email-blacklist-incidents",
        "title": "Email Blacklisting Incidents — Causes, Impact, and Recovery",
        "meta": "IPs get listed for compromised accounts, shared hosting, volume spikes, and spam traps — here's how listing works and how to recover.",
        "h1": "Email Blacklisting: How It Happens and How to Recover",
        "subtitle": "IP blacklisting can happen to any mail server — including those with good sending practices. Shared hosting IPs, compromised accounts, and sudden volume spikes are the most common triggers. Here's how blacklisting happens and how to get removed.",
        "breadcrumb_label": "Email blacklists",
        "body": r"""
      <p>Your IP can land on a blocklist even when you did nothing wrong — shared hosting, a stolen account, or a bad list with spam traps. The impact is immediate: bounces, junk folder, or total silence from major receivers.</p>

      <h2>How servers get blacklisted</h2>
      <p><strong>Compromised account:</strong> One user account gets phished. The attacker uses it to send thousands of spam messages. The IP gets listed on Spamhaus before the owner even notices.</p>
      <p><strong>Shared hosting:</strong> Your IP is shared with 50 other customers. One of them sends spam. Everyone on that IP gets blacklisted together.</p>
      <p><strong>Volume spike:</strong> You send a legitimate bulk campaign after months of low volume. The sudden spike looks like spam. You get listed.</p>
      <p><strong>Spam trap hits:</strong> Your list contains old addresses that have been converted to spam traps. Every email to them counts as spam.</p>

      <h2>Impact by blacklist</h2>
      <div class="dns-block">Spamhaus ZEN:     Major impact — used by
most enterprise mail servers
SpamCop:          Moderate — used by
some providers
Barracuda:        Significant for corporate
email (Barracuda gateways)
Microsoft SNDS:   Critical for Outlook/Hotmail
delivery
Google Postmaster: Affects Gmail delivery</div>

      <h2>Recovery steps</h2>
      <ol>
        <li>Run DomainPreflight Email tool — identify which lists you're on</li>
        <li>Fix the underlying cause first</li>
        <li>Submit removal requests: Spamhaus (spamhaus.org/removal), SpamCop (auto-expires 24-48 hours after spam stops), Barracuda (barracudacentral.org/lookups)</li>
        <li>Monitor for re-listing</li>
      </ol>
      <div class="tool-cta">
        <p>Check if your IP is blacklisted</p>
        <a href="https://domainpreflight.dev/email/">Open Email tool →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/glossary/blacklist/">Blacklist</a> ·
        <a href="/error/blacklisted-ip/">Blacklisted IP</a>
      </div>
""",
        "faqs": [
            (
                "How do I know if my IP is blacklisted?",
                "Run DomainPreflight Email Deliverability with your sending IP — checks 10+ major blacklists instantly.",
            ),
            (
                "How long does blacklist removal take?",
                "Spamhaus: 24-48 hours after request. SpamCop: auto-expires. Barracuda: 12-24 hours after request.",
            ),
            (
                "Can I get blacklisted for sending legitimate email?",
                "Yes — sudden volume spikes, old lists with spam traps, or being on a shared IP with a spammer can trigger listing.",
            ),
            (
                "What if I'm on a shared IP and someone else caused the listing?",
                "Request a dedicated IP from your sending provider. Shared IPs are a permanent risk for high-volume senders.",
            ),
            (
                "Will getting delisted fix my spam folder problem?",
                "If blacklisting was the cause — yes. Run DNS Preflight after delisting to check for other issues.",
            ),
        ],
    },
    {
        "slug": "sendgrid-ip-reputation",
        "title": "SendGrid IP Reputation and Deliverability Issues",
        "meta": "Shared SendGrid IPs can drag reputation — DMARC alignment and domain reputation protect you; dedicated IPs for high volume.",
        "h1": "SendGrid IP Reputation: What Goes Wrong and How to Fix It",
        "subtitle": "SendGrid shared IP pools have experienced periodic reputation issues that affect deliverability for all users on those IPs. Using dedicated IPs and configuring domain authentication properly reduces this risk.",
        "breadcrumb_label": "SendGrid IP reputation",
        "body": r"""
      <p>On a shared pool, someone else's bad mail becomes your problem — Gmail and Yahoo weight domain reputation when DMARC aligns, but a toxic IP still hurts. Here's how shared IP risk shows up and how to harden your setup.</p>

      <h2>Shared IP risk on SendGrid</h2>
      <p>SendGrid, like all major ESPs, uses shared IP pools for free and low-volume accounts. If other senders on your shared IP damage its reputation, your emails are affected too.</p>

      <h2>Signs of shared IP reputation issues</h2>
      <ul>
        <li>Deliverability drops suddenly without changes to your setup</li>
        <li>Gmail Postmaster Tools shows IP reputation declining</li>
        <li>Bounce rates increase without changes to your list</li>
      </ul>

      <h2>How to protect yourself</h2>
      <ol>
        <li>Configure domain authentication properly — DKIM and DMARC alignment means your domain's reputation matters more than the shared IP</li>
        <li>Consider a dedicated IP if you send over 100,000 emails/month</li>
        <li>Monitor your domain reputation in Gmail Postmaster Tools</li>
      </ol>
      <p><strong>Domain authentication is your moat:</strong> With proper DMARC alignment, major providers weight your domain reputation heavily. Even on a shared IP, a clean domain reputation protects you.</p>
      <div class="tool-cta">
        <p>Check SendGrid alignment</p>
        <a href="https://domainpreflight.dev/">Open DNS Preflight →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/fix/dmarc/sendgrid/">SendGrid DMARC</a> ·
        <a href="/fix/spf/sendgrid/">SendGrid SPF</a> ·
        <a href="/fix/dkim/sendgrid/">SendGrid DKIM</a>
      </div>
""",
        "faqs": [
            (
                "Can SendGrid shared IPs affect my deliverability?",
                "Yes. If other senders on your shared IP send spam, it damages the IP's reputation and affects everyone on that pool.",
            ),
            (
                "How do I know if shared IP reputation is causing my problem?",
                "Check Gmail Postmaster Tools — it shows both IP and domain reputation separately. If IP reputation is low but domain is fine, it's the shared IP.",
            ),
            (
                "Should I get a dedicated SendGrid IP?",
                "Consider it if you send 100,000+ emails/month. Below that, the warm-up period for a new dedicated IP often causes more problems than shared IP reputation.",
            ),
            (
                "Does configuring DMARC help with shared IP issues?",
                "Yes. DMARC alignment shifts reputation signals to your domain rather than the sending IP. Providers weight domain reputation heavily.",
            ),
            (
                "How do I set up DMARC alignment for SendGrid?",
                "Add three CNAME records from SendGrid's Sender Authentication dashboard. See the SendGrid DMARC fix guide.",
            ),
        ],
    },
    {
        "slug": "dmarc-adoption-2024",
        "title": "DMARC Adoption in 2024 — Industry Statistics",
        "meta": "DMARC adoption jumped after Google/Yahoo — millions of domains have records, but many stay stuck at p=none forever.",
        "h1": "DMARC Adoption Statistics — Where the Industry Stands",
        "subtitle": "DMARC adoption accelerated sharply in 2024 following Google and Yahoo's enforcement announcement. But millions of domains still have no DMARC record — and many that do are stuck at p=none indefinitely.",
        "breadcrumb_label": "DMARC adoption 2024",
        "body": r"""
      <p>2024 was the year DMARC got real — Google and Yahoo forced the record to exist for bulk senders, and adoption jumped. The gap now is enforcement: most orgs stopped at p=none and never moved to quarantine or reject.</p>

      <h2>Key statistics</h2>
      <ul>
        <li>DMARC adoption grew ~30% in 2024 following Google/Yahoo announcement</li>
        <li>Over 5 million domains have DMARC records</li>
        <li>Of those, roughly 40% are still at p=none</li>
        <li>Only ~25% have reached p=reject</li>
        <li>Fortune 500 companies: ~85% have DMARC, but only ~60% at p=reject</li>
      </ul>

      <h2>What this means</h2>
      <p>The easy part happened — adding a DMARC record. The hard part is tightening policy. Most domains added p=none under deadline pressure and never upgraded. Their domains still have no active spoofing protection.</p>
      <p>The gap between "has DMARC" and "DMARC is actually enforced" is where most brand spoofing happens.</p>

      <h2>What to do</h2>
      <p>Run DNS Preflight on your domain. If DMARC shows p=none and you set it more than 4 weeks ago — it's time to review your aggregate reports and upgrade to p=quarantine.</p>
      <div class="tool-cta">
        <p>Analyze DMARC reports</p>
        <a href="https://domainpreflight.dev/dmarc/">Open DMARC Report Analyzer →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/glossary/dmarc-policy/">DMARC policy</a> ·
        <a href="/blog/dmarc-p-none-still-a-problem/">Blog: p=none problem</a>
      </div>
""",
        "faqs": [
            (
                "What percentage of domains have DMARC?",
                "Roughly 5+ million domains as of 2024, representing significant growth after Google and Yahoo's enforcement announcement.",
            ),
            (
                "What percentage have p=reject?",
                "Approximately 25% of domains with DMARC have reached p=reject. Most are still at p=none.",
            ),
            (
                "Why do most companies stay at p=none?",
                "They set up DMARC under deadline pressure, got the green tick, and moved on without reading reports or upgrading policy.",
            ),
            (
                "Is p=none better than no DMARC?",
                "Yes — it satisfies Google/Yahoo requirements and gives you visibility. But it provides zero spoofing protection.",
            ),
            (
                "How do I move from p=none to p=reject?",
                "Read your DMARC aggregate reports for 2-4 weeks. Fix alignment failures. Move to p=quarantine. Then p=reject. Use DomainPreflight DMARC Report Analyzer.",
            ),
        ],
    },
    {
        "slug": "typosquat-phishing-domains",
        "title": "Typosquat Phishing Domains — How Attackers Use Lookalikes",
        "meta": "Homoglyphs, TLD swaps, and missing letters — attackers register lookalikes for phishing; DomainPreflight Typosquat Monitor finds resolving variants.",
        "h1": "Typosquat Phishing: How Attackers Register Your Lookalike Domains",
        "subtitle": "Attackers register domains that look like yours — one character off, a different TLD, a homoglyph substitution — and use them for phishing campaigns. Here's how it works and how to find lookalike domains targeting your brand.",
        "breadcrumb_label": "Typosquat phishing",
        "body": r"""
      <p>Attackers spend $10 on a lookalike domain — paypa1.com, yourbrand.co — then host a clone of your login page and send mail that almost passes the eye test. Your DMARC on the real domain doesn't stop mail from a different domain.</p>

      <h2>How typosquat phishing works</h2>
      <p><strong>Step 1 — Register a lookalike:</strong> The attacker registers something like paypa1.com (l→1) or paypal.co (TLD swap). The cost is $10-15/year.</p>
      <p><strong>Step 2 — Set up infrastructure:</strong> They configure MX records, create email accounts, and sometimes clone your entire website on the domain.</p>
      <p><strong>Step 3 — Send phishing email:</strong> Emails appear to come from support@paypa1.com — close enough that users don't notice. Links go to a cloned version of your site.</p>
      <p><strong>Step 4 — Harvest credentials:</strong> Users enter usernames and passwords on the fake site. Attackers collect them.</p>

      <h2>Common lookalike techniques</h2>
      <div class="dns-block">Homoglyph:     paypa1.com (l→1)
Missing char:  paypl.com
Doubled char:  paypall.com
TLD swap:      paypal.co, paypal.net
Prefix:        mypaypal.com, getpaypal.com
Suffix:        paypalapp.com
Subdomain:     paypal.com.attacker.com</div>

      <h2>How to find lookalikes</h2>
      <p>Run DomainPreflight Typosquat Monitor — it generates 30-50 variants of your domain and checks which ones resolve to active websites. A resolving domain is higher risk than a registered-but-parked domain — active sites can be hosting phishing.</p>
      <p><strong>Defensive registration:</strong> Consider registering your highest-risk variants. The cost is small compared to the damage from an active phishing campaign.</p>
      <div class="tool-cta">
        <p>Check for typosquats</p>
        <a href="https://domainpreflight.dev/typosquat/">Open Typosquat Monitor →</a>
      </div>
      <div class="glossary-links"><strong>Related:</strong>
        <a href="/glossary/typosquatting/">Typosquatting</a>
      </div>
""",
        "faqs": [
            (
                "What is a typosquat phishing domain?",
                "A domain registered to look like a legitimate brand — one character off, different TLD, or homoglyph swap — used to host phishing pages or send phishing email.",
            ),
            (
                "How do I find domains impersonating my brand?",
                "Run DomainPreflight Typosquat Monitor — checks 30-50 lookalike variants via live DNS to find which ones resolve.",
            ),
            (
                "Should I register lookalike domains defensively?",
                "For high-risk variants (homoglyphs, common TLD swaps) — yes. The cost is low. The alternative is letting attackers register them.",
            ),
            (
                "What if I find a phishing domain using my brand?",
                "Report to the registrar's abuse team, the hosting provider's abuse contact, and Google Safe Browsing (safebrowsing.google.com/safebrowsing/report_phish/).",
            ),
            (
                "Can DMARC protect against typosquat phishing?",
                "Only for your actual domain. DMARC on yourdomain.com doesn't protect against email from paypa1.com — that's a different domain with its own DNS.",
            ),
        ],
    },
]
