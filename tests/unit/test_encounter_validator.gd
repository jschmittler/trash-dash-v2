extends "res://tests/support/test_case.gd"

const EncounterType := preload("res://src/core/schema/encounter.gd")
const EncounterValidatorType := preload("res://src/core/schema/encounter_validator.gd")

const KNOWN_SUPPORTS: Array[StringName] = [&"catwalk_01", &"rooftop_ledge_02"]


func _valid_encounter() -> EncounterType:
	var encounter := EncounterType.new()
	encounter.encounter_id = &"alley_rats_01"
	encounter.section_id = &"section_02"
	encounter.enemy_size_class = EncounterType.EnemySizeClass.SMALL
	encounter.enemy_count = 3
	encounter.support_id = &"catwalk_01"
	return encounter


func test_valid_encounter_produces_no_errors() -> void:
	var errors := EncounterValidatorType.validate(_valid_encounter(), KNOWN_SUPPORTS)
	assert_equal(errors.size(), 0, "valid encounter errors")


func test_missing_encounter_id_is_rejected() -> void:
	var encounter := _valid_encounter()
	encounter.encounter_id = &""
	var errors := EncounterValidatorType.validate(encounter, KNOWN_SUPPORTS)
	assert_true(errors.size() > 0, "missing encounter id rejected")


func test_missing_section_id_is_rejected() -> void:
	var encounter := _valid_encounter()
	encounter.section_id = &""
	var errors := EncounterValidatorType.validate(encounter, KNOWN_SUPPORTS)
	assert_true(errors.size() > 0, "missing section id rejected")


func test_small_group_above_three_is_rejected() -> void:
	var encounter := _valid_encounter()
	encounter.enemy_count = 4
	var errors := EncounterValidatorType.validate(encounter, KNOWN_SUPPORTS)
	assert_true(errors.size() > 0, "oversized small group rejected")


func test_medium_group_above_two_is_rejected() -> void:
	var encounter := _valid_encounter()
	encounter.enemy_size_class = EncounterType.EnemySizeClass.MEDIUM
	encounter.enemy_count = 3
	var errors := EncounterValidatorType.validate(encounter, KNOWN_SUPPORTS)
	assert_true(errors.size() > 0, "oversized medium group rejected")


func test_large_encounter_must_be_isolated_to_one() -> void:
	var encounter := _valid_encounter()
	encounter.enemy_size_class = EncounterType.EnemySizeClass.LARGE
	encounter.enemy_count = 2
	var errors := EncounterValidatorType.validate(encounter, KNOWN_SUPPORTS)
	assert_true(errors.size() > 0, "non-isolated large encounter rejected")


func test_zero_or_negative_enemy_count_is_rejected() -> void:
	var encounter := _valid_encounter()
	encounter.enemy_count = 0
	var errors := EncounterValidatorType.validate(encounter, KNOWN_SUPPORTS)
	assert_true(errors.size() > 0, "zero enemy count rejected")


func test_grounded_encounter_missing_support_is_rejected() -> void:
	var encounter := _valid_encounter()
	encounter.support_id = &""
	var errors := EncounterValidatorType.validate(encounter, KNOWN_SUPPORTS)
	assert_true(errors.size() > 0, "grounded encounter missing support rejected")
	assert_true(
		errors[0].find("missing support") != -1, "missing support error message: %s" % errors[0]
	)


func test_grounded_encounter_unknown_support_is_rejected() -> void:
	var encounter := _valid_encounter()
	encounter.support_id = &"nonexistent_platform"
	var errors := EncounterValidatorType.validate(encounter, KNOWN_SUPPORTS)
	assert_true(errors.size() > 0, "unknown support rejected")
	assert_true(
		errors[0].find("unknown support") != -1, "unknown support error message: %s" % errors[0]
	)


func test_flying_encounter_does_not_require_a_named_support() -> void:
	var encounter := _valid_encounter()
	encounter.is_flying = true
	encounter.support_id = &""
	var errors := EncounterValidatorType.validate(encounter, KNOWN_SUPPORTS)
	assert_equal(errors.size(), 0, "flying encounter without support errors")


func test_flying_encounter_with_a_named_support_is_rejected() -> void:
	var encounter := _valid_encounter()
	encounter.is_flying = true
	var errors := EncounterValidatorType.validate(encounter, KNOWN_SUPPORTS)
	assert_true(errors.size() > 0, "flying encounter with named support rejected")


func test_schema_version_mismatch_is_rejected() -> void:
	var encounter := _valid_encounter()
	encounter.schema_version = EncounterType.CURRENT_SCHEMA_VERSION + 1
	var errors := EncounterValidatorType.validate(encounter, KNOWN_SUPPORTS)
	assert_true(errors.size() > 0, "schema version mismatch rejected")


func test_duplicate_encounter_ids_are_rejected() -> void:
	var first := _valid_encounter()
	var second := _valid_encounter()
	second.section_id = &"section_03"
	var errors := EncounterValidatorType.validate_no_duplicate_ids([first, second])
	assert_true(errors.size() > 0, "duplicate encounter ids rejected")


func test_unique_encounter_ids_produce_no_errors() -> void:
	var first := _valid_encounter()
	var second := _valid_encounter()
	second.encounter_id = &"alley_rats_02"
	var errors := EncounterValidatorType.validate_no_duplicate_ids([first, second])
	assert_equal(errors.size(), 0, "unique encounter ids errors")
