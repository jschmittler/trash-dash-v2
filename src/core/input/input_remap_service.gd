class_name InputRemapService
extends RefCounted

const InputMapContractType := preload("res://src/core/input/input_map_contract.gd")

var _input_map: RefCounted
var _bindings: Dictionary = {}


func _init(input_map: RefCounted) -> void:
	assert(input_map != null, "Input remap service requires an input map adapter")
	_input_map = input_map
	reset_to_defaults()


func bindings() -> Dictionary:
	return _bindings.duplicate(true)


func rebind(action: StringName, physical_keycode: Key) -> Error:
	if not InputMapContractType.ORDERED_ACTIONS.has(action):
		return ERR_DOES_NOT_EXIST
	for other_action: StringName in InputMapContractType.ORDERED_ACTIONS:
		if other_action != action and _bindings.get(other_action, []).has(physical_keycode):
			return ERR_ALREADY_IN_USE
	_bindings[action] = [physical_keycode]
	_apply(action)
	return OK


func reset_to_defaults() -> void:
	for action: StringName in InputMapContractType.ORDERED_ACTIONS:
		_bindings[action] = InputMapContractType.REQUIRED_ACTIONS[action].duplicate()
		_apply(action)


func _apply(action: StringName) -> void:
	if not _input_map.has_action(action):
		return
	_input_map.action_erase_events(action)
	for physical_keycode: Key in _bindings[action]:
		var event := InputEventKey.new()
		event.physical_keycode = physical_keycode
		event.device = -1
		_input_map.action_add_event(action, event)
