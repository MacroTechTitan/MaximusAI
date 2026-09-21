# maximus-post-pipeline — recipes

## Recipe 1: Set the offline/online plan at prep

Decide before day 1 of principal photography:

- **Camera format:** what's the negative? (Alexa ProRes 4444 XQ / RED R3D / BMD BRAW / Sony XAVC-I)
- **Offline codec:** what does editorial cut against? (ProRes 422 Proxy or DNxHD 36 for laptop-based; ProRes 422 for workstation-based)
- **Show LUT:** the DP's viewing LUT, applied at DIT and baked into proxies
- **Reel-name convention:** every clip must have unique reel name (e.g., `A001_C001_YYMMDD_R1`)
- **Frame rate:** 23.976 or 24 (must be consistent across camera, sound, editorial)

Document and share with camera department, DIT, sound recordist, editorial, and post supervisor before day 1.

## Recipe 2: Dailies workflow

Nightly process:

```bash
# 1. Ingest with checksum
rsync -av --progress /Volumes/A001/ /Volumes/PRIMARY/A001/
rsync -av --progress /Volumes/A001/ /Volumes/BACKUP/A001/
md5deep -r /Volumes/PRIMARY/A001/ > /Volumes/PRIMARY/A001/checksums.md5

# 2. Sync sound (double-system) — done in DaVinci Resolve or ScratchLab
# 3. Apply show LUT — same tool, save the graded proxy
# 4. Transcode to proxy
ffmpeg -i "/Volumes/PRIMARY/A001/A001_C001.mov" \
       -c:v prores_ks -profile:v 0 -vendor apl0 \
       -c:a copy \
       "/Volumes/EDIT/PROXIES/A001_C001_PROXY.mov"

# 5. Upload to Frame.io for director/DP review
frameio upload --project "North of Nowhere" /Volumes/EDIT/PROXIES/A001_*
```

Deliver dailies before next-day call. Non-negotiable.

## Recipe 3: Offline → online conform via EDL

At picture lock:

1. In the NLE, ensure all cuts are on camera-original clips with matching reel names + timecode.
2. Export EDL:
   - **Avid:** File → Export → CMX 3600 EDL
   - **Premiere:** File → Export → EDL
   - **Resolve:** File → Export AAF/EDL/XML
3. Send EDL + reference QuickTime + a project-notes PDF to the online colorist.
4. Online colorist relinks EDL to camera originals, produces the conformed timeline in the color bay.
5. Verify conform: play through, watch for missing frames, wrong takes, or offset audio.

## Recipe 4: ACES vs Rec.709 decision

Simple decision tree:

```
Is theatrical DCP required?          → YES → ACES
Is HDR delivery required?            → YES → ACES
Are there multiple deliverables?     → YES → ACES
Is it single-buyer streamer-only?    → YES → Rec.709 (unless HDR required)
Is it indie/festival/single-format?  → YES → Rec.709 (unless theatrical planned)
```

Whichever you pick, use consistent LUTs from DIT → editorial → color. No half-ACES.

## Recipe 5: Prep a DCP for a festival

Using DCP-o-matic (free):

1. Install DCP-o-matic ([dcpomatic.com](https://dcpomatic.com))
2. New DCP project, name it exactly as festival requires (usually `FILM_TITLE_FTR_S_EN-XX_INT_2K_YYYYMMDD_STUDIO_IOP_OV`)
3. Add the color-graded master (ProRes 4444 XQ or DPX/EXR sequence)
4. Add the 5.1 or 7.1 audio master (24-bit 48 kHz PCM)
5. Set color space: XYZ, gamma 2.6, DCI-P3 gamut
6. Set frame rate: 24 fps (not 23.976)
7. Encode. Verify.
8. **Test on a real projector before shipping.** Local theater, rental house, or festival tech-check window.

## Recipe 6: Generate the deliverables matrix

For each confirmed distribution deal, look up the current spec and produce a per-buyer deliverable spec sheet:

```
==============================================
NORTH OF NOWHERE — Deliverables Matrix (v1.0)
==============================================

NETFLIX
  Package:      IMF
  Video:        4K UHD 3840x2160, Dolby Vision + HDR10 fallback
  Audio:        Discrete 5.1 + stereo M&E, 24-bit 48kHz
  Color:        Rec.2020 / PQ
  Extras:       Textless masters, English SDH captions, forced subs
  Deadline:     2027-01-15
  Contact:      netflix-postops@netflix.com

SUNDANCE (festival premiere)
  Package:      DCP (INTEROP)
  Video:        4K DCI, 24fps
  Audio:        5.1 discrete, 24-bit 48kHz
  Color:        XYZ / DCI-P3 gamut
  Extras:       ProRes 4444 backup, key art (posters), stills, EPK
  Deadline:     2026-12-01
  Contact:      programming@sundance.org

FILMHUB (aggregator, streamer secondary window)
  Package:      MP4 (H.264 High)
  Video:        4K UHD 3840x2160, SDR Rec.709
  Audio:        AAC LC stereo, 48kHz 320 kbps
  Color:        Rec.709
  Extras:       Key art JPG 3000x2000
  Deadline:     Post-festival window
  Contact:      via Filmhub dashboard
```

Verify every spec against buyer's current documentation before delivery day.
