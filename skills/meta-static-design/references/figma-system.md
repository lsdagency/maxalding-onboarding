# The Maxalding Figma Ad System

How the statics are built in Figma, and the scripts that apply the standard. Use the Figma MCP (`use_figma`, `get_screenshot`, `upload_assets`, `download_assets`).

## The file
- File key `uI5CNyMcyOjnlTeUcReswu` (https://www.figma.com/design/uI5CNyMcyOjnlTeUcReswu). It sits in the Brim Hydration team drafts because the Figma MCP is logged in there; move it to a Maxalding team when one exists.
- Pages: Maxalding Standard (the rules sheet, 29:954), Templates (one ordered column plus the overview board 29:388), then one page per client campaign (for example "1 TO 360 / Four For Three", 2:22).
- Variable collection "Brand" (VariableCollectionId:2:2): one mode per client (Maxalding 2:0, 1 TO 360 2:1). Variables: ink, paper, accent, on-accent and muted colours, font families and styles, display size and line height, font/body-size. A new client is a new mode.
- Text styles Ad/Headline, Ad/Support, Ad/CTA, all bound to the font variables.

## Templates (component sets, Size=4:5 and Size=9:16)
Location 17:185, Benefits 17:212 (Photo=Yes/No), Problem Solution 17:228, Social Proof 17:251, Audience Addresser 17:261, Ugly (Text Thread) 17:278, Price Offer 17:289, Photo Top 10:27 (Text=Top/Bottom, Show sticker), Big Type 10:40, Offer Sticker 10:2, First Session 26:46, Myth Buster 26:65 (Myth line 1, Myth line 2, drawn strike rules), Meet the Coach 27:40 (credential chips, quote, name), Carousel Card 27:66 (Cover / Step BL / Step TL / Step BR / Photo / End). Every template has Show CTA and CTA properties.

## Gotchas
- A variable-bound paint keeps a stand-in colour that some renders show. Always pass the real colour value when binding. Paint-level opacity on a bound paint is dropped, so put transparency on the layer.
- Instances can't move or resize their sublayers (relative-transform). Only fills, effects, text, visibility and properties can be overridden. A layout change belongs in the template.
- Text decoration thickness only applies to underlines. Draw strike rules instead.
- Cloning a variant into an existing set drops componentPropertyReferences, so re-link them. Clone-then-combine keeps them.
- `upload_assets` can't target instance sublayers. Upload loose, copy the imageHash onto the slot, then delete the loose node. The imageHash is the file's SHA-1, so `shasum` maps local files to hashes already in the file.
- Scripts are atomic: if one call errors, nothing in it applied. Check the state before re-running a toggle.
- `get_screenshot` can lag behind edits. Re-screenshot before judging a change.
- use_figma gotchas: the Inter style is "Semi Bold", and pages change with `await figma.setCurrentPageAsync(page)`.

## Scripts (paste into use_figma, adjust ids)

Lift a photo and fit the scrim to the text (section 4 of the standard):
```js
const H = inst.height;
function relY(n, root){ let y = 0, p = n; while (p && p !== root){ y += p.y; p = p.parent; } return y; }
for (const p of inst.findAll(n => n.name === 'Photo'))
  p.fills = p.fills.map(f => f.type !== 'IMAGE' ? f : {...JSON.parse(JSON.stringify(f)),
    filters: {...(f.filters || {}), exposure: 0.3, shadows: 0.35, highlights: -0.1, contrast: 0.05}});
const texts = inst.findAll(n => n.type === 'TEXT' && n.visible && n.name !== 'CTA');
const top = Math.min(...texts.map(t => relY(t, inst)));
const cta = inst.findOne(n => n.name === 'CTA' && n.visible);
const ctaB = relY(cta, inst) + cta.height;
const s = inst.findOne(n => n.name === 'Bottom Scrim');
const P = y => Math.min(1, Math.max(0, (y - s.y) / s.height));
const stops = H > 1500
  ? [[0,0],[P(top-300),0],[P(top-40),0.56],[P(ctaB+40),0.59],[P(ctaB+340),0.25],[1,0.25]]
  : [[0,0],[P(top-300),0],[P(top-40),0.56],[1,0.6]];
const f = JSON.parse(JSON.stringify(s.fills[0])); const c = f.gradientStops[0].color;
f.gradientStops = stops.map(([p, a]) => ({position: p, color: {r: c.r, g: c.g, b: c.b, a}}));
s.fills = [f];
```
Where a top scrim and a bottom (CTA) scrim meet, fade one to 0 across the overlap or a hard seam shows.

Text shadow on every line over a photo:
```js
for (const t of inst.findAll(x => x.type === 'TEXT' && x.visible))
  t.effects = [
    {type:'DROP_SHADOW', color:{r:0,g:0,b:0,a:0.45}, offset:{x:0,y:2}, radius:28, spread:0, visible:true, blendMode:'NORMAL'},
    {type:'DROP_SHADOW', color:{r:0,g:0,b:0,a:0.30}, offset:{x:0,y:1}, radius:6,  spread:0, visible:true, blendMode:'NORMAL'}];
```
Skip text inside the sticker and the credential chips.

Swap a photo on an instance (after a loose upload returned `hash`):
```js
p.fills = [{type:'IMAGE', scaleMode:'CROP', imageHash: hash,
  imageTransform: [[sx,0,tx],[0,sy,ty]],   // visible fraction and offset of the image; negative sx mirrors (tx is then the right edge)
  filters: {exposure:0.3, shadows:0.35, highlights:-0.1, contrast:0.05, saturation:0, temperature:0, tint:0}}];
```
For a 2:3 phone photo: 4:5 is `[[1,0,0],[0,0.835,ty]]` with ty from 0 to 0.165; 9:16 is `[[0.842,0,tx],[0,1,0]]` with tx from 0 to 0.158.

## Export
`download_assets` with `defaultFormat: "png"`, `defaultScale: 2`, one call per ad node (the URLs are short-lived, so download each batch straight away with curl). Name each PNG `<NN> <CONCEPT> <4x5|9x16>.png` or `CAROUSEL <n> <CARD>.png` in one folder, then:
```
python -m design.export_statics "<png folder>" "<campaign folder>" --client 1TO360
```
