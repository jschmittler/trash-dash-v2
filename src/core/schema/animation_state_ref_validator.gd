class_name AnimationStateRefValidator
extends RefCounted

const AnimationStateRefType := preload("res://src/core/schema/animation_state_ref.gd")
const AnimationManifestType := preload("res://src/core/schema/animation_manifest.gd")


static func validate(
	ref: AnimationStateRefType, manifest: AnimationManifestType
) -> PackedStringArray:
	var errors := PackedStringArray()
	if ref.schema_version != AnimationStateRefType.CURRENT_SCHEMA_VERSION:
		(
			errors
			. append(
				(
					"animation state ref %s/%s has schema version %d, expected %d"
					% [
						ref.family_id,
						ref.state_name,
						ref.schema_version,
						AnimationStateRefType.CURRENT_SCHEMA_VERSION,
					]
				)
			)
		)
	if ref.family_id != manifest.family_id:
		errors.append(
			(
				"animation state ref family %s does not match manifest family %s"
				% [ref.family_id, manifest.family_id]
			)
		)
		return errors
	if String(ref.state_name).is_empty():
		errors.append("animation state ref for %s is missing a state name" % ref.family_id)
	elif not manifest.state_names.has(ref.state_name):
		errors.append(
			(
				"animation state ref references an unknown state: %s/%s"
				% [ref.family_id, ref.state_name]
			)
		)
	return errors
