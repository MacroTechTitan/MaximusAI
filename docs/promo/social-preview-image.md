# Social preview image — generation and upload

GitHub uses this image whenever the repo is shared on X, LinkedIn, Slack,
Discord, or iMessage. A generic default image kills click-through by roughly
half. This is one of the highest-ROI 10-minute jobs in the whole promo pack.

## Specifications

- **Dimensions:** 1280 × 640 pixels (exact — GitHub crops if you go over)
- **Format:** PNG (SVG not accepted)
- **File size:** Under 1 MB
- **Safe zone:** Keep all text at least 80px from every edge — some platforms
  (LinkedIn, iMessage) crop the top and bottom aggressively.

## Design brief

Matte black background. Single amber horizontal accent line one-third of the
way down. Typography-first — no illustration, no horse silhouette, no icons.
The design has to survive being 400px wide in a LinkedIn feed.

Layout:

```
+----------------------------------------------------------+
|                                                          |
|                                                          |
|       Maximus                                            |
|       ────────                                           |   ← amber accent
|                                                          |
|       43 skills.  5 pillars.  Free forever.              |
|                                                          |
|                                                          |
|                                maximus.macrotechtitan.com|
+----------------------------------------------------------+
```

- **"Maximus"** — 120pt serif (Playfair Display, EB Garamond, or similar).
  Weight: regular. Color: #E8E8E8 (near-white on black).
- **Amber accent line** — 4px tall, ~200px wide, sitting immediately under
  the word "Maximus." Color: #E1A34B (warm amber, not neon orange).
- **"43 skills. 5 pillars. Free forever."** — 42pt sans-serif (Inter or
  Söhne). Weight: 400. Color: #B8B8B8 (dimmer than the title).
- **URL** — 24pt monospace (JetBrains Mono or IBM Plex Mono). Weight: 400.
  Color: #E1A34B (matches accent line).
- **Background** — #0A0A0A (matte black, not pure black — pure black looks
  like a broken image on some clients).

Absolutely no: neural-network graphics, glowing brains, robot hands, gears,
gradients, drop shadows, or emoji.

## Prompt to paste into an image generator

Use whichever tool you prefer — the prompt is written to work in Midjourney,
DALL-E 3, Stable Diffusion, Adobe Firefly, or Ideogram. Ideogram handles
exact text best in 2026; use it if you have access.

```
A minimalist typography-only social banner. 1280x640 pixels. Widescreen.

Matte black background (#0A0A0A). No illustration. No graphics. No icons.
Typography only.

Left-aligned, positioned in the upper-third of the frame:
- Large serif word "Maximus" in near-white (#E8E8E8). Approximately 120 point.
  Font is a classic literary serif — Playfair Display, EB Garamond, or Cormorant.
  Restrained. Understated. Not decorative.
- Directly under the word "Maximus": a single horizontal amber line, 4 pixels
  tall, 200 pixels wide, in warm amber (#E1A34B). Not neon. Not orange. Warm.

Left-aligned, centered vertically below the title with breathing room:
- One line of clean sans-serif text: "43 skills.  5 pillars.  Free forever."
  In light gray (#B8B8B8). Approximately 42 point. Font is Inter or Söhne.

Bottom-right corner, with generous padding:
- One line of monospace text: "maximus.macrotechtitan.com"
  In warm amber (#E1A34B). Approximately 24 point. Font is JetBrains Mono
  or IBM Plex Mono.

Overall aesthetic: matte, cinematic, restrained, editorial. Reads like a
book jacket or an editorial print ad, not a SaaS banner. No gradients, no
glow, no shadows, no textures, no photographic elements. Flat matte black.

Style: Swiss typography, Massimo Vignelli, editorial print design, matte
finish, 4:1 aspect ratio widescreen banner.
```

## Text-rendering fallback

Image generators still sometimes garble exact text (2026 has improved, but
not perfectly). If the render comes back with "Maxlmus" or "43 skllls",
either:

1. Regenerate with the seed varied — usually resolves in 2–3 attempts.
2. Or generate the black background + amber line as the base image, then
   overlay the text in Figma, Canva, or Photoshop.

The Figma / Canva route is faster if the first two generations garble text:

- Figma → new frame 1280×640 → fill #0A0A0A → add three text layers as
  specified above → export as PNG.
- Canva → custom size 1280×640 → same layers → download as PNG.

## Upload

1. Go to https://github.com/MacroTechTitan/MaximusAI/settings.
2. Scroll to "Social preview."
3. Click "Edit" → "Upload an image..."
4. Select the PNG.
5. Verify by pasting `https://github.com/MacroTechTitan/MaximusAI` into
   the Twitter/X card validator: https://cards-dev.twitter.com/validator
   (or just paste it into a draft LinkedIn post to preview).

The image can be updated any time. When you cross 50 skills or hit a
star milestone, refresh the image with the new numbers.
