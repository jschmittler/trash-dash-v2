class_name AssetRef
extends Resource

## Schema for a reference from runtime/content data to an approved,
## already-prepared asset. Source sheets and design-source-library paths are
## reference-only (AGENTS.md, APPROVED_ASSET_POLICY.md); only prepared
## assets under an approved runtime root may be referenced here.

const CURRENT_SCHEMA_VERSION := 1

@export var schema_version: int = CURRENT_SCHEMA_VERSION
@export var asset_id: StringName = &""
@export var source_path: String = ""
