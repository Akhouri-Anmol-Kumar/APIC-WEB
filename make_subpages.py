#!/usr/bin/env python3
"""Generate the per-task URLs (/compress/, /remove-background/, ...) from index.html.
Run from the folder that holds index.html:  python3 make_subpages.py
Each folder gets a copy of the app whose only differences are the page title/description/canonical URL
and the ../fonts/ path. The app itself reads the folder name and opens that tool as soon as a photo is loaded."""
import os, re
BASE = 'https://akhouri-anmol-kumar.github.io/APIC-web/'
PAGES = {
 'edit':               ('Free Online Photo Editor — Crop, Straighten, Filters | APIC', 'Edit photos in your browser: crop with ratio presets, straighten, filters, brightness and contrast. Nothing is uploaded.'),
 'advanced':           ('Advanced Photo Editing — Curves, HSL, Color Grading | APIC', 'Curves, HSL mixer, 3-way grading, clarity, grain and vignette in your browser. Nothing is uploaded.'),
 'remove-object':      ('Remove Objects From Photos Free — On-Device AI | APIC', 'Paint over an unwanted object and on-device AI fills it in. Nothing is uploaded.'),
 'resize':             ('Resize Image Online — Exact Pixels or Percent | APIC', 'Resize images to exact dimensions with high-quality resampling, right in your browser.'),
 'convert':            ('Convert Images — PNG, JPG, WebP, HEIC to JPG, PDF | APIC', 'Convert images between PNG, JPEG, WebP, BMP, ICO, PSD and PDF, including HEIC photos. Nothing is uploaded.'),
 'compress':           ('Compress Image Online — Hit Any File Size, No Upload | APIC', 'Compress JPEG, WebP and AVIF to a target size with a live before/after size preview. Nothing is uploaded.'),
 'remove-background':  ('Remove Image Background Free — No Upload | APIC', 'Cut out the background with on-device AI, touch up with a brush and swap in a new background. Nothing is uploaded.'),
 'ai-tools':           ('On-Device AI Photo Tools — Auto-Enhance, Smart Crop | APIC', 'Private on-device AI tools for your photos. Nothing is uploaded.'),
 'layers':             ('Photo Layers Online — Blend Modes, PSD Import & Export | APIC', 'Stack images, text and shapes with blend modes and masks; open and save PSD. Nothing is uploaded.'),
 'social':             ('Social Media Image Sizes — Profile, Banner, Story | APIC', 'Export exact-size images for 15 social networks with safe-zone guides. Nothing is uploaded.'),
 'visual-intelligence':('Image Preflight Check — Size, Quality, Privacy | APIC', 'Check size, quality and privacy issues in your image before you share it. Nothing is uploaded.'),
 'batch':              ('Batch Image Processing — Resize, Compress, Remove BG | APIC', 'Process many images at once and download one ZIP. Runs on your device.'),
 'design':             ('Design Studio — Templates & Fonts in Your Browser | APIC', 'Design posters, posts and more in your browser with built-in templates and fonts.'),
}
src = open('index.html', encoding='utf-8').read()
for slug, (title, desc) in PAGES.items():
    h = src
    h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title.replace('&', '&amp;'), h, count=1, flags=re.S)
    h = h.replace('rel="canonical" href="%s"' % BASE, 'rel="canonical" href="%s%s/"' % (BASE, slug))
    h = h.replace('property="og:url" content="%s"' % BASE, 'property="og:url" content="%s%s/"' % (BASE, slug))
    h = re.sub(r'(<meta property="og:title" content=")[^"]*(")', r'\g<1>%s\2' % title.replace('\\', ''), h, count=1)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*(")', r'\g<1>%s\2' % desc, h, count=1)
    h = re.sub(r'(<meta name="description" content=")[^"]*(")', r'\g<1>%s\2' % desc, h, count=1)
    h = h.replace("base = 'fonts/'", "base = '../fonts/'")
    os.makedirs(slug, exist_ok=True)
    open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8').write(h)
print('wrote %d pages' % len(PAGES))
