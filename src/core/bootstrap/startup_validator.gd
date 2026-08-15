class_name StartupValidator
extends RefCounted


static func validate(
	settings: RefCounted, input_messages: PackedStringArray, registry: RefCounted
) -> PackedStringArray:
	var errors := PackedStringArray()
	_require_equal(
		errors,
		settings.get_value(&"display/window/size/viewport_width"),
		960,
		"viewport width must be 960"
	)
	_require_equal(
		errors,
		settings.get_value(&"display/window/size/viewport_height"),
		540,
		"viewport height must be 540"
	)
	_require_equal(
		errors,
		settings.get_value(&"display/window/stretch/mode"),
		"canvas_items",
		"stretch mode must be canvas_items"
	)
	_require_equal(
		errors,
		settings.get_value(&"display/window/stretch/aspect"),
		"keep",
		"stretch aspect must be keep"
	)
	_require_equal(
		errors,
		settings.get_value(&"rendering/renderer/rendering_method"),
		"gl_compatibility",
		"renderer must be gl_compatibility"
	)
	_require_equal(
		errors,
		settings.get_value(&"rendering/textures/canvas_textures/default_texture_filter"),
		0,
		"default texture filtering must be nearest"
	)
	_require_equal(
		errors,
		settings.get_value(&"physics/common/physics_ticks_per_second"),
		60,
		"physics tick rate must be 60"
	)
	errors.append_array(input_messages)
	for service_id: StringName in registry.missing_service_ids():
		errors.append("missing service: %s" % service_id)
	return errors


static func _require_equal(
	errors: PackedStringArray, actual: Variant, expected: Variant, message: String
) -> void:
	if actual != expected:
		errors.append(message)
