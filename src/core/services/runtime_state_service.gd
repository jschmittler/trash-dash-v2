class_name RuntimeStateService
extends RefCounted

const ServiceResultType := preload("res://src/core/services/service_result.gd")
const SERVICE_ID: StringName = &"runtime_state"


func service_id() -> StringName:
	return StringName()


func read_state(_key: StringName) -> ServiceResultType:
	return ServiceResultType.unavailable(service_id())


func write_state(_key: StringName, _value: Variant) -> Error:
	return ERR_UNAVAILABLE
