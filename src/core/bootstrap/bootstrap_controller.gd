class_name BootstrapController
extends Control

const BuildIdentityType := preload("res://src/core/build/build_identity.gd")
const FoundationStatusType := preload("res://src/core/bootstrap/foundation_status.gd")
const InputMapContractType := preload("res://src/core/input/input_map_contract.gd")
const ProjectSettingsAdapterType := preload("res://src/core/bootstrap/project_settings_adapter.gd")
const ServiceRegistryType := preload("res://src/core/services/service_registry.gd")
const StartupValidatorType := preload("res://src/core/bootstrap/startup_validator.gd")
const BootstrapViewType := preload("res://src/ui/bootstrap/bootstrap_view.gd")

@onready var _view: BootstrapViewType = $SafeMargin

var _configured_registry: ServiceRegistryType
var _configured_settings: ProjectSettingsAdapterType
var _configured_identity: BuildIdentityType
var _status: FoundationStatusType


func configure(
	registry: ServiceRegistryType, settings: ProjectSettingsAdapterType, identity: BuildIdentityType
) -> void:
	assert(not is_inside_tree(), "Bootstrap dependencies must be configured before tree entry")
	_configured_registry = registry
	_configured_settings = settings
	_configured_identity = identity


func _ready() -> void:
	var registry := (
		_configured_registry if _configured_registry != null else ServiceRegistryType.unavailable()
	)
	var settings := (
		_configured_settings if _configured_settings != null else ProjectSettingsAdapterType.new()
	)
	var identity := (
		_configured_identity if _configured_identity != null else BuildIdentityType.development()
	)
	var errors := StartupValidatorType.validate(
		settings, InputMapContractType.validate_current(), registry
	)
	_status = (
		FoundationStatusType.ready(identity)
		if errors.is_empty()
		else FoundationStatusType.error(identity, errors)
	)
	_view.present(_status)


func foundation_state() -> FoundationStatusType.State:
	return _status.state()
