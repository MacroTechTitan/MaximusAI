# maximus-filmhub-delivery

Prepare, validate, and troubleshoot feature-film delivery masters for Filmhub and other film aggregators.

## What it's for

- Diagnosing why an aggregator rejected a delivery (Multiple Video Streams, wrong audio format, wrong bitrate).
- Cleaning an NLE export that has an embedded thumbnail or extra chapter track.
- Correcting audio format without touching the video (48 kHz AAC 320 kbps).
- Running a release-checkpoint verification before upload.
- Flagging WSP/OBA compliance questions for securities-industry filmmakers.

## What it's not for

- Color grading, sound mixing, editing, or any creative alteration.
- Generating a DCP for theatrical release (see `maximus-post-pipeline`).
- Uploading to any aggregator on the filmmaker's behalf.
- Legal, tax, or securities-compliance advice.

## Assumed tooling

- `ffprobe` and `ffmpeg` in `$PATH` (macOS: `brew install ffmpeg`, Debian/Ubuntu: `apt install ffmpeg`, Windows: [ffmpeg.org builds](https://ffmpeg.org/download.html))
- Read/write access to the NLE export directory
- Sufficient free disk space for a copy of the master

## What ships with this skill

- `SKILL.md` — operating rules, remux commands, release checkpoint
- `README.md` — this file
- `HOWTO.md` — recipes for the five most common delivery-prep scenarios
- `examples/attached-thumbnail-cleanup.md` — worked example of the most common Filmora rejection

## Where the boundary sits

This skill assumes the film itself is finished. It is a delivery-prep skill, not a post-production skill. If the underlying picture or sound needs work, that's `maximus-post-pipeline`.

If the aggregator rejects a delivery for a reason not covered here, verify current aggregator documentation before re-encoding. Aggregator specs change.
