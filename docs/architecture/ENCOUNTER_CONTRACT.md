# Encounter contract

Each encounter record defines a stable ID, owning level section, activation/release bounds, teaching role, enemy instances, named support or flight band, patrol/motion bounds, density class, bypass/recovery space, reward relationship, and deterministic reset behavior.

Placement rules:

- small enemies appear in readable groups of one to three;
- medium enemies appear alone or in pairs with limited support pressure;
- large enemies own isolated encounter space;
- no more than two ordinary groups should share a viewport and only one should demand immediate reaction;
- grounded actors remain on named supports through their full collision and artwork envelope;
- flying actors remain inside authored bands;
- enemies use section-specific placement and density, not global spawn tables;
- bosses appear only in boss arenas; ordinary population is removed or excluded on arena activation;
- encounters provide readable tells, negative space, and recovery or bypass where pressure warrants it.

Validation uses the largest visible/motion envelope, not only collision boxes. It must reject unknown supports, patrol escape, platform intersection, duplicate IDs, blocked routes, unreadable clustering, viewport over-density, arena contamination, and nondeterministic invalid fallbacks.
