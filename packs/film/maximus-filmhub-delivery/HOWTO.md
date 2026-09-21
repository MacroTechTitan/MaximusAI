# maximus-filmhub-delivery — recipes

## Recipe 1: Diagnose a rejected delivery

Aggregator returned an error, filmmaker doesn't know which stream is the problem.

```bash
ffprobe -v error -show_streams -show_format INPUT.mp4 > probe.txt
cat probe.txt | grep -E "codec_name|codec_type|width|height|r_frame_rate|sample_rate|bit_rate|channels"
```

Read against the current aggregator spec. Categorize failure as codec, container/extra-stream, bitrate, or audio. Choose the corresponding recipe below.

## Recipe 2: Strip an embedded thumbnail (most common Filmora rejection)

`ffprobe` shows three streams; the third is `mjpeg (attached pic)`.

```bash
ffmpeg -i INPUT.mp4 -map 0:v:0 -map 0:a:0 -c copy INPUT_CLEAN.mp4
ffprobe -v error -show_streams INPUT_CLEAN.mp4 | grep -c "codec_type=video"
# expect: 1
```

If the count is still 2, check that `-map 0:v:0` selected the movie stream and not the thumbnail. In rare cases the thumbnail is stream `0:0` — in that case use `-map 0:v:1`.

## Recipe 3: Fix audio without touching video

Video is compliant, audio is 44.1 kHz or below 320 kbps.

```bash
ffmpeg -i INPUT.mp4 -map 0:v:0 -map 0:a:0 \
  -c:v copy -c:a aac -ar 48000 -b:a 320k \
  INPUT_DELIVERY.mp4
```

Video is copied — no quality loss on picture. Only audio is re-encoded.

## Recipe 4: Full re-encode (last resort)

Video codec is wrong (e.g., HEVC when H.264 is required) and the NLE can't re-export.

```bash
ffmpeg -i INPUT.mp4 -map 0:v:0 -map 0:a:0 \
  -c:v libx264 -profile:v high -pix_fmt yuv420p \
  -b:v 70M -maxrate 80M -bufsize 140M -r 24 \
  -c:a aac -ar 48000 -b:a 320k \
  INPUT_REENCODE.mp4
```

This is a generational quality loss. Prefer re-exporting from the NLE with correct settings whenever possible. Use this recipe only when the NLE is unavailable or refuses to produce the required spec.

## Recipe 5: Release checkpoint

Before upload, run:

```bash
ffprobe -v error -show_streams -show_format INPUT_DELIVERY.mp4
```

Verify against the 13-point checklist in `SKILL.md` → Release checkpoint. If any item fails, do not upload.

## Recipe 6: Compliance flag for securities-industry filmmakers

If the filmmaker is FINRA-registered (Series 7, 63, 65, 66, 82, etc.) and the film's subject involves brokers, investments, or on-screen investment discussion, prompt the filmmaker to:

1. Route the film to their supervisor and CCO before public release.
2. Discuss OBA disclosure under FINRA Rule 3270.
3. Discuss whether the film is a "communication with the public" under FINRA Rule 2210 requiring principal pre-approval.

Do not attempt to advise on the compliance analysis directly. The skill's job is to raise the flag, not to answer the question.
