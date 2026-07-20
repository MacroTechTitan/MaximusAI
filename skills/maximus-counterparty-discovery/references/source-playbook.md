# Source Playbook

## Core source families

1. Regulatory and registration: SEC EDGAR, SEC IAPD, FINRA BrokerCheck, CFTC releases, NFA BASIC, state securities regulators.
2. Litigation and insolvency: PACER where authorized, CourtListener/RECAP, bankruptcy court dockets, receiver/trustee reports, claims registers, complaints and exhibits, state court portals.
3. Institutional allocators: Form ADV, 13F context, family-office websites, conference agendas, podcasts, manager databases, public investment policies, endowment/pension records.
4. Corporate and liquidity events: Form 4, 8-K, Schedule 13D/G, tender offers, merger filings, company press releases, acquisition announcements.
5. Property transactions: licensed real-estate data, public recorder/assessor records, transaction press coverage. Use as a weak capacity signal only.
6. Social and forums: Reddit, public X/LinkedIn posts, futures and trading forums, podcasts, conference transcripts, Substack/blog posts. Follow platform terms and preserve post URL/date/context.
7. CTA-to-CTA indicators: CTA/CPO bios, Form ADV private-fund sections, fund documents, interviews, conference panels, manager-of-managers products, multi-advisor pools, regulatory filings.
8. Professional/contact verification: official organization pages, licensed business-data vendors, public professional directories, user-connected CRM/contact systems.

## Query construction

For each source create:
- exact-entity queries
- role/mandate queries
- event-driven queries
- negative-risk queries
- synonym variants
- date-bounded variants

Examples:
- `"commodity trading advisor" allocator managed futures family office`
- `site:sec.gov/Archives/edgar/data "Form 4" transaction code S`
- `CTA bankruptcy investor schedule LP receiver report`
- `site:reddit.com/r/futures "managed account" allocation`
- `"multi-manager" CTA "managed futures"`

Always record where each query ran and whether it produced useful results.
