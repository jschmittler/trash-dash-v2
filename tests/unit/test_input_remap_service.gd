extends "res://tests/support/test_case.gd"

const InputRemapServiceType := preload("res://src/core/input/input_remap_service.gd")
const InputMapContractType := preload("res://src/core/input/input_map_contract.gd")


class FakeInputMap:
	extends RefCounted
	var actions: Dictionary = {}

	func _init(known_actions: Array) -> void:
		for action: StringName in known_actions:
			actions[action] = []

	func has_action(action: StringName) -> bool:
		return actions.has(action)

	func action_get_events(action: StringName) -> Array:
		return actions.get(action, [])

	func action_erase_events(action: StringName) -> void:
		actions[action] = []

	func action_add_event(action: StringName, event: InputEvent) -> void:
		actions[action].append(event)


func test_construction_applies_default_bindings_to_the_input_map() -> void:
	var fake := FakeInputMap.new(InputMapContractType.ORDERED_ACTIONS)
	var service := InputRemapServiceType.new(fake)
	assert_equal(service.bindings(), InputMapContractType.REQUIRED_ACTIONS, "default bindings")
	assert_equal(fake.action_get_events(&"jump").size(), 1, "jump has one event")
	var jump_event: InputEventKey = fake.action_get_events(&"jump")[0]
	assert_equal(jump_event.physical_keycode, KEY_SPACE, "jump defaults to space")


func test_rebind_updates_bindings_and_the_input_map() -> void:
	var fake := FakeInputMap.new(InputMapContractType.ORDERED_ACTIONS)
	var service := InputRemapServiceType.new(fake)
	var status := service.rebind(&"jump", KEY_K)
	assert_equal(status, OK, "rebind status")
	assert_equal(service.bindings()[&"jump"], [KEY_K], "jump rebound in memory")
	var jump_events: Array = fake.action_get_events(&"jump")
	assert_equal(jump_events.size(), 1, "jump has exactly one event")
	assert_equal(
		(jump_events[0] as InputEventKey).physical_keycode, KEY_K, "jump applied to input map"
	)


func test_rebind_rejects_unknown_actions() -> void:
	var fake := FakeInputMap.new(InputMapContractType.ORDERED_ACTIONS)
	var service := InputRemapServiceType.new(fake)
	var status := service.rebind(&"does_not_exist", KEY_K)
	assert_equal(status, ERR_DOES_NOT_EXIST, "unknown action status")
	assert_equal(service.bindings(), InputMapContractType.REQUIRED_ACTIONS, "bindings unchanged")


func test_rebind_rejects_keys_already_bound_to_another_action() -> void:
	var fake := FakeInputMap.new(InputMapContractType.ORDERED_ACTIONS)
	var service := InputRemapServiceType.new(fake)
	var status := service.rebind(&"jump", KEY_A)
	assert_equal(status, ERR_ALREADY_IN_USE, "conflicting key status")
	assert_equal(service.bindings()[&"jump"], [KEY_SPACE], "jump keeps its original binding")


func test_rebind_allows_reassigning_an_action_to_its_own_current_key() -> void:
	var fake := FakeInputMap.new(InputMapContractType.ORDERED_ACTIONS)
	var service := InputRemapServiceType.new(fake)
	var status := service.rebind(&"jump", KEY_SPACE)
	assert_equal(status, OK, "self-reassignment status")
	assert_equal(service.bindings()[&"jump"], [KEY_SPACE], "jump binding unchanged")


func test_reset_to_defaults_restores_original_bindings_after_a_rebind() -> void:
	var fake := FakeInputMap.new(InputMapContractType.ORDERED_ACTIONS)
	var service := InputRemapServiceType.new(fake)
	service.rebind(&"jump", KEY_K)
	service.reset_to_defaults()
	assert_equal(service.bindings(), InputMapContractType.REQUIRED_ACTIONS, "defaults restored")
	var jump_events: Array = fake.action_get_events(&"jump")
	assert_equal(
		(jump_events[0] as InputEventKey).physical_keycode, KEY_SPACE, "input map restored"
	)


func test_bindings_returns_a_defensive_copy() -> void:
	var fake := FakeInputMap.new(InputMapContractType.ORDERED_ACTIONS)
	var service := InputRemapServiceType.new(fake)
	var snapshot := service.bindings()
	snapshot[&"jump"] = [KEY_Z]
	assert_equal(
		service.bindings()[&"jump"], [KEY_SPACE], "internal bindings unaffected by copy mutation"
	)
