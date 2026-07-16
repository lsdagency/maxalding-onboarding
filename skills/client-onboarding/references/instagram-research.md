# Instagram Research (Stage 1, compulsory)

The client's Instagram account is a required onboarding input, exactly like the Brand Campaign Document. The account shows how the client actually speaks, moves and films, which no questionnaire captures. Every onboarding scans it before anything is written, so hooks, scripts and copy sound like the client and the scripts are filmable in the spaces the client really trains in.

## Required input

The user must supply the client's Instagram handle or profile URL at the hard input gate. If it is missing, stop and ask for it alongside the brand documents. The only waiver is the user explicitly stating the client has no Instagram account; note the waiver in the Onboarding memory and flag that voice and visual-style findings will be thinner.

## Tooling

All tools run from the plugin repo's venv (`.venv/bin`), with transcription via `mlx_whisper`:

- `.venv/bin/yt-dlp`: metadata, captions and video download for individual post and reel URLs. Works anonymously on single-post URLs. It does NOT support profile pages (`/username/reels/`), so recent posts are collected with the browser first.
- `.venv/bin/ffmpeg` / `ffprobe`: frame extraction and audio checks (installed via the `static-ffmpeg` pip package, symlinked into `.venv/bin`).
- `mlx_whisper --model mlx-community/whisper-small-mlx`: transcription. Use the small model; the base model can return an empty file on music-heavy audio without saying why.

If the venv is missing the tools, install them: `.venv/bin/pip install yt-dlp static-ffmpeg`, then fetch and symlink the ffmpeg binaries. Never log into Instagram, never ask for or use credentials or browser cookies. If anonymous access is blocked or the account is private, stop the scan, tell the user what was blocked, and ask them to send the videos directly.

## Procedure

1. Collect the recent posts. Open the profile's `/reels/` page in the browser and read the grid. Note pinned posts separately; "most recent" means most recently published, not pinned-first. Collect the URLs of the five most recent videos, plus any posts the user has nominated (for example as existing-post ads).
2. Pull metadata and captions. For each URL run `yt-dlp --skip-download --dump-json <url>`. Record the caption in full, the uploader's real name, upload date, duration, and like and comment counts. Captions are first-party voice evidence: harvest recurring words, phrases, themes and CTA habits.
3. Download the five most recent videos into the client research folder: `workspace/clients/[Client]/research/instagram/`. Research is client-wide reference, so it lives at the client root, never inside a campaign subfolder. Pass `--ffmpeg-location .venv/bin` so formats merge cleanly.
4. Transcribe every video with `mlx_whisper`. A transcript that comes back empty or as just "Music" means a music-only reel; that is a finding, not a failure. Record it as text-overlay-led rather than spoken.
5. Read the visual style. Extract two or three frames per video with ffmpeg and view them. Note the setting (studio, home, outdoors), lighting, who appears, equipment visible, on-screen text styling, editing pace, and whether the client talks to camera or lets overlays carry the message.
6. Synthesise. Write a short research summary into `workspace/clients/[Client]/research/instagram/` covering: how the client actually speaks (spoken and caption voice, recurring phrases), what they film and where, the balance of talking-head versus b-roll-with-overlay, posting themes, and anything that contradicts the onboarding documents (surface contradictions at the Stage 2 gate).

## Feeding the results forward

- Brand memory: real voice patterns, recurring phrases, natural content formats, visual grammar. The "words to use" list should prefer words the client demonstrably uses.
- Scripts and hooks: video hooks must sound like this person speaking, and scripts must be filmable in the environments seen in the reels. If the client never talks to camera, flag that before scripting a talking-head concept.
- Creative Plan: existing-post ads nominated by the user get their captions and transcripts pulled in this step so the plan can reference them accurately.
