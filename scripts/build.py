#!/usr/bin/env python3
"""Build all SH Control pages using only the Python standard library."""

from pathlib import Path
from html import escape, unescape
from urllib.parse import quote
from datetime import date
import json, os, re, shutil, argparse

ROOT = Path(__file__).resolve().parent.parent
SRC, DIST = ROOT / "src", ROOT / "dist"
UI = json.loads((SRC / "content/ui.json").read_text(encoding="utf-8"))
PAGES = json.loads((SRC / "content/pages.json").read_text(encoding="utf-8"))
CONTENT = {(p["locale"], p["route"]): p for p in PAGES}
LANG_NAMES = {"cz": "Čeština", "en": "English", "ru": "Русский"}
MAIN_ROUTES = ["solutions", "products", "references", "about", "contact"]
HERO = "images/homepage_hero.jpg"
TURBINE = "images/2020114131224604687.jpg"
# FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="5" fill="#a1003a"/><text x="32" y="43" text-anchor="middle" fill="white" font-family="Arial,sans-serif" font-size="34" font-weight="bold">SH</text></svg>'
FAVICON = """<svg
   viewBox="0 0 64 64"
   version="1.1"
   id="svg1"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs
     id="defs1" />
  <path
     id="rect1"
     style="fill:#e20000"
     d="m 5,0 h 54 c 2.77,0 5,2.23 5,5 v 54 c 0,2.77 -2.23,5 -5,5 H 5 C 2.23,64 0,61.77 0,59 V 5 C 0,2.23 2.23,0 5,0 Z" />
  <path
     d="m 23.557018,24.198 q -4.692,0 -8.5,1.428 -3.502,1.326 -4.114,2.89 0,0.646 8.772,2.788 2.754,0.646 3.978,1.802 1.258,1.122 1.258,2.788 0,0.306 -0.068,0.714 -0.034,0.374 -0.068,0.612 -0.884,3.026 -5.916,4.76 -4.386,1.496 -9.7580004,1.496 h -1.054 q -2.38,0 -3.638,-0.34 -1.258,-0.34 -1.598,-1.258 0,-0.85 0.68,-2.006 0.68,-1.19 1.122,-1.462 0.646,-0.306 1.462,-0.578 0.816,-0.272 1.19,-0.272 0.374,0 0.374,0.272 0,0.272 -0.578,0.646 l -0.68,0.544 1.632,0.034 q 5.5080004,0 9.0100004,-0.884 3.502,-0.884 4.828,-2.482 0.068,-0.068 0.136,-0.34 0,-0.85 -3.298,-1.802 -2.176,-0.646 -5.134,-1.088 -2.958,-0.476 -3.4,-0.578 -2.7540004,-0.612 -2.7540004,-2.754 0.068,-0.544 0.102,-0.918 0.068,-0.408 0.136,-0.68 0.748,-2.924 1.632,-3.706 1.1900004,-1.088 4.1480004,-2.278 2.448,-0.986 4.93,-1.428 2.516,-0.442 4.828,-0.442 1.428,0 2.278,0.102 0.85,0.068 1.904,0.272 1.088,0.204 1.088,1.292 0,1.666 -0.952,2.618 -0.816,0.816 -2.584,1.36 -0.85,0.272 -1.938,1.122 -0.952,0.748 -1.36,0.748 l -0.408,-0.204 q -0.102,-0.17 -0.136,-0.204 0.034,-0.442 0.986,-1.326 0.782,-0.748 1.53,-1.19 z m 17.611977,9.112 5.712,-6.188 q 0.714,-0.748 1.428,-1.53 0.952,-1.156 0.952,-1.836 0,-0.306 -0.204,-0.544 -0.306,-0.34 -0.918,-0.34 -1.768,0 -6.358,1.564 -3.638,1.224 -5.406,2.108 0.544,0.102 0.544,0.51 0,0.204 -0.51,0.544 -0.476,0.306 -1.02,0.476 -2.686,1.19 -5.372,2.38 -0.544,0 -0.816,-0.408 -0.238,-0.408 -0.238,-1.122 0,-1.258 0.578,-2.618 0.578,-1.394 1.19,-1.7 3.91,-2.142 9.01,-3.57 5.44,-1.53 9.792,-1.53 1.53,0 2.312,0.918 0.816,0.884 0.816,2.244 0,2.108 -1.734,4.046 l -5.44,5.78 5.236,-0.578 6.052,-7.65 q 1.258,-1.564 1.462,-1.768 0.782,-0.816 1.258,-0.816 0.544,0 0.544,1.054 0,1.156 -1.088,2.55 l -5.508,6.698 h 1.19 q 1.394,0 2.074,0.17 0.68,0.17 1.462,0.612 -2.482,1.972 -4.114,4.59 -0.442,-0.136 -1.02,-0.204 -0.544,-0.068 -1.054,-0.068 h -1.394 q -0.578,0.884 -1.156,1.768 -0.646,1.088 -0.646,1.904 0.034,0.068 0.068,0.306 l 0.34,1.53 q -0.578,0 -1.36,0.34 -1.836,0.782 -2.142,0.782 -0.51,0 -0.68,-0.374 -0.136,-0.51 -0.204,-0.748 0,-0.68 0.442,-2.006 0.476,-1.326 1.632,-3.57 l -6.256,0.884 -3.502,4.046 q -0.476,1.02 -1.054,1.496 -0.578,0.476 -1.224,0.476 -0.544,0 -0.952,-0.442 -0.374,-0.408 -0.442,-1.02 0.136,-0.714 0.34,-0.918 l 2.652,-3.332 q -0.714,0.136 -1.428,0.136 -1.088,0 -1.632,-0.374 -0.51,-0.408 -0.51,-1.088 0,-0.816 0.646,-1.632 0.646,-0.816 1.326,-0.816 0.408,0 0.612,0.204 1.088,-0.306 2.72,-0.68 0.238,-0.068 2.992,-0.646 z"
     id="text1"
     style="font-size:34px;font-family:Banff, cursive;text-anchor:middle;fill:#ffffff"
     aria-label="SH" />
</svg>"""


def esc(value):
    return escape(str(value), quote=True)


def body_html(value):
    """Accept an HTML string or a list of HTML paragraph blocks from pages.json."""
    return "\n".join(value) if isinstance(value, list) else value


def plain(value):
    return re.sub(
        r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", body_html(value)))
    ).strip()


def filepath(locale, route=""):
    return f'{locale}/{route + "/" if route else ""}index.html'


def relative(current, target):
    return os.path.relpath(target, str(Path(current).parent)).replace(os.sep, "/")


def href(current, locale, route=""):
    return relative(current, filepath(locale, route))


def asset(current, name):
    return relative(current, "assets/" + name)


def page_link(current, locale, route, label, cls="", arrow=False):
    arr = '<span class="arrow" aria-hidden="true">↗</span>' if arrow else ""
    return f'<a href="{href(current,locale,route)}" class="{cls}">{esc(label)}{arr}</a>'


def nav(current, locale, route):
    return "".join(
        f'<a href="{href(current,locale,r)}"'
        + (' aria-current="page"' if route == r else "")
        + f">{esc(UI[locale][r])}</a>"
        for r in MAIN_ROUTES
    )


def brand(current, locale):
    return f'<a class="brand" href="{href(current,locale)}" aria-label="SH Control — {esc(UI[locale]["home"])}"><span class="brand-mark">SH Control s.r.o.</span><span class="brand-tagline">{esc(UI[locale]["tagline"])}</span></a>'


def language_links(current, locale, route):
    return "".join(
        f'<a href="{href(current,l,route)}" lang="{UI[l]["htmlLang"]}" hreflang="{UI[l]["htmlLang"]}" aria-label="{LANG_NAMES[l]}"'
        + (' aria-current="page"' if l == locale else "")
        + f">{l.upper()}</a>"
        for l in UI
    )


def home_link(current, locale, route):
    label = esc(UI[locale]["home"])
    active = ' aria-current="page"' if route == "" else ""

    return f"""
    <a class="nav-home" href="{href(current, locale)}"
       aria-label="{label}" title="{label}"{active}>
        <svg width="20" height="20" viewBox="0 0 24 24"
             fill="none" stroke="currentColor" stroke-width="1.8"
             stroke-linecap="round" stroke-linejoin="round"
             aria-hidden="true" focusable="false">
            <path d="M3 10L12 3L21 10"/>
            <path d="M5 9V21H19V9"/>
            <path d="M9 21V14H15V21"/>
        </svg>
        <span class="nav-home-label">{label}</span>
    </a>
    """


def header(current, locale, route):
    u = UI[locale]
    return f"""<a class="skip-link" href="#main">{esc(u['skip'])}</a>
    <header class="site-header"><div class="wrap header-inner">{brand(current,locale)}
      <nav class="desktop-nav" aria-label="{esc(u['menu'])}">{home_link(current,locale,route)}{nav(current,locale,route)}</nav>
      <nav class="languages" aria-label="Language">{language_links(current,locale,route)}</nav>
      <details class="mobile-menu"><summary>{esc(u['menu'])}</summary><nav aria-label="{esc(u['menu'])}">{home_link(current,locale,route)}{nav(current,locale,route)}</nav></details>
    </div></header>"""


def footer(current, locale):
    u = UI[locale]
    return f"""<footer class="site-footer"><div class="wrap">
      <div class="footer-grid"><div><h2>SH Control s.r.o.</h2><p>{esc(u['tagline'])}</p><p>Na Výsluní 1234<br>277 11 Neratovice</p></div>
      <div><h2>{esc(u['contact'])}</h2><div class="footer-links"><a href="mailto:info@shcontrol.cz">info@shcontrol.cz</a><a href="tel:+420315684759">+420 315 684 759</a><a href="tel:+420315683187">+420 315 683 187</a>{page_link(current,locale,'contact',u['locations'])}</div></div>
      <div><h2>{esc(u['solutions'])}</h2><div class="footer-links">{nav(current,locale,'')}</div></div></div>
      <div class="footer-bottom"><span>© {date.today().year} SH Control s.r.o. {esc(u['footerCopyright'])}</span><span>CZ · EN · RU</span></div>
    </div></footer>"""


def cta(current, locale):
    u = UI[locale]
    return f'<section class="cta-band"><div class="wrap cta-inner"><h2>{esc(u["talkTitle"])}</h2>{page_link(current,locale,"contact",u["talk"],"button",True)}</div></section>'


def breadcrumbs(current, locale, route, title):
    u = UI[locale]
    parts = [page_link(current, locale, "", u["home"])]
    if "/" in route:
        group = route.split("/")[0]
        parts.append(page_link(current, locale, group, u[group]))
    parts.append(esc(title))
    return (
        '<nav class="wrap" aria-label="Breadcrumb"><ol class="breadcrumbs">'
        + "".join("<li>" + p + "</li>" for p in parts)
        + "</ol></nav>"
    )


def page_head(current, locale, title, lead="", eyebrow="", photo=None, photo_alt=""):
    pic = (
        f'<img src="{asset(current,photo)}" alt="{esc(photo_alt or title)}" width="560" height="420">'
        if photo
        else ""
    )
    eyebrow_html = f'<p class="eyebrow">{esc(eyebrow)}</p>' if eyebrow else ""
    lead_html = f'<p class="lead">{esc(lead)}</p>' if lead else ""
    return f'<section class="page-head {"has-photo" if pic else ""}"><div class="wrap"><div>{eyebrow_html}<h1>{title}</h1>{lead_html}</div>{pic}</div></section>'


def side_panel(current, locale, headings=None):
    u = UI[locale]
    toc = ""
    if headings:
        toc = (
            f'<h2>{esc(u["onThisPage"])}</h2><ul>'
            + "".join(
                f'<li><a href="#{ident}">{esc(label)}</a></li>'
                for ident, label in headings
            )
            + "</ul>"
        )
    return f'<aside class="aside">{toc}<h2>{esc(u["related"])}</h2><ul><li>{page_link(current,locale,"products",u["products"])}</li><li>{page_link(current,locale,"references",u["references"])}</li></ul><p>{esc(u["talkTitle"])}</p>{page_link(current,locale,"contact",u["talk"],"button",True)}</aside>'


def rich_body(page, current):
    body = re.sub(r"<a>(.*?)</a>", r"\1", body_html(page.get("body", "")), flags=re.S)
    body = re.sub(
        r"@@route:([^@]*)@@", lambda m: href(current, page["locale"], m[1]), body
    )
    body = re.sub(r"@@([^@]+)@@", lambda m: asset(current, m[1]), body)
    # Promote original standalone section labels and create stable local anchors.
    body = re.sub(r"<p>\s*<strong>([^<]{1,145})</strong>\s*</p>", r"<h2>\1</h2>", body)
    headings = []

    def heading(match):
        ident = "section-" + str(len(headings) + 1)
        headings.append((ident, plain(match[1])))
        return f'<h2 id="{ident}">{match[1]}</h2>'

    body = re.sub(r"<h2>(.*?)</h2>", heading, body, flags=re.S)
    return body, headings


def gallery_figure(page, current, im):
    """Render one gallery image, also usable between body paragraphs."""
    u = UI[page["locale"]]
    description = im.get("alt", "")
    label = description or u["photo"] + " — " + page["title"]
    caption = f"<figcaption>{esc(description)}</figcaption>" if description else ""
    return f'<figure><a href="{asset(current,im["src"])}"><img src="{asset(current,im["src"])}" loading="lazy" decoding="async" alt="{esc(label)}"></a>{caption}</figure>'


def gallery(page, current):
    photos = page.get("gallery", [])
    if not photos:
        return ""
    return (
        '<div class="gallery">'
        + "".join(gallery_figure(page, current, im) for im in photos)
        + "</div>"
    )


def project_image(page):
    if page["id"] == "53":
        return TURBINE
    return (
        page.get("gallery", [{}])[0].get("src", TURBINE)
        if page.get("gallery")
        else TURBINE
    )


def project_cards(current, locale, pages):
    cards = []
    for p in pages:
        meta = (
            f'<time datetime="{esc(p["date"])}">{esc(p["date"])}</time>'
            if p.get("date")
            else ""
        )
        cards.append(
            f'<article class="project-card"><a href="{href(current,locale,p["route"])}"><img src="{asset(current,project_image(p))}" width="560" height="420" loading="lazy" alt="{esc(p["title"])}"><p class="meta">{meta}</p><h3>{esc(p["title"])}</h3><p>{esc(p["lead"])}</p></a></article>'
        )
    return '<div class="project-grid">' + "".join(cards) + "</div>"


def home(current, locale):
    u = UI[locale]
    sectors = []
    for n, key in enumerate(["chemistry", "energy", "hydro"], 1):
        p = next(p for p in PAGES if p["locale"] == locale and p.get("service") == key)
        sectors.append(
            f'<a class="sector" href="{href(current,locale,p["route"])}"><span class="number">0{n}</span><div><h2>{esc(u[key])}</h2><p>{esc(u[key+"Short"])}</p></div></a>'
        )
    selected = [
        next(p for p in PAGES if p["locale"] == locale and p["id"] == ident)
        for ident in ["57", "53", "52"]
    ]
    return f"""<section class="hero"><div class="wrap hero-inner"><div class="hero-copy"><p class="eyebrow">{esc(u['heroEyebrow'])}</p><h1>{u['heroTitle']}</h1><p class="lead">{esc(u['heroLead'])}</p><div class="actions">{page_link(current,locale,'solutions',u['ourSolutions'],'button',True)}{page_link(current,locale,'about',u['meetUs'],'text-link')}</div></div></div>
    <figure class="hero-photo"><img src="{asset(current,HERO)}" width="560" height="420" alt="" fetchpriority="high"><figcaption><strong>Name_of_plant</strong>{'Place_of_plant' if locale=='cz' else 'Place_of_plant' if locale=='en' else 'Place_of_plant'}</figcaption></figure></section>
    <section class="sectors" aria-label="{esc(u['solutions'])}"><div class="wrap sector-grid">{''.join(sectors)}</div></section>
    <section class="section"><div class="wrap intro-grid"><h2>{esc(u['aboutHeading'])}</h2><div><p class="lead">{esc(u['aboutLead'])}</p>{page_link(current,locale,'about',u['meetUs'],'text-link')}</div></div></section>
    <section class="section muted-section"><div class="wrap"><div class="section-title"><h2>{esc(u['selectedProjects'])}</h2>{page_link(current,locale,'references',u['allProjects'],'text-link')}</div>{project_cards(current,locale,selected)}</div></section>{cta(current,locale)}"""


def index_page(current, locale, route):
    u = UI[locale]
    head = breadcrumbs(current, locale, route, u[route]) + page_head(
        current, locale, esc(u[route]), u[route + "Lead"]
    )
    if route == "solutions":
        cards = []
        for i, p in enumerate(
            [p for p in PAGES if p["locale"] == locale and p["kind"] == "service"], 1
        ):
            cards.append(
                f'<article class="solution-card"><p class="number">0{i}</p><h2>{page_link(current,locale,p["route"],p["title"])}</h2><p>{esc(p["lead"])}</p>{page_link(current,locale,p["route"],u["readMore"],"text-link")}</article>'
            )
        content = '<div class="solution-grid">' + "".join(cards) + "</div>"
    elif route == "products":
        cards = []
        for p in [p for p in PAGES if p["locale"] == locale and p["kind"] == "product"]:
            title = p["title"].split(" — ", 1)[-1]
            cards.append(
                f'<article class="product-card"><p class="product-code">{esc(p["code"])}</p><h2>{page_link(current,locale,p["route"],title)}</h2><p>{esc(p["lead"])}</p>{page_link(current,locale,p["route"],u["readMore"],"text-link")}</article>'
            )
        content = '<div class="product-grid">' + "".join(cards) + "</div>"
    else:
        projects = sorted(
            [p for p in PAGES if p["locale"] == locale and p["kind"] == "case"],
            key=lambda p: p.get("date", ""),
            reverse=True,
        )
        content = (
            project_cards(current, locale, projects)
            + f'<div class="section-title" style="margin-top:3rem"><h2>{esc(u["history"])}</h2>{page_link(current,locale,"references/archive",u["referenceArchive"],"text-link")}</div>'
        )
    return (
        head
        + f'<section class="section"><div class="wrap">{content}</div></section>'
        + cta(current, locale)
    )


def solution_main_image(page):
    """Use the first gallery image as the solution's main image."""
    photos = page.get("gallery") or []
    if not photos:
        return None, ""
    return photos[0]["src"], photos[0].get("alt", "")


# Each solution owns its layout below. Text and pictures come from pages.json;
# the same function renders CZ, EN and RU using the page's locale.
def solution_petrochemicals(current, page):
    """Place gallery[1] after the first two body blocks from pages.json.

    Use a body list of HTML strings to define the paragraph boundaries. Each
    item can contain a paragraph and its associated bullet list. Existing
    string bodies remain supported as one block, with the image after it.
    Gallery[0] is the header; only gallery[2:] appears in the bottom gallery.
    """
    locale = page["locale"]
    u = UI[locale]
    photos = page.get("gallery") or []
    source_body = page.get("body", "")
    blocks = list(source_body) if isinstance(source_body, list) else [source_body]
    if len(photos) > 1:
        blocks.insert(2, gallery_figure(page, current, photos[1]))

    # Process the complete body once so heading IDs and the sidebar stay in sync.
    body, headings = rich_body({**page, "body": blocks}, current)
    remaining_gallery = gallery({**page, "gallery": photos[2:]}, current)
    photo, photo_alt = solution_main_image(page)
    head = breadcrumbs(current, locale, page["route"], page["title"])
    head += page_head(
        current,
        locale,
        esc(page["title"]),
        page["lead"],
        u["solutions"],
        photo,
        photo_alt,
    )
    return (
        head
        + '<div class="wrap content-layout">'
        + f'<article class="prose">{body}{remaining_gallery}</article>'
        + f"{side_panel(current,locale,headings)}</div>"
        + cta(current, locale)
    )


def solution_power_engineering(current, page):
    """Build the Power engineering solution page."""
    locale = page["locale"]
    u = UI[locale]

    photos = page.get("gallery") or []
    source_body = page.get("body", "")
    blocks = list(source_body) if isinstance(source_body, list) else [source_body]
    if len(photos) > 1:
        blocks.insert(2, gallery_figure(page, current, photos[1]))

    body, headings = rich_body({**page, "body": blocks}, current)
    remaining_gallery = gallery({**page, "gallery": photos[2:]}, current)
    photo, photo_alt = solution_main_image(page)
    head = breadcrumbs(current, locale, page["route"], page["title"])
    head += page_head(
        current,
        locale,
        esc(page["title"]),
        page["lead"],
        u["solutions"],
        photo,
        photo_alt,
    )
    return (
        head
        + '<div class="wrap content-layout">'
        + f'<article class="prose">{body}{remaining_gallery}</article>'
        + f"{side_panel(current,locale,headings)}</div>"
        + cta(current, locale)
    )


def solution_small_hydropower(current, page):
    """Build the Small hydropower solution, including its capabilities strip."""
    locale = page["locale"]
    u = UI[locale]

    photos = page.get("gallery") or []
    source_body = page.get("body", "")
    blocks = list(source_body) if isinstance(source_body, list) else [source_body]
    if len(photos) > 1:
        blocks.insert(2, gallery_figure(page, current, photos[1]))
    if len(photos) > 2:
        blocks.insert(7, gallery_figure(page, current, photos[2]))
    if len(photos) > 3:
        blocks.insert(10, gallery_figure(page, current, photos[3]))
    if len(photos) > 4:
        blocks.insert(14, gallery_figure(page, current, photos[4]))
    if len(photos) > 5:
        blocks.insert(16, gallery_figure(page, current, photos[5]))

    body, headings = rich_body({**page, "body": blocks}, current)
    remaining_gallery = gallery({**page, "gallery": photos[6:]}, current)
    photo, photo_alt = solution_main_image(page)
    head = breadcrumbs(current, locale, page["route"], page["title"])
    head += page_head(
        current,
        locale,
        u["hydroHeadline"],
        u["hydroLead"],
        page["title"],
        photo,
        photo_alt,
    )
    head += (
        f'<section class="capabilities"><div class="wrap capability-grid"><h2>{esc(u["capabilityTitle"])}</h2><ol>'
        + "".join("<li>" + esc(x) + "</li>" for x in u["capabilities"])
        + "</ol></div></section>"
    )
    return (
        head
        + '<div class="wrap content-layout">'
        + f'<article class="prose">{body}{remaining_gallery}</article>'
        + f"{side_panel(current,locale,headings)}</div>"
        + cta(current, locale)
    )


def solution_other_projects(current, page):
    """Build Other projects; also provide a default for new service types."""
    locale = page["locale"]
    u = UI[locale]

    photos = page.get("gallery") or []
    source_body = page.get("body", "")
    blocks = list(source_body) if isinstance(source_body, list) else [source_body]
    if len(photos) > 1:
        blocks.insert(5, gallery_figure(page, current, photos[1]))
    if len(photos) > 2:
        blocks.insert(9, gallery_figure(page, current, photos[2]))
    if len(photos) > 3:
        blocks.insert(11, gallery_figure(page, current, photos[3]))
    if len(photos) > 4:
        blocks.insert(13, gallery_figure(page, current, photos[4]))
    if len(photos) > 5:
        blocks.insert(15, gallery_figure(page, current, photos[5]))
    if len(photos) > 6:
        blocks.insert(17, gallery_figure(page, current, photos[6]))
    if len(photos) > 7:
        blocks.insert(19, gallery_figure(page, current, photos[7]))
    if len(photos) > 8:
        blocks.insert(28, gallery_figure(page, current, photos[8]))

    body, headings = rich_body({**page, "body": blocks}, current)
    remaining_gallery = gallery({**page, "gallery": photos[9:]}, current)
    photo, photo_alt = solution_main_image(page)
    head = breadcrumbs(current, locale, page["route"], page["title"])
    head += page_head(
        current,
        locale,
        esc(page["title"]),
        page["lead"],
        u["solutions"],
        photo,
        photo_alt,
    )
    return (
        head
        + '<div class="wrap content-layout">'
        + f'<article class="prose">{body}{remaining_gallery}</article>'
        + f"{side_panel(current,locale,headings)}</div>"
        + cta(current, locale)
    )


def detail(current, page):
    locale, route, kind = page["locale"], page["route"], page["kind"]
    if kind == "service":
        solution_pages = {
            "chemistry": solution_petrochemicals,
            "energy": solution_power_engineering,
            "hydro": solution_small_hydropower,
            "other": solution_other_projects,
        }
        render_solution = solution_pages.get(page["service"], solution_other_projects)
        return render_solution(current, page)

    u = UI[locale]
    head = breadcrumbs(current, locale, route, page["title"])
    body, headings = rich_body(page, current)
    if kind == "product":
        head += page_head(current, locale, esc(page["title"]), "", u["products"])
        photos = gallery(page, current)

        extra = page.get("extra_download")
        extra_download_html = ""

        if extra:
            extra_download_html = f"""
                <p style="margin-top:1rem;margin-bottom:0">
                    <p>
                        {esc(extra["text"])}
                    </p>
                    <a class="button"
                        href="{asset(current, extra["src"])}"
                        download>
                            {esc(extra["label"])}
                            <span aria-hidden="true">↓</span>
                    </a>
                </p>
            """

        return head + f"""
                <div class="wrap product-summary">
                    <article class="prose">
                        <h2>{esc(u["productDetails"])}</h2>
                        {body}
                        {photos}
                    </article>

                    <aside class="download-panel">
                        <h2>{esc(u["catalogue"])}</h2>
                        <p>
                            {esc(page["code"])} · PDF<br>
                            {esc(u["czechDocument"])}
                        </p>

                        <a class="button"
                           href="{asset(current, page["download"])}"
                           download>
                            {esc(u["download"])}
                            <span aria-hidden="true">↓</span>
                        </a>

                        {extra_download_html}

                        <p style="margin-top:1.3rem;margin-bottom:0">
                            {page_link(current, locale, "products", u["allProducts"], "text-link")}
                        </p>
                    </aside>
                </div>
            """ + cta(current, locale)
    elif kind == "case":
        head += page_head(
            current, locale, esc(page["title"]), "", u["project"], project_image(page)
        )
        body = (
            f'<p class="eyebrow">{esc(u["projectDate"])} · <time datetime="{page["date"]}">{page["date"]}</time></p>'
            + body
        )
    elif kind == "archive":
        head += page_head(
            current, locale, esc(page["title"]), page["lead"], u["references"]
        )
        rows = "".join(
            "<tr>" + "".join("<td>" + esc(x) + "</td>" for x in row) + "</tr>"
            for row in page["rows"]
        )
        table = (
            f'<div class="table-scroll"><table><caption>{esc(u["tableCaption"])}</caption><thead><tr>'
            + "".join('<th scope="col">' + esc(x) + "</th>" for x in u["tableHeads"])
            + "</tr></thead><tbody>"
            + rows
            + "</tbody></table></div>"
        )
        return (
            head
            + f'<section class="section"><div class="wrap">{table}</div></section>'
            + cta(current, locale)
        )
    else:
        head += page_head(
            current, locale, esc(page["title"]), page["lead"], u["heroEyebrow"]
        )
    return (
        head
        + f'<div class="wrap content-layout"><article class="prose">{body}{gallery(page,current)}</article>{side_panel(current,locale,headings)}</div>'
        + cta(current, locale)
    )


def contact(current, locale, directions=False):
    u = UI[locale]
    route = "contact/directions" if directions else "contact"
    title = u["directions"] if directions else u["contact"]
    head = breadcrumbs(current, locale, route, title) + page_head(
        current,
        locale,
        esc(title),
        u["contactLead"] if not directions else u["locationLabel"],
    )
    maps = "https://www.google.com/maps/search/?api=1&query=50.253555%2C14.5102017"
    if directions:
        return (
            head
            + f"""<section class="section"><div class="wrap"><h2>SH Control s.r.o.</h2><p>{esc(u['locationLabel'])}</p><p>{esc(u['coordinates'])}: 50.253555, 14.5102017</p><p><a class="button" href="{maps}" target="_blank" rel="noopener noreferrer">{esc(u['openMap'])} <span aria-hidden="true">↗</span></a></p><p>{page_link(current,locale,'contact',u['contact'],'text-link')}</p></div></section>"""
        )
    return (
        head
        + f"""<section class="section"><div class="wrap"><div class="contact-grid">
    <section class="contact-card"><h2>Neratovice</h2><address>SH Control s.r.o.<br>Na Výsluní 1234<br>277 11 Neratovice</address><p><a href="tel:+420315684759">+420 315 684 759</a></p><p><a href="tel:+420315683187">+420 315 683 187</a></p><p><a href="mailto:info@shcontrol.cz">info@shcontrol.cz</a></p><p>{page_link(current,locale,'contact/directions',u['directions'],'text-link')}</p></section>
    <section class="contact-card"><h2>Karlovy Vary</h2><address>SH Control s.r.o.<br>Partyzánská 285<br>360 17 Karlovy Vary</address><p><a href="tel:+420606610800">+420 606 610 800</a></p><p><a href="mailto:info@shcontrol.cz">info@shcontrol.cz</a></p></section>
    </div><section class="contact-management"><h2>{esc(u['management'])}</h2><div><h3>Ing. Pavel Smotlacha</h3><a class="text-link" href="mailto:pavel.smotlacha@shcontrol.cz">pavel.smotlacha@shcontrol.cz</a></div><div><h3>Ing. Petr Kořan</h3><a class="text-link" href="mailto:petr.koran@shcontrol.cz">petr.koran@shcontrol.cz</a></div></section></div></section>"""
    )


def document(current, locale, route, title, description, body, base_url):
    u = UI[locale]
    title = (
        (title + " | SH Control")
        if title != "SH Control"
        else "SH Control — " + u["tagline"]
    )
    lang_links = "".join(
        f'<link rel="alternate" hreflang="{UI[l]["htmlLang"]}" href="{(base_url+"/"+filepath(l,route).removesuffix("index.html")) if base_url else href(current,l,route)}">'
        for l in UI
    )
    canonical = (
        f'<link rel="canonical" href="{base_url}/{filepath(locale,route).removesuffix("index.html")}">'
        if base_url
        else ""
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "SH Control s.r.o.",
        "email": "info@shcontrol.cz",
        "telephone": "+420315684759",
        "foundingDate": "1992",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Na Výsluní 1234",
            "addressLocality": "Neratovice",
            "postalCode": "277 11",
            "addressCountry": "CZ",
        },
    }
    if base_url:
        schema["url"] = base_url
    return f"""<!doctype html>
<html lang="{u['htmlLang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark">
<title>{esc(title)}</title><meta name="description" content="{esc(plain(description)[:170])}">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme:light)"><meta name="theme-color" content="#14171c" media="(prefers-color-scheme:dark)">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,{quote(FAVICON,safe='')}">
<link rel="stylesheet" href="{asset(current,'fonts/fonts.css')}"><link rel="stylesheet" href="{asset(current,'styles.css')}">{canonical}{lang_links}
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><script src="{asset(current,'site.js')}" defer></script>
</head><body>{header(current,locale,route)}<main id="main">{body}</main>{footer(current,locale)}</body></html>"""


def build(base_url=""):
    DIST.mkdir(exist_ok=True)
    shutil.copytree(SRC / "assets", DIST / "assets", dirs_exist_ok=True)
    shutil.copy2(SRC / "styles.css", DIST / "assets/styles.css")
    shutil.copy2(SRC / "site.js", DIST / "assets/site.js")
    manifest = []
    for locale in UI:
        routes = [
            "",
            "solutions",
            "products",
            "references",
            "contact",
            "contact/directions",
        ] + [p["route"] for p in PAGES if p["locale"] == locale]
        for route in routes:
            current = filepath(locale, route)
            u = UI[locale]
            if not route:
                body = home(current, locale)
                title = "SH Control"
                description = u["heroLead"]
            elif route in ["solutions", "products", "references"]:
                body = index_page(current, locale, route)
                title = u[route]
                description = u[route + "Lead"]
            elif route.startswith("contact"):
                body = contact(current, locale, route.endswith("directions"))
                title = (
                    u["directions"] if route.endswith("directions") else u["contact"]
                )
                description = u["contactLead"]
            else:
                p = CONTENT[locale, route]
                body = detail(current, p)
                title = p["title"]
                description = p.get("lead", plain(p.get("body", "")))
            target = DIST / current
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                document(current, locale, route, title, description, body, base_url),
                encoding="utf-8",
            )
            manifest.append(
                {"locale": locale, "route": route, "file": current, "title": title}
            )
    # The root uses a file-compatible relative redirect, so a ZIP can be opened locally.
    (DIST / "index.html").write_text(
        '<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=cz/index.html"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SH Control</title></head><body><p><a href="cz/index.html">Čeština</a> · <a href="en/index.html">English</a> · <a href="ru/index.html">Русский</a></p></body></html>',
        encoding="utf-8",
    )
    for locale in UI:
        current = f"{locale}/404.html"
        u = UI[locale]
        body = f'<section class="wrap error-page"><p class="eyebrow">404</p><h1>{esc(u["notFound"])}</h1><p class="lead">{esc(u["notFoundLead"])}</p>{page_link(current,locale,"",u["backHome"],"button",True)}</section>'
        result = document(
            current, locale, "", u["notFound"], u["notFoundLead"], body, base_url
        )
        (DIST / current).write_text(result, encoding="utf-8")
    # Static hosts can use this root error page, whose local links are adjusted.
    (DIST / "404.html").write_text(
        (DIST / "cz/404.html")
        .read_text()
        .replace('href="../', 'href="')
        .replace('src="../', 'src="')
        .replace('href="index.html"', 'href="cz/index.html"')
        .replace('href="solutions/', 'href="cz/solutions/')
        .replace('href="products/', 'href="cz/products/')
        .replace('href="references/', 'href="cz/references/')
        .replace('href="about/', 'href="cz/about/')
        .replace('href="contact/', 'href="cz/contact/'),
        encoding="utf-8",
    )
    (ROOT / "route-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if base_url:
        (DIST / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            + "".join(
                "<url><loc>"
                + esc(base_url + "/" + p["file"].removesuffix("index.html"))
                + "</loc></url>"
                for p in manifest
            )
            + "</urlset>"
        )
        (DIST / "robots.txt").write_text(
            "User-agent: *\nAllow: /\nSitemap: " + base_url + "/sitemap.xml\n"
        )
    else:
        (DIST / "sitemap.xml").unlink(missing_ok=True)
        (DIST / "robots.txt").write_text("User-agent: *\nAllow: /\n")
    print(
        f"Built {len(manifest)} pages across CZ/EN/RU, plus language redirects and error pages."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-url",
        default="",
        help="Set the final public origin when hosting is chosen.",
    )
    args = parser.parse_args()
    build(args.base_url.rstrip("/"))
