#!/usr/bin/env python3
"""
Sync application/ld+json FAQPage (acceptedAnswer.text), HowTo (step.text),
and DefinedTerm (description) with visible HTML.
"""
from __future__ import annotations

import json
import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_faq_pairs(html: str) -> list[tuple[str, str]]:
    m = re.search(
        r'<section class="faq-section"[^>]*>(.*?)</section>',
        html,
        re.DOTALL | re.IGNORECASE,
    )
    if not m:
        return []
    section = m.group(1)
    pairs: list[tuple[str, str]] = []
    for block in re.finditer(
        r"<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>", section, re.DOTALL | re.IGNORECASE
    ):
        q = strip_tags(block.group(1))
        a = strip_tags(block.group(2))
        if q and q.lower() != "faq":
            pairs.append((q, a))
    return pairs


def extract_howto_step_texts(html: str) -> list[str]:
    texts: list[str] = []
    for m in re.finditer(
        r'<div class="howto-step"[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE
    ):
        texts.append(strip_tags(m.group(1)))
    return texts


def extract_glossary_first_paragraph(html: str) -> str | None:
    m = re.search(
        r"<article[^>]*>.*?"
        r'(?:<p class="hero-label"[^>]*>.*?</p>\s*)?'
        r"<h1[^>]*>.*?</h1>\s*"
        r"<p[^>]*>(.*?)</p>",
        html,
        re.DOTALL | re.IGNORECASE,
    )
    if not m:
        return None
    return strip_tags(m.group(1))


def update_faqpage_text_only(obj: dict, pairs: list[tuple[str, str]]) -> bool:
    if obj.get("@type") != "FAQPage":
        return False
    me = obj.get("mainEntity")
    if not isinstance(me, list):
        return False
    changed = False
    n = min(len(me), len(pairs))
    for i in range(n):
        ent = me[i]
        if not isinstance(ent, dict):
            continue
        aa = ent.get("acceptedAnswer")
        if not isinstance(aa, dict):
            continue
        new_text = pairs[i][1]
        if aa.get("text") != new_text:
            aa["text"] = new_text
            changed = True
    if len(me) != len(pairs):
        print(
            f"  WARN FAQ count mismatch: schema {len(me)} vs HTML {len(pairs)}",
            file=sys.stderr,
        )
    return changed


def update_howto(obj: dict, steps: list[str]) -> bool:
    if obj.get("@type") != "HowTo":
        return False
    st = obj.get("step")
    if not isinstance(st, list):
        return False
    changed = False
    n = min(len(st), len(steps))
    for i in range(n):
        step = st[i]
        if not isinstance(step, dict):
            continue
        if step.get("text") != steps[i]:
            step["text"] = steps[i]
            changed = True
    if len(st) != len(steps):
        print(
            f"  WARN HowTo step count: schema {len(st)} vs HTML {len(steps)}",
            file=sys.stderr,
        )
    return changed


def update_defined_term(obj: dict, desc: str) -> bool:
    if obj.get("@type") != "DefinedTerm":
        return False
    if obj.get("description") != desc:
        obj["description"] = desc
        return True
    return False


def format_json(obj: dict, raw: str) -> str:
    """Match original formatting: minified vs pretty."""
    sample = raw.strip()
    if "\n" in sample[:400]:
        return json.dumps(obj, ensure_ascii=False, indent=2)
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def process_file(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    faq_pairs = extract_faq_pairs(html)
    howto_steps = extract_howto_step_texts(html)
    glossary_p = extract_glossary_first_paragraph(html)

    needle = '<script type="application/ld+json">'
    pos = 0
    out: list[str] = []
    file_changed = False

    while True:
        i = html.find(needle, pos)
        if i == -1:
            out.append(html[pos:])
            break
        out.append(html[pos:i])
        start_content = i + len(needle)
        j = html.find("</script>", start_content)
        if j == -1:
            out.append(html[i:])
            break
        raw = html[start_content:j]
        raw_strip = raw.strip()
        try:
            obj = json.loads(raw_strip)
        except json.JSONDecodeError:
            out.append(html[i : j + len("</script>")])
            pos = j + len("</script>")
            continue

        changed = False
        if isinstance(obj, dict):
            t = obj.get("@type")
            if t == "FAQPage" and faq_pairs:
                if update_faqpage_text_only(obj, faq_pairs):
                    changed = True
            elif t == "HowTo" and howto_steps:
                if update_howto(obj, howto_steps):
                    changed = True
            elif t == "DefinedTerm" and glossary_p:
                if update_defined_term(obj, glossary_p):
                    changed = True

        if changed:
            file_changed = True
            new_json = format_json(obj, raw)
            # Preserve original newline after opening script tag
            out.append(needle + "\n  " + new_json + "\n  ")
            out.append("</script>")
        else:
            out.append(html[i : j + len("</script>")])
        pos = j + len("</script>")

    if file_changed:
        path.write_text("".join(out), encoding="utf-8")
    return file_changed


def main():
    changed_files: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if "node_modules" in path.parts:
            continue
        try:
            if process_file(path):
                changed_files.append(path)
                print(path.relative_to(ROOT))
        except Exception as e:
            print(f"ERROR {path}: {e}", file=sys.stderr)
            raise
    print(f"\nUpdated {len(changed_files)} files.", file=sys.stderr)


if __name__ == "__main__":
    main()
