class_name EncounterValidator
extends RefCounted

const EncounterType := preload("res://src/core/schema/encounter.gd")

## Readable-group size bounds per ENCOUNTER_CONTRACT.md: small enemies in
## groups of one to three, medium enemies alone or in pairs, large enemies
## owning isolated encounter space (exactly one).
const GROUP_SIZE_BOUNDS: Dictionary = {
	EncounterType.EnemySizeClass.SMALL: Vector2i(1, 3),
	EncounterType.EnemySizeClass.MEDIUM: Vector2i(1, 2),
	EncounterType.EnemySizeClass.LARGE: Vector2i(1, 1),
}


static func validate(
	encounter: EncounterType, known_support_ids: Array[StringName]
) -> PackedStringArray:
	var errors := PackedStringArray()
	if encounter.schema_version != EncounterType.CURRENT_SCHEMA_VERSION:
		(
			errors
			. append(
				(
					"encounter %s has schema version %d, expected %d"
					% [
						encounter.encounter_id,
						encounter.schema_version,
						EncounterType.CURRENT_SCHEMA_VERSION,
					]
				)
			)
		)
	if String(encounter.encounter_id).is_empty():
		errors.append("encounter is missing an encounter id")
	if String(encounter.section_id).is_empty():
		errors.append("encounter %s is missing a section id" % encounter.encounter_id)
	var bounds: Vector2i = GROUP_SIZE_BOUNDS[encounter.enemy_size_class]
	if encounter.enemy_count < bounds.x or encounter.enemy_count > bounds.y:
		errors.append(
			(
				"encounter %s has %d enemies, outside the readable range [%d, %d] for its class"
				% [encounter.encounter_id, encounter.enemy_count, bounds.x, bounds.y]
			)
		)
	if encounter.is_flying:
		if not String(encounter.support_id).is_empty():
			errors.append(
				(
					"encounter %s is flying but also names a ground support: %s"
					% [encounter.encounter_id, encounter.support_id]
				)
			)
	elif String(encounter.support_id).is_empty():
		errors.append(
			(
				"encounter %s is missing support: grounded encounters require a named support"
				% encounter.encounter_id
			)
		)
	elif not known_support_ids.has(encounter.support_id):
		errors.append(
			(
				"encounter %s references an unknown support: %s"
				% [encounter.encounter_id, encounter.support_id]
			)
		)
	return errors


static func validate_no_duplicate_ids(encounters: Array) -> PackedStringArray:
	var errors := PackedStringArray()
	var seen: Dictionary = {}
	for encounter: EncounterType in encounters:
		if seen.has(encounter.encounter_id):
			errors.append("duplicate encounter id: %s" % encounter.encounter_id)
		seen[encounter.encounter_id] = true
	return errors
