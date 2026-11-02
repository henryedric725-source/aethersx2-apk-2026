# BIOS silo deployment

This repository ships **static HTML** for the PS2 BIOS keyword silo at `https://aetherrsx2apk.com/`.

## CMS path

Production may still serve some URLs from WordPress (for example the live `/aethersx2-bios/` pillar). Treat the HTML under each slug folder in this repo as the **source of truth** for content, meta tags, FAQ schema, and internal links.

Deploy options:

1. **Static hosting** — Upload each `*/index.html` to the matching path on Hostinger (or sync via CI).
2. **WordPress** — Paste section HTML into blocks or import static pages; keep canonical URLs identical to this repo.

## BIOS binaries and ZIPs

Sony PS2 BIOS files are **not** stored in git. On deploy:

1. Place verified `.bin` files (4,194,304 bytes) on your CDN or `/downloads/`.
2. Build ZIPs: `ps2-bios-usa.zip`, `ps2-bios-europe.zip`, `ps2-bios-japan.zip`, `ps2-bios-all-regions.zip` using the checksums in `downloads/checksums.txt`.

Placeholder ZIPs in `downloads/` contain README + checksums only until you add bins at deploy time.
