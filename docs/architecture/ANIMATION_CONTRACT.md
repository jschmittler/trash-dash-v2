# Animation contract

Every animated family owns a manifest separate from its source sheet and engine registration. The manifest defines: approved source reference; derived atlas path; cell or explicit source rectangles; state names; ordered frames; FPS/duration; loop or one-shot behavior; transition/interrupt rules; event frames; canonical facing; uniform runtime scale; visible bounds; stable anchor/pivot; ground or hover point; attachment sockets; collision/hurt/attack/weak-point geometry; and full motion/effect envelope.

Source sheets are not runtime atlases. Extraction must exclude labels, backgrounds, gutters, guides, and presentation material. Every used gameplay state needs intentional art and must be registered, reachable, and runtime-verified. Missing states may not silently borrow unrelated frames.

Within one gameplay form, state-specific destination scaling is forbidden. Collision geometry remains independent of transparent padding and may change only through explicit gameplay state data. One-shots clamp on their final frame and reset their local timer on transition. Required transitions must show no jitter, clipping, baseline drift, size pop, detached effect, stale facing, or neighboring-cell bleed.
