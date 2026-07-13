# Technical SEO checklist

~50 items across seven categories. Each item lists a pass criterion and how to check it. Use this as the working checklist during an audit (`maximus-seo-audit` consumes the findings); it complements but does not replace `maximus-content-seo` (content quality) and `maximus-ai-seo-strategy` (what to target).

## Crawlability

1. **robots.txt doesn't block indexable paths.** Pass: no `Disallow` on CSS/JS directories or any indexable content path. Check: `curl https://example.com/robots.txt`.
2. **robots.txt references the sitemap.** Pass: a `Sitemap:` directive points to the live sitemap URL. Check: read the file directly.
3. **No orphan pages.** Pass: every indexable/sitemap URL is reachable via at least one internal link. Check: crawl the site (Screaming Frog/Sitebulb) and diff discovered URLs against the sitemap.
4. **Internal link depth is reasonable.** Pass: important pages are reachable within 3–4 clicks from the homepage. Check: crawler's "crawl depth" report.
5. **No infinite crawl spaces.** Pass: faceted navigation, calendar pages, or search-result pages don't generate unbounded URL permutations. Check: crawl logs or a bounded test crawl with parameter tracking.
6. **Redirect chains are single-hop.** Pass: any redirect resolves in one hop, not a chain of 3xx's. Check: `curl -IL` on suspect URLs.
7. **No crawl traps from session IDs or tracking parameters.** Pass: URLs don't multiply per session/click. Check: inspect URL patterns in logs for parameter explosion.
8. **Pagination is crawlable.** Pass: paginated series (page 2, 3, …) have real, followable links, not JS-only "load more" with no URL. Check: view page source for `<a href>` pagination links.
9. **Mobile and desktop see the same links/content.** Pass: no content hidden from the mobile crawl that desktop sees (Google is mobile-first). Check: fetch as Googlebot Smartphone via Search Console.
10. **Fetch/render works for JS-heavy pages.** Pass: Googlebot's renderer successfully executes the page's JS within its render budget. Check: Search Console URL Inspection → "View Crawled Page."

## Indexation

11. **Pages intended to rank return HTTP 200.** Pass: no soft-404s (200 status but "not found" content). Check: Search Console "Page indexing" report, `Not found (404)` and excluded categories.
12. **`noindex` is intentional.** Pass: every `noindex` tag/header is on a page you actually don't want indexed. Check: crawl report of all `noindex` pages, manually review the list.
13. **No conflicting indexation signals.** Pass: a page isn't simultaneously `noindex` and included in the sitemap, or canonicalized to itself while `noindex`'d. Check: cross-reference sitemap, meta robots, and canonical in one crawl export.
14. **Duplicate content resolves to one indexable version.** Pass: near-duplicate pages (print view, `?ref=`, AMP, trailing slash) canonicalize to a single URL. Check: crawl and cluster by content similarity/hash.
15. **Search Console coverage matches expectations.** Pass: indexed count roughly matches known indexable page count; no unexplained "Excluded" spikes. Check: Search Console → Pages report, trend over time.
16. **Thin/low-value pages are handled deliberately.** Pass: thin pages are either improved, `noindex`'d, or consolidated — not left to rot and drag down crawl priority. Check: content-length + engagement audit.
17. **International/duplicate-market pages don't cannibalize.** Pass: locale variants are hreflang-linked, not competing unmarked duplicates. Check: see Internationalization section below.
18. **Structured data errors don't block indexing.** Pass: JSON-LD is well-formed even if rich-result eligibility is separately assessed. Check: Rich Results Test / Search Console Enhancements report.

## Core Web Vitals

19. **LCP < 2.5s at p75 (field data).** Pass: CrUX/Search Console shows "Good" for the URL group. Check: Search Console Core Web Vitals report.
20. **INP < 200ms at p75 (field data).** Pass: same, INP tab. Check: Search Console Core Web Vitals report; note INP replaced FID as the responsiveness metric.
21. **CLS < 0.1 at p75 (field data).** Pass: same, CLS tab. Check: Search Console Core Web Vitals report.
22. **Lab scores corroborate field data.** Pass: Lighthouse/PageSpeed Insights lab run roughly agrees with the field verdict. Check: `npx lighthouse <url> --view`.
23. **LCP element is discoverable early.** Pass: LCP image/text isn't injected late by JS or hidden behind a CSS background-image the preload scanner can't find. Check: DevTools Performance panel, "LCP" marker and element highlight.
24. **No render-blocking CSS/JS on the critical path.** Pass: critical CSS is inlined or minimal; non-critical CSS/JS is deferred/async. Check: PageSpeed Insights "Eliminate render-blocking resources" diagnostic.
25. **Images are properly sized and modern-format.** Pass: served dimensions match display dimensions; WebP/AVIF used where supported. Check: PageSpeed Insights "Properly size images" / "Serve images in next-gen formats."
26. **Layout-shift sources are eliminated.** Pass: images/embeds/ads have reserved dimensions; fonts don't cause visible reflow. Check: DevTools Rendering tab, "Layout Shift Regions," or PSI CLS breakdown.
27. **Long main-thread tasks are broken up.** Pass: no single JS task blocks the main thread long enough to delay input response. Check: DevTools Performance panel, "Long Tasks" flags; PSI "Minimize main-thread work."
28. **Third-party scripts are audited.** Pass: third-party tags (ads, analytics, chat widgets) are lazy-loaded or deferred, not blocking the critical path. Check: PSI "Reduce impact of third-party code."

## Structured data

29. **JSON-LD is valid syntax.** Pass: parses without errors. Check: Google Rich Results Test or `schema.org` validator.
30. **Structured data matches visible content.** Pass: no mismatched prices, names, or availability between markup and rendered page. Check: manual comparison, automate with a diff script for scale.
31. **Correct schema type for the content.** Pass: `Product`, `Article`, `FAQPage`, `BreadcrumbList`, etc. match what's actually on the page. Check: Rich Results Test eligibility report.
32. **Required properties are present.** Pass: each schema type's required fields per schema.org/Google docs are populated (e.g., `Product` needs `name`, `image`, `offers`). Check: Rich Results Test warnings.
33. **No structured data spam.** Pass: markup isn't added to manipulate rich results with content not visible to users. Check: manual review against Google's structured-data guidelines.
34. **Breadcrumbs match the actual navigation path.** Pass: `BreadcrumbList` markup mirrors the real site hierarchy. Check: manual comparison against site navigation.

## Internationalization

35. **hreflang tags are reciprocal.** Pass: every locale pair references each other (A→B and B→A). Check: Search Console International Targeting report or a dedicated hreflang validator.
36. **x-default is declared.** Pass: an `x-default` variant exists for users not matching any listed locale. Check: view source or sitemap hreflang block.
37. **hreflang matches canonical.** Pass: hreflang URLs aren't redirect targets, 404s, or non-canonical duplicates. Check: crawl and cross-reference hreflang targets' status codes and canonicals.
38. **Locale content is actually localized.** Pass: hreflang variants have distinct, translated content — not identical copy re-tagged. Check: manual content diff across locale versions.
39. **`lang` attribute matches hreflang.** Pass: `<html lang="fr">` on the French version, etc. Check: view source per locale.
40. **Currency/pricing localized where relevant.** Pass: e-commerce locale pages show correct local currency and, ideally, pricing. Check: manual review per locale.

## JS rendering

41. **Indexable content is present without JS execution, or reliably rendered.** Pass: "View Crawled Page" in Search Console shows the real content. Check: Search Console URL Inspection.
42. **Critical routes use SSR/SSG/ISR, not pure CSR.** Pass: `next build` output shows Static/ISR/Server, not client-only, for indexable routes. Check: build output route summary.
43. **Metadata (title, description, canonical) is server-rendered.** Pass: present in the raw HTML response, not injected client-side. Check: `curl` the page and grep for `<title>`/`<link rel="canonical">`.
44. **Client-side routing doesn't break deep-linking.** Pass: every route is directly fetchable and returns full content on a fresh load, not just via client-side navigation. Check: `curl` each route directly.
45. **JS errors don't silently blank the page for bots.** Pass: rendering doesn't throw on the crawler's render pass. Check: Search Console rendered-page screenshot/HTML for JS error signs (blank shell).

## Security

46. **HTTPS is enforced site-wide.** Pass: HTTP requests redirect to HTTPS; no HTTP-only pages. Check: `curl -I http://example.com/...` and confirm a 301 to HTTPS.
47. **No mixed content.** Pass: HTTPS pages don't load HTTP sub-resources. Check: DevTools Console for "mixed content" warnings.
48. **Valid, non-expiring-soon certificate.** Pass: cert chain is valid and not within 30 days of expiry. Check: `openssl s_client -connect example.com:443` or browser padlock details.
49. **HSTS is configured (if appropriate).** Pass: `Strict-Transport-Security` header present for sites ready to commit to HTTPS-only. Check: `curl -I https://example.com`.
50. **No security warnings in Search Console.** Pass: "Security Issues" report is clean. Check: Search Console → Security & Manual Actions.
