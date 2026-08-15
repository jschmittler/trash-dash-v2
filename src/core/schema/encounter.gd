class_name Encounter
extends Resource

## Schema for an encounter record (ENCOUNTER_CONTRACT.md): a stable ID,
## owning level section, enemy density class, and either a named ground
## support or a flying/authored-band placement. Boss arena membership and
## reward relationships are owned by the level record and validated there.

enum EnemySizeClass { SMALL, MEDIUM, LARGE }

const CURRENT_SCHEMA_VERSION := 1

@export var schema_version: int = CURRENT_SCHEMA_VERSION
@export var encounter_id: StringName = &""
@export var section_id: StringName = &""
@export var enemy_size_class: EnemySizeClass = EnemySizeClass.SMALL
@export var enemy_count: int = 1
@export var support_id: StringName = &""
@export var is_flying: bool = false
