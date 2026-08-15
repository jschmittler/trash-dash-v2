class_name SaveSettings
extends Resource

## Schema for persisted player settings: audio volumes, the reduced-motion
## preference (required by the UI kit contract), and remapped key bindings
## (InputRemapService.bindings() shape). Persistence itself is deferred to
## Task 5; this schema only defines the versioned data shape and its
## validator.

const CURRENT_SCHEMA_VERSION := 1

@export var schema_version: int = CURRENT_SCHEMA_VERSION
@export var master_volume: float = 1.0
@export var music_volume: float = 1.0
@export var sfx_volume: float = 1.0
@export var reduced_motion: bool = false
@export var key_bindings: Dictionary = {}
