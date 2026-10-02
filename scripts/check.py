#!/usr/bin/env python3
"""Check the generated site's routes, local assets, language peers and theme contrast."""

from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import json, re, sys

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
errors = []


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = []
        self.h1 = 0
        self.lang = ""
        self.alternates = []
        self.tags = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if tag == "html":
            self.lang = a.get("lang", "")
        if tag == "h1":
            self.h1 += 1
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "img" and "alt" not in a:
            errors.append("Image without alt")
        for key in ["src", "href"]:
            if a.get(key):
                self.refs.append(a[key])
        if tag == "link" and a.get("rel") == "alternate":
            self.alternates.append(a.get("hreflang"))


def require(test, message):
    if not test:
        errors.append(message)


def luminance(h):
    rgb = [int(h[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    values = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
    return sum(a * b for a, b in zip(values, [0.2126, 0.7152, 0.0722]))


manifest = json.loads((ROOT / "route-manifest.json").read_text())
parsed = {}
for f in DIST.rglob("*.html"):
    d = Document()
    text = f.read_text(encoding="utf-8")
    d.feed(text)
    parsed[f.resolve()] = d
    require(not re.search(r"@@|__TURBINE__|__LOGO__", text), f"Unresolved marker: {f}")
    require(len(d.ids) == len(set(d.ids)), f"Duplicate IDs: {f}")
    require("<title>" in text, f"No title: {f}")
    require(
        not re.search(r'<script[^>]*src=["\']https?://', text),
        f"Unexpected remote script: {f}",
    )
for f, d in parsed.items():
    for ref in d.refs:
        p = urlsplit(ref)
        if p.scheme or p.netloc:
            continue
        target = (
            (
                (DIST / unquote(p.path).lstrip("/"))
                if p.path.startswith("/")
                else (f.parent / unquote(p.path))
            ).resolve()
            if p.path
            else f
        )
        if p.path.endswith("/"):
            target /= "index.html"
        require(target.exists(), f"Missing target: {f.relative_to(DIST)} → {ref}")
        if p.fragment and target in parsed:
            require(
                unquote(p.fragment) in parsed[target].ids,
                f"Missing anchor: {f.name} → {ref}",
            )
for p in manifest:
    f = (DIST / p["file"]).resolve()
    d = parsed[f]
    require(d.h1 == 1, f'Expected one H1: {p["file"]}')
    require(
        d.lang == {"cz": "cs", "en": "en", "ru": "ru"}[p["locale"]],
        f'Wrong language: {p["file"]}',
    )
    require(
        set(d.alternates) == {"cs", "en", "ru"}, f'Missing language peers: {p["file"]}'
    )
    for locale in ["cz", "en", "ru"]:
        same = DIST / locale / p["route"] / "index.html"
        require(same.exists(), f"Missing locale route: {same}")
for f in DIST.rglob("*.css"):
    for ref in re.findall(r'url\(["\']?([^\)"\']+)', f.read_text()):
        if not urlsplit(ref).scheme:
            require((f.parent / ref).exists(), f"Missing CSS asset: {ref}")
pdfs = list((DIST / "assets/documents").glob("*.pdf"))
require(len(pdfs) == 12, "Expected 12 PDFs")
for f in pdfs:
    require(f.read_bytes().startswith(b"%PDF-"), f"Invalid PDF: {f}")
pages = json.loads((ROOT / "src/content/pages.json").read_text())
for locale in ["cz", "en", "ru"]:
    require(
        sum(p["locale"] == locale and p["kind"] == "product" for p in pages) == 12,
        f"Product count {locale}",
    )
    require(
        sum(p["locale"] == locale and p["kind"] == "case" for p in pages) == 11,
        f"Case count {locale}",
    )
    archive = next(p for p in pages if p["locale"] == locale and p["kind"] == "archive")
    require(len(archive["rows"]) == 103, f"Archive rows {locale}")
    require(all(len(row) == 4 for row in archive["rows"]), f"Archive columns {locale}")
pairs = [
    ("light sector headings", "#191919", "#f3f3f5"),
    ("light sector descriptions", "#585d67", "#f3f3f5"),
    ("light sector numbers", "#a1003a", "#f3f3f5"),
    ("dark sector headings", "#f7f8fa", "#20252d"),
    ("dark sector descriptions", "#bec5d0", "#20252d"),
    ("dark sector numbers", "#f48bb0", "#20252d"),
    ("light body", "#191919", "#ffffff"),
    ("dark body", "#f7f8fa", "#14171c"),
    ("white on brand red", "#ffffff", "#a1003a"),
    ("light muted", "#585d67", "#ffffff"),
    ("dark muted", "#bec5d0", "#14171c"),
]
contrasts = []
for label, fg, bg in pairs:
    a, b = sorted([luminance(fg), luminance(bg)])
    ratio = (b + 0.05) / (a + 0.05)
    require(ratio >= 4.5, f"Low contrast {label}: {ratio:.2f}")
    contrasts.append({"pair": label, "ratio": round(ratio, 2)})
css = (ROOT / "src/styles.css").read_text()
require("@media (prefers-color-scheme: dark)" in css, "Missing native dark scheme")
require("border-top: 7px solid var(--brand)" in css, "Missing red page stripe")
require(
    "localStorage" not in (ROOT / "src/site.js").read_text(),
    "Theme must not override browser preference",
)
report = {
    "status": "pass" if not errors else "fail",
    "content_pages": len(manifest),
    "html_files_checked": len(parsed),
    "local_references_checked": sum(len(d.refs) for d in parsed.values()),
    "pdfs": len(pdfs),
    "languages": dict(Counter(p["locale"] for p in manifest)),
    "contrast": contrasts,
    "errors": errors,
    "visual_browser_qa": "Not run: managed preview does not support plain static projects.",
}
(ROOT / "verification.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2)
)
print(json.dumps(report, ensure_ascii=False, indent=2))
sys.exit(bool(errors))
