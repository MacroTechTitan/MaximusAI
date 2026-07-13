# HOWTO — maximus-technical-seo

Six recipes for the most common technical SEO tasks. Each recipe is diagnostic-first: confirm the failure with real tool output before applying a fix.

---

## (a) Diagnose a Core Web Vitals regression

1. **Confirm the regression is real and field-based.** Open Search Console → Core Web Vitals report. Check whether the affected URLs failed at the 75th percentile of real-user (CrUX) data, not just a single lab run. A lab-only failure on an otherwise-passing field metric is lower priority.
2. **Reproduce in the lab.** Run PageSpeed Insights (or `npx lighthouse <url> --view`) on the specific failing URL, not the homepage. Note which metric fails: LCP, INP, or CLS — the fix path differs completely for each.
3. **For LCP**: open Chrome DevTools → Performance panel → record a load → find the LCP element in the timeline. Common causes: slow server response (TTFB), render-blocking CSS/JS, unoptimized/unsized hero image, client-side rendering delaying the LCP element's appearance.
4. **For INP**: use the Performance panel's "Interactions" track to find the slowest interaction. Common causes: long JavaScript tasks on the main thread, heavy event handlers, third-party scripts blocking input response.
5. **For CLS**: use DevTools → Rendering tab → "Layout Shift Regions," or check the PageSpeed Insights CLS breakdown. Common causes: images/ads without reserved dimensions, web fonts causing FOIT/FOUT reflow, content injected above existing content after load.
6. **Apply the targeted fix** (see `examples/cwv-diagnosis-trace.md` for a full worked LCP fix with code) and re-measure with the same tool before declaring it resolved. Then wait for CrUX to refresh (rolling 28-day window) to confirm the field data actually moved.

---

## (b) Audit crawlability on a fresh site

1. Fetch `robots.txt` directly (`curl https://example.com/robots.txt`) and confirm it doesn't disallow `/`, CSS/JS directories, or any path that should be indexable.
2. Fetch `sitemap.xml` and spot-check that listed URLs return 200 (not 3xx/4xx) and are canonical (not duplicates or parameterized variants).
3. Run a crawl (Screaming Frog, Sitebulb, or a simple recursive fetch) starting from the homepage and compare the discovered URL set against the sitemap — any sitemap URL with zero internal links pointing to it is an orphan page.
4. Check Search Console → Pages → "Why pages aren't indexed" for `Discovered – currently not indexed` and `Crawled – currently not indexed` buckets; both usually indicate thin content, duplication, or crawl-budget starvation rather than a hard block.
5. Verify HTTPS and redirect hygiene: no redirect chains longer than one hop, no mixed HTTP/HTTPS internal links.
6. Document findings against `references/technical-seo-checklist.md` and prioritize by indexation impact, not by ease of fix.

---

## (c) Fix canonical / duplication issues

1. Identify duplicates: same or near-identical content served at multiple URLs (with/without trailing slash, `http`/`https`, `www`/non-`www`, tracking parameters, paginated variants, print versions).
2. Pick one canonical URL per content cluster — always the version you actually want indexed and ranked.
3. Add a self-referencing canonical on the canonical page itself:
   ```html
   <link rel="canonical" href="https://example.com/product/widget" />
   ```
4. Add the same canonical URL on every duplicate/near-duplicate variant, pointing to the canonical — never to a redirect target, a 404, or a noindexed page.
5. For parameterized URLs (`?sort=price`, `?utm_source=...`), canonicalize to the clean URL and confirm the parameter doesn't change the page's core content; if it does (e.g., real pagination), don't canonicalize page 2 to page 1 — use `rel=prev/next` conventions or self-canonicalize each paginated page instead.
6. Re-crawl and confirm exactly one canonical tag per page, no conflicting signals from sitemap entries or internal links pointing to non-canonical versions.

---

## (d) Implement hreflang for a 3-locale site

Example: English (default), French, German — all served on locale subpaths.

1. Confirm the URL structure: `example.com/`, `example.com/fr/`, `example.com/de/`.
2. Add reciprocal hreflang tags to **every** locale variant, including the default:
   ```html
   <link rel="alternate" hreflang="en" href="https://example.com/" />
   <link rel="alternate" hreflang="fr" href="https://example.com/fr/" />
   <link rel="alternate" hreflang="de" href="https://example.com/de/" />
   <link rel="alternate" hreflang="x-default" href="https://example.com/" />
   ```
3. **Return-tag rule**: if `/fr/` references `/de/`, then `/de/` must reference `/fr/` back. One-directional hreflang is treated as invalid and ignored.
4. Alternatively (preferred at scale), declare hreflang in the sitemap instead of `<head>` tags — easier to keep consistent across hundreds of URLs:
   ```xml
   <url>
     <loc>https://example.com/</loc>
     <xhtml:link rel="alternate" hreflang="en" href="https://example.com/" />
     <xhtml:link rel="alternate" hreflang="fr" href="https://example.com/fr/" />
     <xhtml:link rel="alternate" hreflang="de" href="https://example.com/de/" />
     <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/" />
   </url>
   ```
5. Validate with Search Console → Legacy tools → International Targeting (or a third-party hreflang validator) to catch missing return tags and locale-code typos.
6. Confirm each locale variant also has correctly localized `lang` attribute (`<html lang="fr">`) and that content is actually translated, not just re-tagged — hreflang on identical content across locales gets ignored.

---

## (e) Log-file analysis for crawl-budget waste

1. Pull raw access logs from the origin server or CDN for at least 30 days (logs, not analytics — bots are typically excluded from analytics tools).
2. Filter to verified search-engine bots by reverse-DNS lookup on the IP (never trust the User-Agent string alone — it's trivially spoofed).
3. Aggregate: hits per URL path, per status code, per day.
4. Find waste signals:
   - High crawl frequency on parameterized/faceted-nav URLs that don't need to be indexed.
   - Repeated crawls of 3xx redirect chains or 404s.
   - Crawl hits concentrated on low-value pages while priority pages get few or no hits.
5. Cross-reference crawl dates against content `lastmod` — pages updated often but rarely crawled are under-served relative to their importance.
6. Act: `noindex`/block waste sources in robots.txt where appropriate, collapse redirect chains to single hops, and add internal links from high-authority pages to under-crawled priority URLs to pull crawl attention toward them. See `references/technical-seo-checklist.md` (Crawlability section) for pass criteria.

---

## (f) Migrate CSR content to SSG for indexation

1. Confirm the problem first: use Search Console → URL Inspection → "View Crawled Page" on a sample product/content page. If the rendered HTML snapshot is missing the content that's visible in a browser, CSR is the likely cause.
2. Identify which routes are indexable-critical (product pages, articles, category pages) versus interactive-only (cart, account, checkout) — only the former needs to change rendering strategy.
3. In Next.js (App Router), convert client-fetched pages to server components with `generateStaticParams` for SSG, or add `revalidate` for ISR:
   ```tsx
   // app/products/[slug]/page.tsx
   export async function generateStaticParams() {
     const products = await getAllProductSlugs();
     return products.map((p) => ({ slug: p.slug }));
   }

   export const revalidate = 3600; // ISR: rebuild this page at most every hour

   export default async function ProductPage({ params }: { params: { slug: string } }) {
     const product = await getProduct(params.slug);
     return <ProductDetail product={product} />;
   }
   ```
4. Run `next build` and check the route summary — confirm the migrated routes show as `●` (SSG) or `λ` (ISR/Server), not left as client-only.
5. Deploy to a staging environment and re-run the Search Console URL Inspection "Test Live URL" check — the rendered HTML should now contain the full content server-side.
6. After production deploy, request re-indexing for the migrated routes and monitor Search Console → Pages over the following 1–2 weeks for the `Crawled – currently not indexed` bucket shrinking. See `examples/js-seo-migration-trace.md` for the full worked trace.
