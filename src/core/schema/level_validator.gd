class_name LevelValidator
extends RefCounted

const LevelType := preload("res://src/core/schema/level.gd")
const EncounterType := preload("res://src/core/schema/encounter.gd")


static func validate(level: LevelType, encounters: Array) -> PackedStringArray:
	var errors := PackedStringArray()
	if level.schema_version != LevelType.CURRENT_SCHEMA_VERSION:
		errors.append(
			(
				"level %s has schema version %d, expected %d"
				% [level.level_id, level.schema_version, LevelType.CURRENT_SCHEMA_VERSION]
			)
		)
	if String(level.level_id).is_empty():
		errors.append("level is missing a level id")
	if level.section_ids.is_empty():
		errors.append("level %s declares no sections" % level.level_id)
	if (
		not String(level.boss_arena_section_id).is_empty()
		and not level.section_ids.has(level.boss_arena_section_id)
	):
		errors.append(
			(
				"level %s boss arena section is not a declared section: %s"
				% [level.level_id, level.boss_arena_section_id]
			)
		)

	var encounters_by_id: Dictionary = {}
	for encounter: EncounterType in encounters:
		encounters_by_id[encounter.encounter_id] = encounter

	var seen_encounter_ids: Dictionary = {}
	for encounter_id: StringName in level.encounter_ids:
		if seen_encounter_ids.has(encounter_id):
			errors.append("level %s duplicates encounter id: %s" % [level.level_id, encounter_id])
		seen_encounter_ids[encounter_id] = true
		if not encounters_by_id.has(encounter_id):
			errors.append(
				"level %s references an unknown encounter: %s" % [level.level_id, encounter_id]
			)
			continue
		var encounter: EncounterType = encounters_by_id[encounter_id]
		if not level.section_ids.has(encounter.section_id):
			errors.append(
				(
					"level %s encounter %s belongs to an undeclared section: %s"
					% [level.level_id, encounter_id, encounter.section_id]
				)
			)

	if not String(level.boss_encounter_id).is_empty():
		if not encounters_by_id.has(level.boss_encounter_id):
			errors.append(
				"level %s boss encounter is unknown: %s" % [level.level_id, level.boss_encounter_id]
			)
		else:
			var boss_encounter: EncounterType = encounters_by_id[level.boss_encounter_id]
			if boss_encounter.section_id != level.boss_arena_section_id:
				errors.append(
					(
						"level %s boss encounter %s is outside its boss arena"
						% [level.level_id, level.boss_encounter_id]
					)
				)

	if not String(level.boss_arena_section_id).is_empty():
		for encounter_id: StringName in level.encounter_ids:
			if encounter_id == level.boss_encounter_id or not encounters_by_id.has(encounter_id):
				continue
			var encounter: EncounterType = encounters_by_id[encounter_id]
			if encounter.section_id == level.boss_arena_section_id:
				errors.append(
					(
						"level %s has ordinary encounter %s inside the locked boss arena"
						% [level.level_id, encounter_id]
					)
				)

	return errors
