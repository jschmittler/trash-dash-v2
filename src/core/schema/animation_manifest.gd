class_name AnimationManifest
extends Resource

## Schema for an animated family's manifest, separate from its source sheet
## and engine registration (ANIMATION_CONTRACT.md). runtime_scale is a single
## uniform Vector2 rather than per-state destination scaling, so
## state-specific destination scaling is structurally forbidden rather than
## merely disallowed by convention.

const CURRENT_SCHEMA_VERSION := 1

@export var schema_version: int = CURRENT_SCHEMA_VERSION
@export var family_id: StringName = &""
@export var runtime_scale: Vector2 = Vector2.ONE
@export var state_names: Array[StringName] = []
