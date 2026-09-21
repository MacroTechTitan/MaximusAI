# Example: post plan for a $1M indie feature (streamer + festival)

## Situation

- 96-page screenplay, 14-day shoot wrapped 2026-10-18
- Camera: ARRI Alexa 35, ProRes 4444 XQ, 3.8K 16:9
- Sound: Sound Devices MixPre-10 II, 24-bit 48kHz, double-system
- Distribution deals confirmed:
  - Sundance premiere (Jan 2027)
  - Netflix streamer window (Q2 2027)
  - Filmhub aggregator (Q3 2027 secondary window)
- Post budget: $154k (per top-sheet example in `maximus-film-budget`)
- Post house: local color/sound bay, 4-week booking

## Decisions locked at prep

| Decision | Locked value | Reason |
|---|---|---|
| Offline codec | ProRes 422 Proxy | Editorial cuts on laptop, needs to be light |
| Show LUT | ARRI LogC3 → Rec.709 K1S1 | DP's preferred viewing LUT |
| Reel naming | `A001_C###_YYMMDD_R1` | Standard ARRI convention |
| Frame rate | 24 fps | Locked at 24, not 23.976, to simplify DCP prep |
| Color pipeline | **ACES 1.3** | Theatrical (Sundance DCP) + HDR (Netflix) → ACES required |
| Round-trip format | AAF | Post house is Avid + Resolve, AAF is common denominator |

## Pipeline plan

```
Camera negatives (ProRes 4444 XQ)
  → DIT: ACES sync + K1S1 viewing LUT baked to proxies
  → Dailies: nightly, delivered before next-day call, Frame.io links
  → Editorial: Avid, cuts ProRes 422 Proxy against picture + sync sound
  → Picture lock: 2026-11-30
  → Online conform: Resolve, relink AAF to camera originals, verify
  → Color grade: Resolve, ACES timeline, 6 days
      → Deliverable 1: DCI-P3 DCP for Sundance
      → Deliverable 2: Rec.2020 PQ master for Netflix Dolby Vision + HDR10
      → Deliverable 3: Rec.709 SDR master for Filmhub
  → Sound edit + mix: Pro Tools, 3 weeks starting picture lock
      → 5.1 discrete + stereo M&E for all deliverables
  → VFX: 12 shots, 4 weeks parallel to color
  → Final finish: 2027-01-05
```

## Deliverables matrix

```
==================================================
NORTH OF NOWHERE — Deliverables Matrix (v1.0)
==================================================

SUNDANCE (world premiere)
  Package:      DCP INTEROP
  Video:        2K DCI 2048x858 (2.39:1), 24 fps
                XYZ color, gamma 2.6, DCI-P3 gamut
  Audio:        5.1 discrete + stereo M&E, 24-bit 48kHz PCM
  Extras:       ProRes 4444 XQ backup, key art (theatrical poster),
                8 production stills, EPK, subtitle files (SRT English)
  Delivery:     2026-12-15
  Ship to:      Sundance Technical Services (address on submission portal)

NETFLIX (streamer, post-Sundance window)
  Package:      IMF (Interoperable Master Format)
  Video:        4K UHD 3840x2160 (letterboxed to 2.39:1)
                Rec.2020 / PQ, Dolby Vision + HDR10 fallback
  Audio:        Dolby Atmos preferred, discrete 5.1 + stereo M&E
                24-bit 48kHz
  Extras:       Textless masters, English SDH captions, forced subtitles
                Foreign-language dubs when licensed
  Delivery:     2027-02-15 (contract deadline)
  Contact:      Netflix Post-Ops (specific contact per contract)

FILMHUB (aggregator, secondary window)
  Package:      MP4
  Video:        4K UHD 3840x2160, H.264 High profile
                Rec.709 SDR, 24 fps
                ~70 Mbps video bitrate
  Audio:        AAC LC stereo, 48kHz, 320 kbps
                One video stream, one audio stream, no extras
  Extras:       Key art JPG (3000x2000)
  Delivery:     Q3 2027 secondary window
  Prep skill:   See maximus-filmhub-delivery for validation
```

## Budget allocation (from post subtotal $154k)

| Line | Amount | Notes |
|---|---|---|
| Editing (4000)         | $42,000 | Editor 8 weeks, AE 6 weeks, edit suite rental |
| Music (4100)           | $22,000 | Composer flat + orchestration + music clearance reserve |
| Post sound (4200)      | $38,000 | Sound designer, mixer, foley artist, dialogue editor, ADR reserve |
| Post DI/VFX/color (4300)| $46,000 | Colorist 6 days, VFX 12 shots at ~$1500/shot, DCP mastering $8k |
| Titles & opticals (4400)| $6,000 | Motion designer for main title sequence + end credits |
| **Subtotal**           | **$154,000** | |

## Risk flags for the post supervisor

1. **DCP mastering budget is tight.** $8k allows one DCP master + one revision. If Sundance rejects the first DCP for spec, second revision may exceed budget.
2. **Dolby Vision grade adds ~$8-12k over Rec.709 grade.** Confirm Netflix Dolby Vision is contractual before allocating.
3. **Music clearance reserve is small ($3k of the $22k).** Any needle-drop of a commercial song will blow this. Composer-only budget assumed.
4. **VFX at $1500/shot** is achievable for beauty work but not for full CGI. Confirm the 12 shots are the right scope.
5. **ADR reserve** should be booked studio time for at least 2 cast members. Any more and audio budget is tight.

## What the skill did

- Planned the pipeline
- Locked prep decisions
- Generated the deliverables matrix
- Flagged budget risks

## What the skill did not do

- Did not book the color bay
- Did not select the editor, colorist, or mixer
- Did not upload dailies
- Did not conform a single frame
- Did not master a DCP

Those are the artists' work. This skill produces the technical framework the artists work inside.
