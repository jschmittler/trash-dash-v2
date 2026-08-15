extends "res://tests/support/test_case.gd"

const CollisionGeometryType := preload("res://src/core/schema/collision_geometry.gd")
const CollisionGeometryValidatorType := preload(
	"res://src/core/schema/collision_geometry_validator.gd"
)


func _valid_geometry() -> CollisionGeometryType:
	var geometry := CollisionGeometryType.new()
	geometry.owner_id = &"platform_01"
	geometry.role = CollisionGeometryType.Role.SUPPORT
	geometry.rect = Rect2(Vector2.ZERO, Vector2(64, 16))
	return geometry


func test_valid_collision_geometry_produces_no_errors() -> void:
	var errors := CollisionGeometryValidatorType.validate(_valid_geometry())
	assert_equal(errors.size(), 0, "valid collision geometry errors")


func test_missing_owner_id_is_rejected() -> void:
	var geometry := _valid_geometry()
	geometry.owner_id = &""
	var errors := CollisionGeometryValidatorType.validate(geometry)
	assert_true(errors.size() > 0, "missing owner id rejected")


func test_zero_width_is_rejected_as_degenerate() -> void:
	var geometry := _valid_geometry()
	geometry.rect = Rect2(Vector2.ZERO, Vector2(0, 16))
	var errors := CollisionGeometryValidatorType.validate(geometry)
	assert_true(errors.size() > 0, "zero width rejected")


func test_zero_height_is_rejected_as_degenerate() -> void:
	var geometry := _valid_geometry()
	geometry.rect = Rect2(Vector2.ZERO, Vector2(64, 0))
	var errors := CollisionGeometryValidatorType.validate(geometry)
	assert_true(errors.size() > 0, "zero height rejected")


func test_negative_size_is_rejected_as_degenerate() -> void:
	var geometry := _valid_geometry()
	geometry.rect = Rect2(Vector2.ZERO, Vector2(-4, 16))
	var errors := CollisionGeometryValidatorType.validate(geometry)
	assert_true(errors.size() > 0, "negative size rejected")


func test_out_of_range_role_is_rejected() -> void:
	var geometry := _valid_geometry()
	geometry.role = 999 as CollisionGeometryType.Role
	var errors := CollisionGeometryValidatorType.validate(geometry)
	assert_true(errors.size() > 0, "out of range role rejected")


func test_schema_version_mismatch_is_rejected() -> void:
	var geometry := _valid_geometry()
	geometry.schema_version = CollisionGeometryType.CURRENT_SCHEMA_VERSION + 1
	var errors := CollisionGeometryValidatorType.validate(geometry)
	assert_true(errors.size() > 0, "schema version mismatch rejected")


func test_every_role_value_is_individually_valid() -> void:
	for role: CollisionGeometryType.Role in CollisionGeometryType.ROLE_VALUES:
		var geometry := _valid_geometry()
		geometry.role = role
		var errors := CollisionGeometryValidatorType.validate(geometry)
		assert_equal(errors.size(), 0, "role %s is valid" % role)
