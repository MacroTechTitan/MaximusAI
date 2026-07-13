# Worked example: migrating client-rendered product pages to SSG/ISR

**Scenario**: A Next.js app renders product pages entirely client-side — the route shell ships empty and a `useEffect` fetches product data after mount. Search Console shows most product URLs stuck in "Crawled – currently not indexed." The task: migrate to SSG/ISR and verify indexation actually improves.

## Step 1 — Confirm the CSR problem, don't assume it

Search Console → URL Inspection → paste a sample product URL → "View Crawled Page" → "HTML." The captured HTML shows:

```html
<div id="__next">
  <div class="product-page-shell"></div>
</div>
<script src="/_next/static/chunks/product-page.js"></script>
```

No product name, price, or description in the rendered snapshot — confirms Googlebot's renderer either didn't wait for or didn't execute the client fetch reliably. This is the actual failure, not a guess.

## Step 2 — Inspect the current implementation

```tsx
// app/products/[slug]/page.tsx  (BEFORE — client component, fetch on mount)
"use client";

import { useEffect, useState } from "react";

export default function ProductPage({ params }: { params: { slug: string } }) {
  const [product, setProduct] = useState(null);

  useEffect(() => {
    fetch(`/api/products/${params.slug}`)
      .then((res) => res.json())
      .then(setProduct);
  }, [params.slug]);

  if (!product) return <div className="product-page-shell" />;

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <span>{product.price}</span>
    </div>
  );
}
```

Every piece of content a search engine needs is fetched after the initial paint, client-side only.

## Step 3 — Decide the rendering strategy

Run the JS SEO decision tree from `SKILL.md`:

- Content is indexable-critical (product name, price, description) → not CSR-only.
- Content doesn't vary per user/session → not SSR-per-request.
- Content (price, stock) changes periodically but not per-request → **SSG + ISR** is the right fit: pre-render at build time, revalidate on an interval so price/stock updates without a full redeploy.

## Step 4 — Migrate to a server component with `generateStaticParams` + ISR

```tsx
// app/products/[slug]/page.tsx  (AFTER — server component, SSG + ISR)
import { getAllProductSlugs, getProduct } from "@/lib/products";
import type { Metadata } from "next";

export const revalidate = 3600; // regenerate this page at most every hour

export async function generateStaticParams() {
  const slugs = await getAllProductSlugs();
  return slugs.map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Promise<Metadata> {
  const product = await getProduct(params.slug);
  return {
    title: `${product.name} | Example Store`,
    description: product.shortDescription,
    alternates: { canonical: `https://example.com/products/${params.slug}` },
  };
}

export default async function ProductPage({
  params,
}: {
  params: { slug: string };
}) {
  const product = await getProduct(params.slug);

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <span>{product.price}</span>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Product",
            name: product.name,
            description: product.description,
            offers: {
              "@type": "Offer",
              price: product.price,
              priceCurrency: "USD",
              availability: "https://schema.org/InStock",
            },
          }),
        }}
      />
    </div>
  );
}
```

Notes on the migration:
- `generateStaticParams` pre-renders every known product slug at build time — full HTML with content present for each.
- `revalidate = 3600` turns this into ISR: after the first hour, the next request triggers a background regeneration so price/stock drift doesn't require a redeploy.
- `generateMetadata` moves the canonical tag and meta description server-side too — these were likely also missing or client-injected before.
- Product `Product` JSON-LD is now emitted server-side in the initial HTML, making it visible to any crawler without JS execution — bonus fix for `maximus-aeo-optimization`-relevant rich-result eligibility.

## Step 5 — Verify the build output

```bash
npm run build
```

```
Route (app)                              Size     First Load JS
○ /products/[slug]                       2.1 kB    89 kB
  ├ /products/trail-runner-x2
  ├ /products/summit-pack-40l
  └ [+248 more paths]
```

The `○` symbol confirms these routes are now statically generated (SSG/ISR), not server-only or client-only.

## Step 6 — Verify in staging before shipping

Deploy to a staging URL, then in Search Console → URL Inspection → "Test Live URL" (or fetch the raw HTML directly):

```bash
curl -s https://staging.example.com/products/trail-runner-x2 | grep -A2 "<h1"
```

```html
<h1>Trail Runner X2</h1>
<p>A lightweight trail running shoe built for technical terrain.</p>
```

Content is now present in the raw server response — no JS execution required to see it.

## Step 7 — Ship and monitor indexation

1. Deploy to production.
2. Submit the updated sitemap (or request re-crawl for a sample of affected URLs via Search Console).
3. Track Search Console → Pages weekly. Expect the `Crawled – currently not indexed` count for `/products/*` to shrink over 2–4 weeks as Google re-crawls and finds real content.
4. Cross-check with log-file analysis (`HOWTO.md` recipe e) to confirm crawl frequency on product pages increases post-migration — a sign Google now finds them worth re-visiting.

## Takeaways

- Never assume CSR is the problem — confirm with "View Crawled Page" first. The fix is expensive; the diagnosis is cheap.
- SSG + ISR is the right default for content that changes periodically but not per-request (most product catalogs, most content sites) — full SSR is usually overkill and costs more at request time.
- Moving JSON-LD server-side in the same migration is close to free and directly benefits `maximus-aeo-optimization` rich-result eligibility — bundle it into the same PR.
