class_name ProjectSettingsAdapter
extends RefCounted

func get_value(key: StringName) -> Variant:
	return ProjectSettings.get_setting(key)
