---
name: maximus-filmhub-delivery
description: "Prepare, validate, and troubleshoot feature-film delivery masters for Filmhub and other aggregators (Amazon Prime Direct, Apple, Vimeo OTT). FFprobe-first stream diagnosis, remux-don't-re-encode discipline, attached-thumbnail cleanup, audio-format correction to 48 kHz AAC 320 kbps. Use when preparing a feature for distribution upload, an aggregator rejected a delivery, an NLE exported unwanted extra streams (thumbnails, chapters, multi-track video), a securities-industry filmmaker needs a WSP/OBA compliance flag, or the user says 'filmhub delivery', 'aggregator upload', 'ffprobe stream check', 'remux the film', 'multiple video streams error', 'delivery master', 'film distribution encode'. Do not re-encode a locked master to fix a container problem. Do not assume any spec without verifying current docs. Delivery-prep only — not a color, sound, or edit skill."
license: MIT
metadata:
  pack: film
  authored_by: Macro Tech Titan
---

# maximus-filmhub-delivery

Prepare, validate, and troubleshoot feature-film delivery masters. Minimize unnecessary re-renders and preserve picture and sound quality.

## Core operating rules

1. **Diagnose before re-exporting.** Run `ffprobe` on the file the NLE produced before deciding what needs to change. Most delivery rejections are container or extra-stream problems, not the actual film.
2. **Enumerate every stream.** `ffprobe -v error -show_streams -show_format input.mp4`. Confirm exactly how many video streams, how many audio streams, and what codec each is.
3. **Distinguish four failure classes:**
   - **Codec incompatibility** — video isn't H.264 High or audio isn't AAC LC. Requires re-encode of the affected stream.
   - **Extra-stream / container error** — attached thumbnail as second video stream (`mjpeg (attached pic)`), extra chapter track, multi-track video export. Requires remux only, no re-encode.
   - **Bitrate warning** — video below the accepted minimum. Requires re-encode of video stream at higher bitrate.
   - **Audio format issue** — sample rate not 48 kHz, bit rate below 320 kbps stereo. Requires re-encode of audio stream only, video stays copy.
4. **Remux when the film itself is fine.** If the video and primary audio streams are compliant and the only problem is an unwanted second video stream (embedded thumbnail) or extra chapter track, remux with `ffmpeg -c copy` — do not re-encode.
5. **Preserve the master.** Never overwrite the original NLE output. Create a new `_CLEAN.mp4` (or `_DELIVERY.mp4`) alongside it.
6. **Verify the cleaned file.** Re-run `ffprobe` on the output and confirm only the intended streams remain and the spec values match.
7. **Verify current aggregator requirements.** Filmhub's spec can change; check the current official Filmhub delivery documentation before assuming any value is correct. Do the same for Amazon Prime Direct, Apple, and Vimeo OTT if delivering to those.

## Proven Ghosted 4K delivery profile

A successfully accepted Filmhub 4K delivery master used the following spec. Treat as a working profile, not an immutable Filmhub specification — check current docs.

| Setting | Value |
|---|---|
| Container | MP4 |
| Video codec | H.264 High profile |
| Resolution | 3840 × 2160 |
| Frame rate | 24 fps |
| Color | SDR / Rec.709 |
| Video bitrate | ~70 Mbps |
| Audio codec | AAC LC stereo |
| Audio sample rate | 48 kHz |
| Audio bitrate | 320 kbps |
| Video streams | 1 |
| Audio streams | 1 |
| Extra streams | none |

## Wondershare Filmora export settings

For a Filmhub-oriented master from Filmora, disable:

- **Embed / Add Thumbnail** — Filmora writes this as `Video: mjpeg (attached pic)` which Filmhub reads as Multiple Video Streams and rejects.
- **Multi-track video export** — Filmhub expects one video stream.
- **Chapter export** — unless the distributor specifically requires chapters.

## Inspection reference

Healthy stream output:

```text
Stream #0:0: Video: h264 (High) ... 3840x2160, 24 fps
Stream #0:1: Audio: aac (LC) ... 48000 Hz, stereo, 320 kb/s
```

Problem (extra attached thumbnail):

```text
Stream #0:0: Video: h264 ...
Stream #0:1: Audio: aac ...
Stream #0:2: Video: mjpeg ... (attached pic)   ← reject cause
```

Problem (wrong audio sample rate):

```text
Stream #0:0: Video: h264 ...
Stream #0:1: Audio: aac ... 44100 Hz, stereo, 256 kb/s   ← below 48 kHz / 320 kbps
```

## Remux commands

**Drop unwanted extra streams (attached thumbnail, second video, chapters):**

```bash
ffmpeg -i input.mp4 -map 0:v:0 -map 0:a:0 -c copy "output_CLEAN.mp4"
```

**Video is compliant, audio needs 48 kHz AAC 320 kbps:**

```bash
ffmpeg -i input.mp4 -map 0:v:0 -map 0:a:0 -c:v copy -c:a aac -ar 48000 -b:a 320k "output_DELIVERY.mp4"
```

**Full re-encode as a last resort (only if video codec/bitrate is wrong and NLE cannot re-export):**

```bash
ffmpeg -i input.mp4 -map 0:v:0 -map 0:a:0 \
  -c:v libx264 -profile:v high -pix_fmt yuv420p -b:v 70M -maxrate 80M -bufsize 140M -r 24 \
  -c:a aac -ar 48000 -b:a 320k \
  "output_REENCODE.mp4"
```

Re-encoding a locked master is a quality loss. Prefer re-exporting from the NLE with correct settings whenever possible.

## Release checkpoint

Before uploading to any aggregator, verify:

1. **Picture lock confirmed** with all stakeholders (director, producer, editor).
2. **Runtime** matches the expected duration to the second.
3. **Aspect ratio** matches the intended presentation (2.39:1, 1.85:1, 16:9).
4. **Codec** matches the current distributor spec.
5. **Resolution** matches the current distributor spec.
6. **Frame rate** matches the shooting frame rate (usually 23.976 or 24).
7. **Stream count** is exactly the number the distributor expects (usually 1 video + 1 audio, sometimes 1 video + N audio for multi-language).
8. **Bitrate** is within the accepted range.
9. **Color space** matches (Rec.709 SDR for standard, Rec.2020/HDR for HDR deliveries).
10. **Audio format** matches (48 kHz, 320 kbps stereo minimum, or discrete 5.1 if delivering surround).
11. **Credits and disclaimers** on-screen are present and correctly attributed.
12. **Key art** is prepared separately as a still image at the aggregator's spec, not embedded in the video file.
13. **Archival master** is preserved separately from the delivery master.

## Compliance flag — securities-industry filmmakers

If the filmmaker is a registered representative of a broker-dealer or investment adviser, and the film's subject matter involves brokers, investment strategies, financial products, or an on-screen role that could be read as investment recommendation:

- **Flag a compliance / WSP check** with the filmmaker's supervisor or CCO before public release.
- The film may qualify as an Outside Business Activity (OBA) under FINRA Rule 3270 and require pre-approval and disclosure.
- The film may qualify as a communication with the public under FINRA Rule 2210 and require pre-use principal approval.
- Do **not** assume FINRA automatically requires review — the analysis is fact-specific.
- Do **not** provide legal advice. Route to compliance counsel or the CCO.

This flag is preventive, not diagnostic. It does not replace a compliance review.

## What this skill does not do

- Does not color grade, sound mix, edit, or otherwise creatively alter the film.
- Does not generate a DCP for theatrical release — see `maximus-post-pipeline` for the DCP prep step.
- Does not upload to Filmhub or any aggregator — the filmmaker performs the upload themselves.
- Does not provide legal, tax, or securities-compliance advice.

## Quality checkpoint

Before declaring a delivery master ready:

- [ ] `ffprobe` output shows exactly the streams the distributor expects, no more, no less.
- [ ] Video codec, profile, resolution, frame rate, and bitrate match spec.
- [ ] Audio codec, sample rate, bit rate, and channel count match spec.
- [ ] Original master is preserved untouched at its NLE-exported path.
- [ ] Delivery file has a distinct filename (`_CLEAN` or `_DELIVERY` suffix).
- [ ] Compliance flag has been raised if the filmmaker is in a regulated industry and the subject matter warrants it.
