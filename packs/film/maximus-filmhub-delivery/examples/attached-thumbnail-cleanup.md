# Example: attached-thumbnail cleanup (Filmora → Filmhub)

## Situation

Filmmaker exports a 4K feature from Wondershare Filmora with "Add Thumbnail" left checked (the default). Uploads to Filmhub. Filmhub rejects with **"Multiple Video Streams Detected."**

The film itself is fine. The thumbnail is a second `mjpeg` video stream Filmora embedded as picture metadata, and Filmhub reads it as a second movie stream.

## Diagnosis

```bash
$ ffprobe -v error -show_streams -show_format Ghosted_4K_Master.mp4 | \
    grep -E "codec_name|codec_type"

codec_type=video
codec_name=h264
codec_type=audio
codec_name=aac
codec_type=video           ← the problem
codec_name=mjpeg
```

Three streams. Third is `mjpeg` — the embedded thumbnail.

## Fix

```bash
ffmpeg -i "Ghosted_4K_Master.mp4" \
       -map 0:v:0 -map 0:a:0 -c copy \
       "Ghosted_4K_Master_CLEAN.mp4"
```

- `-map 0:v:0` — take only the first video stream (the movie).
- `-map 0:a:0` — take only the first audio stream (the mix).
- `-c copy` — stream copy, no re-encode, no generational loss, no wait time.

Runtime for a ~90-minute 4K master on a 2020-era laptop: 30-90 seconds. Because there's no decode/re-encode step.

## Verification

```bash
$ ffprobe -v error -show_streams Ghosted_4K_Master_CLEAN.mp4 | \
    grep -c "codec_type=video"

1

$ ffprobe -v error -show_streams Ghosted_4K_Master_CLEAN.mp4 | \
    grep -E "codec_name|width|height|r_frame_rate|sample_rate|bit_rate"

codec_name=h264
width=3840
height=2160
r_frame_rate=24/1
codec_name=aac
sample_rate=48000
bit_rate=320000
```

One video stream, one audio stream, spec values match the Ghosted delivery profile. Ready for upload.

## What we did not do

- Did **not** re-encode the video. Would have taken hours on a 4K master and introduced generational quality loss.
- Did **not** overwrite the original. The Filmora master stays untouched at its original path for archival.
- Did **not** re-export from Filmora. Wasn't necessary — the film itself was fine.

## What the filmmaker changes for the next export

In Filmora's export dialog, uncheck **"Add thumbnail"** before rendering the next delivery master. Prevents the same rejection loop on future exports.

## Sidenote: compliance flag

This filmmaker is a Series 7-registered broker. The film is a psychological thriller with no financial subject matter. The compliance flag was raised, reviewed with the CCO, and closed as "no OBA disclosure required, no communications-review obligation" — but the flag was raised. That's the discipline. Never skip the flag because you're sure the answer is no.
