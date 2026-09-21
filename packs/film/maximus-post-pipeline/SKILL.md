---
name: maximus-post-pipeline
description: "Technical spine of feature-film post: dailies workflow, offline/online resolution, EDL/AAF/XML round-trip between NLE and color/sound bays, ACES vs Rec.709 color pipeline decisions, DCP prep for theatrical, deliverables matrix for streamer/festival/broadcast. Use when planning post for a feature, setting up offline that will conform to higher-res online, deciding ACES vs Rec.709 vs Rec.2020/HDR, preparing DCP for theatrical/festival, generating deliverables matrix for Netflix/Amazon/Apple/A24/festivals, or the user says 'post pipeline', 'dailies workflow', 'offline online conform', 'EDL AAF XML', 'ACES workflow', 'DCP prep', 'deliverables matrix', 'streamer specs', 'color pipeline'. Not for creative work (edit, grade, mix) or TV episodic post. Produces the pipeline plan; artists execute the creative work."
license: MIT
metadata:
  pack: film
  authored_by: Macro Tech Titan
---

# maximus-post-pipeline

Technical spine of feature-film post-production. Plans the pipeline, produces the round-trip artifacts, generates the deliverables matrix. Not a color-grade, sound-mix, or edit skill.

## Core operating rules

1. **Decide offline resolution before rolling on set.** Camera negatives (ProRes 4444 XQ, RAW, BRAW, R3D) are too heavy for a laptop-based offline edit. Editorial cuts proxies at ProRes 422 Proxy or DNxHD 36. Decision made at prep, not at wrap.
2. **Keep offline and online in sync via timecode + reel names.** Every camera clip must have unique reel name and continuous timecode. Editorial cuts against proxies; online conforms against camera originals using EDL/AAF/XML round-trip.
3. **Pick the color pipeline at prep.** ACES for finished color pipelines that will include HDR grading or theatrical DCP. Rec.709 SDR for streamer-only, indie, festival-DCP-optional. Once picked, LUTs are consistent from on-set monitor through DIT to editorial proxies to final grade.
4. **Round-trip formats are boring; pick the one your bays accept.** Avid uses AAF. Premiere and Resolve use XML. Final Cut uses FCPXML. EDL is the lowest common denominator. Pick one and stick with it.
5. **Sound follows picture lock, not before.** Sound editorial (dialogue edit, ADR, foley, sound design) starts at picture lock. Doing it earlier means redoing it after the lock. Music can start earlier at composer's risk.
6. **DCP is a specialty output.** J2K sequences in an MXF wrapper, 24-bit 48/96 kHz PCM audio, XYZ color space, DCI-P3 gamut. Use dedicated tools (DCP-o-matic, easyDCP, Colorfront). Don't try to hand-roll it.
7. **Deliverables matrix is per-buyer.** Netflix, Amazon, Apple, A24, Sundance, TIFF, Cannes each have their own spec. Look up the current spec at delivery time, not from memory.

## Standard post pipeline (linear)

```
Camera negatives → DIT sync + LUT → Dailies (offline proxies + sound sync)
                                                 │
                                                 ▼
                                           Offline edit
                                                 │
                                                 ▼
                                        Picture lock (v1)
                                    ┌────────────┼────────────┐
                                    ▼            ▼            ▼
                              Online conform  Sound edit   VFX finals
                                    │            │            │
                                    ▼            ▼            ▼
                                Color grade   Sound mix    Composite
                                    │            │            │
                                    └────────────┼────────────┘
                                                 ▼
                                        Final finish (v.final)
                                                 │
                                    ┌────────────┼────────────┐
                                    ▼            ▼            ▼
                                  DCP        Master MP4   Streamer specs
                              (theatrical)  (aggregators) (Netflix/Amazon)
```

## Dailies workflow

Dailies happen every night the camera rolls. Steps:

1. **Ingest** camera cards to primary storage + backup.
2. **Verify** with checksum (md5 or xxHash). Never move on unverified.
3. **Sync sound** if double-system. Match slate + timecode.
4. **Apply show LUT** (from color prep) for viewing.
5. **Transcode to editorial proxy** (ProRes 422 Proxy, DNxHD 36, or similar).
6. **Deliver** to editorial with viewing links (Frame.io, Sohonet Clearview, or similar).
7. **Publish call sheet-linked note** so director and DP see dailies before next-day call.

Turnaround: dailies must land before the next day's call. Anything longer breaks the DP's ability to adjust.

## Offline/online conform

- **Offline** happens at low resolution against proxies. Editor cuts against ProRes Proxy timeline in Avid, Premiere, or Resolve.
- **Online** happens at full resolution against camera originals. Assistant editor exports EDL/AAF/XML from the offline; online colorist relinks to camera originals using reel names + timecode.
- **Conform verification** — every cut must resolve to the correct camera clip and in-out point. Missing frames or wrong takes surface here; fix in offline before proceeding.

## ACES vs Rec.709 decision

| Choose ACES when… | Choose Rec.709 when… |
|---|---|
| Delivering theatrical DCP | Streamer-only delivery |
| Grading HDR (Dolby Vision, HDR10, HDR10+) | SDR-only delivery |
| Multiple deliverables (theatrical + streamer + festival + broadcast) | Single deliverable |
| Mixed camera negatives (Alexa + RED + BMD) | Single camera format |
| Prestige finish or awards-track | Indie / low-budget / one-buyer |

ACES adds workflow overhead but pays off when multiple deliverables need consistent color. Rec.709 is simpler and sufficient for streamer-first indies.

## DCP prep

DCPs are the theatrical deliverable. Format:

- **Container:** IMF / DCP package
- **Video:** JPEG 2000 (J2K) sequence in MXF wrapper
- **Audio:** 24-bit PCM, 48 or 96 kHz, 5.1 or 7.1 discrete channels
- **Color:** XYZ color space, gamma 2.6, DCI-P3 gamut
- **Frame rate:** 24 fps (23.976 not supported by DCP — must conform to 24)

Tools:
- [DCP-o-matic](https://dcpomatic.com) — free, cross-platform, works for most festival DCPs
- easyDCP — commercial, used by professional post houses
- Colorfront Transkoder — professional-grade

Test the DCP on a real projector before shipping. Ingest it into a Dolby CP750 or Doremi server via a lab or a friendly local theater.

## Deliverables matrix (per buyer)

Buyer specs change frequently. Always verify at delivery time. General shape:

| Buyer | Container | Video | Audio | Color | Special |
|---|---|---|---|---|---|
| Netflix | IMF or ProRes 4444 XQ | 4K UHD, HDR10 or Dolby Vision | Discrete 5.1 + stereo M&E | Rec.2020/PQ | Full IMF deliverable + textless + captions |
| Amazon Prime Video | ProRes 422 HQ | 4K SDR or HDR10 | 5.1 + stereo | Rec.709 or Rec.2020 | Broadcast wrap available |
| Apple TV+ | IMF | 4K UHD, Dolby Vision preferred | Dolby Atmos preferred | Rec.2020/PQ | Very strict spec — Apple lab pass required |
| A24 / prestige indie | ProRes 4444 or IMF | 4K DCI, Dolby Vision + DCP | 5.1 + stereo | Rec.2020/PQ + DCI-P3 | Theatrical + streamer bundle |
| Sundance / SXSW | DCP + ProRes 422 HQ backup | 2K or 4K DCP + Rec.709 backup | 5.1 discrete + stereo M&E | DCI-P3 + Rec.709 | Screening room test required |
| TIFF / Cannes | DCP | 4K DCP | Discrete 5.1 or 7.1 | DCI-P3 | Native language + English subs |
| Broadcast (linear TV) | XDCAM or IMX | HD 1080i, SDR only | Discrete 5.1 + stereo | Rec.709 | Closed captions + descriptive audio |
| Filmhub / aggregators | MP4 | 4K H.264 High, SDR | AAC stereo 320 kbps | Rec.709 | See `maximus-filmhub-delivery` |

## What this skill does not do

- Does not perform the edit, color grade, sound mix, or VFX work.
- Does not manage editorial or post-house scheduling.
- Does not process camera-original media through a DIT station.
- Does not run a DCP mastering job (though it plans the pipeline).
- Does not provide legal/QC advice on captions, subtitles, or M&E deliverables.

## Quality checkpoint

- [ ] Offline resolution + codec + LUT decided before principal photography starts.
- [ ] Color pipeline (ACES vs Rec.709) decided at prep.
- [ ] Round-trip format (EDL / AAF / XML / FCPXML) chosen and consistent across bays.
- [ ] Dailies turnaround plan documented and tested with a test-roll before day 1.
- [ ] Deliverables matrix generated per confirmed distribution deal.
- [ ] DCP tested on real projector before festival ship (if theatrical).
- [ ] Every deliverable has a spec verified against buyer's current documentation.
