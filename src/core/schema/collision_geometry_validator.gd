class_name CollisionGeometryValidator
extends RefCounted

const CollisionGeometryType := preload("res://src/core/schema/collision_geometry.gd")


static func validate(geometry: CollisionGeometryType) -> PackedStringArray:
	var errors := PackedStringArray()
	if geometry.schema_version != CollisionGeometryType.CURRENT_SCHEMA_VERSION:
		(
			errors
			. append(
				(
					"collision geometry %s has schema version %d, expected %d"
					% [
						geometry.owner_id,
						geometry.schema_version,
						CollisionGeometryType.CURRENT_SCHEMA_VERSION,
					]
				)
			)
		)
	if String(geometry.owner_id).is_empty():
		errors.append("collision geometry is missing an owner id")
	if not CollisionGeometryType.ROLE_VALUES.has(geometry.role):
		errors.append("collision geometry %s has an unknown role" % geometry.owner_id)
	if geometry.rect.size.x <= 0.0 or geometry.rect.size.y <= 0.0:
		errors.append(
			(
				"collision geometry %s must have a positive nonzero size, got %s"
				% [geometry.owner_id, geometry.rect.size]
			)
		)
	return errors
