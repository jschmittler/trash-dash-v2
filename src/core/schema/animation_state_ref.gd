class_name AnimationStateRef
extends Resource

## Schema for a reference to one declared state of an AnimationManifest.
## Every used gameplay state must be registered and reachable
## (ANIMATION_CONTRACT.md); this is validated against the owning manifest by
## AnimationStateRefValidator rather than against a global state enum, since
## state names are per-family.

const CURRENT_SCHEMA_VERSION := 1

@export var schema_version: int = CURRENT_SCHEMA_VERSION
@export var family_id: StringName = &""
@export var state_name: StringName = &""
