extends "res://tests/support/test_case.gd"

const RenderObjectRefType := preload("res://src/core/schema/render_object_ref.gd")
const RenderObjectRefValidatorType := preload(
	"res://src/core/schema/render_object_ref_validator.gd"
)


func _valid_ref() -> RenderObjectRefType:
	var ref := RenderObjectRefType.new()
	ref.object_id = &"trashy"
	ref.layer_name = &"GAMEPLAY"
	return ref


func test_valid_render_object_ref_produces_no_errors() -> void:
	var errors := RenderObjectRefValidatorType.validate(_valid_ref())
	assert_equal(errors.size(), 0, "valid render object ref errors")


func test_missing_object_id_is_rejected() -> void:
	var ref := _valid_ref()
	ref.object_id = &""
	var errors := RenderObjectRefValidatorType.validate(ref)
	assert_true(errors.size() > 0, "missing object id rejected")


func test_unknown_layer_name_is_rejected() -> void:
	var ref := _valid_ref()
	ref.layer_name = &"MIDGROUND"
	var errors := RenderObjectRefValidatorType.validate(ref)
	assert_true(errors.size() > 0, "unknown layer name rejected")
	assert_true(
		errors[0].find("unknown layer") != -1, "unknown layer error message: %s" % errors[0]
	)


func test_empty_layer_name_is_rejected() -> void:
	var ref := _valid_ref()
	ref.layer_name = &""
	var errors := RenderObjectRefValidatorType.validate(ref)
	assert_true(errors.size() > 0, "empty layer name rejected")


func test_schema_version_mismatch_is_rejected() -> void:
	var ref := _valid_ref()
	ref.schema_version = RenderObjectRefType.CURRENT_SCHEMA_VERSION + 1
	var errors := RenderObjectRefValidatorType.validate(ref)
	assert_true(errors.size() > 0, "schema version mismatch rejected")
