# Concentrated launch bundle — 49 skills + Film Pack

Refreshed 2026-09-20 for the Film Pack launch. Every asset now leads with the Film Pack as the differentiator, with the 49-skill breadth as reinforcement.

Six assets, tuned per platform, ready to post in one 90-minute morning window. Post Tuesday or Wednesday. Never Monday (too much competition), never Friday (audience checking out).

Order:

1. **8:30 AM PT** — Hacker News (Show HN)
2. **9:00 AM PT** — r/LocalLLaMA
3. **9:05 AM PT** — r/Filmmakers
4. **9:10 AM PT** — r/Cinematography
5. **9:15 AM PT** — LinkedIn
6. **9:20 AM PT** — X thread

The Reddit posts are separated by 5 minutes each so mods don't see a burst of the same URL across multiple subs (which triggers self-promo filters).

---

## Asset 1: Hacker News — Show HN

### Title (80-char limit)

```
Show HN: Maximus 49 – open-source AI agent skills, plus a Film Pack that refuses AI slop
```

### URL field

```
https://github.com/MacroTechTitan/MaximusAI
```

### First comment (post immediately after submission)

```
Author here.

Maximus is 49 open-source Agent Skills (SKILL.md format, MIT). Works with Claude, GPT, Gemini, Perplexity, and local models (Llama, Qwen, K3).

The pattern I've been iterating on for two years is what I call the "workhorse" model. A model is intelligence for rent. A skill is a procedure — the specific gotchas a generic model would miss, which is where the value lives.

What's new in this launch: a Film Pack. 5 skills for working filmmakers, feature-length only, console-first, no generative video, no voice cloning, no AI slop. This is the pack that doesn't exist anywhere else in the AI-skill space, because every "AI filmmaking" tool of the last two years has been chasing the wrong problem (generate the frames) instead of the actual problem (format the screenplay, schedule the shoot, budget the film, coordinate post, deliver the master).

The five film skills:

- maximus-screenplay-format — Fountain plain-text → industry-standard PDF (Courier Prime 12pt, 1.5" margin, 55-58 lines/page) + Final Draft .fdx
- maximus-production-schedule — Locked Fountain → stripboard, one-liner, day-out-of-days
- maximus-film-budget — AICP/AMPTP account codes (1000-4700 series), CSV round-trip with Movie Magic Budgeting
- maximus-post-pipeline — Dailies, offline/online conform, EDL/AAF/XML, ACES vs Rec.709, DCP prep, per-buyer deliverables matrix
- maximus-filmhub-delivery — FFprobe-first delivery-master validation, remux-don't-re-encode, includes a WSP/OBA compliance flag for filmmakers who happen to be FINRA-registered

The pack came out of a real Filmhub rejection on a real 4K feature. Filmora had embedded a thumbnail as a second mjpeg stream and Filmhub read it as two movies. The fix wasn't a hours-long 4K re-encode — it was a 30-second ffmpeg -c copy remux. Diagnose before you re-encode.

Rest of the suite is 44 skills across 5 pillars: Cognitive OS (1), Build & Ship (11), AI Engineering (15), Writing/Research/People (10), plus 2 other opt-in packs (AI SEO with 7 skills, Dev Workflow with 1).

Free forever, no signup, no gate, no telemetry.

Happy to answer questions on the film pack specifically, the workhorse model, the SKILL.md format, or any individual skill's implementation. Push-back welcomed — I'd rather hear where the pack is thin than where it's strong.
```

### HN posting rules

- Do not ask friends to upvote from the same IP or new accounts (HN flags voting rings within minutes).
- Do ask established HN users to genuinely engage — a real question in a comment, a real critique.
- Answer every top-level comment within 30 minutes for the first 4 hours.
- If it doesn't front-page in 90 minutes, don't panic. Some posts climb slowly.

---

## Asset 2: r/LocalLLaMA

### Title

```
Maximus is now 49 open-source AI agent skills (works with local Llama/Qwen/K3) — plus a new Film Pack that refuses AI slop
```

### Body

```
Been iterating on this library for two years and shipped the 49th skill today. Full library at https://github.com/MacroTechTitan/MaximusAI (MIT).

The format is Agent Skills (SKILL.md with YAML frontmatter — same format Claude Skills uses, portable to OpenAI Assistants, Perplexity, and any custom orchestrator). Because r/LocalLLaMA cares about running things locally, the two skills specifically for you:

**maximus-k3-model-selection** — decides when Kimi K3 (2.8T MoE, 104B active, 1M context, MXFP4 native) is the right pick vs Claude Fable 5, Opus 4.8, GPT-5.6 Sol, or GLM-5.2. Every recommendation ships with the benchmark that drove it, the harness, and the date the numbers were pulled. Refuses to recommend K3 when task fit is genuinely worse.

**maximus-k3-self-hosting** — plan and execute a self-hosted K3 deployment on your own GPUs. Sizing hardware, choosing vLLM vs SGLang vs TokenSpeed, native MXFP4 weights + MXFP8 activations, OpenAI/Anthropic-compatible endpoint, preserved-thinking across turns, license gate before commercial deployment.

Everything else in the library is model-agnostic — point it at your local Llama or Qwen server just as easily as at a hosted API.

The new addition today is a Film Pack. 5 skills for working filmmakers, feature-length only, no generative video. Not really this sub's territory but worth mentioning because it's the pack that refuses every "AI filmmaking" pitch of the last two years. Fountain screenplay → Final Draft, AICP account-code budgets, stripboards, post pipelines, Filmhub delivery-master validation. Console-first.

Full 5-pillar + 3-pack structure: Cognitive OS 1, Build & Ship 11, AI Engineering 15, Research/People 10, AI SEO 7, Dev Workflow 1, Film 5.

No signup, no telemetry, no upsell, no "free tier with limits." MIT license.

Happy to answer questions on any specific skill. Feedback on where the library is thin is welcomed.
```

### Flair

Use **"Resources"** or **"Discussion"** (never "News" or "Tutorial" for a project link).

---

## Asset 3: r/Filmmakers

### Title

```
Open-source console-based tools for working filmmakers: screenplay formatting, stripboard, AICP budgets, post pipeline, Filmhub delivery validation. Feature-length only. No AI slop.
```

### Body

```
Been shipping a library of AI agent skills for two years and today added a 5-skill pack specifically for working filmmakers. Everything free, MIT, no signup. Not a generative-video tool. Not an "AI filmmaking" tool. It formats, validates, schedules, budgets, and delivers work you already did.

Every AI-tool launch of the last two years has taken a run at "filmmaking." Generate the frames. Generate the voice. Generate the cast. That's not filmmaking. It's slop. This pack is the opposite — it's for people who make features the old way (cameras, cast, shot list, call sheet, color bay, delivery master).

The 5 skills:

**maximus-screenplay-format** — Author your screenplay in Fountain plain text (like Markdown for screenplays). Output to industry-standard PDF (Courier Prime 12pt, 1.5" left margin, 55-58 lines/page) and Final Draft .fdx. Version-controllable, greppable, diffable. Never write a single character of your script in an AI generator.

**maximus-production-schedule** — Turn a locked Fountain script into a scene breakdown, a stripboard grouped by location, a chronological one-liner, and a day-out-of-days matrix showing which cast works which shoot day. Console-first. No Movie Magic Scheduling license required. The AD adjusts for weather, permits, cast holds — the skill produces the first-draft artifacts.

**maximus-film-budget** — Line-item budget templating with standard AICP/AMPTP account codes (1000-4700 series). ATL vs BTL. Contingency, completion bond, fringes, payroll handling. CSV/XLSX for Movie Magic Budgeting round-trip. Never invents a rate — every dollar figure is a TBD for the line producer to fill.

**maximus-post-pipeline** — Dailies workflow, offline/online conform, EDL/AAF/XML round-trip between NLE and color/sound, ACES vs Rec.709 pipeline decision, DCP prep for theatrical, and a per-buyer deliverables matrix for Netflix, Amazon, Apple, A24, Sundance, TIFF.

**maximus-filmhub-delivery** — FFprobe-first delivery-master validation. Includes a real-world story: this whole pack started because a 4K feature got rejected by Filmhub for "Multiple Video Streams Detected." The film was fine. Filmora had embedded a thumbnail as a second mjpeg stream. Fix was a 30-second ffmpeg -c copy remux, not a hours-long re-encode. Diagnose before you re-encode. Preserve the master.

Also includes a WSP/OBA compliance flag for any FINRA-registered filmmaker releasing a film about brokers or investments — a real edge case that would break most tools.

Repo: https://github.com/MacroTechTitan/MaximusAI
Pack: https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/film
Blog post explaining the philosophy: https://github.com/MacroTechTitan/MaximusAI/blob/main/blog/2026-09-20-film-pack-launch.md

Free forever, MIT, no signup. Feedback on where the pack is thin is genuinely welcomed — happy to add the skills you actually need.
```

### r/Filmmakers rules

- Weekly self-promo rules — check the sub sidebar the day of posting.
- Text post only. Not link post.
- Answer every comment within 15 minutes for the first 90 minutes.
- If a mod removes it, one polite modmail: "Happy to strip any promotional framing — the pack is genuinely free and MIT, and I lead with what it does rather than a pitch."

---

## Asset 4: r/Cinematography

### Title

```
Free open-source post-pipeline skill: dailies, offline/online conform, EDL/AAF/XML, ACES vs Rec.709 decision, DCP prep, per-buyer deliverables matrix
```

### Body

```
Shipped an open-source skill today for the technical spine of feature-film post. Free, MIT, no signup. Part of a larger library (49 skills total) but this one is worth calling out here on its own.

**maximus-post-pipeline** covers:

- Dailies workflow — ingest + checksum + LUT + sync + proxy + Frame.io upload
- Offline/online resolution — cutting ProRes 422 Proxy against picture, conforming EDL/AAF/XML to camera originals
- Color pipeline decision tree — ACES vs Rec.709 vs Rec.2020/PQ, when each is right
- DCP prep — J2K in MXF, XYZ color, DCI-P3, 24 fps (not 23.976), tool recommendations (DCP-o-matic, easyDCP)
- Per-buyer deliverables matrix — Netflix (IMF + Dolby Vision), Amazon, Apple, A24, Sundance, TIFF, Cannes, broadcast, aggregators

Not a color-grade skill. Not a mix skill. Not an edit skill. Doesn't touch a frame or a sample. It plans the pipeline, produces the round-trip artifacts, and generates the deliverables matrix. Artists do the artist work.

Also companion skill **maximus-filmhub-delivery** for the delivery-master validation step: ffprobe-first stream check, remux-don't-re-encode discipline, attached-thumbnail cleanup, audio-format correction.

The whole pack came out of a real Ghosted 4K feature that got rejected by Filmhub for "Multiple Video Streams Detected" — Filmora had embedded a thumbnail as a second mjpeg stream. Fix was a 30-second ffmpeg -c copy remux, not a hours-long 4K re-encode.

Repo: https://github.com/MacroTechTitan/MaximusAI
Post pipeline skill: https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/film/maximus-post-pipeline
Filmhub delivery skill: https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/film/maximus-filmhub-delivery

Feedback welcomed. If your bay does something differently and the skill's opinion is wrong, tell me and I'll fix it.
```

### r/Cinematography rules

- Very tolerant of technical posts; less tolerant of anything that reads as marketing.
- Answer technical questions in detail — this sub rewards depth.

---

## Asset 5: LinkedIn

### Post (approximately 2,900 characters)

Use `docs/promo/social-shareable-pack.md` Block 7 verbatim. It's tuned for LinkedIn's professional audience with the workhorse philosophy up front.

### LinkedIn posting notes

- Post at 9:15 AM PT (12:15 PM ET) — peak weekday engagement.
- No hashtag pyramid at the end — deprioritized as of 2025.
- Add the social preview image if generated (see `social-preview-image.md`).
- Reply to every comment in the first hour. LinkedIn's algorithm rewards early reply rate more than absolute like count.

---

## Asset 6: X (Twitter) thread — 6 tweets

Use `docs/promo/social-shareable-pack.md` Block 4 verbatim. Post the whole thread at once, chained. Do not "let it breathe" between tweets.

### X posting notes

- Do not tag anyone in the thread itself. Reply to your own thread with a single "cc @simonw @svpino @LangChainAI @IndieWire — thought this might be interesting" as a separate reply, one hour later. Tagging in the original thread gets throttled.
- Quote-tweet yourself 24 hours later using Block 5 (or with a specific follow-up: "The most common question was X — here's the answer") to recycle the audience.

---

## The 90-minute launch morning — minute by minute

**T-24h (Monday evening if launching Tuesday):**
- DM 5-10 friends: "I'm launching Tuesday at 9 AM PT. Genuine engagement > upvotes. If it's useful to you, an honest comment on HN or one of the Reddit posts would mean a lot."
- Get commitments from 3-5.

**T-30min (8:00 AM PT):**
- Coffee. Phone off notifications. Clear calendar for 4 hours.
- Open all 6 platforms in tabs.

**8:30 AM PT — Post HN.**
- Submit the Show HN.
- Immediately post the first comment (verbatim above).
- DM the friends: "HN is live: [link]."

**9:00 AM PT — Post r/LocalLLaMA.**

**9:05 AM PT — Post r/Filmmakers.**

**9:10 AM PT — Post r/Cinematography.**

**9:15 AM PT — Post LinkedIn.**

**9:20 AM PT — Post X thread.**

**9:30 AM PT to 1:30 PM PT — Answer every comment.**
- Rule: no comment goes more than 30 minutes without a reply.
- If a comment is critical, engage directly. Do not get defensive. "That's a fair point — here's how I've been thinking about it, and I'd genuinely welcome the pushback" wins the room.

**End of day:**
- Screenshot the star count.
- Write down what worked and what didn't.
- Do not post again for at least 5 days. Let it settle.

## Realistic outcome

With the Film Pack differentiator (which we did not have in August):

- **HN:** 400-1,200 stars in 24h if it front-pages. 60-150 if it lands in "New" and stalls.
- **r/LocalLLaMA:** 40-150 stars per top-of-hot day.
- **r/Filmmakers + r/Cinematography:** 30-100 stars combined, plus a different-shape audience (working filmmakers, not AI engineers) who convert to newsletter/follow at higher rates.
- **LinkedIn:** 30-100 stars from professional network.
- **X:** 30-150 stars if the thread gets picked up by one mid-tier account.

Total realistic: **500-1,500 stars in 24-48h**, plus /trending appearance if you clear ~40 in the first 12 hours.
