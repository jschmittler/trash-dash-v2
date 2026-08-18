# Trash Dash Animation Minimum Production Checklist

**Status:** Approved design

**Approved:** 2026-08-18

## Goal

Define one compact production checklist that applies consistently across every
hero, enemy, and boss without requiring character-inappropriate actions.

## Decision

Use a role-based minimum inventory:

- a shared core for idle, movement, combat communication, damage response, and
  defeat;
- role-specific required states for entry, victory, retreat, and boss phase
  behavior; and
- conditional mobility or transformation states only where approved gameplay
  behavior supports them.

The canonical checklist lives at
[`docs/design/trash-dash/manuals/ANIMATION_MINIMUM_CHECKLIST.md`](../../design/trash-dash/manuals/ANIMATION_MINIMUM_CHECKLIST.md).
It supplements, rather than replaces, the runtime manifest and transition
requirements in `docs/architecture/ANIMATION_CONTRACT.md`.

## Acceptance criteria

1. The checklist identifies every required state separately for heroes,
   enemies, and bosses.
2. It distinguishes conditional states from required production work.
3. It requires telegraph, active, and recovery readability for attacks.
4. It preserves existing hero, enemy, and boss visual canon.
5. It requires runtime manifest coverage and gameplay-scale verification
   before an applicable animation set is considered complete.
