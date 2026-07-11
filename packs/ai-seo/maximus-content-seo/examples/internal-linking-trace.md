# Worked example — internal linking audit on a 50-post blog

## Setup

A blog with 50 published posts across three topic areas: "email marketing" (18 posts), "SEO basics" (14 posts), and "content strategy" (18 posts). No internal linking plan has ever been deliberately applied — links exist only where a writer happened to add one.

## Step 1 — inventory

Pulling the sitemap (`fetch_url`) and cross-referencing with the CMS export produces a 50-row table: URL, topic area, inbound internal link count, outbound internal link count. Summary after counting:

| Topic area | Posts | Posts with 0 inbound links | Posts with 0 outbound links |
|---|---|---|---|
| Email marketing | 18 | 4 | 6 |
| SEO basics | 14 | 3 | 5 |
| Content strategy | 18 | 5 | 7 |

12 orphan pages (zero inbound links) out of 50 — a material discovery risk.

## Step 2 — map hub and spoke

Each topic area needs exactly one hub. Checking which post in each area is broadest and already ranks best:

- **Email marketing hub:** `/blog/email-marketing-guide` (2,800 words, ranks position 4 for "email marketing guide") — correct hub candidate.
- **SEO basics hub:** no single post qualifies; the closest is `/blog/seo-basics` at 900 words, too thin to serve as a hub. Flagged as a gap — recommend expanding this post before it can anchor the cluster (hand-off note for `maximus-write-article` or a refresh pass per recipe c).
- **Content strategy hub:** `/blog/content-strategy-guide` (3,100 words, ranks position 6) — correct hub candidate.

## Step 3 — identify orphans

The 12 zero-inbound-link posts, cross-referenced against topic area:

1. `/blog/cold-email-subject-lines` (email marketing)
2. `/blog/email-list-segmentation` (email marketing)
3. `/blog/re-engagement-campaigns` (email marketing)
4. `/blog/email-deliverability-basics` (email marketing)
5. `/blog/schema-markup-101` (SEO basics)
6. `/blog/canonical-tags-explained` (SEO basics)
7. `/blog/xml-sitemaps-guide` (SEO basics)
8. `/blog/content-calendar-templates` (content strategy)
9. `/blog/repurposing-content-guide` (content strategy)
10. `/blog/content-audit-checklist` (content strategy)
11. `/blog/brand-voice-guidelines` (content strategy)
12. `/blog/evergreen-vs-trending-content` (content strategy)

Every one of these is a legitimate spoke for its topic area's hub — none is a pruning candidate, they simply were never linked in.

## Step 4 — anchor text check

Grepping the site export for generic anchor phrases turns up 9 instances of "click here" or "read more" across the content-strategy posts specifically (a pattern traced to one contributor's drafting habit). All 9 flagged for anchor-text rewrite.

## Step 5 — produce the link-add plan

| Source page | Target page | Anchor text | Link type |
|---|---|---|---|
| `/blog/email-marketing-guide` (hub) | `/blog/cold-email-subject-lines` | "writing subject lines that get opened" | hub-to-spoke |
| `/blog/email-marketing-guide` (hub) | `/blog/email-list-segmentation` | "segmenting your list by engagement" | hub-to-spoke |
| `/blog/email-marketing-guide` (hub) | `/blog/re-engagement-campaigns` | "running a re-engagement campaign" | hub-to-spoke |
| `/blog/email-marketing-guide` (hub) | `/blog/email-deliverability-basics` | "avoiding the spam folder" | hub-to-spoke |
| `/blog/cold-email-subject-lines` | `/blog/email-marketing-guide` | "back to the full email marketing guide" | spoke-to-hub |
| `/blog/email-list-segmentation` | `/blog/re-engagement-campaigns` | "re-engaging segments that go cold" | spoke-to-spoke (sibling) |
| `/blog/seo-basics` (expand first) | `/blog/schema-markup-101` | "adding schema markup to your pages" | hub-to-spoke (pending hub expansion) |
| `/blog/seo-basics` (expand first) | `/blog/canonical-tags-explained` | "handling duplicate content with canonical tags" | hub-to-spoke (pending hub expansion) |
| `/blog/seo-basics` (expand first) | `/blog/xml-sitemaps-guide` | "submitting an XML sitemap" | hub-to-spoke (pending hub expansion) |
| `/blog/content-strategy-guide` (hub) | `/blog/content-calendar-templates` | "building a content calendar" | hub-to-spoke |
| `/blog/content-strategy-guide` (hub) | `/blog/content-audit-checklist` | "running a content audit" | hub-to-spoke |
| `/blog/content-strategy-guide` (hub) | `/blog/brand-voice-guidelines` | "defining your brand voice" | hub-to-spoke |
| `/blog/content-calendar-templates` | `/blog/evergreen-vs-trending-content` | "balancing evergreen and trending topics" | spoke-to-spoke (sibling) |
| `/blog/repurposing-content-guide` | `/blog/content-strategy-guide` | "part of a broader content strategy" | spoke-to-hub |
| (9 posts, content-strategy area) | n/a — anchor text rewrite only | replace "click here" / "read more" with destination-topic phrase | anchor-text fix |

## Step 6 — priority order

1. Fix the 12 orphans first (biggest crawl-discovery risk) — all rows above targeting the 12 listed URLs.
2. Flag the SEO-basics hub gap as a blocking dependency — the three schema/canonical/sitemap links are written into the plan but held until the hub post is expanded past 900 words, otherwise they'd be linking into a page too thin to justify hub status.
3. Anchor text cleanup last — lowest risk, easiest to batch in one editing pass across the 9 flagged instances.

## Step 7 — re-check after execution

After links are added, re-pull the sitemap and confirm all 12 previously-orphaned URLs now show at least one inbound internal link, and that the SEO-basics hub has been expanded before its three spoke links go live.
