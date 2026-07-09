# Boolean Query Cookbook

Proven patterns for step 3 (Boolean Query Build) of the deep loop. Use these as templates, not literal copy-paste — always substitute the actual must-haves/synonyms from the current brief.

## LinkedIn X-Ray (via `search_web`)

X-ray search means searching a site's indexed public pages through a general search engine rather than the site's own search box — useful because LinkedIn's own search is heavily gated for non-Recruiter-seat accounts.

**Base pattern:**
```
site:linkedin.com/in ("title synonym 1" OR "title synonym 2") (must-have skill) (must-have skill 2) -exclusion
```

**Worked examples:**
- `site:linkedin.com/in ("senior backend engineer" OR "staff engineer" OR "senior software engineer") (Go OR Golang) (Kubernetes) -"talent acquisition" -recruiter`
- `site:linkedin.com/in ("site reliability engineer" OR SRE OR "platform engineer") (Terraform) (AWS OR GCP OR Azure) (remote)`
- `site:linkedin.com/in ("product designer" OR "senior product designer") (fintech OR banking) (Figma)`

**Rules of thumb:**
- Always OR-chain title synonyms — "Senior Software Engineer," "Staff Engineer," "Senior Backend Engineer" are often the same role at different companies.
- Keep the AND chain to 2-3 hard must-haves max per query. More than that over-narrows and returns near-zero results (the single biggest failure mode — see Gotchas).
- Use `-recruiter -"talent acquisition" -"hiring manager"` to cut recruiter/HR noise, which otherwise pollutes people-search results heavily.
- Run title-synonym rotation as *separate* queries when the OR chain still under-returns, not just as one mega-query.

## GitHub Advanced Search

GitHub's own search syntax supports language, topic, org, and activity filters directly — no X-ray needed.

**Patterns:**
- By language + topic: `language:Go topic:distributed-systems` (use GitHub's code/repo search or `search_web` with `site:github.com`)
- By org membership: `org:target-company-org` to find engineers who contribute to a target company's public repos
- By contribution to a known project: search a project's `CONTRIBUTORS.md` or its contributor graph directly for names, then cross-reference to LinkedIn
- By recency: filter/sort by "recently updated" or check commit dates directly on candidate profiles — recent activity is a strong passive-candidate and recency signal

**Rules of thumb:**
- GitHub activity is evidence of hands-on skill that a LinkedIn title cannot provide by itself — always treat a GitHub match as a strong corroborating signal in step 5 (Enrichment).
- A dormant GitHub account (no commits in 1+ years) is weak evidence on its own; pair with a current LinkedIn title before counting it as a live signal.
- Search star/fork-worthy personal projects too, not just employer-org contributions — side projects often reveal skill depth a day job doesn't showcase.

## Google/Bing Site-Search Patterns (general)

For sources without a dedicated advanced-search UI (Stack Overflow user pages, Kaggle profiles, Behance/Dribbble, conference speaker pages):

- `site:stackoverflow.com/users ("Go" OR "Kubernetes")` — weaker signal source, use as tertiary corroboration only.
- `site:kaggle.com ("competition" OR "notebook") (NLP OR "large language model")` for data/ML roles.
- `site:behance.net (fintech OR banking) ("case study" OR "onboarding")` for design roles.
- `("KubeCon" OR "PyCon" OR "NeurIPS") speakers 2024 2025 [topic]` for conference-speaker discovery — a strong passive-candidate signal since it indicates public technical credibility.
- `site:linkedin.com/in ("[Target Company] alumni" OR "formerly at [Target Company]")` for alumni-network sourcing.

## Boolean combination structure (general template)

Every query set should include, at minimum, one query of each type:

1. **AND-chain (precision)**: all must-haves combined — narrowest, highest-precision, often smallest result count.
2. **OR-chain (recall)**: title/skill synonyms combined with OR — broadest, used to catch people whose title doesn't match the "obvious" phrasing.
3. **NOT-chain (noise reduction)**: exclude recruiters, students, wrong-seniority terms, and (for X-ray searches) index noise like job-posting pages that also contain the same keywords.

## Common gotchas

- **Over-narrow AND chains.** Stacking 4+ hard requirements into one AND chain often returns zero or near-zero results, because LinkedIn/GitHub indexing and profile text don't reliably contain every exact term. Cap at 2-3 hard musts per query; use separate queries for the rest.
- **Single fixed-phrase queries.** Running only `"senior backend engineer" Go Kubernetes` and stopping there under-returns by design — real profiles use dozens of phrasing variants. Always rotate synonyms across multiple query variants (see step 3 iteration rule in `deep-loop-spec.md`).
- **Ignoring exclusion terms.** Without `-recruiter -"talent acquisition"`, X-ray searches are frequently dominated by recruiters who have the same keywords in their own profiles (because they recruit for that skill set).
- **Treating one source as sufficient.** A LinkedIn-only search misses passive candidates who are under-indexed there but highly visible on GitHub, in papers, or at conferences. Always cross reference at least 2 source types for technical roles.
- **Stale query reuse.** A query set built for one role/level shouldn't be copy-pasted for a different seniority — "senior" vs. "staff" vs. "principal" have different typical phrasing and different realistic must-have bars.
- **Mistaking search-engine indexing gaps for "no candidates exist."** If a well-constructed query set returns very few hits, broaden (drop a must-have to nice-to-have, add synonyms, add a source) before concluding the talent pool is genuinely small.
