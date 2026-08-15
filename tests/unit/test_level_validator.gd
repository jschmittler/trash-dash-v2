extends "res://tests/support/test_case.gd"

const LevelType := preload("res://src/core/schema/level.gd")
const LevelValidatorType := preload("res://src/core/schema/level_validator.gd")
const EncounterType := preload("res://src/core/schema/encounter.gd")


func _encounter(encounter_id: StringName, section_id: StringName) -> EncounterType:
	var encounter := EncounterType.new()
	encounter.encounter_id = encounter_id
	encounter.section_id = section_id
	encounter.enemy_size_class = EncounterType.EnemySizeClass.SMALL
	encounter.enemy_count = 1
	encounter.support_id = &"catwalk_01"
	return encounter


func _valid_level() -> LevelType:
	var level := LevelType.new()
	level.level_id = &"level_03"
	level.section_ids = [&"section_01", &"boss_section"]
	level.encounter_ids = [&"alley_rats_01", &"diamond_don_boss"]
	level.boss_arena_section_id = &"boss_section"
	level.boss_encounter_id = &"diamond_don_boss"
	return level


func _valid_encounters() -> Array:
	return [
		_encounter(&"alley_rats_01", &"section_01"),
		_encounter(&"diamond_don_boss", &"boss_section"),
	]


func test_valid_level_produces_no_errors() -> void:
	var errors := LevelValidatorType.validate(_valid_level(), _valid_encounters())
	assert_equal(errors.size(), 0, "valid level errors")


func test_missing_level_id_is_rejected() -> void:
	var level := _valid_level()
	level.level_id = &""
	var errors := LevelValidatorType.validate(level, _valid_encounters())
	assert_true(errors.size() > 0, "missing level id rejected")


func test_level_with_no_sections_is_rejected() -> void:
	var level := _valid_level()
	level.section_ids = []
	var errors := LevelValidatorType.validate(level, _valid_encounters())
	assert_true(errors.size() > 0, "no sections rejected")


func test_unknown_encounter_id_is_rejected() -> void:
	var level := _valid_level()
	level.encounter_ids.append(&"nonexistent_encounter")
	var errors := LevelValidatorType.validate(level, _valid_encounters())
	assert_true(errors.size() > 0, "unknown encounter id rejected")
	assert_true(
		errors[0].find("unknown encounter") != -1, "unknown encounter error message: %s" % errors[0]
	)


func test_encounter_in_undeclared_section_is_rejected() -> void:
	var level := _valid_level()
	var encounters := _valid_encounters()
	(encounters[0] as EncounterType).section_id = &"section_never_declared"
	var errors := LevelValidatorType.validate(level, encounters)
	assert_true(errors.size() > 0, "encounter in undeclared section rejected")


func test_duplicate_encounter_ids_in_level_are_rejected() -> void:
	var level := _valid_level()
	level.encounter_ids.append(&"alley_rats_01")
	var errors := LevelValidatorType.validate(level, _valid_encounters())
	assert_true(errors.size() > 0, "duplicate encounter ids in level rejected")


func test_boss_arena_section_not_declared_is_rejected() -> void:
	var level := _valid_level()
	level.boss_arena_section_id = &"undeclared_boss_section"
	var errors := LevelValidatorType.validate(level, _valid_encounters())
	assert_true(errors.size() > 0, "undeclared boss arena section rejected")


func test_boss_outside_boss_arena_is_rejected() -> void:
	var level := _valid_level()
	var encounters := _valid_encounters()
	(encounters[1] as EncounterType).section_id = &"section_01"
	var errors := LevelValidatorType.validate(level, encounters)
	assert_true(errors.size() > 0, "boss outside boss arena rejected")
	assert_true(
		errors[0].find("boss") != -1 and errors[0].find("outside") != -1,
		"boss outside arena error message: %s" % errors[0]
	)


func test_ordinary_enemy_inside_locked_boss_arena_is_rejected() -> void:
	var level := _valid_level()
	var encounters := _valid_encounters()
	(encounters[0] as EncounterType).section_id = &"boss_section"
	var errors := LevelValidatorType.validate(level, encounters)
	assert_true(errors.size() > 0, "ordinary enemy inside boss arena rejected")
	assert_true(
		errors[0].find("locked boss arena") != -1,
		"boss contamination error message: %s" % errors[0]
	)


func test_unknown_boss_encounter_id_is_rejected() -> void:
	var level := _valid_level()
	level.boss_encounter_id = &"nonexistent_boss"
	var errors := LevelValidatorType.validate(level, _valid_encounters())
	assert_true(errors.size() > 0, "unknown boss encounter id rejected")


func test_level_without_a_boss_arena_produces_no_boss_errors() -> void:
	var level := _valid_level()
	level.boss_arena_section_id = &""
	level.boss_encounter_id = &""
	var errors := LevelValidatorType.validate(level, _valid_encounters())
	assert_equal(errors.size(), 0, "non-boss level errors")


func test_schema_version_mismatch_is_rejected() -> void:
	var level := _valid_level()
	level.schema_version = LevelType.CURRENT_SCHEMA_VERSION + 1
	var errors := LevelValidatorType.validate(level, _valid_encounters())
	assert_true(errors.size() > 0, "schema version mismatch rejected")
