class_name Level
extends Resource

## Schema for a level record (LEVEL_CONTRACT.md): a stable ID, its declared
## sections/zones, the encounters that belong to it, and its optional boss
## arena membership. A level is validated data, not executable spawn code;
## the level does not embed encounter/support geometry directly but instead
## references stable IDs, validated against the actual records by
## LevelValidator.

const CURRENT_SCHEMA_VERSION := 1

@export var schema_version: int = CURRENT_SCHEMA_VERSION
@export var level_id: StringName = &""
@export var section_ids: Array[StringName] = []
@export var encounter_ids: Array[StringName] = []
@export var boss_arena_section_id: StringName = &""
@export var boss_encounter_id: StringName = &""
