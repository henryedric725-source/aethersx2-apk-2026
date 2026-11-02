#!/usr/bin/env python3
"""Generate static BIOS silo HTML pages for aetherrsx2apk.com."""
from __future__ import annotations

import json
import os
from textwrap import dedent

BASE = "https://aetherrsx2apk.com"
SITE = "Android Emulation Guides"


def head(title: str, description: str, canonical_path: str, extra_graph: list | None = None) -> str:
    canonical = f"{BASE}{canonical_path}"
    graph = [
        {
            "@type": "Article",
            "headline": title,
            "description": description,
            "author": {"@type": "Organization", "name": SITE},
            "publisher": {"@type": "Organization", "name": SITE},
            "mainEntityOfPage": canonical,
            "datePublished": "2026-11-02",
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "PS2 BIOS", "item": f"{BASE}/aethersx2-bios/"},
            ],
        },
    ]
    if extra_graph:
        graph.extend(extra_graph)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2)
    return dedent(
        f"""\
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <meta name="description" content="{description}">
        <link rel="canonical" href="{canonical}">
        <meta name="robots" content="index, follow">
        <meta property="og:type" content="article">
        <meta property="og:title" content="{title}">
        <meta property="og:description" content="{description}">
        <meta property="og:url" content="{canonical}">
        <meta property="og:site_name" content="{SITE}">
        <meta property="og:locale" content="en_US">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/assets/bios-silo.css">
        <script type="application/ld+json">
        {ld}
        </script>"""
    )


def shell(
    depth: int,
    crumb_label: str,
    hero_badges: str,
    h1: str,
    hero_sub: str,
    toc_items: list[tuple[str, str]],
    body: str,
    head_html: str,
) -> str:
    prefix = "../" * depth
    asset = "/" if depth == 0 else prefix
    toc = "".join(f'<li><a href="{href}">{label}</a></li>' for href, label in toc_items)
    nav = f"""
    <nav class="topbar">
        <div class="topbar-inner">
            <a class="logo" href="{BASE}/"><span class="logo-mark">🎮</span> {SITE}</a>
            <div class="nav-links">
                <a href="{BASE}/aethersx2-bios/">PS2 BIOS Hub</a>
                <a href="{BASE}/aethersx2-apk-2026-guide">AetherSX2 Guide</a>
            </div>
            <div class="crumbs"><a href="{BASE}/">Home</a> / <a href="{BASE}/aethersx2-bios/">PS2 BIOS</a> / <span>{crumb_label}</span></div>
        </div>
    </nav>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_html}
</head>
<body>
<div class="progress" id="progress"></div>
{nav}
<header class="hero">
<div class="hero-inner">
<div class="badge-row">{hero_badges}</div>
<h1>{h1}</h1>
<p class="hero-sub">{hero_sub}</p>
</div>
</header>
<div class="wrap">
<aside class="toc" aria-label="Table of contents">
<h4>On this page</h4>
<ol>{toc}</ol>
</aside>
<article class="article">
{body}
</article>
</div>
<p class="foot">© 2026 {SITE}</p>
<script>
var bar=document.getElementById('progress');
window.addEventListener('scroll',function(){{var h=document.documentElement;var s=h.scrollTop/(h.scrollHeight-h.clientHeight);bar.style.width=(s*100)+'%';}},{{passive:true}});
</script>
</body>
</html>"""


def faq_block(items: list[tuple[str, str]]) -> str:
    parts = ['<div class="faq">']
    for q, a in items:
        parts.append(f"<details><summary>{q}</summary><p>{a}</p></details>")
    parts.append("</div>")
    return "\n".join(parts)


def faq_schema(items: list[tuple[str, str]]) -> dict:
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }


GUIDES_BOX = """
<div class="guides-box">
<a href="/which-ps2-bios-to-use-for-aethersx2/">Which PS2 BIOS to use</a>
<a href="/how-to-dump-ps2-bios/">How to dump PS2 BIOS</a>
<a href="/ps2-bios-vs-ps2-rom/">PS2 BIOS vs ROM</a>
<a href="/is-downloading-ps2-bios-legal-safe/">Legal &amp; safe downloads</a>
<a href="/ps2-bios-not-found-invalid-bios-fix/">BIOS not found fix</a>
<a href="/ps2-bios-region-mismatch-pal-ntsc-fix/">Region mismatch fix</a>
<a href="/ps2-bios-scph-numbers-explained/">SCPH numbers explained</a>
</div>"""

REGION_GRID = """
<div class="region-grid">
<div class="region-card">
<img src="/assets/images/region-usa.svg" alt="PS2 BIOS USA download" width="640" height="240" loading="lazy">
<div class="body"><h3>USA (NTSC-U)</h3><p>SCPH-70012 for North American games. <a href="/ps2-bios-usa-scph-70012/">USA BIOS guide →</a></p>
<div class="btns"><a class="btn-sm" href="/downloads/ps2-bios-usa.zip">ZIP</a><a class="btn-sm btn-outline" href="/ps2-bios-usa-scph-70012/">Details</a></div></div></div>
<div class="region-card">
<img src="/assets/images/region-europe.svg" alt="PS2 BIOS Europe PAL" width="640" height="240" loading="lazy">
<div class="body"><h3>Europe (PAL)</h3><p>SCPH-70004 for 50 Hz libraries. <a href="/ps2-bios-europe-scph-70004/">Europe BIOS guide →</a></p>
<div class="btns"><a class="btn-sm" href="/downloads/ps2-bios-europe.zip">ZIP</a><a class="btn-sm btn-outline" href="/ps2-bios-europe-scph-70004/">Details</a></div></div></div>
<div class="region-card">
<img src="/assets/images/region-japan.svg" alt="PS2 BIOS Japan NTSC-J" width="640" height="240" loading="lazy">
<div class="body"><h3>Japan (NTSC-J)</h3><p>SCPH-70000 for Japanese titles. <a href="/ps2-bios-japan-scph-70000/">Japan BIOS guide →</a></p>
<div class="btns"><a class="btn-sm" href="/downloads/ps2-bios-japan.zip">ZIP</a><a class="btn-sm btn-outline" href="/ps2-bios-japan-scph-70000/">Details</a></div></div></div>
</div>"""


def write_page(path: str, html: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def pillar_page() -> None:
    title = "PS2 BIOS Download (USA, Europe, Japan) for AetherSX2 & PCSX2"
    desc = "PS2 BIOS file download for AetherSX2, NetherSX2, and PCSX2 — bios for ps2 in .bin or ZIP, exactly 4,194,304 bytes. Dump your own console or verify SHA-256; Android and PC setup."
    faqs = [
        (
            "What is a PS2 BIOS file and why do emulators need it?",
            "The PS2 BIOS is Sony firmware (~4 MB) that boots the Emotion Engine before any game runs. AetherSX2 and PCSX2 require a legal dump from hardware you own; they cannot ship this file inside the APK.",
        ),
        (
            "Is AetherSX2 BIOS the same as a normal PS2 BIOS dump?",
            "Yes. There is no special AetherSX2 BIOS — import the same SCPH-XXXXX.bin you use on desktop PCSX2.",
        ),
        (
            "Can I use one BIOS pack for USA, Europe, and Japan?",
            "You can store all three regional .bin files, but only one is active at a time in AetherSX2. Download the all-regions ZIP or pick the region that matches most of your games.",
        ),
        (
            "Are free PS2 BIOS downloads safe or legal?",
            "Random downloads may be corrupt, incomplete, or illegal copies of Sony firmware. See our guide on <a href=\"/is-downloading-ps2-bios-legal-safe/\">whether downloading a PS2 BIOS is legal and safe</a> and prefer dumping your own console.",
        ),
        (
            "Where does PS2 BIOS go on Android after import?",
            "Open AetherSX2 or NetherSX2 → Settings → BIOS → Import BIOS. The app copies the file into private storage; you do not manually path it like PCSX2 on PC.",
        ),
        (
            "Does RetroArch use the same PS2 BIOS?",
            "The PCSX2 libretro core uses the same SCPH .bin dumps. You still need firmware from your own console; RetroArch does not replace the BIOS requirement.",
        ),
        (
            "What is PS2 BIOS NTSC and do I need a USA dump?",
            "NTSC-U firmware (for example SCPH-70012) runs at ~60 Hz for North American games. If audio pitch is wrong on PAL titles, you likely need a <a href=\"/ps2-bios-europe-scph-70004/\">PAL BIOS</a> — see <a href=\"/ps2-bios-region-mismatch-pal-ntsc-fix/\">region mismatch fixes</a>.",
        ),
        (
            "Is PS2 BIOS a per-game download like GTA or Naruto?",
            "No. One regional BIOS boots the whole library. Game-specific search terms usually mean ISO/ROM confusion — read <a href=\"/ps2-bios-vs-ps2-rom/\">PS2 BIOS vs PS2 ROM</a>.",
        ),
        (
            "Can I find PS2 BIOS on GitHub?",
            "GitHub hosts homebrew tools (dumpers, guides), not a legal substitute for owning a console. Use those projects to dump your own BIOS, not to download Sony firmware.",
        ),
        (
            "Do I need a different BIOS for Damon PS2?",
            "Damon PS2 uses the same Sony dump format. This site focuses on AetherSX2; see <a href=\"/which-ps2-bios-to-use-for-aethersx2/\">which PS2 BIOS to use</a> for defaults.",
        ),
        (
            "Do I need a China (NTSC-C) PS2 BIOS?",
            "Most emulators and libraries only need USA, Europe, or Japan dumps. China-region consoles are rare in home emulation; match firmware to your disc region if you own such hardware.",
        ),
    ]
    body = f"""
<div class="quick">
<h2>Quick summary</h2>
<p><strong>PS2 BIOS download</strong> means a verified <code>SCPH-XXXXX.bin</code> (4,194,304 bytes) for AetherSX2, NetherSX2, or PCSX2 — not part of the emulator APK. Match region to your games when you can.</p>
<ul>
<li>USA SCPH-70012 · Europe SCPH-70004 · Japan SCPH-70000</li>
<li>Verify SHA-256 after every transfer; re-dump if size is wrong</li>
<li><a href="/how-to-dump-ps2-bios/">Full dump tutorial</a> (~20 min with Free McBoot)</li>
</ul>
</div>
{GUIDES_BOX}
<h2 id="download">PS2 BIOS download (USA, Europe, Japan)</h2>
<p>Use these regional packages only if you already dumped matching firmware from a PS2 you own, or you are verifying a personal backup against our published hashes.</p>
{REGION_GRID}
<h2 id="pack">PS2 BIOS pack (all regions ZIP)</h2>
<p>Keywords like <strong>bios pack ps2</strong> and <strong>all ps2 bios</strong> refer to a single archive with USA, PAL, and Japan dumps. Download <a href="/downloads/ps2-bios-all-regions.zip">ps2-bios-all-regions.zip</a> (includes <code>checksums.txt</code>). Free PS2 BIOS sites are risky — read our <a href="/is-downloading-ps2-bios-legal-safe/">legal guide</a> first.</p>
<h2 id="binzip">PS2 BIOS file: .bin, 4 MB, and ZIP</h2>
<p>A valid <strong>ps2 bios bin</strong> is exactly 4,194,304 bytes. <strong>PS2 bios zip</strong> archives should contain only the raw dump plus checksum notes — import the extracted <code>.bin</code>, not the zip, in AetherSX2.</p>
<h2 id="android">PS2 BIOS for Android (AetherSX2 &amp; NetherSX2)</h2>
<p><strong>Bios ps2 android</strong> setup: transfer your dump via USB or cloud, then Settings → BIOS → Import BIOS. Same file as <strong>ps2 bios download android</strong> guides describe for PCSX2-on-PC workflows.</p>
<h2 id="emulator">PlayStation 2 BIOS vs emulator APK</h2>
<p>The emulator APK is not the <strong>bios emulator ps2</strong> firmware. Without Sony boot code, you see “BIOS not found” — fix steps are in our <a href="/ps2-bios-not-found-invalid-bios-fix/">invalid BIOS guide</a>.</p>
<h2 id="damon">Damon PS2 and other Android emulators</h2>
<p><strong>Damon ps2 bios</strong> searches still require a normal SCPH dump. We recommend AetherSX2/NetherSX2 for compatibility; <a href="/which-ps2-bios-to-use-for-aethersx2/">best PS2 BIOS</a> defaults to USA SCPH-70012 for mixed libraries.</p>
<h2 id="install">Install on AetherSX2, NetherSX2, and PCSX2</h2>
<ol>
<li>Android: Import BIOS in app settings (see <a href="/aethersx2-apk-2026-guide">AetherSX2 2026 guide</a>).</li>
<li>PC: Copy dumps to <code>Documents/PCSX2/bios</code> or your chosen BIOS directory — details in <a href="/which-ps2-bios-to-use-for-aethersx2/#pcsx2">PCSX2 BIOS setup</a>.</li>
</ol>
<h2 id="dump">How to dump your own BIOS (summary)</h2>
<p>Dumping from your console is the lawful path. Use Free McBoot, uLaunchELF, and a BIOS dumper homebrew to write <code>SCPH-XXXXX.bin</code> to FAT32 USB. <a href="/how-to-dump-ps2-bios/">Step-by-step dump guide →</a></p>
<h2 id="faq">Frequently asked questions</h2>
{faq_block(faqs)}
"""
    toc = [
        ("#download", "PS2 BIOS download"),
        ("#pack", "All regions pack"),
        ("#binzip", ".bin and ZIP"),
        ("#android", "Android import"),
        ("#install", "PCSX2 install"),
        ("#dump", "Dump summary"),
        ("#faq", "FAQ"),
    ]
    html = shell(
        1,
        "AetherSX2 BIOS Download",
        '<span class="pill hot">PS2 BIOS</span><span class="pill">AetherSX2</span><span class="pill">PCSX2</span>',
        "AetherSX2 BIOS Download",
        "PS2 BIOS files for USA, Europe, and Japan — verified size and checksums for AetherSX2, NetherSX2, and PCSX2.",
        toc,
        body,
        head(title, desc, "/aethersx2-bios/", [faq_schema(faqs)]),
    )
    write_page("aethersx2-bios/index.html", html)


def which_page() -> None:
    title = "Which PS2 BIOS to Use for AetherSX2? Version and Region Guide"
    desc = "Best PS2 BIOS for PCSX2 and AetherSX2 — pcsx2 bios, bios pcsx2, ps2 bios for pcsx2, and regional SCPH picks explained."
    faqs = [
        (
            "What is the best BIOS for PCSX2?",
            "For most English libraries, USA SCPH-70012 (NTSC-U) is the default. Match PAL or Japan firmware when you primarily play those regions.",
        ),
        (
            "What is the best PS2 BIOS for Android?",
            "AetherSX2 users typically import USA SCPH-70012 first; switch to SCPH-70004 for PAL-only collections.",
        ),
        (
            "Is there a separate PCSX2 BIOS download?",
            "No. PCSX2 uses the same Sony SCPH .bin dump as AetherSX2. Download by region from the <a href=\"/aethersx2-bios/\">PS2 BIOS hub</a>.",
        ),
        (
            "I searched psx2 bios or pcx2 bios — is that different?",
            "Those are common misspellings of PCSX2. You still need a 4 MB SCPH dump, not a special PCX2 file.",
        ),
        (
            "Do PCSX2 plugins and BIOS come in one zip?",
            "Plugins are separate. BIOS is still one or more SCPH-XXXXX.bin files from your console.",
        ),
    ]
    body = f"""
<p class="lead">Choosing <strong>which PS2 BIOS to use</strong> fixes black screens, region errors, and PAL speed-up. This guide covers <strong>best ps2 bios</strong> defaults for AetherSX2 and the full <strong>pcsx2 bios</strong> setup path on Windows.</p>
<h2 id="best">Best PS2 BIOS for most game libraries</h2>
<p><strong>Best ps2 bios</strong> for mixed North American folders: <strong>SCPH-70012</strong> (USA). Use <a href="/ps2-bios-europe-scph-70004/">SCPH-70004</a> for PAL-heavy libraries and <a href="/ps2-bios-japan-scph-70000/">SCPH-70000</a> for NTSC-J exclusives.</p>
<h2 id="pcsx2">PCSX2 BIOS setup on Windows</h2>
<p><strong>Bios pcsx2</strong> setup happens during first-run wizard or Settings → BIOS. Place dumps in your BIOS directory (commonly <code>Documents/PCSX2/bios</code> on Windows 10/11 64-bit).</p>
<img class="screenshot" src="/assets/images/pcsx2-bios-directory.svg" alt="PCSX2 BIOS directory selection" width="960" height="540" loading="lazy">
<h3>PCSX2 BIOS download for Windows 10 64-bit</h3>
<p>There is no official Sony CDN — <strong>bios pcsx2 download</strong> flows mean verifying a personal 4 MB dump. Get files from the <a href="/aethersx2-bios/">PS2 BIOS download</a> hub or <a href="/how-to-dump-ps2-bios/">dump your console</a>.</p>
<h2 id="same">PS2 BIOS for PCSX2 vs AetherSX2</h2>
<p><strong>Ps2 bios for pcsx2</strong> is identical to Android firmware. <strong>Bios ps2 pcsx2</strong> and <strong>ps2 bios for pcsx2</strong> searches should land here, not on a separate pirate pack.</p>
<h2 id="faq">FAQ</h2>
{faq_block(faqs)}
<div class="cta"><div class="cta-text"><h3>Download verified regional BIOS</h3><p>Same .bin for PC and Android.</p></div><a class="cta-btn" href="/aethersx2-bios/">PS2 BIOS hub →</a></div>
"""
    html = shell(
        1,
        "Which PS2 BIOS",
        '<span class="pill hot">PCSX2</span><span class="pill">Best BIOS</span>',
        "Which PS2 BIOS to Use for AetherSX2 (and PCSX2)",
        "Best PS2 BIOS by region, PCSX2 folder setup, and when to switch USA, PAL, or Japan firmware.",
        [("#best", "Best PS2 BIOS"), ("#pcsx2", "PCSX2 setup"), ("#same", "Same file on Android"), ("#faq", "FAQ")],
        body,
        head(title, desc, "/which-ps2-bios-to-use-for-aethersx2/", [faq_schema(faqs)]),
    )
    write_page("which-ps2-bios-to-use-for-aethersx2/index.html", html)


def region_usa() -> None:
    title = "PS2 BIOS USA (SCPH-70012): NTSC-U Setup for AetherSX2"
    desc = "PS2 BIOS USA download — ps2 bios us, american bios, scph 70012 bin, scph 39001, and NTSC-U setup for AetherSX2 and PCSX2."
    faqs = [
        ("What is the ps2 bios usa file name?", "Common dumps are named SCPH-70012.bin or SCPH-39001.bin depending on the console you dumped."),
        ("Is ps2 bios download usa the same as NTSC?", "Yes — USA firmware is NTSC-U (~60 Hz). See region mismatch guide if PAL games run fast."),
    ]
    body = f"""
<p><strong>Ps2 bios usa</strong>, <strong>ps2 american bios</strong>, and <strong>bios ps2 usa</strong> refer to NTSC-U firmware. Default model: <strong>SCPH-70012</strong> (also search <strong>scph 70012 bin</strong>).</p>
<h2>SCPH-70012 vs SCPH-39001</h2>
<p>Older USA consoles may dump as <strong>scph 39001 bin</strong> or <strong>bios scph 39001</strong>. Either works when region matches; see <a href="/ps2-bios-scph-numbers-explained/">SCPH numbers explained</a>.</p>
<p class="checksum">SHA-256 (SCPH-70012): c7628a01da23d7d38851aec8403e535581d0f2a781fee5b86b1c648b13a9970d</p>
<h2>Import on AetherSX2 and PCSX2</h2>
<p>Android: Settings → BIOS → Import. PC: BIOS folder + wizard — <a href="/which-ps2-bios-to-use-for-aethersx2/#pcsx2">PCSX2 steps</a>.</p>
<p><a href="/downloads/ps2-bios-usa.zip">Download USA ZIP</a> · <a href="/aethersx2-bios/">All regions hub</a> · <a href="/ps2-bios-region-mismatch-pal-ntsc-fix/">NTSC mismatch fixes</a></p>
<h2>FAQ</h2>
{faq_block(faqs)}
"""
    write_page(
        "ps2-bios-usa-scph-70012/index.html",
        shell(1, "USA BIOS", '<span class="pill hot">NTSC-U</span>', "PS2 BIOS USA (SCPH-70012)", "NTSC-U firmware for North American PS2 games on AetherSX2 and PCSX2.", [("#faq", "FAQ")], body, head(title, desc, "/ps2-bios-usa-scph-70012/", [faq_schema(faqs)])),
    )


def region_europe() -> None:
    title = "PS2 BIOS Europe (SCPH-70004): PAL Setup for AetherSX2"
    desc = "PS2 BIOS Europe and PS2 BIOS PAL — SCPH-70004 for 50 Hz games on AetherSX2 and PCSX2."
    faqs = [
        ("What is ps2 bios pal?", "PAL firmware such as SCPH-70004 runs European and Australian games at 50 Hz."),
        ("Ps2 bios europe vs USA?", "Use Europe dumps for PAL libraries to avoid speed-up and pitch issues."),
    ]
    body = f"""
<p><strong>Ps2 bios europe</strong> maps to PAL firmware. This page targets <strong>ps2 bios pal</strong> and SCPH-70004 for AetherSX2.</p>
<p class="checksum">SHA-256 (SCPH-70004): 8921e73006ac2c01922fcc7b76da6b9caed6b20fbd4e69f165635e18542de6ab</p>
<p><a href="/downloads/ps2-bios-europe.zip">Europe ZIP</a> · <a href="/ps2-bios-region-mismatch-pal-ntsc-fix/">Fix PAL on NTSC BIOS</a> · <a href="/aethersx2-bios/">Hub</a></p>
<h2>FAQ</h2>
{faq_block(faqs)}
"""
    write_page(
        "ps2-bios-europe-scph-70004/index.html",
        shell(1, "Europe BIOS", '<span class="pill hot">PAL</span>', "PS2 BIOS Europe (SCPH-70004)", "PAL PS2 BIOS for European and Australian game libraries.", [("#faq", "FAQ")], body, head(title, desc, "/ps2-bios-europe-scph-70004/", [faq_schema(faqs)])),
    )


def region_japan() -> None:
    title = "PS2 BIOS Japan (SCPH-70000): NTSC-J Setup for AetherSX2"
    desc = "PS2 BIOS Japan — ps2 japan bios, bios japan ps2, SCPH-70000, and legacy SCPH-10000 dumps."
    faqs = [
        ("What about scph 10000 bin searches?", "Launch-era Japan consoles dump SCPH-10000.bin; newer units use SCPH-70000 — both are NTSC-J."),
    ]
    body = """
<h2>Modern Japan BIOS (SCPH-70000)</h2>
<p><strong>Ps2 bios japan</strong> and <strong>bios japan ps2</strong> usually mean NTSC-J firmware for Japanese discs.</p>
<p class="checksum">SHA-256 (SCPH-70000): c4dad3b5c6ad58bce70a47fc332602880f041c0338ac6be89061c928f6919ab1</p>
<h2>Older Japan models</h2>
<div class="table-wrap"><table><thead><tr><th>Model</th><th>Notes</th></tr></thead><tbody>
<tr><td><strong>SCPH-10000</strong></td><td>Early Japan hardware; scph10000 zip searches refer to this dump name</td></tr>
<tr><td><strong>SCPH-70000</strong></td><td>Recommended default for new setups</td></tr>
</tbody></table></div>
<p><a href="/downloads/ps2-bios-japan.zip">Japan ZIP</a> · <a href="/aethersx2-bios/">Hub</a></p>
<h2>FAQ</h2>
""" + faq_block(faqs)
    write_page(
        "ps2-bios-japan-scph-70000/index.html",
        shell(1, "Japan BIOS", '<span class="pill hot">NTSC-J</span>', "PS2 BIOS Japan (SCPH-70000)", "Japanese PS2 BIOS for NTSC-J games and imports.", [("#faq", "FAQ")], body, head(title, desc, "/ps2-bios-japan-scph-70000/", [faq_schema(faqs)])),
    )


def dump_page() -> None:
    title = "How to Dump PS2 BIOS from Your Own Console for AetherSX2"
    desc = "How to dump PS2 BIOS legally with Free McBoot, uLaunchELF, and a BIOS dumper — for PCSX2 and AetherSX2."
    steps = [
        {"@type": "HowToStep", "name": "Prepare FMCB and USB", "text": "FAT32 USB with uLaunchELF and BIOS dumper homebrew."},
        {"@type": "HowToStep", "name": "Launch dumper", "text": "Boot Free McBoot, run uLaunchELF, execute the dumper."},
        {"@type": "HowToStep", "name": "Verify file", "text": "Confirm SCPH-XXXXX.bin is 4,194,304 bytes and matches checksums."},
    ]
    faqs = [("How to dump ps2 bios on unmodded hardware?", "Use disc-based exploits to launch uLaunchELF once, then run the same dumper.")]
    body = """
<p>This is the full <strong>how to dump ps2 bios</strong> tutorial. The <a href="/aethersx2-bios/">BIOS hub</a> keeps a short summary only.</p>
<h2>Modded PS2 (Free McBoot)</h2>
<ol><li>Boot FMCB → uLaunchELF → BIOS dumper → save to USB.</li><li>Copy to PC/phone; verify size and SHA-256.</li></ol>
<h2>Unmodded PS2</h2>
<p>Requires a temporary exploit (FreeDVDBoot, swap trick, etc.) to launch uLaunchELF, then the same dumper steps.</p>
<h2>FAQ</h2>
""" + faq_block(faqs)
    write_page(
        "how-to-dump-ps2-bios/index.html",
        shell(1, "Dump BIOS", '<span class="pill hot">HowTo</span>', "How to Dump PS2 BIOS", "Legal BIOS dump for AetherSX2 and PCSX2 using homebrew tools.", [("#faq", "FAQ")], body, head(title, desc, "/how-to-dump-ps2-bios/", [{"@type": "HowTo", "name": title, "step": steps}, faq_schema(faqs)])),
    )


def scph_page() -> None:
    title = "PS2 BIOS SCPH Numbers Explained: Model Codes and BIOS Versions"
    desc = "SCPH model numbers for PS2 BIOS — scph 90004, 77000, 7502, and PCSX2 1.6.0 BIOS confusion explained."
    faqs = [
        (
            "Does PCSX2 1.6.0 include a special BIOS?",
            "Users often confuse PCSX2 app version 1.6.0 with console firmware. You still need SCPH .bin dumps from your PS2.",
        ),
    ]
    body = """
<div class="table-wrap"><table><thead><tr><th>SCPH</th><th>Region</th><th>Typical .bin</th></tr></thead><tbody>
<tr><td>70012</td><td>USA NTSC-U</td><td><a href="/ps2-bios-usa-scph-70012/">SCPH-70012</a></td></tr>
<tr><td>70004</td><td>Europe PAL</td><td><a href="/ps2-bios-europe-scph-70004/">SCPH-70004</a></td></tr>
<tr><td>70000</td><td>Japan NTSC-J</td><td><a href="/ps2-bios-japan-scph-70000/">SCPH-70000</a></td></tr>
<tr><td>90004 / 90006</td><td>PAL late models</td><td>Region-specific dumps</td></tr>
<tr><td>77000</td><td>Japan</td><td>Alternate Japan hardware</td></tr>
<tr><td>7502 / 1001</td><td>PAL / USA legacy</td><td>Older model names in filenames</td></tr>
</tbody></table></div>
<h2>FAQ</h2>
""" + faq_block(faqs)
    write_page(
        "ps2-bios-scph-numbers-explained/index.html",
        shell(1, "SCPH codes", '<span class="pill">Reference</span>', "PS2 BIOS SCPH Numbers Explained", "Model codes, regions, and filename patterns for PS2 BIOS dumps.", [("#faq", "FAQ")], body, head(title, desc, "/ps2-bios-scph-numbers-explained/", [faq_schema(faqs)])),
    )


def vs_rom() -> None:
    title = "PS2 BIOS vs PS2 ROM (ISO): What Each File Actually Does"
    desc = "PS2 BIOS vs ROM — bios rom ps2, ps2 bios rom, and bios iso ps2 explained."
    faqs = [("What is coolrombios?", "ROM sites often mislabel game ISOs as BIOS; you still need a separate SCPH firmware dump.")]
    body = """
<p><strong>Bios rom ps2</strong> searches mix two files: firmware (BIOS) vs game disc images (ISO/CHD ROM). Emulators need both, legally obtained.</p>
<p><a href="/aethersx2-bios/">Get BIOS</a> · <a href="/how-to-dump-ps2-bios/">Dump BIOS</a></p>
<h2>FAQ</h2>
""" + faq_block(faqs)
    write_page(
        "ps2-bios-vs-ps2-rom/index.html",
        shell(1, "BIOS vs ROM", '<span class="pill">Guide</span>', "PS2 BIOS vs PS2 ROM (ISO)", "What PS2 BIOS files do compared to game ISOs.", [("#faq", "FAQ")], body, head(title, desc, "/ps2-bios-vs-ps2-rom/", [faq_schema(faqs)])),
    )


def legal_page() -> None:
    title = "Is Downloading a PS2 BIOS Legal and Safe? Dump-Your-Own Explained"
    desc = "Is PS2 BIOS legal? Is downloading PS2 BIOS safe? Copyright, malware risk, and dumping from your own console."
    faqs = [
        ("Is ps2 bios legal to download?", "Downloading Sony firmware from random sites is copyright infringement in most countries. Dumping from your own console is the supported approach."),
        ("Is downloading ps2 bios safe?", "Unverified downloads may include truncated or malicious files. Verify 4,194,304-byte size and SHA-256."),
    ]
    body = """
<p>Short answer: treat the BIOS like licensed firmware, not abandonware.</p>
<p><a href="/how-to-dump-ps2-bios/">Dump guide</a> · <a href="/aethersx2-bios/">Verified downloads</a></p>
<h2>FAQ</h2>
""" + faq_block(faqs)
    write_page(
        "is-downloading-ps2-bios-legal-safe/index.html",
        shell(1, "Legal", '<span class="pill">Legal</span>', "Is Downloading a PS2 BIOS Legal and Safe?", "Copyright and safety guidance for PS2 BIOS files.", [("#faq", "FAQ")], body, head(title, desc, "/is-downloading-ps2-bios-legal-safe/", [faq_schema(faqs)])),
    )


def not_found() -> None:
    title = "PS2 BIOS Not Found or Invalid BIOS in AetherSX2: Fix"
    desc = "Fix PS2 BIOS not found and invalid BIOS errors — file size, path, and import checklist."
    faqs = [("Why ps2 bios invalid?", "Wrong size, corrupt download, or selecting .nvm instead of main .bin.")]
    body = """
<ol>
<li>Confirm <code>4194304</code> bytes.</li><li>Extract ZIP before import on Android.</li>
<li>Re-dump or re-copy over USB.</li><li>Match region if black screen persists.</li>
</ol>
<p><a href="/how-to-dump-ps2-bios/">Dump BIOS</a> · <a href="/is-downloading-ps2-bios-legal-safe/">Legal sources</a></p>
<h2>FAQ</h2>
""" + faq_block(faqs)
    write_page(
        "ps2-bios-not-found-invalid-bios-fix/index.html",
        shell(1, "Not found fix", '<span class="pill hot">Fix</span>', "PS2 BIOS Not Found or Invalid BIOS", "Checklist for AetherSX2 and PCSX2 BIOS errors.", [("#faq", "FAQ")], body, head(title, desc, "/ps2-bios-not-found-invalid-bios-fix/", [faq_schema(faqs)])),
    )


def mismatch() -> None:
    title = "PS2 BIOS Region Mismatch: PAL Games Too Fast and NTSC Pitch Fixes"
    desc = "PS2 BIOS region mismatch and ps2 ntsc bios — fix PAL speed-up and pitch on wrong firmware."
    faqs = [("What is ps2 ntsc bios?", "NTSC-U firmware such as SCPH-70012; PAL games may run fast until you import PAL BIOS.")]
    body = """
<p>PAL titles on USA BIOS often run ~17–20% fast with higher audio pitch. Import <a href="/ps2-bios-europe-scph-70004/">PAL BIOS</a> or use USA dumps for NTSC libraries — see <a href="/which-ps2-bios-to-use-for-aethersx2/">which BIOS to use</a>.</p>
<h2>FAQ</h2>
""" + faq_block(faqs)
    write_page(
        "ps2-bios-region-mismatch-pal-ntsc-fix/index.html",
        shell(1, "Region mismatch", '<span class="pill">Fix</span>', "PS2 BIOS Region Mismatch", "PAL vs NTSC BIOS timing and pitch fixes.", [("#faq", "FAQ")], body, head(title, desc, "/ps2-bios-region-mismatch-pal-ntsc-fix/", [faq_schema(faqs)])),
    )


def sitemap() -> None:
    paths = [
        "/aethersx2-bios/",
        "/which-ps2-bios-to-use-for-aethersx2/",
        "/ps2-bios-usa-scph-70012/",
        "/ps2-bios-europe-scph-70004/",
        "/ps2-bios-japan-scph-70000/",
        "/how-to-dump-ps2-bios/",
        "/ps2-bios-scph-numbers-explained/",
        "/ps2-bios-vs-ps2-rom/",
        "/is-downloading-ps2-bios-legal-safe/",
        "/ps2-bios-not-found-invalid-bios-fix/",
        "/ps2-bios-region-mismatch-pal-ntsc-fix/",
        "/aethersx2-apk-2026-guide",
    ]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in paths:
        lines.append(f"  <url><loc>{BASE}{p}</loc><lastmod>2026-11-02</lastmod></url>")
    lines.append("</urlset>")
    write_page("sitemap.xml", "\n".join(lines) + "\n")


def main() -> None:
    pillar_page()
    which_page()
    region_usa()
    region_europe()
    region_japan()
    dump_page()
    scph_page()
    vs_rom()
    legal_page()
    not_found()
    mismatch()
    sitemap()
    print("Generated BIOS silo pages.")


if __name__ == "__main__":
    main()
