extends "res://tests/support/test_case.gd"

const AnimationManifestType := preload("res://src/core/schema/animation_manifest.gd")
const AnimationStateRefType := preload("res://src/core/schema/animation_state_ref.gd")
const AnimationStateRefValidatorType := preload(
	"res://src/core/schema/animation_state_ref_validator.gd"
)


func _manifest() -> AnimationManifestType:
	var manifest := AnimationManifestType.new()
	manifest.family_id = &"trashy"
	manifest.runtime_scale = Vector2(1.0, 1.0)
	manifest.state_names = [&"idle", &"run", &"jump"]
	return manifest


func _valid_ref() -> AnimationStateRefType:
	var ref := AnimationStateRefType.new()
	ref.family_id = &"trashy"
	ref.state_name = &"run"
	return ref


func test_known_state_produces_no_errors() -> void:
	var errors := AnimationStateRefValidatorType.validate(_valid_ref(), _manifest())
	assert_equal(errors.size(), 0, "known state errors")


func test_unknown_state_is_rejected() -> void:
	var ref := _valid_ref()
	ref.state_name = &"crouch"
	var errors := AnimationStateRefValidatorType.validate(ref, _manifest())
	assert_true(errors.size() > 0, "unknown state rejected")
	assert_true(
		errors[0].find("unknown state") != -1, "unknown state error message: %s" % errors[0]
	)


func test_family_id_mismatch_with_manifest_is_rejected() -> void:
	var ref := _valid_ref()
	ref.family_id = &"jimothy"
	var errors := AnimationStateRefValidatorType.validate(ref, _manifest())
	assert_true(errors.size() > 0, "family id mismatch rejected")


func test_missing_state_name_is_rejected() -> void:
	var ref := _valid_ref()
	ref.state_name = &""
	var errors := AnimationStateRefValidatorType.validate(ref, _manifest())
	assert_true(errors.size() > 0, "missing state name rejected")


func test_schema_version_mismatch_is_rejected() -> void:
	var ref := _valid_ref()
	ref.schema_version = AnimationStateRefType.CURRENT_SCHEMA_VERSION + 1
	var errors := AnimationStateRefValidatorType.validate(ref, _manifest())
	assert_true(errors.size() > 0, "schema version mismatch rejected")
