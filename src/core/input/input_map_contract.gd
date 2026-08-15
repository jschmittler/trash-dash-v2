class_name InputMapContract
extends RefCounted

const ORDERED_ACTIONS: Array[StringName] = [
	&"move_left",
	&"move_right",
	&"jump",
	&"dash",
	&"action",
	&"pause",
]

const REQUIRED_ACTIONS: Dictionary = {
	&"move_left": [KEY_A, KEY_LEFT],
	&"move_right": [KEY_D, KEY_RIGHT],
	&"jump": [KEY_SPACE],
	&"dash": [KEY_SHIFT],
	&"action": [KEY_E],
	&"pause": [KEY_ESCAPE],
}


static func validate_current() -> PackedStringArray:
	var actual: Dictionary = {}
	for action: StringName in ORDERED_ACTIONS:
		if not InputMap.has_action(action):
			continue
		actual[action] = InputMap.action_get_events(action)
	return validate_actions(actual)


static func validate_actions(actual: Dictionary) -> PackedStringArray:
	var messages := PackedStringArray()
	for action: StringName in ORDERED_ACTIONS:
		if not actual.has(action):
			messages.append("missing input action: %s" % action)
			continue
		if not _events_match_exactly(actual[action], REQUIRED_ACTIONS[action]):
			messages.append("input defaults mismatch: %s" % action)
	return messages


static func _events_match_exactly(actual_events: Variant, required_keys: Array) -> bool:
	if not actual_events is Array or actual_events.size() != required_keys.size():
		return false
	for event_index: int in required_keys.size():
		var event: Variant = actual_events[event_index]
		if not event is InputEventKey:
			return false
		if not _key_event_matches(event as InputEventKey, required_keys[event_index]):
			return false
	return true


static func _key_event_matches(event: InputEventKey, required_key: Key) -> bool:
	return (
		event.physical_keycode == required_key
		and event.keycode == KEY_NONE
		and event.key_label == KEY_NONE
		and event.unicode == 0
		and event.location == KeyLocation.KEY_LOCATION_UNSPECIFIED
		and not event.alt_pressed
		and not event.shift_pressed
		and not event.ctrl_pressed
		and not event.meta_pressed
		and not event.command_or_control_autoremap
		and not event.pressed
		and not event.echo
		and event.device == -1
		and event.window_id == 0
		and not event.resource_local_to_scene
		and event.resource_name.is_empty()
		and event.get_script() == null
	)
