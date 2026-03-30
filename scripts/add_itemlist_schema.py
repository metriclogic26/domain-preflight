#!/usr/bin/env python3
"""Insert schema.org ItemList (step-by-step) JSON-LD into HTML pages."""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STEP_BY_STEP = "Step by Step"


class _TextHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.chunks: list[str] = []

    def handle_data(self, data: str) -> None:
        self.chunks.append(data)


def strip_tags_norm(fragment: str) -> str:
    p = _TextHTMLParser()
    p.feed(fragment)
    p.close()
    return " ".join(" ".join(p.chunks).split())


def extract_howto_steps(html: str) -> list[str]:
    steps: list[str] = []
    pos = 0
    needle = '<div class="howto-step"'
    while True:
        idx = html.find(needle, pos)
        if idx == -1:
            break
        depth = 0
        k = idx
        while k < len(html):
            if html[k : k + 4] == "<div":
                depth += 1
                k += 4
                continue
            if html[k : k + 6] == "</div>":
                depth -= 1
                k += 6
                if depth == 0:
                    inner = html[html.find(">", idx) + 1 : k - 6]
                    text = strip_tags_norm(inner)
                    text = re.sub(
                        r"^Step\s+\d+(?:\s*\([^)]*\))?\s*", "", text, flags=re.I
                    )
                    if text:
                        steps.append(text)
                    pos = k
                    break
                continue
            k += 1
        else:
            break
    return steps


def extract_ol_steps(html: str) -> list[str]:
    m = re.search(r'<ol class="how-to-use-steps">(.*?)</ol>', html, re.DOTALL)
    if not m:
        return []
    block = m.group(1)
    items = re.findall(r"<li[^>]*>(.*?)</li>", block, re.DOTALL)
    return [strip_tags_norm(x) for x in items if strip_tags_norm(x)]


def extract_title_tool(html: str) -> str:
    m = re.search(r"<title>([^<]+)</title>", html)
    if m:
        t = m.group(1).replace("&amp;", "&").strip()
        return re.sub(r"\s*[—–-]\s*DomainPreflight\s*$", "", t).strip()
    return "DomainPreflight"


def extract_h1(html: str) -> str | None:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
    if m:
        return strip_tags_norm(m.group(1))
    return None


def pick_list_name(path: Path, html: str, tool_name: str | None) -> str:
    if tool_name:
        return tool_name
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("learn/") or rel.startswith("fix/"):
        return extract_h1(html) or extract_title_tool(html)
    return extract_title_tool(html) or extract_h1(html) or "DomainPreflight"


def build_itemlist(tool_name: str, steps: list[str]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{tool_name} — {STEP_BY_STEP}",
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "numberOfItems": len(steps),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": s}
            for i, s in enumerate(steps)
        ],
    }


def itemlist_script(obj: dict) -> str:
    return (
        "  <script type=\"application/ld+json\">\n"
        + json.dumps(obj, indent=2, ensure_ascii=False)
        + "\n  </script>\n"
    )


def strip_existing_step_itemlist(html: str) -> str:
    """Remove ItemList blocks we added (name ends with — Step by Step)."""
    parts: list[str] = []
    i = 0
    while i < len(html):
        start = html.find('<script type="application/ld+json">', i)
        if start == -1:
            parts.append(html[i:])
            break
        parts.append(html[i:start])
        end = html.find("</script>", start)
        if end == -1:
            parts.append(html[start:])
            break
        inner = html[start + len('<script type="application/ld+json">'): end].strip()
        drop = False
        try:
            data = json.loads(inner)
            if (
                data.get("@type") == "ItemList"
                and STEP_BY_STEP in (data.get("name") or "")
            ):
                drop = True
        except json.JSONDecodeError:
            pass
        if not drop:
            parts.append(html[start : end + len("</script>")])
        i = end + len("</script>")
        while i < len(html) and html[i] in "\n\r":
            i += 1
    return (
        "".join(parts).replace(
            '</script>  <script type="application/ld+json">',
            '</script>\n  <script type="application/ld+json">',
        )
    )


def insert_after_last_jsonld(html: str, snippet: str) -> str:
    last_end = 0
    search_from = 0
    while True:
        s = html.find('<script type="application/ld+json">', search_from)
        if s == -1:
            break
        e = html.find("</script>", s)
        if e == -1:
            break
        last_end = e + len("</script>")
        search_from = e + 1
    if last_end == 0:
        print("  SKIP: no application/ld+json found", file=sys.stderr)
        return html
    tail = html[last_end:]
    return html[:last_end] + "\n" + snippet + tail


def process_file(path: Path, tool_name: str | None = None) -> bool:
    html = path.read_text(encoding="utf-8")
    html = strip_existing_step_itemlist(html)
    steps = extract_howto_steps(html)
    if not steps:
        steps = extract_ol_steps(html)
    if not steps:
        print(f"  SKIP {path.relative_to(ROOT)}: no steps found", file=sys.stderr)
        path.write_text(html, encoding="utf-8")
        return False
    name = pick_list_name(path, html, tool_name)
    obj = build_itemlist(name, steps)
    snippet = itemlist_script(obj)
    new_html = insert_after_last_jsonld(html, snippet)
    if new_html == html:
        path.write_text(html, encoding="utf-8")
        return False
    path.write_text(new_html, encoding="utf-8")
    return True


def main() -> None:
    tool_paths = [
        ROOT / "index.html",
        ROOT / "email" / "index.html",
        ROOT / "whois" / "index.html",
        ROOT / "dangling" / "index.html",
        ROOT / "typosquat" / "index.html",
        ROOT / "dmarc" / "index.html",
        ROOT / "propagation" / "index.html",
    ]
    learn_guides = sorted((ROOT / "learn").glob("*/index.html"))
    learn_guides = [p for p in learn_guides if p != ROOT / "learn" / "index.html"]

    fix_paths: list[Path] = []
    for sub in ("dmarc", "spf", "dkim"):
        fix_paths.extend(sorted((ROOT / "fix" / sub).glob("**/index.html")))

    all_paths = tool_paths + learn_guides + fix_paths
    n = 0
    for p in all_paths:
        if not p.is_file():
            continue
        extra = "DNS Preflight Checker" if p.resolve() == (ROOT / "index.html").resolve() else None
        if process_file(p, extra):
            n += 1
            print("+", p.relative_to(ROOT))
    print(f"Updated {n} files", file=sys.stderr)


if __name__ == "__main__":
    main()
