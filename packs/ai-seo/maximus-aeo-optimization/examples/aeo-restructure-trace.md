# Worked example — restructuring a bloated blog draft for AEO

This trace applies HOWTO recipe (a) to a realistic draft: a blog post about standing desks that ranks reasonably for SEO but has near-zero extractable material. Every change below maps to one of the six AEO levers from `SKILL.md`.

## The original draft (before)

```
Standing Desks: Everything You Need to Know

These days, more and more people are working from home, and one thing
that has become really popular is the standing desk. There are a lot of
reasons why people like them, and in this article we're going to talk
about all of that.

First, let's talk about health. Sitting for a long time isn't great for
you, and standing desks can help with that. Many studies have looked
into this and found some interesting things. It's worth noting that
results can vary from person to person, and there are a lot of factors
that go into it.

There are also different kinds of standing desks. Some are electric,
some are manual, and some just sit on top of your existing desk. Each
one has pros and cons, and it really depends on your budget and how much
space you have.

A lot of customers ask us questions about standing desks, like whether
they're actually worth it, how long it takes to get used to one, and
whether kids can use them too. We get these questions a lot and figured
we'd just address a few of the common ones somewhere in this post.

In conclusion, standing desks can be a good addition to your home office
setup if you think it might work for you.
```

Problems, mapped to the six levers:

- **Entity clarity**: "this," "that," "it" everywhere — no sentence names "a standing desk" as the subject on its own.
- **Quotable atomic claims**: zero. Every sentence depends on the one before it.
- **Factual density**: no numbers, no named studies, no dates.
- **Schema**: none present.
- **Source signals**: no author, no cited study, no organization name.
- **Freshness**: "these days" — no date anywhere.

## Step-by-step restructure

### 1. Definition-first opening (lever: entity clarity)

Replace the throat-clearing intro with a subject-named definition sentence.

**Before:** "These days, more and more people are working from home, and one thing that has become really popular is the standing desk."

**After:** "A standing desk is a height-adjustable desk that lets a user alternate between sitting and standing while working."

### 2. Factual density in the health section (levers: factual density, source signals)

**Before:** "Sitting for a long time isn't great for you, and standing desks can help with that. Many studies have looked into this and found some interesting things."

**After:** "A 2018 meta-analysis published in the *Journal of Occupational and Environmental Medicine* found that using a sit-stand desk reduced daily sitting time by an average of 100 minutes per 8-hour workday. The American Heart Association has separately linked prolonged sitting to increased cardiovascular risk independent of overall exercise levels."

Each sentence now names a source, a number, and a specific finding — three separate atomic, attributable claims instead of one vague one.

### 3. Comparison table instead of prose (lever: content structure)

**Before:** "There are also different kinds of standing desks. Some are electric, some are manual, and some just sit on top of your existing desk. Each one has pros and cons, and it really depends on your budget and how much space you have."

**After:**

| Type | Typical price | Adjustment method | Best for |
|---|---|---|---|
| Electric sit-stand desk | $300-$800 | Motorized, one-touch | Daily switchers, shared workstations |
| Manual crank desk | $150-$350 | Hand crank | Budget buyers, occasional standers |
| Desktop converter | $80-$250 | Manual lift/lower | Renters, no room for a full desk swap |

### 4. FAQ block with real questions (levers: quotable claims, schema readiness)

**Before:** "A lot of customers ask us questions about standing desks... we get these questions a lot and figured we'd just address a few of the common ones somewhere in this post."

**After (becomes its own section, each answer self-contained):**

**Is a standing desk actually worth it?**
For most people who sit more than 6 hours a day, a standing desk is worth the cost because it directly addresses the sedentary time linked to cardiovascular risk by the American Heart Association. It is not a substitute for regular exercise.

**How long does it take to get used to a standing desk?**
Most new users adjust within 1-2 weeks, starting with 30-60 minutes of standing per session and increasing gradually.

**Can children use a standing desk?**
Yes — height-adjustable desks are commonly used in classrooms, and pediatric ergonomics guidance recommends adjusting desk height so the child's elbows rest at a 90-degree angle when standing.

### 5. Freshness marker (lever: freshness)

Added directly under the title: `Last updated: July 2026.` and the health-claims paragraph now cites a specific year (2018) rather than "many studies."

### 6. Author and organization signal (lever: source signals / E-E-A-T)

Added a byline block: `Written by [Author Name], certified ergonomics consultant. Reviewed by the [Company] Workplace Health team.`

## The restructured draft (after) — full text

```
Standing Desks: What They Are, When They Help, and How to Choose One
Last updated: July 2026
Written by Author Name, certified ergonomics consultant.

A standing desk is a height-adjustable desk that lets a user alternate
between sitting and standing while working.

Sitting for extended periods is linked to measurable health risk. A 2018
meta-analysis published in the Journal of Occupational and Environmental
Medicine found that using a sit-stand desk reduced daily sitting time by
an average of 100 minutes per 8-hour workday. The American Heart
Association has separately linked prolonged sitting to increased
cardiovascular risk independent of overall exercise levels.

[comparison table as above]

FAQ

Is a standing desk actually worth it?
For most people who sit more than 6 hours a day, a standing desk is
worth the cost because it directly addresses the sedentary time linked
to cardiovascular risk by the American Heart Association. It is not a
substitute for regular exercise.

How long does it take to get used to a standing desk?
Most new users adjust within 1-2 weeks, starting with 30-60 minutes of
standing per session and increasing gradually.

Can children use a standing desk?
Yes -- height-adjustable desks are commonly used in classrooms, and
pediatric ergonomics guidance recommends adjusting desk height so the
child's elbows rest at a 90-degree angle when standing.
```

## Schema added (Article + FAQPage)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Standing Desks: What They Are, When They Help, and How to Choose One",
  "datePublished": "2024-03-10",
  "dateModified": "2026-07-01",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "jobTitle": "Certified Ergonomics Consultant"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Company Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "mainEntityOfPage": "https://example.com/standing-desks"
}
```

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is a standing desk actually worth it?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "For most people who sit more than 6 hours a day, a standing desk is worth the cost because it directly addresses the sedentary time linked to cardiovascular risk by the American Heart Association. It is not a substitute for regular exercise."
      }
    },
    {
      "@type": "Question",
      "name": "How long does it take to get used to a standing desk?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Most new users adjust within 1-2 weeks, starting with 30-60 minutes of standing per session and increasing gradually."
      }
    },
    {
      "@type": "Question",
      "name": "Can children use a standing desk?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes -- height-adjustable desks are commonly used in classrooms, and pediatric ergonomics guidance recommends adjusting desk height so the child's elbows rest at a 90-degree angle when standing."
      }
    }
  ]
}
```

## Result summary

| Lever | Before | After |
|---|---|---|
| Entity clarity | Pronoun-chained throughout | Every key sentence names "a standing desk," "sit-stand desk," or the specific source |
| Quotable atomic claims | 0 | 6+ (definition, 2 stat sentences, 3 FAQ answers) |
| Factual density | 0 numbers, 0 named sources | 1 named study + year, 1 named organization, 1 price table, 1 angle spec |
| Schema | None | Article + FAQPage JSON-LD |
| Source signals | No author, no org | Named credentialed author, named organization, reviewer line |
| Freshness | "These days" | Explicit "Last updated: July 2026" + dated study reference |

No new facts were invented in this pass — only the American Heart Association's general sitting/cardiovascular-risk position and the ergonomics elbow-angle guideline are commonly cited public claims; in a real restructure, verify each externally-sourced claim against its primary source before publishing (see `SKILL.md` anti-patterns: unattributed claims).
