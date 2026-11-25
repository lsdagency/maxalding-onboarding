# Edit plan format

One JSON file per ad, in `edit-work/plans/`. Paths are relative to the plan file. Times are seconds in the source clip.

```json
{
  "client": "1 TO 360 Strength and Fitness",
  "ad": "INT Kevin",
  "concept": "interview",
  "formats": ["9x16", "4x5"],
  "max_seconds": 45,
  "transcripts_dir": "../transcripts",
  "punch_in": 1.1,
  "brand": {
    "font": "TikTok Sans", "title_weight": 900, "caption_weight": 700,
    "caption_color": "#F7F5F1", "highlight": "#F7F5F1", "outline": "#181B1E",
    "title_color": "#181B1E", "title_box": "#F7F5F1",
    "card_bg": "#BC6F4C", "card_fg": "#F7F5F1"
  },
  "clips": [
    {"src": "/path/C4911-003.MP4", "in": 84.2, "out": 91.6, "role": "hook", "tighten": true,
     "focus": {"9x16": [0.5, 0.3], "4x5": [0.5, 0.3]}, "zoom": 1.15},
    {"card": {"duration": 3.5, "bg": "#BC6F4C",
              "lines": [{"text": "4 for 3", "size": 300, "y": 0.36},
                        {"text": "Start with four sessions for the price of three.", "size": 64, "y": 0.52, "face": "caption"},
                        {"text": "Tap below and Sergio will call you", "size": 64, "y": 0.62}],
              "audio": {"src": "/path/sergio_cta.wav", "in": 0, "out": 2.9}}, "role": "cta"}
  ],
  "broll": [{"src": "/path/C4930.MP4", "in": 12.0, "at": 6.4, "dur": 2.2, "focus": [0.5, 0.5]}],
  "titles": [{"text": "18 months with Sergio", "start": 0, "end": 3.0, "style": "hook"}],
  "captions": {"on": true, "fixes": {"free": "three"}, "keep_together": ["South Kensington"]},
  "music": {"src": "/path/track.mp3", "gain_db": -22, "duck": true}
}
```

## Fields
- `clips`: the cut in order. A clip is a span of one source file. `tighten: true` cuts the pauses and fillers inside it into jump cuts (from the word timings). `focus` is where the eyes are in the source frame, as fractions (x, y), per format or one value for both. The crop puts that point on the eye line (upper third on 9x16) at any zoom, clamped to the picture. `zoom` above 1 crops in. `mute: true` drops its audio. `cap_first: true` capitalises the first caption word when a clip starts mid-sentence.
- `punch_in`: alternate tightened pieces are cropped in by this factor to hide jump cuts (1.08 to 1.12).
- A `card` is a solid frame: one `text`, or a `lines` stack (`text`, `size`, `y` as a fraction of height, `face` title or caption, `color`). `audio` puts a voice line under it (`src`, `in`, `out`, optional `at` delay and `gain_db`).
- `broll`: overlays on the output timeline at `at` seconds for `dur`, starting `in` seconds into the source. The main audio keeps running.
- `titles`: on-screen text. `style` is `hook` (top of the safe zone, boxed), `cta` (bottom of the safe zone) or `label`. Optional `y`, `size`, `formats`.
- `captions`: `fixes` maps a misheard word to the right one, `keep_together` lists phrases never split across chunks, `max_words`, `size`, `y`.
- `music`: licensed tracks only. `gain_db` under the voice, `duck` sidechains it to the voice.

## Commands
```
python -m editor.cli timeline plan.json            # the cut as text: times, pieces, words, length
python -m editor.cli build plan.json --out edits/v1 # render both formats, QA, contact sheets
python -m editor.cli qa edits/v1                    # re-run the QA gate
```
