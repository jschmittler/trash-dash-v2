# Level 3 Plate Prompt Record

All plates used the user-approved shared rules: 1320×540 design target, polished late-16-bit side-on pixel art, rainy nighttime, nearest-neighbor/hard pixels, 120 px quiet edges, clear x≈346 gameplay corridor, exclusive plane ownership, no text/logos/UI/characters/gameplay objects/platforms/hazards, and independent generation rather than separating a flattened image.

## Far

- `restaurant-alley`: opaque storm clouds and anonymous low/mid-rise city massing only.
- `rainy-downtown-avenue`: opaque denser tall anonymous high-rise skyline only.
- `rooftop-run`: opaque elevated skyline, storm clouds, and exactly one moon; no water tower.
- `subway-maintenance-tunnels`: opaque flat distant tiled vault and exactly two tunnel mouths; no route geometry.
- `construction-site-finale`: opaque skyline, storm clouds, and exactly one research tower; no moon or construction geometry.

## Middle

- `restaurant-alley`: separated brick facades, one wall-flush fire escape, kitchen window, fixed utilities.
- `rainy-downtown-avenue`: separated facade fragments, red/blue awnings, two unmarked cars, one interrupted wall-flush scaffold.
- `rooftop-run`: one isolated water tower, antenna/dish unit, individual planters, one clothesline; no roof slabs.
- `subway-maintenance-tunnels`: exactly one stationary train and separated rear infrastructure.
- `construction-site-finale`: exactly two cranes, separated vertical cores, one suspended bundle.

## Close

- `restaurant-alley`: narrow edge walls/pipes and upper cables.
- `rainy-downtown-avenue`: narrow awning/wall edge fragments and upper cables.
- `rooftop-run`: upper wires, tiny extreme-edge vertical fragments and weeds; no parapets.
- `subway-maintenance-tunnels`: narrow edge columns and upper cable loops.
- `construction-site-finale`: sparse mesh/rebar/cable edge fragments.

Middle/close source prompt requirement: perfectly flat uniform `#FF00FF`, no magenta in retained artwork, hard isolated objects, no shadows or gradients on the key. Final intended alpha: background 0, retained pixels 255 only.
