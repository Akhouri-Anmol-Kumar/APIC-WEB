#!/usr/bin/env python3
"""Build the per-task pages, sitemap.xml, robots.txt and vercel.json from index.html.
Run from the folder that holds index.html:   python3 make_subpages.py
Each task folder (/compress/, /remove-background/, ...) is a copy of the app with its own title, description,
canonical URL, heading, intro text, breadcrumb schema and internal links. The app reads the folder name and
opens that tool as soon as a photo is loaded."""
import os, re, json, html, datetime
BASE = 'https://apic-online.vercel.app/'
TODAY = datetime.date.today().isoformat()
# slug: (title, meta description, h1, eyebrow, h2, lead, [3 steps])
P = {
 'remove-background': ('Free remove.bg Alternative: Remove Image Background, No Upload | APIC',
   'Remove image backgrounds free in your browser with on-device AI. No upload, no sign-up, no credits. Brush touch-up and one-click new background. A remove.bg alternative.',
   'Remove Image Background Free — remove.bg Alternative With No Upload',
   'Remove background', 'Remove an image background free, without uploading it.',
   'APIC cuts the background out of a photo with AI that runs inside your browser. Your image never leaves your device, there is no account and no per-image credit. It is a free alternative to remove.bg, whose standalone site and API are closing on 1 December 2026.',
   ['Drop in a JPG, PNG, WebP or HEIC photo.','Open the Remove BG tab and press Remove.','Touch up with the Restore or Erase brush, pick a new background if you like, then export a transparent PNG.']),
 'compress': ('Compress Image to Exact File Size Online — No Upload | APIC',
   'Compress JPEG, WebP and AVIF to a target size in KB, with a live before and after size preview. Free, in your browser, nothing uploaded.',
   'Compress Images to an Exact File Size, Free and Private',
   'Compress image', 'Hit any file-size limit without guessing quality.',
   'Set a target size in KB or drag a quality slider. APIC searches for the best quality that fits and shows the result size live before you download. Works with JPEG, WebP and AVIF and never uploads your photo.',
   ['Drop in your image.','Open Compress, choose a format and a target size or quality.','Check the before and after size, then download.']),
 'resize': ('Resize Image Online — Exact Pixels or Percent, No Upload | APIC',
   'Resize images to exact pixel sizes or a percentage with high-quality resampling. Free, private and done in your browser.',
   'Resize Images to Exact Pixels or Percent',
   'Resize image', 'Resize to the exact size you need.',
   'Enter exact width and height in pixels or scale by percent, with the aspect ratio locked if you want. APIC uses step-down resampling so downsized images stay sharp, and nothing is uploaded.',
   ['Drop in your image.','Open Resize and enter pixels or a percentage.','Apply, then export in the format you need.']),
 'convert': ('Convert Images: HEIC to JPG, PNG, WebP, PDF Online — No Upload | APIC',
   'Convert HEIC to JPG and convert between PNG, JPEG, WebP, BMP, ICO, PSD and PDF, or merge images into one PDF. Free and private in your browser.',
   'Convert HEIC to JPG, PNG, WebP and PDF Online',
   'Convert image', 'Convert any image format, including iPhone HEIC.',
   'Open HEIC photos from an iPhone, then save them as JPG, PNG, WebP, BMP, ICO, PSD or PDF. You can also combine several images into one multi-page PDF. All conversion happens on your device.',
   ['Drop in an image (HEIC, JPG, PNG, WebP and more).','Choose Export and pick the format.','For a multi-page PDF, choose PDF and add more images, then download.']),
 'edit': ('Free Online Photo Editor — Crop, Straighten, Filters, Blur | APIC',
   'Edit photos free in your browser: crop with ratio presets, straighten, filters, brightness, contrast, blur or pixelate private areas. Nothing is uploaded.',
   'Free Online Photo Editor With Crop, Straighten and Blur',
   'Edit photo', 'Everyday photo editing, no install and no upload.',
   'Crop to 1:1, 4:5, 16:9 and more, straighten a tilted horizon, adjust brightness, contrast and saturation, add filters, and blur or pixelate faces and plates. Everything runs on your device.',
   ['Drop in your photo.','Use the Edit tab for crop, straighten, filters and adjustments.','Select an area and use Hide area to blur or pixelate, then export.']),
 'advanced': ('Advanced Photo Editing Online — Curves, HSL, Colour Grading | APIC',
   'Pro colour tools in your browser: RGB curves, HSL mixer, 3-way colour grading, clarity, grain, vignette and 3D LUT export. Free and private.',
   'Advanced Online Photo Editor: Curves, HSL and Colour Grading',
   'Advanced editing', 'Pro colour control in the browser.',
   'Shape tone with RGB curves and a live histogram, mix colours with HSL, grade shadows, mids and highlights, add clarity, grain and vignette, and export a .cube LUT. No upload and no install.',
   ['Drop in your photo.','Open Advanced and adjust curves, HSL or grading.','Hold the before button to compare, then export.']),
 'remove-object': ('Remove Objects From Photos Free — On-Device AI, No Upload | APIC',
   'Paint over a person, sign or blemish and on-device AI fills the area to match its surroundings. Free, private, with zoom for precise painting.',
   'Remove Objects From Photos Free With On-Device AI',
   'Remove object', 'Erase what should not be in the picture.',
   'Paint over a photobomber, sign, wire or blemish and APIC fills the area to match what is around it. Zoom and pan make precise painting easy on a phone. The AI runs on your device.',
   ['Drop in your photo.','Open Remove Object and paint over what you want gone (pinch to zoom).','Press Remove, check the result, then export.']),
 'ai-tools': ('On-Device AI Photo Tools — Background and Object Removal | APIC',
   'AI background removal and object removal that run privately in your browser. No upload, no account.',
   'On-Device AI Photo Tools That Never Upload Your Images',
   'AI tools', 'AI that runs on your device, not on a server.',
   'APIC loads small AI models into your browser the first time you use them, asks before any large download, and caches them so later runs are fast. Your photos are never sent anywhere.',
   ['Drop in your photo.','Open AI Tools and pick background or object removal.','Approve the one-time model download if asked, then run it.']),
 'layers': ('Photo Layers Online — Blend Modes, Masks, PSD Import and Export | APIC',
   'Stack images, text and shapes with blend modes and masks, and open or save PSD files. Free, in your browser, nothing uploaded.',
   'Photo Layers Online With Blend Modes and PSD Support',
   'Layers', 'Compose with layers, right in the browser.',
   'Add images, text and shapes as layers, set blend modes and opacity, mask, reorder and flatten. Open and save PSD files. Undo covers everything, including flatten.',
   ['Drop in your base photo.','Open Layers and add images, text or shapes.','Arrange, blend and mask, then export PNG or PSD.']),
 'social': ('Social Media Image Sizes — Profile Picture, Banner, Story Maker | APIC',
   'Exact-size profile pictures, banners, posts and stories for Instagram, YouTube, X, TikTok, LinkedIn and more, with safe-zone guides. Free and private.',
   'Social Media Image Resizer: Profile Pictures, Banners and Stories',
   'Social media sizes', 'The right size for every network.',
   'Pick a network and format, drag and zoom to frame your photo, check the safe-zone guides, and download one size or a ZIP of every size. APIC keeps files under each platform’s size limit.',
   ['Drop in your photo.','Open Social and choose a network and size.','Frame it with the guides, then download.']),
 'visual-intelligence': ('Image Preflight Check — Size, Quality and Privacy Issues | APIC',
   'Check an image for size, quality and privacy problems such as hidden location data before you share it. Free and private.',
   'Image Preflight Check Before You Share',
   'Visual intelligence', 'Catch problems before you post.',
   'Visual Intelligence flags size and quality issues and privacy risks before you share an image, so you can fix them first. The check runs on your device.',
   ['Drop in your image.','Open Visual Intelligence to run the checks.','Fix what it flags, then export.']),
 'batch': ('Batch Image Processing — Resize, Compress, Remove BG, ZIP | APIC',
   'Process many images at once: resize, compress, convert or remove backgrounds, then download one ZIP. Free and private on your device.',
   'Batch Image Processing in Your Browser',
   'Batch', 'Do many images at once.',
   'Add a set of images, apply the same steps to all of them and download one ZIP. It all runs on your device, so nothing is uploaded.',
   ['Open the Batch studio and add your images.','Choose the steps to apply.','Run it and download the ZIP.']),
 'design': ('Design Studio — Posters and Social Posts With Templates and Fonts | APIC',
   'Design posters, posts and graphics in your browser with templates and fonts. Free, with nothing uploaded.',
   'Design Studio: Templates and Fonts in Your Browser',
   'Design Studio', 'Make graphics from templates.',
   'Start from a template, add text with built-in fonts and your own images, and export. It runs in your browser.',
   ['Open Design Studio.','Pick a template and edit text and images.','Export your design.']),
}
LINKS = [('remove-background','Remove background'),('compress','Compress image'),('resize','Resize image'),('convert','Convert image · HEIC to JPG'),('edit','Edit photo'),('advanced','Advanced colour tools'),('remove-object','Remove objects'),('ai-tools','AI tools'),('layers','Layers &amp; PSD'),('social','Social media sizes'),('visual-intelligence','Image preflight check'),('batch','Batch processing'),('design','Design Studio')]
src = open('index.html', encoding='utf-8').read()
m = re.search(r'<!--SEO-ABOUT-->.*?<!--/SEO-ABOUT-->', src, re.S)
table = re.search(r'<div class="cmp-wrap reveal">.*?</table>\s*</div>', m.group(0), re.S).group(0)
esc = lambda t: html.escape(t, quote=False)
def attr(t): return html.escape(t, quote=True)

def region(slug):
    title, desc, h1, eyebrow, h2, lead, steps = P[slug]
    nav = ''.join('<a href="../%s/">%s</a>' % (k, v) for k, v in LINKS if k != slug)
    return ('<!--SEO-ABOUT-->\n  <section class="features seo-about" id="alternative">\n    <div class="wrap">\n      <div class="section-head">\n'
      '        <div class="eyebrow">%s</div>\n        <h2>%s</h2>\n        <p>%s</p>\n      </div>\n' % (esc(eyebrow), esc(h2), esc(lead))
      + ('      %s\n' % table if slug == 'remove-background' else '')
      + '      <h3 class="seo-h3">How it works</h3>\n      <ol class="seo-steps">\n' + ''.join('        <li>%s</li>\n' % esc(x) for x in steps) + '      </ol>\n'
      '      <h3 class="seo-h3">More APIC tools</h3>\n      <nav class="seo-links" aria-label="APIC tools"><a href="../">APIC home</a>' + nav + '</nav>\n    </div>\n  </section>\n  <!--/SEO-ABOUT-->')

for slug, (title, desc, h1, *_rest) in P.items():
    url = BASE + slug + '/'
    h = src
    h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % esc(title), h, count=1, flags=re.S)
    h = h.replace('<link rel="canonical" href="%s" />' % BASE, '<link rel="canonical" href="%s" />' % url)
    h = h.replace('<meta property="og:url" content="%s" />' % BASE, '<meta property="og:url" content="%s" />' % url)
    for key in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        h = re.sub(r'(<meta %s content=")[^"]*(")' % key, lambda mm: mm.group(1) + attr(desc) + mm.group(2), h, count=1)
    for key in ('property="og:title"', 'name="twitter:title"'):
        h = re.sub(r'(<meta %s content=")[^"]*(")' % key, lambda mm: mm.group(1) + attr(title) + mm.group(2), h, count=1)
    h = re.sub(r'(<h1 style="[^"]*">)[^<]*(</h1>)', lambda mm: mm.group(1) + esc(h1) + mm.group(2), h, count=1)
    h = re.sub(r'<!--SEO-ABOUT-->.*?<!--/SEO-ABOUT-->', lambda mm: region(slug), h, count=1, flags=re.S)
    crumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'APIC', 'item': BASE},
        {'@type': 'ListItem', 'position': 2, 'name': P[slug][3], 'item': url}]}
    h = h.replace('<link rel="icon"', '<script type="application/ld+json">\n%s\n</script>\n<link rel="icon"' % json.dumps(crumbs, ensure_ascii=False, indent=2), 1)
    h = h.replace("base = 'fonts/'", "base = '../fonts/'")
    os.makedirs(slug, exist_ok=True)
    open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8').write(h)

urls = [(BASE, '1.0')] + [(BASE + k + '/', '0.9' if k == 'remove-background' else '0.8') for k in P]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    '  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>%s</priority></url>\n' % (u, TODAY, pr) for u, pr in urls) + '</urlset>\n'
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
open('robots.txt', 'w', encoding='utf-8').write('User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % BASE)
open('vercel.json', 'w', encoding='utf-8').write(json.dumps({'cleanUrls': True, 'trailingSlash': True}, indent=2) + '\n')
print('wrote %d pages + sitemap.xml, robots.txt, vercel.json' % len(P))
