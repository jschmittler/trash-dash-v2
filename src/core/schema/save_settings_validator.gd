class_name SaveSettingsValidator
extends RefCounted

const SaveSettingsType := preload("res://src/core/schema/save_settings.gd")
const InputMapContractType := preload("res://src/core/input/input_map_contract.gd")


static func validate(settings: SaveSettingsType) -> PackedStringArray:
	var errors := PackedStringArray()
	if settings.schema_version != SaveSettingsType.CURRENT_SCHEMA_VERSION:
		errors.append(
			(
				"save settings has schema version %d, expected %d"
				% [settings.schema_version, SaveSettingsType.CURRENT_SCHEMA_VERSION]
			)
		)
	errors.append_array(_validate_volume("master", settings.master_volume))
	errors.append_array(_validate_volume("music", settings.music_volume))
	errors.append_array(_validate_volume("sfx", settings.sfx_volume))
	errors.append_array(_validate_key_bindings(settings.key_bindings))
	return errors


static func _validate_volume(label: String, volume: float) -> PackedStringArray:
	var errors := PackedStringArray()
	if volume < 0.0 or volume > 1.0:
		errors.append(
			"save settings %s volume must be between 0.0 and 1.0, got %s" % [label, volume]
		)
	return errors


static func _validate_key_bindings(bindings: Dictionary) -> PackedStringArray:
	var errors := PackedStringArray()
	var used_keys: Dictionary = {}
	for action: StringName in InputMapContractType.ORDERED_ACTIONS:
		if not bindings.has(action):
			errors.append("save settings is missing key binding for action: %s" % action)
			continue
		var keys: Variant = bindings[action]
		if not keys is Array or (keys as Array).is_empty():
			errors.append("save settings has an empty key binding for action: %s" % action)
			continue
		for key: Variant in keys:
			if not key is int:
				errors.append("save settings has a non-key binding for action: %s" % action)
				continue
			for other_action: StringName in InputMapContractType.ORDERED_ACTIONS:
				if other_action == action:
					continue
				var other_keys: Variant = bindings.get(other_action, [])
				if other_keys is Array and (other_keys as Array).has(key):
					errors.append(
						(
							"save settings key binding conflict: %s and %s both use key %s"
							% [action, other_action, key]
						)
					)
			if used_keys.has(key):
				errors.append("save settings duplicates key %s within action %s" % [key, action])
			used_keys[key] = action
	for action: StringName in bindings.keys():
		if not InputMapContractType.ORDERED_ACTIONS.has(action):
			errors.append("save settings has an unknown action: %s" % action)
	return errors
