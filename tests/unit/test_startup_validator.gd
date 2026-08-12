extends "res://tests/support/test_case.gd"

const StartupValidatorType := preload("res://src/core/bootstrap/startup_validator.gd")
const ServiceRegistryType := preload("res://src/core/services/service_registry.gd")

const EXPECTED_ERRORS: Array[String] = [
	"viewport width must be 960",
	"viewport height must be 540",
	"stretch mode must be canvas_items",
	"stretch aspect must be keep",
	"renderer must be gl_compatibility",
	"default texture filtering must be nearest",
	"missing input action: jump",
	"missing service: audio",
]

class FakeSettingsAdapter extends RefCounted:
	var _values: Dictionary

	func _init(values: Dictionary) -> void:
		_values = values.duplicate(true)

	func get_value(key: StringName) -> Variant:
		return _values.get(key)

func test_valid_contract_has_no_errors() -> void:
	assert_equal(
		StartupValidatorType.validate(_valid_settings(), PackedStringArray(), ServiceRegistryType.unavailable()),
		PackedStringArray(),
		"valid"
	)

func test_failures_are_ordered() -> void:
	assert_equal(
		StartupValidatorType.validate(
			_invalid_settings(),
			PackedStringArray(["missing input action: jump"]),
			_incomplete_registry()
		),
		PackedStringArray(EXPECTED_ERRORS),
		"order"
	)

func _valid_settings() -> FakeSettingsAdapter:
	return FakeSettingsAdapter.new({
		&"display/window/size/viewport_width": 960,
		&"display/window/size/viewport_height": 540,
		&"display/window/stretch/mode": "canvas_items",
		&"display/window/stretch/aspect": "keep",
		&"rendering/renderer/rendering_method": "gl_compatibility",
		&"rendering/textures/canvas_textures/default_texture_filter": 0,
	})

func _invalid_settings() -> FakeSettingsAdapter:
	return FakeSettingsAdapter.new({
		&"display/window/size/viewport_width": 961,
		&"display/window/size/viewport_height": 541,
		&"display/window/stretch/mode": "viewport",
		&"display/window/stretch/aspect": "expand",
		&"rendering/renderer/rendering_method": "mobile",
		&"rendering/textures/canvas_textures/default_texture_filter": 1,
	})

func _incomplete_registry() -> ServiceRegistryType:
	var complete_registry := ServiceRegistryType.unavailable()
	return ServiceRegistryType.new(
		complete_registry.save_settings(),
		null,
		complete_registry.scenes(),
		complete_registry.runtime_state()
	)
