# Reference — Schema markup cookbook for AEO

Copy-paste JSON-LD templates for the schema.org types that matter most for AEO. Every template is a runnable starting point — replace placeholder values, delete unused optional fields, and validate before publishing (see Validation tools at the end).

All templates use `@context: "https://schema.org"` and are meant to be embedded in a `<script type="application/ld+json">` tag in the page `<head>` or immediately before `</body>`.

## FAQPage

Highest-leverage schema for AI Overviews and chat-assistant citations. Question `name` and answer `text` must match the visible on-page text verbatim.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is Answer Engine Optimization?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Answer Engine Optimization (AEO) is the practice of structuring content so AI assistants and AI Overviews can extract, quote, or cite it directly in their answers, rather than only optimizing for search-result ranking."
      }
    },
    {
      "@type": "Question",
      "name": "How is AEO different from SEO?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO optimizes for ranking so a human clicks through and reads the page; AEO optimizes for extraction so an AI system can lift a self-contained claim and cite it, often without the user ever visiting the page."
      }
    }
  ]
}
```

**Gotcha:** Google disqualifies FAQ rich results if the schema text doesn't match visible content, or if the FAQ block is used for promotional/ad content rather than genuine Q&A. Keep schema and visible copy synced on every edit.

## HowTo

Use for step-by-step processes. Models frequently extract steps verbatim for "how do I..." queries.

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to add FAQPage schema to a blog post",
  "totalTime": "PT15M",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Identify real questions",
      "text": "Pull 3-8 questions the page already answers in prose, from existing headers or common customer questions."
    },
    {
      "@type": "HowToStep",
      "name": "Write self-contained answers",
      "text": "Write each answer as a 40-300 word paragraph that makes sense with no other context."
    },
    {
      "@type": "HowToStep",
      "name": "Match schema to visible text",
      "text": "Ensure the question and answer text in the JSON-LD exactly matches the text visible on the page."
    },
    {
      "@type": "HowToStep",
      "name": "Validate",
      "text": "Run the page through the Google Rich Results Test and the Schema.org Validator before publishing."
    }
  ]
}
```

**Gotcha:** `totalTime` uses ISO 8601 duration format (`PT15M` = 15 minutes, `PT1H30M` = 1 hour 30 minutes). Omit it rather than guessing if there's no real basis for the estimate.

## Article

Establishes author, publish date, and headline as structured entities — feeds E-E-A-T signals directly to the crawler.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "What Is Answer Engine Optimization (AEO)?",
  "description": "A definition and practical guide to structuring content so LLMs and AI Overviews cite it.",
  "image": "https://example.com/images/aeo-guide-cover.jpg",
  "datePublished": "2026-01-15",
  "dateModified": "2026-07-01",
  "author": {
    "@type": "Person",
    "name": "Jane Doe",
    "jobTitle": "SEO Strategist",
    "url": "https://example.com/authors/jane-doe"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Example Corp",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/blog/what-is-aeo"
  }
}
```

**Gotcha:** `dateModified` should reflect real content changes, not be bumped cosmetically — some engines discount pages that claim frequent updates with no visible content change.

## Organization

Anchors the entity behind the content so a model can attribute claims to a nameable, checkable source. Usually placed site-wide (homepage or a shared template), not per-article.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Corp",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://www.linkedin.com/company/example-corp",
    "https://twitter.com/examplecorp",
    "https://www.crunchbase.com/organization/example-corp"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer support",
    "email": "support@example.com"
  }
}
```

**Gotcha:** `sameAs` links matter more than they look — they let a model cross-reference the organization against other known profiles to corroborate legitimacy.

## Product

For commerce/review content. Price, rating, and availability are the facts most often lifted for shopping-style queries.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Maximus Team Plan",
  "description": "Team collaboration plan for up to 10 seats with shared workspace and priority support.",
  "brand": {
    "@type": "Brand",
    "name": "Maximus"
  },
  "offers": {
    "@type": "Offer",
    "price": "49.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://example.com/pricing/team"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.6",
    "reviewCount": "312"
  }
}
```

**Gotcha:** `aggregateRating` requires real, disclosed review data behind it — schema for ratings you don't actually have is a policy violation, not just an AEO risk.

## Person

Author bios with credentials — strengthens E-E-A-T for expertise-dependent claims (health, finance, legal).

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Jane Doe",
  "jobTitle": "Certified Ergonomics Consultant",
  "worksFor": {
    "@type": "Organization",
    "name": "Example Corp"
  },
  "url": "https://example.com/authors/jane-doe",
  "sameAs": [
    "https://www.linkedin.com/in/janedoe",
    "https://orcid.org/0000-0000-0000-0000"
  ],
  "alumniOf": {
    "@type": "CollegeOrUniversity",
    "name": "State University"
  }
}
```

**Gotcha:** Only include credentials that are true and verifiable — `alumniOf`/`sameAs` claims that don't resolve to a real, matching profile hurt trust signals more than omitting them would.

## BreadcrumbList

Helps establish page hierarchy and topical context — supports entity clarity for the model inferring what a page is "about" within a site.

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "https://example.com/blog"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "What Is Answer Engine Optimization (AEO)?",
      "item": "https://example.com/blog/what-is-aeo"
    }
  ]
}
```

**Gotcha:** The final `ListItem` (the current page) technically doesn't need an `item` URL per spec, but including it avoids validator warnings on some tools — safe to leave in.

## Combining multiple schema types on one page

Multiple JSON-LD blocks can coexist on a single page, either as separate `<script>` tags or as an array under a single `@graph`:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Article", "headline": "..." },
    { "@type": "FAQPage", "mainEntity": [] },
    { "@type": "BreadcrumbList", "itemListElement": [] }
  ]
}
```

Use `@graph` when the types share the same context and you want one script tag; use separate script tags when it's clearer to manage them independently (e.g., Organization schema injected site-wide vs. Article schema per template).

## Common gotchas (cross-cutting)

- **Schema/visible-text mismatch** — the single most common cause of disqualified rich results. Any edit to visible FAQ or HowTo content must be mirrored in the schema.
- **Missing required fields** — `Organization.logo`, `Article.author`, and `Product.offers.price` are commonly required by validators; omitting them causes silent rich-result eligibility loss, not just a warning.
- **Fake or inflated ratings/counts** — `aggregateRating` without real underlying reviews is a policy violation across major search and AI providers.
- **Stale `dateModified`** — bumping the date without a real content change is detectable and discounted over time.
- **Wrong duration/date formats** — `totalTime` and similar fields require ISO 8601 (`PT15M`, `P3D`), not free text like "15 minutes."
- **Orphaned schema** — schema describing content that no longer exists on the page (e.g., FAQ schema left in place after the FAQ section was removed) actively hurts trust once detected.
- **Over-nesting entities** — keep `@type` nesting only as deep as the spec requires; inventing custom properties not in the schema.org vocabulary is ignored by parsers, not rewarded.

## Validation tools

- **Google Rich Results Test** — `https://search.google.com/test/rich-results` — validates against Google's specific rich-result eligibility rules.
- **Schema.org Validator** — `https://validator.schema.org` — validates against the general schema.org vocabulary, independent of any one search engine's rich-result rules.
- **Google Search Console** — Enhancements reports surface schema errors detected post-indexing across the whole site, useful for catching drift over time.

Run both the Rich Results Test and the Schema.org Validator before publishing — they check different things, and passing one does not guarantee passing the other.
