class_name CollisionGeometry
extends Resource

## Schema for collision geometry that is authored independently from visual
## art (LEVEL_CONTRACT.md, ANIMATION_CONTRACT.md, RENDERING_LAYERS.md all
## require collision to remain independent of rendering/padding). This
## resource intentionally has no texture, sprite, or scale field so it cannot
## be derived from destination-rect scaling.

enum Role { SUPPORT, HAZARD, HURTBOX, ATTACK, WEAK_POINT }

const ROLE_VALUES: Array[Role] = [
	Role.SUPPORT,
	Role.HAZARD,
	Role.HURTBOX,
	Role.ATTACK,
	Role.WEAK_POINT,
]

const CURRENT_SCHEMA_VERSION := 1

@export var schema_version: int = CURRENT_SCHEMA_VERSION
@export var owner_id: StringName = &""
@export var role: Role = Role.SUPPORT
@export var rect: Rect2 = Rect2()
