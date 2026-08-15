extends "res://tests/support/test_case.gd"

const DisplayPolicyType := preload("res://src/core/display/display_policy.gd")
const BOOTSTRAP_SCENE: PackedScene = preload("res://scenes/bootstrap/bootstrap.tscn")

const LOGICAL_VIEWPORT_SIZE := Vector2i(960, 540)
const REQUIRED_LOGICAL_FONT_SIZE := 32
const MINIMUM_EFFECTIVE_FONT_PIXELS := 13.0

const REQUIRED_TARGET_WINDOW_SIZES: Dictionary = {
	"1280x720": Vector2i(1280, 720),
	"1440x900": Vector2i(1440, 900),
	"1280x800": Vector2i(1280, 800),
	"narrow_portrait": Vector2i(390, 844),
}


func test_content_rect_is_centered_and_16_9_at_every_required_target_size() -> void:
	for label: String in REQUIRED_TARGET_WINDOW_SIZES:
		var physical_size: Vector2i = REQUIRED_TARGET_WINDOW_SIZES[label]
		var rect := DisplayPolicyType.content_rect(physical_size)
		assert_true(rect.size.x > 0 and rect.size.y > 0, "%s: nonzero content rect" % label)
		assert_true(
			absf(float(rect.size.x) / float(rect.size.y) - 16.0 / 9.0) < 0.01,
			"%s: content rect keeps 16:9" % label
		)
		assert_equal(
			rect.position,
			Vector2i((physical_size.x - rect.size.x) / 2, (physical_size.y - rect.size.y) / 2),
			"%s: content rect is centered" % label
		)


func test_diagnostic_typography_stays_readable_at_every_required_target_size() -> void:
	var bootstrap := BOOTSTRAP_SCENE.instantiate()
	var tree := Engine.get_main_loop() as SceneTree
	tree.root.add_child(bootstrap)
	await tree.process_frame
	var safe_margin := bootstrap.get_node("SafeMargin") as MarginContainer
	var logical_font_size: int = (
		safe_margin.theme.default_font_size if safe_margin.theme != null else 0
	)
	assert_equal(logical_font_size, REQUIRED_LOGICAL_FONT_SIZE, "diagnostic logical font size")
	for label: String in REQUIRED_TARGET_WINDOW_SIZES:
		var physical_size: Vector2i = REQUIRED_TARGET_WINDOW_SIZES[label]
		var keep_aspect_scale := minf(
			float(physical_size.x) / float(LOGICAL_VIEWPORT_SIZE.x),
			float(physical_size.y) / float(LOGICAL_VIEWPORT_SIZE.y)
		)
		assert_true(
			float(logical_font_size) * keep_aspect_scale >= MINIMUM_EFFECTIVE_FONT_PIXELS,
			"%s: effective font pixels stay readable" % label
		)
	bootstrap.queue_free()
	await tree.process_frame
