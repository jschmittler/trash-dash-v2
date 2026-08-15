extends "res://tests/support/test_case.gd"

const LiveSceneTransitionServiceType := preload(
	"res://src/core/services/live_scene_transition_service.gd"
)
const SceneTransitionServiceType := preload("res://src/core/services/scene_transition_service.gd")
const BOOTSTRAP_SCENE_PATH := "res://scenes/bootstrap/bootstrap.tscn"


func test_service_id_matches_the_stable_contract() -> void:
	var container := Node.new()
	var service := LiveSceneTransitionServiceType.new(container)
	assert_equal(service.service_id(), SceneTransitionServiceType.SERVICE_ID, "service id")
	container.free()


func test_change_scene_instantiates_and_reports_current_scene() -> void:
	var tree := Engine.get_main_loop() as SceneTree
	var container := Node.new()
	tree.root.add_child(container)
	var service := LiveSceneTransitionServiceType.new(container)
	assert_equal(service.current_scene(), null, "no scene before first change")
	var status := service.change_scene(BOOTSTRAP_SCENE_PATH)
	assert_equal(status, OK, "change scene status")
	assert_equal(container.get_child_count(), 1, "container child count")
	assert_true(service.current_scene() != null, "current scene present")
	assert_equal(service.current_scene().name, &"Bootstrap", "current scene name")
	container.queue_free()
	await tree.process_frame


func test_change_scene_replaces_the_previous_scene() -> void:
	var tree := Engine.get_main_loop() as SceneTree
	var container := Node.new()
	tree.root.add_child(container)
	var service := LiveSceneTransitionServiceType.new(container)
	service.change_scene(BOOTSTRAP_SCENE_PATH)
	var first_instance := service.current_scene()
	service.change_scene(BOOTSTRAP_SCENE_PATH)
	var second_instance := service.current_scene()
	assert_true(first_instance != second_instance, "replaced with a fresh instance")
	assert_equal(container.get_child_count(), 1, "still exactly one active scene")
	container.queue_free()
	await tree.process_frame


func test_change_scene_rejects_missing_scene_paths_without_mutation() -> void:
	var tree := Engine.get_main_loop() as SceneTree
	var container := Node.new()
	tree.root.add_child(container)
	var service := LiveSceneTransitionServiceType.new(container)
	service.change_scene(BOOTSTRAP_SCENE_PATH)
	var status := service.change_scene("res://scenes/bootstrap/does-not-exist.tscn")
	assert_equal(status, ERR_FILE_NOT_FOUND, "missing scene status")
	assert_equal(container.get_child_count(), 1, "container untouched on failure")
	container.queue_free()
	await tree.process_frame


func test_change_scene_rejects_non_scene_resource_paths() -> void:
	var tree := Engine.get_main_loop() as SceneTree
	var container := Node.new()
	tree.root.add_child(container)
	var service := LiveSceneTransitionServiceType.new(container)
	var status := service.change_scene("res://src/core/services/live_scene_transition_service.gd")
	assert_equal(status, ERR_CANT_ACQUIRE_RESOURCE, "non-scene resource status")
	assert_equal(container.get_child_count(), 0, "container remains empty")
	container.queue_free()
	await tree.process_frame
