extends "res://tests/support/test_case.gd"

const AnimationManifestType := preload("res://src/core/schema/animation_manifest.gd")
const AnimationManifestValidatorType := preload(
	"res://src/core/schema/animation_manifest_validator.gd"
)


func _valid_manifest() -> AnimationManifestType:
	var manifest := AnimationManifestType.new()
	manifest.family_id = &"trashy"
	manifest.runtime_scale = Vector2(1.0, 1.0)
	manifest.state_names = [&"idle", &"run", &"jump"]
	return manifest


func test_valid_manifest_produces_no_errors() -> void:
	var errors := AnimationManifestValidatorType.validate(_valid_manifest())
	assert_equal(errors.size(), 0, "valid manifest errors")


func test_missing_family_id_is_rejected() -> void:
	var manifest := _valid_manifest()
	manifest.family_id = &""
	var errors := AnimationManifestValidatorType.validate(manifest)
	assert_true(errors.size() > 0, "missing family id rejected")


func test_no_declared_states_is_rejected() -> void:
	var manifest := _valid_manifest()
	manifest.state_names = []
	var errors := AnimationManifestValidatorType.validate(manifest)
	assert_true(errors.size() > 0, "no declared states rejected")


func test_duplicate_state_names_are_rejected() -> void:
	var manifest := _valid_manifest()
	manifest.state_names = [&"idle", &"idle"]
	var errors := AnimationManifestValidatorType.validate(manifest)
	assert_true(errors.size() > 0, "duplicate state names rejected")


func test_empty_state_name_is_rejected() -> void:
	var manifest := _valid_manifest()
	manifest.state_names = [&"idle", &""]
	var errors := AnimationManifestValidatorType.validate(manifest)
	assert_true(errors.size() > 0, "empty state name rejected")


func test_nonuniform_runtime_scale_is_rejected() -> void:
	var manifest := _valid_manifest()
	manifest.runtime_scale = Vector2(1.0, 1.5)
	var errors := AnimationManifestValidatorType.validate(manifest)
	assert_true(errors.size() > 0, "nonuniform scale rejected")
	assert_true(errors[0].find("uniform") != -1, "nonuniform scale error message: %s" % errors[0])


func test_nonpositive_runtime_scale_is_rejected() -> void:
	var manifest := _valid_manifest()
	manifest.runtime_scale = Vector2(0.0, 0.0)
	var errors := AnimationManifestValidatorType.validate(manifest)
	assert_true(errors.size() > 0, "nonpositive scale rejected")


func test_schema_version_mismatch_is_rejected() -> void:
	var manifest := _valid_manifest()
	manifest.schema_version = AnimationManifestType.CURRENT_SCHEMA_VERSION + 1
	var errors := AnimationManifestValidatorType.validate(manifest)
	assert_true(errors.size() > 0, "schema version mismatch rejected")
