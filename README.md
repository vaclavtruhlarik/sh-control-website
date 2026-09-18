# SH Control website

A complete static website with 35 pages in each of Czech, English and Russian (105 content pages), plus entry and error pages. No hosting account, server-side application, database, npm installation or paid service is required to view the site.

## Open the site

Unzip the project and open **OPEN-WEBSITE.html**. You can also open `dist/index.html` directly. All navigation, photos, fonts and product PDFs use relative local paths. Map directions open Google Maps and need an internet connection.

For a local HTTP preview, run the following from this project folder, then open `http://localhost:8080`:

```sh
python3 -m http.server 8080 --directory dist
```

On Windows, `py` may be used instead of `python3`.

## Design and color modes

- Both modes share the layout selected from concept B and IBM Plex Sans typography.
- Light mode uses concept C's deep red hero, white/light-gray content surfaces, dark body text and red page headings.
- Dark mode uses concept B's graphite surfaces, white headings and readable pale secondary text.
- Service pages include the brand red stripe in both modes. The three homepage sectors have explicit, independently checked heading, description and number colors in each mode.
- The core logo color is `#A1003A`. The original wordmark is preserved on a white plaque.
- CSS `prefers-color-scheme` follows the visitor's browser/operating-system preference and responds when that preference changes. There is no stored theme override. If the browser reports no dark preference, light mode is used.

Change your operating system's appearance or your browser's preferred website appearance to try both modes. Developer tools can also emulate `prefers-color-scheme`.

## Included content

Each language has home, about, solutions, four service pages, a 12-product catalogue and all product detail pages, references, 11 project detail pages, a historical reference table, contacts and directions. The historical reference tables each preserve 103 original turbine-entry rows; they are not presented as counts of distinct projects.

The original 12 Czech technical PDFs are included, unchanged. Their download labels identify the document language on English and Russian pages. The website text has been completed in all three languages; technical PDF translations have not been fabricated.

Photographs, technical illustrations and the original logo are included as local files. The original image resolution is retained. IBM Plex Sans fonts are bundled with their SIL Open Font License. This project does not use analytics, cookies, third-party scripts or a contact form; email and telephone links are real.

## Edit and rebuild

Python 3.9+ is required only for rebuilding. The build uses the standard library and has no installation step.

```sh
python3 scripts/build.py
python3 scripts/check.py
```

Files to edit:

- `src/styles.css`: shared layout and the two palettes.
- `src/content/ui.json`: interface labels, headlines and introductory copy in three languages.
- `src/content/pages.json`: complete page text, photo captions, source references, historical rows and product associations.
- `src/assets/`: original images, PDFs and self-hosted fonts.
- `scripts/build.py`: shared page templates and static page generation.
- `src/site.js`: small mobile-menu enhancement; navigation also works without JavaScript.

`dist/` is the ready-to-serve website. Source files and migration notes should remain outside the public document root. The optional `package.json` commands are wrappers for the Python commands; they do not introduce npm dependencies.

## Hosting later

Nothing has been published. When a host and public address are chosen, the contents of `dist/` can be used as the public site. Rebuild with the final public origin to add absolute canonical links and an XML sitemap:

```sh
python3 scripts/build.py --base-url https://your-final-domain.example
```

The example address is illustrative, not a configured domain. Set the real address only when hosting is decided. `migration/legacy-urls.json` maps the discovered ASP URLs to the new pages. Permanent redirects, including old query-string URLs and old PDF URLs, must be configured for the chosen host before replacing the current website. They are deliberately not claimed to be active in this offline project.

## Content provenance and review

Content was captured from the original SH Control website on 17 September 2026. `migration/source-manifest.json` records page sources, newly translated pages and original asset checksums. The linked crawl covered all three original language trees and pagination, plus the search-indexed Favorit article. Other unlinked or unpublished CMS content would require an export to discover.

Existing technical claims, customer references, system models, historical dates and photographs were retained. Newly translated English/Russian product pages, Russian case studies, English Favorit/Libchavy pages and Czech/English Other Projects pages are editorial drafts for technical review before public launch. Historical source text can describe older hardware and remote-access arrangements; it is not a recommendation for a new installation. Contact details should also be confirmed before launch.

The original map used an obsolete embedded API. The new directions page preserves the source coordinates and provides a working standard map link without embedding an API key.

## Verification

`verification.json` records route, local asset, language, PDF and contrast checks. `scripts/check.py` checks every generated local link and fragment, language counterpart, image alt attribute, the 12 PDF signatures, archive row counts and key color pairs (minimum 4.5:1). These are static checks, not browser rendering tests. Browser/device visual QA remains to be completed because the managed preview environment does not support this plain static project.

## Rights

Company copy, logo, photographs and technical documents originate from SH Control's site and are included for this requested redesign. Their ownership remains with the respective rights holders. IBM Plex Sans is under the bundled license at `src/assets/fonts/OFL.txt`.
