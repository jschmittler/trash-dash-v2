class_name SaveSettingsService
extends RefCounted

const ServiceResultType := preload("res://src/core/services/service_result.gd")
const SERVICE_ID: StringName = &"save_settings"

func service_id() -> StringName:
	return StringName()

func load_settings() -> ServiceResultType:
	return ServiceResultType.unavailable(service_id())

func save_settings(_settings: Dictionary) -> Error:
	return ERR_UNAVAILABLE
