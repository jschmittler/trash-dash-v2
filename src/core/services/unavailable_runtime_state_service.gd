class_name UnavailableRuntimeStateService
extends "res://src/core/services/runtime_state_service.gd"

const RuntimeStateServiceType := preload("res://src/core/services/runtime_state_service.gd")


func service_id() -> StringName:
	return RuntimeStateServiceType.SERVICE_ID
