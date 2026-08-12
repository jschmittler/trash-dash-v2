extends "res://tests/support/test_case.gd"

const FoundationStatusType := preload("res://src/core/bootstrap/foundation_status.gd")
const BuildIdentityType := preload("res://src/core/build/build_identity.gd")
const ProjectSettingsAdapterType := preload("res://src/core/bootstrap/project_settings_adapter.gd")
const ServiceRegistryType := preload("res://src/core/services/service_registry.gd")
const BOOTSTRAP_SCENE: PackedScene = preload("res://scenes/bootstrap/bootstrap.tscn")

const REQUIRED_NODE_PATHS: Array[NodePath] = [
	NodePath("SafeMargin"),
	NodePath("SafeMargin/StatusColumn"),
	NodePath("SafeMargin/StatusColumn/ProjectTitle"),
	NodePath("SafeMargin/StatusColumn/FoundationStatus"),
	NodePath("SafeMargin/StatusColumn/BuildIdentity"),
	NodePath("SafeMargin/StatusColumn/RuntimePolicy"),
	NodePath("SafeMargin/StatusColumn/ContentStatus"),
]
const LOGICAL_VIEWPORT_SIZE := Vector2i(960, 540)
const PORTRAIT_WINDOW_SIZE := Vector2i(390, 844)
const REQUIRED_LOGICAL_FONT_SIZE := 32
const MINIMUM_PORTRAIT_FONT_PIXELS := 13.0

func test_scene_presents_ready_foundation_and_frees_cleanly() -> void:
	var bootstrap := BOOTSTRAP_SCENE.instantiate()
	assert_equal(bootstrap.name, &"Bootstrap", "root name")
	for node_path: NodePath in REQUIRED_NODE_PATHS:
		assert_true(bootstrap.has_node(node_path), "missing node: %s" % node_path)
	assert_true(bootstrap is Control, "root type")
	assert_true(bootstrap.get_node("SafeMargin") is MarginContainer, "safe margin type")
	assert_true(bootstrap.get_node("SafeMargin/StatusColumn") is VBoxContainer, "status column type")
	assert_equal(bootstrap.get_child_count(), 1, "root child count")
	assert_equal(bootstrap.get_node("SafeMargin").get_child_count(), 1, "safe margin child count")
	assert_equal(bootstrap.get_node("SafeMargin/StatusColumn").get_child_count(), 5, "label count")
	var tree := Engine.get_main_loop() as SceneTree
	tree.root.add_child(bootstrap)
	await tree.process_frame
	await tree.process_frame
	assert_equal(
		bootstrap.call("foundation_state"),
		FoundationStatusType.State.FOUNDATION_READY,
		"foundation state"
	)
	assert_equal(_label_text(bootstrap, "ProjectTitle"), "Trash Dash 2.0", "project title")
	assert_equal(
		_label_text(bootstrap, "FoundationStatus"),
		"macOS prototype foundation — FOUNDATION_READY",
		"foundation status"
	)
	assert_equal(
		_label_text(bootstrap, "BuildIdentity"),
		"0.1.0-foundation (development)",
		"build identity"
	)
	assert_equal(_label_text(bootstrap, "RuntimePolicy"), "960×540 / Compatibility", "runtime policy")
	assert_equal(_label_text(bootstrap, "ContentStatus"), "prototype content not loaded", "content status")
	bootstrap.queue_free()
	await tree.process_frame
	assert_true(not is_instance_valid(bootstrap), "bootstrap freed")

func test_configured_error_presentation_appends_validation_messages() -> void:
	var bootstrap := BOOTSTRAP_SCENE.instantiate()
	var complete_registry := ServiceRegistryType.unavailable()
	var incomplete_registry := ServiceRegistryType.new(
		complete_registry.save_settings(),
		null,
		complete_registry.scenes(),
		complete_registry.runtime_state()
	)
	bootstrap.call(
		"configure",
		incomplete_registry,
		ProjectSettingsAdapterType.new(),
		BuildIdentityType.development()
	)
	var tree := Engine.get_main_loop() as SceneTree
	tree.root.add_child(bootstrap)
	await tree.process_frame
	await tree.process_frame
	assert_equal(
		bootstrap.call("foundation_state"),
		FoundationStatusType.State.FOUNDATION_ERROR,
		"configured foundation state"
	)
	assert_equal(
		_label_text(bootstrap, "FoundationStatus"),
		"macOS prototype foundation — FOUNDATION_ERROR",
		"error state text"
	)
	assert_equal(
		_label_text(bootstrap, "ContentStatus"),
		"prototype content not loaded\nmissing service: audio",
		"validation message"
	)
	bootstrap.queue_free()
	await tree.process_frame
	assert_true(not is_instance_valid(bootstrap), "error bootstrap freed")

func test_container_theme_keeps_portrait_diagnostics_readable() -> void:
	var bootstrap := BOOTSTRAP_SCENE.instantiate()
	var tree := Engine.get_main_loop() as SceneTree
	tree.root.add_child(bootstrap)
	await tree.process_frame
	var safe_margin := bootstrap.get_node("SafeMargin") as MarginContainer
	assert_true(safe_margin.theme != null, "safe margin owns diagnostic theme")
	var logical_font_size := (
		safe_margin.theme.default_font_size if safe_margin.theme != null else 0
	)
	assert_equal(
		logical_font_size,
		REQUIRED_LOGICAL_FONT_SIZE,
		"container-owned logical font size"
	)
	var keep_aspect_scale := minf(
		float(PORTRAIT_WINDOW_SIZE.x) / float(LOGICAL_VIEWPORT_SIZE.x),
		float(PORTRAIT_WINDOW_SIZE.y) / float(LOGICAL_VIEWPORT_SIZE.y)
	)
	assert_true(
		float(logical_font_size) * keep_aspect_scale >= MINIMUM_PORTRAIT_FONT_PIXELS,
		"portrait effective font pixels"
	)
	for label_name: String in [
		"ProjectTitle",
		"FoundationStatus",
		"BuildIdentity",
		"RuntimePolicy",
		"ContentStatus",
	]:
		var label := safe_margin.get_node("StatusColumn/%s" % label_name) as Label
		assert_equal(
			label.get_theme_font_size(&"font_size"),
			REQUIRED_LOGICAL_FONT_SIZE,
			"inherited font size: %s" % label_name
		)
	bootstrap.queue_free()
	await tree.process_frame
	assert_true(not is_instance_valid(bootstrap), "typography bootstrap freed")

func _label_text(bootstrap: Node, label_name: String) -> String:
	var path := NodePath("SafeMargin/StatusColumn/%s" % label_name)
	var label := bootstrap.get_node_or_null(path) as Label
	return label.text if label != null else "<missing>"
