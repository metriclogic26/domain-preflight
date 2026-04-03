# DomainPreflight

Find security risks hiding in your domain —
before attackers do.

DomainPreflight is a free, browser-based suite
of domain security and email authentication tools.
No signup. No backend. Nothing leaves your browser.

## Live

**[domainpreflight.dev](https://domainpreflight.dev)**

## Tools

| Tool | What it does |
|---|---|
| **DNS Preflight** | SPF, DKIM, DMARC, PTR, IP reputation — full pre-send audit |
| **Email Deliverability** | IP blacklist checks, AbuseIPDB reputation, email header analyzer |
| **WHOIS / Expiry** | Domain expiry countdown, registrar info, risk tiers |
| **Dangling Records** | Subdomain takeover detection via certificate transparency logs |
| **Typosquat Monitor** | Lookalike domain detection with live DNS resolution |
| **DMARC Report Analyzer** | Paste XML aggregate reports — get visual breakdown instantly |
| **DNS Propagation** | Check propagation across 5 resolvers in real time |

## Why DomainPreflight?

Most tools are reactive — you use them
when email is already bouncing or a
subdomain has already been taken over.

DomainPreflight is the proactive check:

- **Dangling Records** — browser-based subdomain
  takeover detection. No CLI, no Python install.
  Pulls from cert logs + can-i-take-over-xyz fingerprints.
- **Typosquat Monitor** — browser version of dnstwist.
  Generates lookalikes, checks which ones resolve live.
- **Alignment Engine** — detects provider-specific
  DMARC alignment failures for 10 ESPs including
  SendGrid, Mailgun, Microsoft 365, Google Workspace.
- **Copy-paste fixes** — every audit ships the exact
  DNS record to paste. Not just a grade.

## Stack

- Vanilla HTML/CSS/JS — zero frameworks
- DNS-over-HTTPS (Cloudflare DoH)
- Cloudflare Worker for IP reputation proxy
- No backend, no database, no tracking
- Deployed on Vercel

## Run Locally
```bash
git clone https://github.com/metriclogic26/domain-preflight.git
cd domain-preflight
python3 -m http.server 3000
```

Open http://localhost:3000

## Part of MetricLogic

| Suite | What it does |
|---|---|
| [ConfigClarity.dev](https://configclarity.dev) | Server & DevOps audit tools |
| [DomainPreflight.dev](https://domainpreflight.dev) | Domain security & email authentication |
| [PackageFix.dev](https://packagefix.dev) | Dependency vulnerability scanner |

## License

MIT © MetricLogic —
the moat is the live data fetch, not the code.
