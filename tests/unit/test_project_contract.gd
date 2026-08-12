extends "res://tests/support/test_case.gd"

const REQUIRED_ACTIONS := {
	&"move_left": [KEY_A, KEY_LEFT],
	&"move_right": [KEY_D, KEY_RIGHT],
	&"jump": [KEY_SPACE],
	&"dash": [KEY_SHIFT],
	&"action": [KEY_E],
	&"pause": [KEY_ESCAPE],
}

func test_settings_are_exact() -> void:
	assert_equal(ProjectSettings.get_setting("application/run/main_scene"), "res://scenes/bootstrap/bootstrap.tscn", "main scene")
	assert_true(ResourceLoader.exists("res://scenes/bootstrap/bootstrap.tscn"), "main scene resource")
	assert_equal(ProjectSettings.get_setting("display/window/size/viewport_width"), 960, "width")
	assert_equal(ProjectSettings.get_setting("display/window/size/viewport_height"), 540, "height")
	assert_equal(ProjectSettings.get_setting("display/window/stretch/mode"), "canvas_items", "stretch")
	assert_equal(ProjectSettings.get_setting("display/window/stretch/aspect"), "keep", "aspect")
	assert_equal(ProjectSettings.get_setting("rendering/renderer/rendering_method"), "gl_compatibility", "renderer")
	assert_equal(ProjectSettings.get_setting("rendering/textures/canvas_textures/default_texture_filter"), 0, "nearest")

func test_actions_have_exact_physical_defaults() -> void:
	for action: StringName in REQUIRED_ACTIONS:
		assert_true(InputMap.has_action(action), "missing action: %s" % action)
		var keys: Array[Key] = []
		for event: InputEvent in InputMap.action_get_events(action):
			if event is InputEventKey:
				keys.append((event as InputEventKey).physical_keycode)
		assert_equal(keys, REQUIRED_ACTIONS[action], "defaults: %s" % action)
	var config := ConfigFile.new()
	assert_equal(config.load("res://project.godot"), OK, "project config loads")
	var action_names: Array[String] = []
	for action_name: String in config.get_section_keys("input"):
		action_names.append(action_name)
	action_names.sort()
	var expected_names: Array[String] = []
	for required_action: StringName in REQUIRED_ACTIONS:
		expected_names.append(String(required_action))
	expected_names.sort()
	assert_equal(action_names, expected_names, "project-defined actions")
