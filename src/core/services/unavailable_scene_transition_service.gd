class_name UnavailableSceneTransitionService
extends "res://src/core/services/scene_transition_service.gd"

const SceneTransitionServiceType := preload("res://src/core/services/scene_transition_service.gd")


func service_id() -> StringName:
	return SceneTransitionServiceType.SERVICE_ID
