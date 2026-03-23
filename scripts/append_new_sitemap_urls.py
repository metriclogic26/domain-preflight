#!/usr/bin/env python3
"""Append Batch 1–4 URLs to sitemap.xml if missing."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "sitemap.xml"

BASE = "https://domainpreflight.dev"

NEW_URLS: list[tuple[str, str, str]] = []
# (path, changefreq, priority)

# DNS providers (25)
NEW_URLS.append(("/dns/provider/", "weekly", "0.85"))
for p in (
    "cloudflare-dns",
    "aws-route53",
    "google-cloud-dns",
    "azure-dns",
    "digitalocean-dns",
):
    NEW_URLS.append((f"/dns/provider/{p}/", "weekly", "0.85"))
    for t in ("dmarc-setup", "spf-record", "dkim-record", "propagation-times"):
        NEW_URLS.append((f"/dns/provider/{p}/{t}/", "weekly", "0.8"))

# Email providers (30)
NEW_URLS.append(("/email-providers/", "weekly", "0.85"))
for p in (
    "sendgrid",
    "mailgun",
    "google-workspace",
    "microsoft-365",
    "postmark",
    "amazon-ses",
    "mailchimp",
    "klaviyo",
    "hubspot",
    "brevo",
):
    NEW_URLS.append((f"/email-providers/{p}/", "weekly", "0.85"))
    for t in ("spf-setup", "dkim-setup"):
        NEW_URLS.append((f"/email-providers/{p}/{t}/", "weekly", "0.8"))

# Blog (12)
for slug in (
    "dmarc-reject-safe",
    "ptr-record-email-delivery",
    "dmarc-mailchimp-setup",
    "spf-include-explained",
    "email-authentication-checklist",
    "dmarc-subdomain-policy",
    "ip-warmup-guide",
    "check-dmarc-from-terminal",
    "google-postmaster-tools",
    "bulk-sender-requirements-2024",
    "dkim-rotation-guide",
    "domain-registrar-comparison",
):
    NEW_URLS.append((f"/blog/{slug}/", "weekly", "0.75"))

# Glossary (15)
for slug in (
    "bounce-rate",
    "spam-trap",
    "email-header",
    "return-path",
    "dkim-signature",
    "smtp",
    "email-spoofing-vs-phishing",
    "dnsbl",
    "email-warm-up",
    "list-unsubscribe",
    "spf-alignment",
    "dkim-alignment",
    "ip-reputation",
    "envelope-sender",
    "feedback-loop",
):
    NEW_URLS.append((f"/glossary/{slug}/", "monthly", "0.7"))


def main() -> None:
    text = ROOT.read_text(encoding="utf-8")
    if "/dns/provider/cloudflare-dns/dmarc-setup/" in text:
        print("Sitemap already contains new URLs — skip")
        return
    blocks = []
    for path, cf, pr in NEW_URLS:
        loc = BASE + path
        blocks.append(
            f"""  <url>
    <loc>{loc}</loc>
    <changefreq>{cf}</changefreq>
    <priority>{pr}</priority>
  </url>"""
        )
    insert = "\n".join(blocks) + "\n"
    text = text.replace("</urlset>", insert + "</urlset>")
    ROOT.write_text(text, encoding="utf-8")
    print("Appended", len(NEW_URLS), "URLs to sitemap.xml")


if __name__ == "__main__":
    main()
