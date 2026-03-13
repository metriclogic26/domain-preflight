# DomainPreflight

> Audit your DNS before you deploy it — not after your email stops working.

DomainPreflight is a free, browser-based DNS pre-flight checker. 
Check PTR/rDNS, IP reputation, SPF, DKIM, and DMARC in seconds — 
before you send a single email. No sending required. No signup. 
Nothing leaves your browser.

## Live Tool

**[domainpreflight.dev](https://domainpreflight.dev)**

## Why DomainPreflight?

Existing tools like MxToolbox are reactive — you use them when 
email is already bouncing. DomainPreflight is the proactive 
pre-flight check.

- **PTR / rDNS** — reverse lookup + forward match verification
- **IP Reputation** — Spamhaus ZEN, SpamCop, Barracuda blocklists
- **SPF** — recursive lookup counter, PermError detection, +all trap
- **DKIM** — 15+ common selectors, key strength validation
- **DMARC** — policy level, rua= check, upgrade path suggestions
- **Health Score** — 0–100 with animated ring and action cards
- **Shareable URLs** — ?domain=example.com auto-runs on load

## Stack

- Vanilla HTML/CSS/JS — zero frameworks
- DNS-over-HTTPS (Cloudflare + Google DoH fallback)
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

Also try **[ConfigClarity.dev](https://configclarity.dev)** — 
server & DevOps audit tools.

## License

MIT © MetricLogic

