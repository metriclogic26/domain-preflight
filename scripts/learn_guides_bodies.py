# Long-form HTML bodies for learn guides (no FAQ — those live in learn_pages_data).
# Each string is article content + tool CTA; HowTo steps are appended by generate_learn_guides.py.

def tool_cta(href: str, link_text: str, lead: str) -> str:
    return f"""      <div class="tool-cta">
        <p><strong>Tool:</strong> {lead}</p>
        <p><a href="{href}">{link_text}</a></p>
      </div>"""


BODIES: dict[str, str] = {}

BODIES["dmarc"] = r"""
      <p>DMARC is where email authentication stops being “we have TXT records” and becomes “here is what receivers must do when mail fails.” If you only read one sentence: <strong>do not skip SPF and DKIM</strong>. DMARC is the policy layer on top — not a substitute for either. The <a href="/glossary/dmarc/">DMARC glossary entry</a> spells out the vocabulary; this guide is the operational walkthrough. Use <a href="https://domainpreflight.dev/">domainpreflight.dev</a> for day-to-day checks and <a href="https://domainpreflight.dev/dmarc/">the DMARC Report Analyzer</a> when XML lands in your inbox.</p>

      <h2>What DMARC actually does</h2>
      <p>Receivers already check SPF and DKIM. DMARC adds three things: a published policy (<a href="/glossary/dmarc-policy/">p=none, quarantine, or reject</a>), alignment rules (<a href="/glossary/dmarc-alignment/">SPF and/or DKIM must align with the From domain</a>), and optional reporting (<a href="/glossary/dmarc-aggregate-report/">aggregate XML</a> to a mailbox you control). Policy is what most people mean when they say “we turned on DMARC.” Reporting is how you prove legitimate senders are aligned before you tighten policy.</p>
      <p>Think of DMARC as a contract. You publish what you want receivers to do. They compare results against your From: domain. Misaligned mail can be treated as suspicious or rejected — depending on policy and receiver implementation. That is why “DMARC pass” is not one checkbox; it is SPF/DKIM pass <em>plus</em> alignment under your record.</p>
      <p>Receivers may apply policy differently for subdomains (<code>sp=</code>) or use local heuristics beyond DMARC. Your job is to make legitimate mail pass and align; anything else should show up clearly in aggregate reports so you can decide whether to quarantine or reject.</p>

      <h2>The three components you need first</h2>
      <p>You need <strong>SPF</strong> (who may send for your domain), <strong>DKIM</strong> (cryptographic signatures), and <strong>DMARC</strong> (policy + reporting). Order matters operationally: fix SPF and DKIM until real mail passes, then layer DMARC. Our <a href="/learn/spf/">SPF guide</a> and <a href="/learn/dkim/">DKIM guide</a> cover the mechanics. If either is broken, DMARC will surface failures in reports — which is useful — but you should not advance policy until senders align.</p>
      <p>Common mistake: publishing DMARC while marketing mail still sends from a subdomain without DKIM or with SPF that does not include the ESP’s include. You will see volume in reports with <code>spf=fail</code> or <code>dkim=fail</code>. Fix the sender configuration first; the <a href="/fix/dmarc/">DMARC fix hub</a> links provider-specific steps.</p>
      <p>Another mistake: assuming Google Workspace or Microsoft 365 “handles everything.” Third-party CRMs, support desks, invoice tools, and AWS SES all add sending paths. Each path needs SPF includes and/or DKIM keys aligned to the From domain you use in campaigns. Inventory before policy — spreadsheets are boring and lifesaving.</p>

      <h2>Adding your first DMARC record</h2>
      <p>Create a TXT record at <code>_dmarc.yourdomain.com</code> (some UIs show “host” as <code>_dmarc</code> only). Start with monitoring — <code>p=none</code> — and always include a mailbox for aggregate reports.</p>
      <div class="dns-block">v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com; fo=1; adkim=r; aspf=r; pct=100</div>
      <p><code>rua=</code> is where daily <a href="/glossary/dmarc-aggregate-report/">aggregate reports</a> go. Use a dedicated address (or alias) and confirm the mailbox receives mail. <code>fo=1</code> requests failure reports when either SPF or DKIM fails — helpful during rollout. <code>adkim</code> and <code>aspf</code> set relaxed vs strict alignment; relaxed is typical for first deployments. Document the record in your runbook; you will change <code>p=</code> later.</p>
      <p>Exact syntax reference also lives on our <a href="/dns/dmarc-record/">DMARC DNS record</a> page. If your DNS host splits name/value oddly, paste the full string into one TXT value field.</p>
      <p>Validate propagation: query <code>_dmarc</code> from multiple resolvers after publish. TTLs can delay visibility; do not panic-change the record twice in an hour unless you confirmed a typo.</p>

      <h2>Reading your aggregate reports</h2>
      <p>Reports are gzip’d XML from large providers. You can grep them — or use a parser. The fastest path for humans is <strong>DomainPreflight’s DMARC Report Analyzer</strong>: paste XML, see pass/fail by source IP and aligned domains. That beats staring at raw files when you are answering “who is sending as us?”</p>
      <p>When you review reports, tag each source: legitimate (keep), third-party (add include or DKIM), unknown (investigate), malicious (plan for reject once legit mail is clean). Link this work to the <a href="/blog/dmarc-p-none-still-a-problem/">p=none still a problem</a> discussion — monitoring without eventual enforcement leaves spoofing on the table.</p>
      <p>Pay attention to volume spikes from unexpected ASNs. A small amount of spoofing is normal for large brands; sustained spoof volume deserves incident response. Cross-check with abuse desk contacts at major receivers when needed.</p>

      <h2>Fixing alignment failures</h2>
      <p>Alignment means the SPF domain or DKIM signing domain matches the organizational domain in the From: header (per your relaxed/strict settings). Failures show up as aligned=no in tooling even when SPF or DKIM “passes” for a different domain.</p>
      <p>Fix paths: add missing SPF includes, enable DKIM at the ESP, align From: addresses with authenticated domains, or use a subdomain strategy. Our <a href="/fix/dmarc/">DMARC fix collection</a> points to provider guides (Google, Microsoft, SendGrid, etc.). Work one sender at a time; re-check reports after DNS TTLs.</p>
      <p>Strict alignment (<code>adkim=s</code> / <code>aspf=s</code>) breaks more legitimate setups — only enable when you understand subdomains and envelope domains. Most orgs stay relaxed until mature.</p>

      <h2>Moving from p=none to p=quarantine</h2>
      <p>Upgrade when reports show consistent alignment for all known senders and you have a rollback plan. Quarantine sends failing mail to spam at many receivers — softer than reject. Use <code>pct=</code> to sample (e.g. <code>pct=25</code> then increase) if your risk tolerance requires it. Communicate with internal teams before you flip; helpdesk volume spikes when one forgotten newsletter source breaks.</p>
      <p>Document the change window. Keep screenshots of DMARC record before/after. If something screams, revert <code>p=</code> to none temporarily — data beats pride.</p>

      <h2>Moving from p=quarantine to p=reject</h2>
      <p>Reject is the end state for spoofing defense: failing mail should not be delivered. Confirm no critical systems send unaligned mail. Watch transactional paths (receipts, password resets) especially. Keep <code>rua=</code> active — you still want visibility. Large providers have pushed stricter expectations; see <a href="/incidents/google-dmarc-enforcement-2024/">Google DMARC enforcement (2024)</a> for why “eventually” is now “soon.”</p>
      <p>Some mail still bypasses strict DMARC (direct server-to-server edge cases). Reject raises the bar; it does not replace fraud training or attachment policies.</p>

      <h2>The complete rollout timeline</h2>
      <p>Week 1: Publish <code>p=none</code>, validate mailbox receives reports. Week 2–3: Eliminate alignment failures for known apps. Week 4: Evaluate quarantine if clean. Week 5–6: Ramp <code>pct</code> for quarantine or move to full quarantine. Week 7–8: Plan reject after no surprises. Longer if you have many ESPs or acquisitions. This is a guideline — not a law — but rushing policy without data breaks mail.</p>
      <p>Enterprise tip: maintain a spreadsheet of sending services, owner, SPF includes, DKIM selectors, and last report date. Tie changes to CAB tickets. When someone says “email stopped,” you open DMARC reports first.</p>
      <p>Forensic reports (<code>ruf=</code>) are optional and often ignored by receivers for privacy reasons. Do not block a rollout on <code>ruf</code>; lean on aggregate data and message headers. If legal needs message-level samples, use controlled testing in your own tenant instead of expecting global <code>ruf</code> delivery.</p>

""" + tool_cta(
        "https://domainpreflight.dev/dmarc/",
        "Open DMARC Report Analyzer →",
        "Paste aggregate XML from your inbox and get a clear pass/fail breakdown before you change policy.",
    )

BODIES["spf"] = r"""
      <p>SPF is a single TXT record that answers: which hosts may use this domain in the SMTP envelope sender (Return-Path / MAIL FROM)? One typo, one duplicate <code>v=spf1</code> record, or one too many <code>include:</code> lookups — and you get <a href="/glossary/spf-permerror/">SPF PermError</a>. Receivers treat that as “no valid SPF,” which is worse than a softfail. Our <a href="/glossary/spf-record/">SPF glossary</a> defines the pieces; this page is how you build and keep a record that survives real infrastructure.</p>

      <h2>What SPF does and why it matters</h2>
      <p>SPF does not sign message bodies. It authorizes IP-based senders and some indirections via <code>include:</code>, <code>a</code>, <code>mx</code>, and <code>ptr</code> mechanisms (though PTR in SPF is limited and often avoided). Receivers evaluate SPF against the envelope — not the visible From: header. That distinction matters when marketing tools use their own bounce domain: SPF may pass for <code>bounces.example.com</code> while DMARC still requires DKIM alignment to your brand domain. Pair SPF with DKIM and DMARC; see <a href="/learn/dmarc/">the DMARC guide</a>.</p>
      <p>Why operators care: SPF is cheap to deploy, easy to break, and the first thing spam filters check when mail volume spikes. A PermError during a product launch is a bad news story. A correct SPF with <code>~all</code> buys time while you map every sender.</p>

      <h2>Building your first SPF record</h2>
      <p>Start minimal. One mechanism, one fallback. Expand when you add providers.</p>
      <div class="dns-block">v=spf1 include:_spf.google.com ~all</div>
      <p><code>~all</code> is <a href="/glossary/spf-softfail/">softfail</a>: unlisted senders are marked suspicious but often still delivered. <code>-all</code> is hardfail — use only when every path is known. The literal “all” mechanism must be last. Only one SPF TXT may start with <code>v=spf1</code> per domain/DNS node — duplicates cause immediate failure.</p>
      <p>DNS details: publish at the domain that appears in the envelope sender you control. Subdomain sending is common; you may need SPF on those labels too. Our <a href="/dns/spf-record/">SPF DNS reference</a> shows host placement patterns.</p>

      <h2>Adding multiple senders</h2>
      <p>Merge includes into one record. Example: Google Workspace + SendGrid + a static IP.</p>
      <div class="dns-block">v=spf1 include:_spf.google.com include:sendgrid.net ip4:203.0.113.10 ~all</div>
      <p>Order does not change semantics, but readability matters for audits. Document each include’s owner. When an ESP changes their include chain, your lookup count can cross ten without you editing characters — re-run a tree regularly. Multi-ESP setups are covered in <a href="/fix/spf/multiple-providers/">SPF with multiple providers</a>.</p>
      <p>If a vendor asks you to flatten SPF, understand why: they are trying to save lookups. Flattening hardcodes IPs and adds operational risk when those IPs rotate. Prefer removing unused includes or splitting mail across subdomains when possible.</p>

      <h2>The 10-lookup limit — why it exists</h2>
      <p>SPF evaluation follows DNS chains. Each <code>include:</code>, <code>a</code>, <code>mx</code>, <code>ptr</code>, and <code>exists</code> consumes lookups. The RFC cap stops unbounded resolver load. Exceeding ten triggers <a href="/error/spf-permerror/">PermError</a> in strict parsers — and many large receivers are strict.</p>
      <p>Nested includes count. <code>include:sendgrid.net</code> might pull three more DNS targets. You cannot “see” the count from the outer string; you must expand the tree. That is what <a href="https://domainpreflight.dev/">DomainPreflight DNS Preflight</a> SPF visualization is for — paste your domain, read the lookup count before go-live.</p>

      <h2>How to count your lookups</h2>
      <p>Manual method: recursively resolve each mechanism, count terminal mechanisms, stop at ten. Automated method: use DNS Preflight’s SPF tree and fix the highest-churn includes first. Re-check after any ESP onboarding.</p>
      <p>When you are over the limit, remove dead vendors first. Then consolidate sending through fewer IPs or subdomains. Last resort: controlled flattening with monitoring. Deep dive: <a href="/blog/spf-lookup-limit/">SPF lookup limit</a> on our blog.</p>

      <h2>Fixing PermError</h2>
      <p>Symptoms: authentication headers show <code>permerror</code>, or tools report two SPF TXT strings. Fixes: merge TXT records, fix syntax (double spaces rarely matter; malformed macros do), remove duplicate <code>v=spf1</code>, reduce lookups below ten. Walkthrough: <a href="/fix/spf/too-many-lookups/">Too many lookups</a> and <a href="/fix/spf/multiple-providers/">multiple providers</a>.</p>

      <h2>Softfail vs hardfail (~all vs -all)</h2>
      <p>Use <code>~all</code> until monitoring proves every legitimate sender is covered. Move to <code>-all</code> when DMARC is at enforcement and stray mail is either gone or acceptable. Sudden <code>-all</code> with unknown senders creates false positives. Compare tradeoffs in <a href="/fix/spf/softfail-vs-hardfail/">softfail vs hardfail</a>.</p>

      <h2>Testing your SPF record</h2>
      <p>After publish, wait for TTL. Query authoritative servers, not just your laptop cache. Send test mail through each provider and inspect Authentication-Results. Run <a href="https://domainpreflight.dev/">DNS Preflight</a> on the domain — it surfaces SPF, DMARC, and related issues in one pass.</p>
      <p>Red-team tip: test from a non-production subdomain before changing corporate <code>-all</code>. Measure helpdesk impact. Document rollback (previous TXT value) in change management.</p>

""" + tool_cta(
        "https://domainpreflight.dev/",
        "Run DNS Preflight →",
        "Count SPF lookups, validate syntax, and catch PermError before receivers do.",
    )

BODIES["dkim"] = r"""
      <p>DKIM proves a message was not tampered with in transit — and that a signer you trust vouched for it. The sending server holds a private key; DNS publishes the public key. Receivers verify the signature against headers/body hashes. This guide walks key generation, DNS publication, selector strategy, rotation, and failure modes. Terms: <a href="/glossary/dkim/">DKIM glossary</a>, <a href="/glossary/dkim-selector/">selectors</a>.</p>

      <h2>What DKIM does</h2>
      <p>Unlike SPF (IP authorization), DKIM is cryptographic. It survives forwarding less predictably than SPF in some cases, but it aligns with your brand domain when configured correctly. DMARC “pass” typically needs DKIM or SPF alignment — DKIM is often easier for ESPs because they control signing with their infrastructure.</p>

      <h2>How DKIM signing works</h2>
      <p>Outbound mail gets a <code>DKIM-Signature</code> header with <code>d=</code> (signing domain), <code>s=</code> (selector), and hashes over canonicalized headers/body. The receiver looks up <code>s._domainkey.d</code> TXT, parses the public key, and verifies. If DNS is wrong or the key does not match, you see <a href="/error/dkim-signature-failed/">signature failed</a> or <a href="/error/dkim-none/">dkim=none</a> in diagnostics.</p>

      <h2>Generating a DKIM key</h2>
      <p>Most teams generate keys inside their ESP (Google, Microsoft, SendGrid, etc.). Self-hosters use OpenSSL or mail stack wizards (Postfix/OpenDKIM, Exim, rspamd). Minimum key size today is <strong>2048-bit</strong>; 1024-bit keys are legacy and should be rotated — see <a href="/fix/dkim/key-length/">key length fix</a>.</p>

      <h2>Publishing the DKIM record</h2>
      <p>Format is a TXT at <code>selector._domainkey.example.com</code>. Value contains <code>v=DKIM1</code>, <code>k=rsa</code>, and <code>p=</code> with the base64 public key. Some DNS panels split long strings into multiple strings — that is fine; DNS concatenates them. Truncation is a common outage: if you paste half a key, verification fails silently for a percentage of traffic.</p>
      <div class="dns-block">selector._domainkey IN TXT ("v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEB..." )</div>
      <p>Our <a href="/dns/dkim-record/">DKIM DNS page</a> lists pitfalls (quotes, 255-char chunks, CNAME vs TXT). Double-check with a DNS lookup from multiple resolvers after publish.</p>

      <h2>Key length — why 2048-bit matters</h2>
      <p>1024-bit RSA is within reach of nation-scale adversaries and increasingly casual attackers. Providers have moved to 2048-bit defaults. If your panel still shows 1024, plan rotation — <a href="/fix/dkim/rotate-keys/">rotate keys safely</a> by dual-publishing old and new selectors before cutover.</p>

      <h2>Verifying your DKIM record</h2>
      <p>Use <a href="https://domainpreflight.dev/">DNS Preflight</a> — it probes common selectors and reports key strength when found. Send a test message and inspect <code>DKIM-Signature</code> in raw headers; the selector there must match DNS.</p>

      <h2>DKIM selectors — what they are</h2>
      <p>Selectors let you run multiple keys concurrently — for rotation, multi-tenant ESP setups, or product lines. A mismatch (<code>s=mar2026</code> in header but DNS only has <code>default._domainkey</code>) fails verification. Troubleshooting: <a href="/fix/dkim/selector/">selector issues</a> and <a href="/fix/dkim/signature-failed/">signature failed</a>.</p>

      <h2>Rotating DKIM keys safely</h2>
      <p>Publish the new selector, verify traffic signs with it, then remove the old key after a overlap window (often 48–168 hours depending on volume). Never delete the old DNS record first. Playbook: <a href="/fix/dkim/rotate-keys/">rotate keys</a>.</p>

      <h2>Why DKIM alone is not enough</h2>
      <p>DKIM proves integrity and ties to a domain, but without DMARC, receivers may still accept spoofed From: domains that do not align. Layer <a href="/learn/dmarc/">DMARC</a> for policy. Combine with <a href="/learn/spf/">SPF</a> for coverage when forwarding breaks DKIM.</p>

""" + tool_cta(
        "https://domainpreflight.dev/",
        "Run DNS Preflight →",
        "Probe DKIM selectors, key strength, and DNS publication in one check.",
    )

BODIES["email-deliverability"] = r"""
      <p>Deliverability is the answer to: “Did it land in the inbox, and will the next message?” Delivery alone means the remote server accepted the message — spam folder still counts as delivered. This guide stacks the signals that actually move the needle and points to the tools that surface them. Start with <a href="/glossary/email-deliverability/">email deliverability</a> vocabulary if any term is new.</p>

      <h2>The deliverability stack</h2>
      <p>Order of impact for most senders: <strong>authentication</strong> → <strong>reputation</strong> → <strong>content</strong> → <strong>engagement</strong>. Skip fixing engagement copy before SPF/DKIM/DMARC are correct — you will chase ghosts. Authentication is binary-ish (pass/fail/pererror). Reputation is fuzzy and slow to heal. Content can trigger filters in seconds. Engagement feeds ML models over weeks.</p>

      <h2>Authentication — the foundation</h2>
      <p>SPF, DKIM, DMARC — implement in that operational sequence for most teams. Walkthroughs: <a href="/learn/spf/">SPF</a>, <a href="/learn/dkim/">DKIM</a>, <a href="/learn/dmarc/">DMARC</a>. Without alignment, brand mail looks like mixed signals to large receivers. Bulk sender requirements from major mailbox providers now assume at least baseline DMARC — even <code>p=none</code> with reporting.</p>

      <h2>IP reputation</h2>
      <p>Sending IP history matters for bulk sends. New IPs need warm-up. Check <a href="/glossary/ptr-record/">PTR</a> (reverse DNS) — many filters expect forward/reverse consistency for direct mail. Monitor <a href="/glossary/blacklist/">blocklists</a>; delist only after fixing the cause. Symptoms: <a href="/error/blacklisted-ip/">blacklisted IP</a> errors in bounces.</p>

      <h2>Domain reputation</h2>
      <p>Domains accrue trust from sending volume, complaint rates, spam trap hits, and bounce handling. Sudden list purchases torch domains. Keep lists clean, process bounces, suppress complainers. Authentication failures drag domain reputation indirectly by increasing spam placement.</p>

      <h2>Content signals</h2>
      <p>URL shorteners, heavy images, mismatched HTML/text, and spammy phrases can tip filters when reputation is weak. Content rarely overrides bad authentication — but it can cap performance even when auth passes. A/B test subject lines and bodies; avoid deceptive <code>From:</code> names.</p>

      <h2>Engagement signals</h2>
      <p>Opens (where available), clicks, replies, deletes without opens, and “report spam” clicks train models. High complaints are a leading indicator of future blocks. Treat low engagement segments separately; stop mailing dead addresses.</p>

      <h2>How to diagnose a deliverability problem</h2>
      <p>Symptom → tool: authentication oddities → <a href="https://domainpreflight.dev/">DNS Preflight</a> + headers. IP/blocklist issues → <a href="https://domainpreflight.dev/email/">DomainPreflight Email tool</a>. Content tests → seed inboxes + provider postmaster tools. Inbox placement mystery with clean auth → reputation and engagement — timeline fixes.</p>
      <p>General spam folder: <a href="/error/emails-going-to-spam/">emails going to spam</a> checklist.</p>

      <h2>The pre-send checklist</h2>
      <p>Confirm SPF/DKIM/DMARC for the sending domain, PTR for dedicated IPs, list hygiene, suppression files loaded, bounce handling enabled, and DMARC reporting flowing. Preview links. Send a small cohort before full blast. Document who owns rollback.</p>

""" + tool_cta(
        "https://domainpreflight.dev/email/",
        "Open DomainPreflight Email →",
        "Check IP reputation, blocklists, and related signals for outbound mail.",
    )

BODIES["dns-for-email"] = r"""
      <p>Email depends on DNS the way HTTPS depends on certificates — invisible until it breaks. Five records cover most of what operators need: MX, SPF, DKIM, DMARC, and PTR for sending IPs. Miss one and symptoms look like “random spam folder” or “works from Gmail but not Outlook.” This page ties them together. Deep dives: <a href="/glossary/mx-record/">MX</a>, <a href="/glossary/spf-record/">SPF</a>, <a href="/glossary/dkim/">DKIM</a>, <a href="/glossary/dmarc/">DMARC</a>, <a href="/glossary/ptr-record/">PTR</a>. For end-to-end context, read <a href="/learn/email-deliverability/">email deliverability</a> after you understand each record.</p>
      <p>Teams often optimise one layer — perfect DMARC while PTR is wrong — and still see spam placement. Verify holistically. SaaS mail hides complexity; self-hosted mail exposes every gap immediately in bounces and deferrals.</p>

      <h2>The five records</h2>
      <ul>
        <li><strong>MX</strong> — where inbound mail for the domain should be delivered.</li>
        <li><strong>SPF</strong> — which servers may send mail using your domain in the envelope path.</li>
        <li><strong>DKIM</strong> — public key for verifying signatures on outbound mail.</li>
        <li><strong>DMARC</strong> — policy for receivers when SPF/DKIM do not align.</li>
        <li><strong>PTR</strong> — reverse DNS for a sending IP; expected for many MTA filters.</li>
      </ul>

      <h2>MX record — receiving email</h2>
      <p>MX records point to mail hosts with priorities. You need at least one reachable host accepting SMTP for your domain. Misconfigured MX means mail queues or bounces. Reference: <a href="/dns/mx-record/">MX DNS</a>.</p>

      <h2>SPF record — authorising senders</h2>
      <p>TXT at the domain used in SPF evaluation (often the envelope domain). Single string, watch lookup limits. <a href="/dns/spf-record/">SPF DNS</a> and <a href="/learn/spf/">SPF guide</a>.</p>

      <h2>DKIM record — signing email</h2>
      <p>TXT at <code>selector._domainkey</code>. Publish complete keys; partial keys fail open verification. <a href="/dns/dkim-record/">DKIM DNS</a>.</p>

      <h2>DMARC record — enforcing policy</h2>
      <p>TXT at <code>_dmarc</code>. Start with <code>p=none</code> and reporting; tighten when aligned. <a href="/dns/dmarc-record/">DMARC DNS</a> and <a href="/learn/dmarc/">DMARC guide</a>.</p>

      <h2>PTR record — reverse DNS</h2>
      <p>For your sending IP, PTR should resolve to a hostname that forward-resolves back to the same IP. Self-hosted mail depends on this. <a href="/dns/ptr-record/">PTR DNS</a>.</p>

      <h2>How they work together</h2>
      <p>Inbound: MX directs mail to your provider. Outbound: SPF authorizes sending IPs/includes; DKIM signs content; DMARC ties policy to the From: domain alignment; PTR supports IP-level trust. A gap in any layer surfaces as spam placement or rejects — not always “SMTP 550.”</p>
      <p>Example: marketing sends through an ESP with DKIM pass but From: uses the root domain while SPF only covers the ESP’s bounce domain — DMARC may fail alignment until you align signatures or SPF. Another: transactional mail from a subdomain without its own SPF/DKIM while strict policies expect the parent — test every stream.</p>
      <p>Google and Yahoo bulk-sender rules pushed teams to publish at least baseline DMARC even at <code>p=none</code>. That does not replace SPF/DKIM quality; it forces visibility via <code>rua</code> reporting so you cannot ignore drift.</p>

      <h2>How to verify all five at once</h2>
      <p>Use <a href="https://domainpreflight.dev/">DNS Preflight</a> — it walks MX, SPF, DKIM, DMARC, and PTR-related checks with a health score so you do not chase five tabs.</p>

""" + tool_cta(
        "https://domainpreflight.dev/",
        "Run DNS Preflight →",
        "Validate MX, SPF, DKIM, DMARC, and PTR-related signals in one pass.",
    )

BODIES["domain-security"] = r"""
      <p>Your domain is the root of trust for email, your website, APIs, and every DNS record attackers probe. Lose it to expiry or hijack — you lose everything at once. This guide covers expiry, transfer lock, WHOIS exposure, auth codes, and monitoring. Vocabulary: <a href="/glossary/whois/">WHOIS</a>, <a href="/glossary/domain-expiry/">domain expiry</a>. Related reading: <a href="/blog/domain-expiry-infrastructure-failure/">infrastructure failure</a> when renewals slip.</p>
      <p>Security teams focus on application pentests while the domain expires on a corporate card that expired. Operations owns DNS — but procurement owns the registrar. Bridge that gap with joint accountability.</p>

      <h2>The three domain security risks</h2>
      <p><strong>Expiry</strong> — accidental non-renewal. <strong>Unauthorised transfer</strong> — attacker obtains auth code and moves the domain. <strong>WHOIS data exposure</strong> — personal contact data used for phishing or takeover prep. All three are preventable with process.</p>

      <h2>Domain expiry — the preventable disaster</h2>
      <p>Enable auto-renew. Keep a valid payment method on file. Set calendar reminders ahead of registry expiry. Monitor expiry dates — especially portfolios with acquired brands. Read <a href="/blog/domain-expiry-infrastructure-failure/">domain expiry infrastructure failure</a> and case notes from <a href="/incidents/domain-expiry-outages/">domain expiry outages</a>.</p>

      <h2>Transfer lock — preventing hijacking</h2>
      <p>Registrar lock blocks outbound transfers without explicit unlock + auth code. Leave lock on unless you are intentionally moving registrars. Verify status in your registrar control panel after any contact change.</p>

      <h2>WHOIS privacy — protecting your data</h2>
      <p>Privacy/redaction hides personal addresses and phone numbers from public WHOIS. It reduces phishing risk against domain admins. It is not a substitute for DNS security — but it removes one reconnaissance channel.</p>

      <h2>Auth codes and transfers</h2>
      <p>Auth codes (EPP codes) prove transfer intent. Never share them in chat, tickets, or email with unverified parties. Treat them like passwords. If leaked, rotate/regenerate and re-lock the domain.</p>
      <p>Social engineering against support desks is common: attacker pretends to be the CEO, rushes a “DNS emergency,” and tries to extract codes. Train support to use out-of-band verification and ticket workflows — never instant messaging.</p>

      <h2>Monitoring your domain health</h2>
      <p>Run periodic WHOIS checks for registrar, expiry, lock state, and nameservers. Use <a href="https://domainpreflight.dev/whois/">DomainPreflight WHOIS</a> for a quick read on risk tier and expiry.</p>
      <p>After mergers, verify billing contacts still route to active inboxes. After card renewals, spot-check auto-renew flags. Incident retrospectives from <a href="/incidents/domain-expiry-outages/">domain expiry outages</a> read like avoidable tragedies — because they are.</p>
      <p>Pair registrar hygiene with <a href="/learn/dns-for-email/">email DNS</a> reviews: losing a domain invalidates every certificate and mail path simultaneously. No amount of SPF tuning recovers a name someone else registered.</p>

""" + tool_cta(
        "https://domainpreflight.dev/whois/",
        "Open WHOIS lookup →",
        "See expiry, registrar, and risk signals before you get surprised by renewal.",
    )

BODIES["subdomain-security"] = r"""
      <p>Subdomains are cheap to create and expensive to forget. A CNAME to a SaaS host you no longer own is a dangling record — attackers can claim the target and serve content on your domain. This guide explains dangling DNS, takeover mechanics, and cleanup. Core term: <a href="/glossary/subdomain-takeover/">subdomain takeover</a>; <a href="/glossary/cname-record/">CNAME</a> mechanics.</p>

      <h2>What is a dangling DNS record?</h2>
      <p>A record that still points to a resource you deleted — commonly a CNAME to <code>github.io</code>, <code>azurewebsites.net</code>, <code>herokuapp.com</code>, or similar. The cloud name is still delegatable; your DNS still routes traffic to it.</p>

      <h2>How subdomain takeover happens</h2>
      <p>Attacker enumerates your subdomains (cert transparency, search engines, brute force). They see a CNAME to a provider they can control. They claim the app name on the provider. Traffic intended for your subdomain now hits their content — often phishing or malware. Real cases: <a href="/incidents/subdomain-takeover-cases/">subdomain takeover cases</a>.</p>

      <h2>Which services are vulnerable</h2>
      <p>Common: GitHub Pages, S3 static hosting, Heroku, Netlify, Azure App Service — any platform where a name can be (re)registered after you release it. Your DNS record is the permanent switchboard.</p>

      <h2>How attackers use taken subdomains</h2>
      <p>Phishing against your customers, malware distribution, credential harvesting, and SEO abuse. The domain trust is yours; the payload is theirs.</p>

      <h2>How to find your dangling records</h2>
      <p>Inventory subdomains, resolve each CNAME, check if the target exists and is yours. Automate with <a href="https://domainpreflight.dev/dangling/">DomainPreflight Dangling Records</a> — discovery via certificate logs plus fingerprint checks.</p>

      <h2>The fix — delete the record</h2>
      <p>Remove the CNAME or replace it with a controlled service. If you still need the hostname, provision the service first, then point DNS. No half measures.</p>

      <h2>Defensive DNS hygiene</h2>
      <p>Deprovisioning checklist: cancel SaaS, delete app, remove DNS, verify resolution. Quarterly audits. Read <a href="/blog/subdomain-takeover-dangling-cnames/">dangling CNAMEs</a> for patterns.</p>
      <p>Engineers rotate projects faster than DNS ages out. A marketing microsite on Netlify abandoned in 2023 can still have a CNAME in 2026 — and certificate transparency keeps the hostname discoverable forever. Treat DNS like code: review diffs, blame owners, remove dead routes.</p>
      <p>Combine this guide with <a href="/learn/brand-protection/">brand protection</a> — takeover undermines customer trust even when DMARC is perfect on the root domain.</p>

""" + tool_cta(
        "https://domainpreflight.dev/dangling/",
        "Run Dangling Records →",
        "Discover subdomains and flag CNAMEs that point to abandoned services.",
    )

BODIES["dmarc-reporting"] = r"""
      <p>Aggregate reports are daily XML digests of who sent mail using your domain and whether SPF/DKIM passed and aligned. They are the feedback loop for DMARC policy. This guide covers mailboxes, XML structure, reading tools, triage, and forensic options. See <a href="/glossary/dmarc-aggregate-report/">aggregate reports</a> and <a href="/glossary/dmarc-policy/">policy</a>.</p>

      <h2>What DMARC reports are</h2>
      <p>Major receivers (Google, Microsoft, Yahoo, etc.) send compressed XML to <code>rua=</code> addresses. Each file contains records per source IP with auth results, DKIM domains, SPF domains, and disposition if policy applied.</p>

      <h2>How to start receiving reports</h2>
      <p>Add <code>rua=mailto:dmarc@yourdomain.com</code> to your DMARC TXT. Confirm the address receives mail and is not spam-filtered into oblivion. Reports usually arrive within 24 hours of first publish.</p>

      <h2>What the XML contains</h2>
      <p>High level: <code>report_metadata</code> (org, date range), <code>policy_published</code> (your p=, pct, alignment), and <code>record</code> rows with <code>source_ip</code>, <code>count</code>, and <code>policy_evaluated</code>. Each record includes <code>auth_results</code> for SPF and DKIM. You do not need to love XML — you need a workflow.</p>

      <h2>How to read reports without decoding XML</h2>
      <p>Use <a href="https://domainpreflight.dev/dmarc/">DomainPreflight DMARC Report Analyzer</a> — paste XML, get charts and tables. Pair with <a href="/blog/how-to-read-dmarc-report/">how to read a DMARC report</a> on the blog.</p>

      <h2>What to look for</h2>
      <p>Green paths: aligned SPF or DKIM with your From domain. Orange: partial passes — investigate alignment. Red: clear spoofing sources — plan blocks after legit mail is clean. Map IPs to owners (whois, ASN, ESP dashboards).</p>

      <h2>Acting on what you find</h2>
      <p>Fix legitimate senders first — add includes, DKIM, or correct From domains. Then tighten DMARC using guidance from <a href="/fix/dmarc/">DMARC fixes</a> and the <a href="/learn/dmarc/">main DMARC guide</a>.</p>

      <h2>How often to check</h2>
      <p>Weekly during rollout; monthly when stable. Re-check after any new vendor sends mail.</p>

      <h2>Forensic reports (ruf=)</h2>
      <p>Optional failure samples (<code>ruf=mailto:...</code>) — many providers suppress or redact for privacy. Treat aggregate as primary; forensic as bonus.</p>
      <p>When leadership asks “are we spoofed?”, export a week of XML, run the analyzer, and show top IPs by volume. Pair numbers with <a href="/glossary/dmarc-policy/">policy</a> context — <code>p=none</code> means observation, not protection. The <a href="/learn/dmarc/">DMARC setup guide</a> explains when to move policy forward.</p>
      <p>Reporting volume can spike after DNS changes — not every spike is abuse; some are misconfigured senders waking up. Differentiate by ASN and known ESP ranges before panicking.</p>

""" + tool_cta(
        "https://domainpreflight.dev/dmarc/",
        "Open DMARC Report Analyzer →",
        "Turn raw aggregate XML into a readable summary in seconds.",
    )

BODIES["self-hosted-email"] = r"""
      <p>Self-hosting mail in 2026 means fighting port blocks, IP reputation, and mandatory authentication. This guide covers provider choice, PTR, SPF, DKIM, DMARC, warm-up, and monitoring. See <a href="/glossary/ptr-record/">PTR</a>, <a href="/glossary/rdns/">rDNS</a>, and <a href="/glossary/email-deliverability/">deliverability</a>.</p>

      <h2>Why self-hosted email is hard in 2026</h2>
      <p>Residential and many cloud IPs block outbound 25. Large receivers require aligned SPF/DKIM/DMARC and often sane PTR. New IPs have no reputation — warm-up is mandatory. Expect to spend engineering time on TLS, queues, and blocklists.</p>

      <h2>Choosing a hosting provider</h2>
      <p>You need outbound SMTP allowed (or smart host), ability to set PTR for your IP, and ideally clean IP space. Common VPS providers allow port 25 with policy; hyperscalers often require unblock tickets. Verify before you build.</p>

      <h2>PTR record — the first thing to set</h2>
      <p>Ask your provider for reverse DNS pointing to your mail hostname (e.g. <code>mail.example.com</code>). Create matching A/AAAA records. PTR mismatch → spam or rejection. <a href="/dns/ptr-record/">PTR DNS</a>.</p>

      <h2>SPF for self-hosted</h2>
      <p>Include your IP with <code>ip4:</code>/<code>ip6:</code> and any ESP relays. Single SPF record. <a href="/learn/spf/">SPF guide</a>.</p>

      <h2>DKIM for Postfix/Exim/Dovecot</h2>
      <p>Generate 2048-bit keys, configure OpenDKIM/rspamd, publish selector TXT. Test with swaks or mail clients. Verify headers show <code>dkim=pass</code>.</p>

      <h2>DMARC for self-hosted</h2>
      <p>Publish <code>p=none</code> with <code>rua=</code>, align sending domains, then tighten. Same process as hosted mail — <a href="/learn/dmarc/">DMARC guide</a>.</p>

      <h2>IP warm-up</h2>
      <p>Start with low daily volume, increase gradually, watch bounces and spam folder rates. Takes weeks. Patience beats throttling.</p>

      <h2>Ongoing monitoring</h2>
      <p>Check blocklists, DMARC reports, and TLS expiry. Errors: <a href="/error/ptr-mismatch/">PTR mismatch</a>, <a href="/error/blacklisted-ip/">blacklisted IP</a>. Use <a href="https://domainpreflight.dev/">DNS Preflight</a> for DNS-side checks.</p>
      <p>Queue monitoring matters: deferred mail that expires hurts reputation. Bounce handling matters: repeated sends to bad addresses flag you as negligent. Self-hosted operators wear SPF, DKIM, DMARC, <em>and</em> deliverability engineering hats — budget time accordingly.</p>
      <p>Cross-reference <a href="/learn/spf/">SPF</a>, <a href="/learn/dkim/">DKIM</a>, and <a href="/learn/dmarc/">DMARC</a> guides when upgrading stack components; one Postfix update can change signing defaults.</p>

""" + tool_cta(
        "https://domainpreflight.dev/",
        "Run DNS Preflight →",
        "Check PTR, SPF, DKIM, DMARC, and related DNS for your sending IP and domain.",
    )

BODIES["brand-protection"] = r"""
      <p>Brand protection is not a single product — it is DMARC enforcement, monitoring for lookalike domains, and cleaning up DNS attack surface. This guide covers spoofing defense, typosquats, and dangling subdomains. Terms: <a href="/glossary/typosquatting/">typosquatting</a>, <a href="/glossary/subdomain-takeover/">subdomain takeover</a>, <a href="/glossary/email-spoofing/">email spoofing</a>. If you only fix one channel this quarter, pick DMARC alignment — it raises the cost of spoofing at scale.</p>
      <p>Security awareness training helps employees spot phish; DMARC and DNS hygiene stop messages from looking legitimate in the first place. Combine both — neither replaces the other.</p>

      <h2>The three brand attack surfaces</h2>
      <p><strong>Spoofing</strong> — forged From: on your domain. <strong>Typosquats</strong> — register lookalike domains for phishing. <strong>Dangling subdomains</strong> — host content on your namespace via forgotten CNAMEs.</p>

      <h2>Stopping domain spoofing with DMARC</h2>
      <p>Publish SPF and DKIM aligned to your From domain, then move DMARC to <code>p=reject</code>. That removes spoofed mail that fails alignment at participating receivers. Full playbook: <a href="/learn/dmarc/">DMARC guide</a>.</p>
      <p>Spoofing volume often drops in reports before users notice fewer phish — track both metrics. When spoof attempts approach zero and legitimate mail stays aligned, you have evidence for auditors and executives that the control works.</p>

      <h2>Finding lookalike domains</h2>
      <p>Run <a href="https://domainpreflight.dev/typosquat/">DomainPreflight Typosquat Monitor</a> — 30–50 variants via live DNS. Decide which to register defensively. Incidents: <a href="/incidents/typosquat-phishing-domains/">typosquat phishing domains</a>.</p>

      <h2>Subdomain takeover risk</h2>
      <p>Audit CNAMEs with <a href="https://domainpreflight.dev/dangling/">Dangling Records</a>. Read <a href="/blog/subdomain-takeover-dangling-cnames/">dangling CNAMEs</a> and <a href="/learn/subdomain-security/">subdomain security guide</a>.</p>

      <h2>WHOIS privacy</h2>
      <p>Reduce attacker recon on your admin contacts. Complements technical controls — does not replace them.</p>
      <p>Public WHOIS data feeds spear-phishing: names, phones, and roles. Redaction slows down attackers who script reconnaissance — buy time for your users to report suspicious mail.</p>

      <h2>Building a brand protection checklist</h2>
      <p>Monthly: DMARC reports review, typosquat scan, dangling DNS scan, registrar lock/expiry check. Quarterly: tabletop phishing exercise. Tie tools together at <a href="https://domainpreflight.dev/">domainpreflight.dev</a>.</p>
      <p>Executive dashboards: spoof volume down, lookalike domains registered by you vs unknowns, dangling records at zero. When any metric regresses, assign an owner and a due date — brand defence rots without accountability.</p>
      <p>Legal may ask for defensive registrations — finance may push back. Frame cost as incident prevention: one successful phishing campaign exceeds decades of typo domains. Cite <a href="/incidents/typosquat-phishing-domains/">typosquat incidents</a> when building the business case.</p>
      <p>Technical minimum: <a href="/learn/dmarc/">DMARC to reject</a>, <a href="/learn/subdomain-security/">subdomain hygiene</a>, and continuous typosquat monitoring — three controls, mostly process.</p>

""" + tool_cta(
        "https://domainpreflight.dev/",
        "Open DomainPreflight →",
        "Run DNS Preflight, Typosquat Monitor, and Dangling Records from one hub.",
    )

