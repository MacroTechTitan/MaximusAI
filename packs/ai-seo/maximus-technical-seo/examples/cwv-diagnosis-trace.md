# Worked example: diagnosing and fixing an LCP failure

**Scenario**: `/products/trail-runner-x2` on a Next.js e-commerce site is flagged in Search Console's Core Web Vitals report as failing LCP at the 75th percentile (field data: 4.1s, threshold 2.5s). The task: find the actual cause and fix it, not guess.

## Step 1 — Confirm the regression is field-real

Search Console → Core Web Vitals → Mobile → the URL group containing this page shows "Poor" for LCP over the last 28 days, at 4.1s p75. This is real user data (CrUX), not a lab artifact — worth fixing.

## Step 2 — Reproduce in the lab

```bash
npx lighthouse https://example.com/products/trail-runner-x2 \
  --only-categories=performance --view --preset=mobile
```

Lighthouse reports LCP at 4.3s, consistent with the field data. The report identifies the LCP element as the hero product image (`<img class="hero-shot">`).

## Step 3 — Inspect in DevTools Performance panel

Open Chrome DevTools → Performance → record a reload with "Slow 4G" throttling. The trace shows:

- TTFB: 380ms (acceptable).
- A render-blocking stylesheet (`/styles/global.css`, 210KB, unminified) delays first paint until ~1.6s.
- The hero image itself is a 2400×1600px JPEG served at native resolution and only decoded/painted at ~3.9s, because it isn't marked as a priority resource and the browser discovers it late (it's set via a CSS `background-image`, not an `<img>` tag, so the preload scanner can't find it early).

Two causes stack: a blocking oversized stylesheet, and a hidden/undiscoverable LCP image.

## Step 4 — Confirm with PageSpeed Insights diagnostics

PageSpeed Insights (field + lab) flags:
- "Eliminate render-blocking resources" → `global.css`.
- "Preload Largest Contentful Paint image" → the hero image.
- "Properly size images" → the hero is serving a 2400px-wide image into a 600px-wide slot.

All three diagnostics point at the same two fixes.

## Step 5 — Apply the fixes

**Fix 1: convert the CSS background-image hero to a real `<img>` with `priority` (Next.js `Image`) so the preload scanner and Next.js can prioritize it:**

```tsx
// Before
<div className="hero-shot" style={{ backgroundImage: `url(${product.heroUrl})` }} />

// After
import Image from "next/image";

<Image
  src={product.heroUrl}
  alt={product.name}
  width={800}
  height={533}
  priority
  sizes="(max-width: 768px) 100vw, 800px"
/>
```

`priority` tells Next.js to add `<link rel="preload">` for this image and skip lazy-loading it — exactly what an LCP element needs.

**Fix 2: split and defer non-critical CSS.** Move above-the-fold styles inline (Next.js does this automatically for CSS Modules/styled-jsx per route) and defer the rest:

```tsx
// next.config.js
module.exports = {
  experimental: {
    optimizeCss: true, // enables critical CSS extraction
  },
};
```

And audit `global.css` for rules unrelated to the product page template — split into route-scoped CSS Modules so the product page doesn't load unrelated page styles.

**Fix 3: serve appropriately sized images.** With `next/image`, sizing and responsive `srcset` are automatic once `width`/`height`/`sizes` are set correctly (as in Fix 1) — Next.js's built-in image optimizer generates the right resolution per `sizes` breakpoint.

## Step 6 — Re-measure

```bash
npx lighthouse https://staging.example.com/products/trail-runner-x2 \
  --only-categories=performance --view --preset=mobile
```

Lab LCP drops from 4.3s to 2.1s. Deploy to production, then wait for the CrUX 28-day rolling window to refresh before declaring the field metric fixed — a lab win is a leading indicator, not confirmation.

## Step 7 — Confirm in the field

Two to four weeks later, Search Console → Core Web Vitals shows the URL group has moved from "Poor" to "Good" for LCP at p75. Regression closed.

## Takeaways

- Lab tools (Lighthouse, PageSpeed) tell you *what's slow*; field tools (Search Console CWV, CrUX) tell you *whether it matters to real users*. Use both — lab to diagnose, field to confirm.
- LCP failures are almost always one of: slow TTFB, render-blocking resources, or a late-discovered/oversized LCP element. Check all three before touching code.
- `next/image` with `priority` solves the "late discovery" half of LCP failures for free; it does not fix a slow TTFB or blocking CSS — those need separate fixes.
