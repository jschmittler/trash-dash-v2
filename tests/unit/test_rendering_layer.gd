extends "res://tests/support/test_case.gd"

const RenderingLayerType := preload("res://src/core/schema/rendering_layer.gd")

const EXPECTED_ORDER: Array[StringName] = [
	&"FAR_BACKGROUND",
	&"BACKGROUND_SCENERY",
	&"REAR_ENVIRONMENT",
	&"TERRAIN",
	&"GROUND_DECOR",
	&"GAMEPLAY",
	&"GAMEPLAY_EFFECTS",
	&"FOREGROUND",
	&"HUD",
]


func test_ordered_layers_matches_rendering_layers_contract_back_to_front() -> void:
	assert_equal(RenderingLayerType.ORDERED_LAYERS.size(), EXPECTED_ORDER.size(), "layer count")
	for i: int in range(EXPECTED_ORDER.size()):
		var layer: RenderingLayerType.Layer = RenderingLayerType.ORDERED_LAYERS[i]
		assert_equal(
			RenderingLayerType.name_of(layer), EXPECTED_ORDER[i], "layer name at depth %d" % i
		)


func test_depth_of_is_the_single_source_of_numeric_ordering() -> void:
	for i: int in range(EXPECTED_ORDER.size()):
		var layer: RenderingLayerType.Layer = RenderingLayerType.ORDERED_LAYERS[i]
		assert_equal(RenderingLayerType.depth_of(layer), i, "depth of %s" % EXPECTED_ORDER[i])


func test_from_name_resolves_every_known_layer_name() -> void:
	for layer_name: StringName in EXPECTED_ORDER:
		var resolved: Variant = RenderingLayerType.from_name(layer_name)
		assert_true(resolved != null, "resolves known layer %s" % layer_name)
		assert_equal(RenderingLayerType.name_of(resolved), layer_name, "roundtrip %s" % layer_name)


func test_from_name_rejects_unknown_layer_names() -> void:
	assert_equal(RenderingLayerType.from_name(&"MIDGROUND"), null, "unknown layer name")
	assert_equal(RenderingLayerType.from_name(&""), null, "empty layer name")
