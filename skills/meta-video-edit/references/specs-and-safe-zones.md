# Delivery specs and safe zones

Mirrors `editor/specs.py`. Change both together.

## Files
| Format | Size | Placement |
|---|---|---|
| 9x16 | 1080 x 1920 | Reels, Stories |
| 4x5 | 1080 x 1350 | Feed |

- H.264 High, yuv420p, CRF 18, 30 fps, AAC 192 kbps 48 kHz, faststart.
- Name: `<AD NAME> 9x16.mp4` and `<AD NAME> 4x5.mp4`, using the Creative Plan's file names (for example `INT Kevin`, `AA HOOK 1`).
- Saved to `clients/<Client>/<campaign>/edits/v<N>/` with the `.render.json` manifest beside each file.

## Safe zones (fractions of the frame)
| Format | Top | Bottom | Sides |
|---|---|---|---|
| 9x16 | 14% | 35% | 6% |
| 4x5 | 6% | 12% | 6% |

The 9x16 numbers cover the Reels and Stories interface (account bar at the top, caption, name and CTA button at the bottom, action rail on the right). Third-party guides agree on 14 / 35 / 6; Meta's own help pages say to keep the edges clear without giving numbers, so preview in Ads Manager before launch.

## Audio
- Integrated loudness -14 LUFS (plus or minus 1.5), true peak under -1 dBTP. Two-pass normalisation in the renderer.
- Music bed about -22 dB under voice, sidechain ducked.

## Timing
- First spoken word by 0.7 seconds unless the ad opens on a card.
- Silence over 0.8 seconds mid-ad is flagged.
- Length guides (warnings): interview 20 to 75 seconds (singles briefed at 30 to 45), Audience Addresser 15 to 45, Incentive 10 to 30, montage 8 to 30. A plan can set `max_seconds`.

## Text
- Minimum 54 px at 1080 wide for anything burned in.
- Captions 80 px (9x16) and 70 px (4x5). Hook titles 84 px and 76 px.
