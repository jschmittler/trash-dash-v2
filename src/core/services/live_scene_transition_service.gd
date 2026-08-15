class_name LiveSceneTransitionService
extends "res://src/core/services/scene_transition_service.gd"

const SceneTransitionServiceType := preload("res://src/core/services/scene_transition_service.gd")

var _container: Node


func _init(container: Node) -> void:
	assert(container != null, "Live scene transition service requires a container node")
	_container = container


func service_id() -> StringName:
	return SceneTransitionServiceType.SERVICE_ID


func change_scene(scene_path: String) -> Error:
	if not ResourceLoader.exists(scene_path, "PackedScene"):
		return ERR_FILE_NOT_FOUND
	var packed: Resource = ResourceLoader.load(scene_path, "PackedScene")
	if packed == null or not packed is PackedScene:
		return ERR_CANT_ACQUIRE_RESOURCE
	var instance: Node = (packed as PackedScene).instantiate()
	if instance == null:
		return ERR_CANT_CREATE
	_clear_container()
	_container.add_child(instance)
	return OK


func current_scene() -> Node:
	return _container.get_child(0) if _container.get_child_count() > 0 else null


func _clear_container() -> void:
	for existing_child: Node in _container.get_children():
		_container.remove_child(existing_child)
		existing_child.queue_free()
