extends "res://tests/support/test_case.gd"

const REQUIRED_ACTIONS := {
	&"move_left": [KEY_A, KEY_LEFT],
	&"move_right": [KEY_D, KEY_RIGHT],
	&"jump": [KEY_SPACE],
	&"dash": [KEY_SHIFT],
	&"action": [KEY_E],
	&"pause": [KEY_ESCAPE],
}

const FORBIDDEN_EXPORT_PLATFORMS: Array[String] = [
	"Windows Desktop",
	"Android",
	"iOS",
	"Linux",
	"Web",
]

func test_settings_are_exact() -> void:
	assert_equal(ProjectSettings.get_setting("application/run/main_scene"), "res://scenes/bootstrap/bootstrap.tscn", "main scene")
	assert_true(ResourceLoader.exists("res://scenes/bootstrap/bootstrap.tscn"), "main scene resource")
	assert_equal(ProjectSettings.get_setting("display/window/size/viewport_width"), 960, "width")
	assert_equal(ProjectSettings.get_setting("display/window/size/viewport_height"), 540, "height")
	assert_equal(ProjectSettings.get_setting("display/window/stretch/mode"), "canvas_items", "stretch")
	assert_equal(ProjectSettings.get_setting("display/window/stretch/aspect"), "keep", "aspect")
	assert_equal(ProjectSettings.get_setting("rendering/renderer/rendering_method"), "gl_compatibility", "renderer")
	assert_equal(ProjectSettings.get_setting("rendering/textures/canvas_textures/default_texture_filter"), 0, "nearest")
	assert_equal(
		ProjectSettings.get_setting("rendering/textures/vram_compression/import_etc2_astc"),
		true,
		"universal macOS texture import"
	)

func test_actions_have_exact_physical_defaults() -> void:
	for action: StringName in REQUIRED_ACTIONS:
		assert_true(InputMap.has_action(action), "missing action: %s" % action)
		assert_equal(InputMap.action_get_deadzone(action), 0.5, "deadzone: %s" % action)
		var events := InputMap.action_get_events(action)
		assert_equal(events.size(), REQUIRED_ACTIONS[action].size(), "event count: %s" % action)
		for event_index: int in events.size():
			_assert_exact_key_event(
				events[event_index],
				REQUIRED_ACTIONS[action][event_index],
				"%s event %d" % [action, event_index]
			)
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

func _assert_exact_key_event(event: InputEvent, expected_key: Key, context: String) -> void:
	assert_true(event is InputEventKey, "%s type" % context)
	if not event is InputEventKey:
		return
	var key_event := event as InputEventKey
	assert_equal(key_event.physical_keycode, expected_key, "%s physical key" % context)
	assert_equal(key_event.keycode, KEY_NONE, "%s logical key" % context)
	assert_equal(key_event.key_label, KEY_NONE, "%s key label" % context)
	assert_equal(key_event.unicode, 0, "%s unicode" % context)
	assert_equal(key_event.location, KeyLocation.KEY_LOCATION_UNSPECIFIED, "%s location" % context)
	assert_equal(key_event.alt_pressed, false, "%s alt modifier" % context)
	assert_equal(key_event.shift_pressed, false, "%s shift modifier" % context)
	assert_equal(key_event.ctrl_pressed, false, "%s control modifier" % context)
	assert_equal(key_event.meta_pressed, false, "%s command modifier" % context)
	assert_equal(key_event.pressed, false, "%s pressed state" % context)
	assert_equal(key_event.echo, false, "%s echo state" % context)
	assert_equal(key_event.device, -1, "%s device" % context)
	assert_equal(key_event.window_id, 0, "%s window" % context)
	assert_equal(key_event.resource_local_to_scene, false, "%s local resource" % context)
	assert_equal(key_event.resource_name, "", "%s resource name" % context)
	assert_equal(key_event.get_script(), null, "%s script" % context)

func test_macos_export_preset_is_single_and_unsigned() -> void:
	var preset_path := "res://export_presets.cfg"
	assert_true(FileAccess.file_exists(preset_path), "export preset exists")
	var preset_text := FileAccess.get_file_as_string(preset_path)
	var preset_header := RegEx.new()
	assert_equal(
		preset_header.compile("(?m)^\\[preset\\.[0-9]+\\]$"),
		OK,
		"preset header regex"
	)
	assert_equal(preset_header.search_all(preset_text).size(), 1, "exactly one preset")
	assert_equal(preset_text.count("[preset.0]"), 1, "single preset.0 section")
	assert_true(not preset_text.contains("[preset.1]"), "no second preset")
	assert_true(preset_text.contains('name="macOS"'), "macOS preset name")
	assert_true(preset_text.contains('platform="macOS"'), "macOS platform")
	assert_true(preset_text.contains("codesign/codesign=0"), "code signing disabled")
	assert_true(
		preset_text.contains("notarization/notarization=0"),
		"notarization disabled"
	)
	for platform_name: String in FORBIDDEN_EXPORT_PLATFORMS:
		assert_true(
			not preset_text.contains(platform_name),
			"deferred export platform absent: %s" % platform_name
		)

func test_macos_export_preset_contains_no_credentials_or_local_paths() -> void:
	var preset_text := FileAccess.get_file_as_string("res://export_presets.cfg")
	var forbidden_assignment := RegEx.new()
	assert_equal(
		forbidden_assignment.compile(
			"(?im)^[^=\\n]*(team[_ ]?id|certificate|identity|password|provisioning[_ ]?profile|secret|token|api[_ ]?key|private[_ ]?key)[^=\\n]*="
		),
		OK,
		"forbidden assignment regex"
	)
	assert_equal(
		forbidden_assignment.search(preset_text),
		null,
		"no credential or secret-looking assignment"
	)
	var absolute_path := RegEx.new()
	assert_equal(
		absolute_path.compile("(?i)(/Users/|/home/|[A-Z]:[\\\\/])"),
		OK,
		"absolute path regex"
	)
	assert_equal(absolute_path.search(preset_text), null, "no absolute user path")
