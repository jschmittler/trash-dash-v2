class_name RenderingLayer
extends RefCounted

## Single adapter for the ordered, symbolic render layers defined in
## docs/architecture/RENDERING_LAYERS.md. Numeric depth is derived only
## through depth_of(); gameplay/content data must reference layers by name.

enum Layer {
	FAR_BACKGROUND,
	BACKGROUND_SCENERY,
	REAR_ENVIRONMENT,
	TERRAIN,
	GROUND_DECOR,
	GAMEPLAY,
	GAMEPLAY_EFFECTS,
	FOREGROUND,
	HUD,
}

const ORDERED_LAYERS: Array[Layer] = [
	Layer.FAR_BACKGROUND,
	Layer.BACKGROUND_SCENERY,
	Layer.REAR_ENVIRONMENT,
	Layer.TERRAIN,
	Layer.GROUND_DECOR,
	Layer.GAMEPLAY,
	Layer.GAMEPLAY_EFFECTS,
	Layer.FOREGROUND,
	Layer.HUD,
]

const NAMES: Dictionary = {
	Layer.FAR_BACKGROUND: &"FAR_BACKGROUND",
	Layer.BACKGROUND_SCENERY: &"BACKGROUND_SCENERY",
	Layer.REAR_ENVIRONMENT: &"REAR_ENVIRONMENT",
	Layer.TERRAIN: &"TERRAIN",
	Layer.GROUND_DECOR: &"GROUND_DECOR",
	Layer.GAMEPLAY: &"GAMEPLAY",
	Layer.GAMEPLAY_EFFECTS: &"GAMEPLAY_EFFECTS",
	Layer.FOREGROUND: &"FOREGROUND",
	Layer.HUD: &"HUD",
}


static func name_of(layer: Layer) -> StringName:
	return NAMES[layer]


static func depth_of(layer: Layer) -> int:
	return ORDERED_LAYERS.find(layer)


static func from_name(layer_name: StringName) -> Variant:
	for layer: Layer in ORDERED_LAYERS:
		if NAMES[layer] == layer_name:
			return layer
	return null
