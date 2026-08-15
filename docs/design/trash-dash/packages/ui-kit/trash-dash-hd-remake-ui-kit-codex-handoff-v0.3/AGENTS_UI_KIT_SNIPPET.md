## Trash Dash UI Kit Source of Truth

Before modifying menu, HUD, notification, alert, pause, results, reward, or Character Select code or art, read the canonical UI Kit at:

```text
docs/design/trash-dash/ui-kit/
```

Required authority order:

1. written contracts, tokens, and approval rules
2. overall concept board
3. matching phase concept board
4. matching phase source sheet
5. implementation judgment that preserves the contract

Rules:

- The visual language is Reclaimed Playground.
- Source sheets are extraction sources, not ready runtime atlases.
- Preserve source sheets unchanged and extract into staging first.
- Never stretch or squash raster UI art.
- Use 9-slice or layered construction for scalable panels.
- Keep dynamic text and values separate from decorative art.
- Preserve Trashy and Jimothy proportions and full silhouettes.
- Use the motion-token system and reduced-motion behavior.
- Do not introduce alternate source-sheet logos, characters, or off-style UI.
- Validate all UI changes in live gameplay.
