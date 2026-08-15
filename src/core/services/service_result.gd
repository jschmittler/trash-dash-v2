class_name ServiceResult
extends RefCounted

const ServiceResultType := preload("res://src/core/services/service_result.gd")

var _error: Error
var _value: Variant


func _init(error_code: Error, stored_value: Variant) -> void:
	_error = error_code
	_value = (
		stored_value.duplicate(true)
		if stored_value is Dictionary or stored_value is Array
		else stored_value
	)


static func unavailable(_service_id: StringName) -> ServiceResultType:
	return ServiceResultType.new(ERR_UNAVAILABLE, null)


func error() -> Error:
	return _error


func value() -> Variant:
	if _value is Dictionary or _value is Array:
		return _value.duplicate(true)
	return _value
