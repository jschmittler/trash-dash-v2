class_name DisplayPolicy
extends RefCounted

static func content_rect(physical_size: Vector2i) -> Rect2i:
	if physical_size.x <= 0 or physical_size.y <= 0:
		return Rect2i()
	var width: int = physical_size.x
	var height: int = width * 9 / 16
	if height > physical_size.y:
		height = physical_size.y
		width = height * 16 / 9
	return Rect2i((physical_size.x - width) / 2, (physical_size.y - height) / 2, width, height)

static func is_mobile_ui_enabled(platform_name: StringName, has_mobile_feature: bool) -> bool:
	return has_mobile_feature and (platform_name == &"Android" or platform_name == &"iOS")
