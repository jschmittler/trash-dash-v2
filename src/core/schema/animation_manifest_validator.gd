class_name AnimationManifestValidator
extends RefCounted

const AnimationManifestType := preload("res://src/core/schema/animation_manifest.gd")


static func validate(manifest: AnimationManifestType) -> PackedStringArray:
	var errors := PackedStringArray()
	if manifest.schema_version != AnimationManifestType.CURRENT_SCHEMA_VERSION:
		(
			errors
			. append(
				(
					"animation manifest %s has schema version %d, expected %d"
					% [
						manifest.family_id,
						manifest.schema_version,
						AnimationManifestType.CURRENT_SCHEMA_VERSION,
					]
				)
			)
		)
	if String(manifest.family_id).is_empty():
		errors.append("animation manifest is missing a family id")
	if manifest.state_names.is_empty():
		errors.append("animation manifest %s declares no states" % manifest.family_id)
	else:
		var seen: Dictionary = {}
		for state_name: StringName in manifest.state_names:
			if String(state_name).is_empty():
				errors.append("animation manifest %s has an empty state name" % manifest.family_id)
			elif seen.has(state_name):
				errors.append(
					(
						"animation manifest %s duplicates state name: %s"
						% [manifest.family_id, state_name]
					)
				)
			seen[state_name] = true
	if manifest.runtime_scale.x <= 0.0 or manifest.runtime_scale.y <= 0.0:
		errors.append(
			(
				"animation manifest %s must have a positive runtime scale, got %s"
				% [manifest.family_id, manifest.runtime_scale]
			)
		)
	elif not is_equal_approx(manifest.runtime_scale.x, manifest.runtime_scale.y):
		errors.append(
			(
				"animation manifest %s runtime scale must be uniform, got %s"
				% [manifest.family_id, manifest.runtime_scale]
			)
		)
	return errors
