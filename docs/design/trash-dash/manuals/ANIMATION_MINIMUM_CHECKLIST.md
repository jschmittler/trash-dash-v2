# Animation Minimum Production Checklist

**Status:** Approved design reference  
**Approved:** 2026-08-18

## Purpose

This is the minimum animation inventory for a production-ready Trash Dash
character. It is an audit baseline, not permission to give every character the
same moves. Only implement a conditional state when the approved character
design and gameplay behavior support it.

This checklist supplements the runtime requirements in
[`docs/architecture/ANIMATION_CONTRACT.md`](../../../architecture/ANIMATION_CONTRACT.md).
Character, enemy, and boss canon remains authoritative over this shared list.

## Shared production rules

- Preserve the approved character design, silhouette, proportions, facing,
  scale, and stable anchor/pivot in every state.
- Every attack has a readable **telegraph -> active -> recovery** sequence.
  Damage colliders may be active only during its declared active frames.
- Each one-shot has an intentional end pose and transition. Do not borrow an
  unrelated frame as a missing state.
- Test every state at source resolution and gameplay scale. There must be no
  clipping, baseline drift, scale pop, stale facing, neighboring-frame bleed,
  or detached effect.
- State-specific collision, hurtbox, weak-point, and effect-envelope changes
  must be declared explicitly in the animation manifest.

## Required state inventory

| State | Hero | Enemy | Boss | Requirement |
|---|:---:|:---:|:---:|---|
| Idle / ready loop | Required | Required | Required | The neutral active gameplay pose. |
| Movement loop | Required | Required | Required | Use the supported locomotion: walk, run, hover, crawl, roll, etc. |
| Spawn / enter | — | Required | Required | Communicates arrival or activation. |
| Alert / engage / telegraph | — | Required | Required | Clearly warns of an imminent attack or behavior change. |
| Primary attack | Required | Required | Required | The character's core offensive action. |
| Attack recovery | Required | Required | Required | Returns from the attack and establishes a readable response window. |
| Hit / hurt reaction | Required | Required | Required | A distinct response to taking damage. |
| Defeat | Required | Required | Required | Unmistakably communicates encounter loss without unapproved redesign or damage. |
| Exit / despawn | — | Conditional | Required | Required when the character deliberately leaves or deactivates. |
| Jump start | Required | Conditional | Conditional | Include only for an approved jump action. |
| Airborne rise / fall | Required | Conditional | Conditional | Include only for an approved airborne state. |
| Landing | Required | Conditional | Conditional | Include when airborne motion ends on a surface. |
| Stop / skid | Required | Conditional | Conditional | Include when momentum or stopping is mechanically meaningful. |
| Crouch / low profile | Conditional | Conditional | Conditional | Include only when gameplay uses a lowered profile. |
| Stunned / incapacitated | Conditional | Conditional | Required | Required for bosses; other roles include it when gameplay exposes a vulnerability state. |
| Victory / celebration | Required | — | — | The hero's post-encounter success state. |
| Phase change / transformation | — | Conditional | Conditional | Required when a discrete behavior or form change occurs. |
| Retreat | — | Conditional | Required | A boss retreat is distinct from defeat and must leave it visibly able to return. |

## Role gates

### Heroes

Heroes ship with all required hero states above. Conditional mobility states
become required only when the player can invoke them. Their animation set must
also support regular and powered forms without changing frame scale or anchor
rules within a form.

### Enemies

Enemies ship with the required enemy states above and only the conditional
states their canon supports. Their entry, telegraph, attack, recovery, hit,
and defeat states must communicate their intended player decision at gameplay
scale.

### Bosses

Bosses ship with all required boss states above. In addition, each boss must
have **emerge**, **retreat**, and **defeat** sequences as defined by the
canonical boss animation contract. Multi-phase bosses require a phase-change
sequence for every discrete phase transition.

## Completion gate

A character does not pass animation production until every applicable row is
represented in its animation manifest, reachable in runtime, and visually
verified in gameplay. A missing conditional state is acceptable only when its
supporting behavior is absent from that character's approved canon.
