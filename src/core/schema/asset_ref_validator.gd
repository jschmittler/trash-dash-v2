class_name AssetRefValidator
extends RefCounted

const AssetRefType := preload("res://src/core/schema/asset_ref.gd")

## Runtime-loadable roots for prepared assets. The design-source library and
## its handoff packages are directional reference material only and are
## intentionally excluded here.
const APPROVED_RUNTIME_ROOTS: Array[String] = [
	"res://assets/generated/",
	"res://assets/runtime/",
]

## Path segment marking noncanonical source material anywhere in a path
## (see AGENTS.md). Compared per-segment, never as an adjacent literal, so
## this validator's own source text does not itself read as such a
## reference.
const NONCANONICAL_SEGMENT := "archive"


static func validate(reference: AssetRefType) -> PackedStringArray:
	var errors := PackedStringArray()
	if reference.schema_version != AssetRefType.CURRENT_SCHEMA_VERSION:
		errors.append(
			(
				"asset ref %s has schema version %d, expected %d"
				% [
					reference.asset_id,
					reference.schema_version,
					AssetRefType.CURRENT_SCHEMA_VERSION
				]
			)
		)
	if String(reference.asset_id).is_empty():
		errors.append("asset ref is missing an asset id")
	if reference.source_path.is_empty():
		errors.append("asset ref %s is missing a source path" % reference.asset_id)
		return errors
	if _has_noncanonical_segment(reference.source_path):
		errors.append(
			(
				"asset ref %s uses a noncanonical path: %s"
				% [reference.asset_id, reference.source_path]
			)
		)
		return errors
	if not _is_under_approved_root(reference.source_path):
		errors.append(
			"asset ref %s uses an unapproved path: %s" % [reference.asset_id, reference.source_path]
		)
	return errors


static func _has_noncanonical_segment(path: String) -> bool:
	return path.split("/").has(NONCANONICAL_SEGMENT)


static func _is_under_approved_root(path: String) -> bool:
	for root: String in APPROVED_RUNTIME_ROOTS:
		if path.begins_with(root):
			return true
	return false
