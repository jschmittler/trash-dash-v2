class_name ServiceRegistry
extends RefCounted

const AudioServiceType := preload("res://src/core/services/audio_service.gd")
const RuntimeStateServiceType := preload("res://src/core/services/runtime_state_service.gd")
const SaveSettingsServiceType := preload("res://src/core/services/save_settings_service.gd")
const SceneTransitionServiceType := preload("res://src/core/services/scene_transition_service.gd")
const ServiceRegistryType := preload("res://src/core/services/service_registry.gd")
const UnavailableAudioServiceType := preload("res://src/core/services/unavailable_audio_service.gd")
const UnavailableRuntimeStateServiceType := preload(
	"res://src/core/services/unavailable_runtime_state_service.gd"
)
const UnavailableSaveSettingsServiceType := preload(
	"res://src/core/services/unavailable_save_settings_service.gd"
)
const UnavailableSceneTransitionServiceType := preload(
	"res://src/core/services/unavailable_scene_transition_service.gd"
)

var _save_settings: SaveSettingsServiceType
var _audio: AudioServiceType
var _scenes: SceneTransitionServiceType
var _runtime_state: RuntimeStateServiceType


func _init(
	save_settings_service: SaveSettingsServiceType,
	audio_service: AudioServiceType,
	scene_transition_service: SceneTransitionServiceType,
	runtime_state_service: RuntimeStateServiceType
) -> void:
	_save_settings = save_settings_service
	_audio = audio_service
	_scenes = scene_transition_service
	_runtime_state = runtime_state_service


static func unavailable() -> ServiceRegistryType:
	return ServiceRegistryType.new(
		UnavailableSaveSettingsServiceType.new(),
		UnavailableAudioServiceType.new(),
		UnavailableSceneTransitionServiceType.new(),
		UnavailableRuntimeStateServiceType.new()
	)


func save_settings() -> SaveSettingsServiceType:
	return _save_settings


func audio() -> AudioServiceType:
	return _audio


func scenes() -> SceneTransitionServiceType:
	return _scenes


func runtime_state() -> RuntimeStateServiceType:
	return _runtime_state


func missing_service_ids() -> Array[StringName]:
	var missing_ids: Array[StringName] = []
	if _save_settings == null:
		missing_ids.append(SaveSettingsServiceType.SERVICE_ID)
	if _audio == null:
		missing_ids.append(AudioServiceType.SERVICE_ID)
	if _scenes == null:
		missing_ids.append(SceneTransitionServiceType.SERVICE_ID)
	if _runtime_state == null:
		missing_ids.append(RuntimeStateServiceType.SERVICE_ID)
	return missing_ids


func is_complete() -> bool:
	return missing_service_ids().is_empty()
