# Level contract

Each level is validated data, not executable spawn code. A level record must define:

- identity: stable `id`, display name, design-source references, schema version;
- world: bounds, logical resolution policy, sections/zones, lighting and background ownership;
- supports: stable IDs, geometry, visible construction, collision behavior, and allowed attachments;
- hazards: independent geometry, telegraph, response, reset/recovery behavior;
- routes: required path, optional/bypass paths, landing targets, gates, rewards, and recovery space;
- checkpoints: activation bounds, named support, respawn transform, camera restore state;
- encounters: IDs referencing records that satisfy `ENCOUNTER_CONTRACT.md`;
- boss arena: enemy-free runway, trigger, lock bounds, player/boss bounds, named floor/supports, open lanes, defeat/release sequence;
- exit: reachability, next-level transition, carried-progress policy;
- evidence: approval sources, validation command, target-resolution runtime routes.

No level may embed render objects, engine instances, arbitrary callbacks, or unvalidated asset paths. Supports and collision are authored independently from reference art. Platforms must be visibly supported or grounded, props may not float or intersect platform silhouettes, and archive references are forbidden.

Validation must reject unknown IDs, gaps in required zone coverage, overlapping structural geometry, unsupported attachments, unreachable required routes, missing recovery space, bosses outside boss arenas, ordinary enemies inside locked boss arenas, unapproved assets, and schema-version mismatches.
