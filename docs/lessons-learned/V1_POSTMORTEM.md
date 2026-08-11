# Trash Dash V1 postmortem

V1 proved the core side-scrolling concept and produced useful behavioral contracts, but implementation and asset concerns accumulated inside a large custom runtime. V2 keeps the evidence and lessons while rebuilding the production system cleanly.

## Non-negotiable lessons

1. **Source sheets are not runtime atlases.** Presentation sheets can contain labels, guides, backgrounds, inconsistent gutters, and poses that do not map cleanly to runtime states. Extract and validate derived atlases deterministically.
2. **Preserve sprite aspect ratios.** One uniform scale derives both runtime dimensions. Never force independent width and height to make art fit a gameplay box.
3. **Use independent collision geometry.** Collision, hurtboxes, attacks, weak points, supports, and effect origins are gameplay data, not transparent sprite bounds.
4. **Platforms must be grounded or visibly supported.** A valid collision rectangle does not excuse a floating or physically impossible silhouette.
5. **Props may not float or intersect platform silhouettes.** Resolve every prop to a named support or attachment and validate its complete visible/motion footprint.
6. **Enemies need section-specific placement and density rules.** Global spawn tables flatten teaching, pacing, recovery, bypass, and environmental identity.
7. **Bosses belong only in boss arenas.** Arenas require a quiet runway, controlled camera lifecycle, open lanes, no ordinary population, and defeat-gated release.
8. **Static fixtures do not replace uninterrupted gameplay validation.** Fixtures help isolate states, but acceptance requires normal input and traversal through surrounding content.
9. **Every required animation state must be present and verified.** Runtime registration, reachability, transition timing, facing, active frames, and completion behavior all require evidence.
10. **Visual audits must use real gameplay at target resolutions.** Source inspection, contact sheets, unit tests, and screenshots from artificial routes are supporting evidence only.

## Architectural causes

- Gameplay, input, camera, audio ownership, loading, simulation, and rendering converged in one very large React component.
- Declarative contracts emerged later, so some runtime behavior remained coupled to implementation-specific dimensions and branches.
- Source, generated, contact-sheet, and runtime asset roles were not consistently separated by directory and promotion policy.
- Multiple hosting/build paths increased configuration surface.
- Strong visual tests existed, but some source-text and fixture assertions could pass without proving uninterrupted player-controlled behavior.

## V2 response

V2 begins with explicit engine, rendering, level, animation, encounter, and visual-audit contracts; immutable approved design references; separate generated/runtime outputs; deterministic validation tools; and a mandatory release gate. No V1 gameplay code, runtime atlas, spawn table, or level module is approved for direct reuse.
