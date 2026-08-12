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
		var physical_keys: Array[Key] = []
		for event: InputEvent in InputMap.action_get_events(action):
			if event is InputEventKey:
				physical_keys.append((event as InputEventKey).physical_keycode)
		actual[action] = physical_keys
	return validate_actions(actual)

static func validate_actions(actual: Dictionary) -> PackedStringArray:
	var messages := PackedStringArray()
	for action: StringName in ORDERED_ACTIONS:
		if not actual.has(action):
			messages.append("missing input action: %s" % action)
			continue
		if actual[action] != REQUIRED_ACTIONS[action]:
			messages.append("input defaults mismatch: %s" % action)
	return messages
