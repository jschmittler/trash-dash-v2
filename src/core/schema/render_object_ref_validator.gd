class_name RenderObjectRefValidator
extends RefCounted

const RenderObjectRefType := preload("res://src/core/schema/render_object_ref.gd")
const RenderingLayerType := preload("res://src/core/schema/rendering_layer.gd")


static func validate(ref: RenderObjectRefType) -> PackedStringArray:
	var errors := PackedStringArray()
	if ref.schema_version != RenderObjectRefType.CURRENT_SCHEMA_VERSION:
		errors.append(
			(
				"render object %s has schema version %d, expected %d"
				% [ref.object_id, ref.schema_version, RenderObjectRefType.CURRENT_SCHEMA_VERSION]
			)
		)
	if String(ref.object_id).is_empty():
		errors.append("render object is missing an object id")
	if String(ref.layer_name).is_empty():
		errors.append("render object %s is missing a layer name" % ref.object_id)
	elif RenderingLayerType.from_name(ref.layer_name) == null:
		errors.append(
			"render object %s references an unknown layer: %s" % [ref.object_id, ref.layer_name]
		)
	return errors
