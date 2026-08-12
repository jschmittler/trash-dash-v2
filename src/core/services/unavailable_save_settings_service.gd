class_name UnavailableSaveSettingsService
extends "res://src/core/services/save_settings_service.gd"

const SaveSettingsServiceType := preload("res://src/core/services/save_settings_service.gd")

func service_id() -> StringName:
	return SaveSettingsServiceType.SERVICE_ID
