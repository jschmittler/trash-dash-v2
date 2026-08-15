class_name InputMapAdapter
extends RefCounted


func has_action(action: StringName) -> bool:
	return InputMap.has_action(action)


func action_get_events(action: StringName) -> Array:
	return InputMap.action_get_events(action)


func action_erase_events(action: StringName) -> void:
	InputMap.action_erase_events(action)


func action_add_event(action: StringName, event: InputEvent) -> void:
	InputMap.action_add_event(action, event)
