class_name SceneTransitionService
extends RefCounted

const SERVICE_ID: StringName = &"scene_transition"

func service_id() -> StringName:
	return StringName()

func change_scene(_scene_path: String) -> Error:
	return ERR_UNAVAILABLE
