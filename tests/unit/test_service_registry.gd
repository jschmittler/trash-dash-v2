extends "res://tests/support/test_case.gd"

const ServiceRegistryType := preload("res://src/core/services/service_registry.gd")
const ServiceResultType := preload("res://src/core/services/service_result.gd")


func test_unavailable_registry_is_complete() -> void:
	var registry := ServiceRegistryType.unavailable()
	assert_true(registry.is_complete(), "registry complete")
	assert_equal(registry.missing_service_ids(), [], "no missing IDs")


func test_unavailable_services_have_stable_ids() -> void:
	var registry := ServiceRegistryType.unavailable()
	assert_equal(registry.save_settings().service_id(), &"save_settings", "save settings ID")
	assert_equal(registry.audio().service_id(), &"audio", "audio ID")
	assert_equal(registry.scenes().service_id(), &"scene_transition", "scene transition ID")
	assert_equal(registry.runtime_state().service_id(), &"runtime_state", "runtime state ID")


func test_unavailable_services_fail_without_state_change() -> void:
	var registry := ServiceRegistryType.unavailable()
	var tree := Engine.get_main_loop() as SceneTree
	var root_child_count := tree.root.get_child_count()
	var audio_bus_count := AudioServer.get_bus_count()
	var settings_exists := ResourceLoader.exists("user://settings.json")
	for _index: int in 2:
		assert_equal(registry.save_settings().load_settings().error(), ERR_UNAVAILABLE, "load")
		assert_equal(
			registry.save_settings().save_settings({"muted": true}), ERR_UNAVAILABLE, "save"
		)
		assert_equal(registry.audio().play_music(&"foundation"), ERR_UNAVAILABLE, "play")
		assert_equal(registry.audio().stop_music(), ERR_UNAVAILABLE, "stop")
		assert_equal(registry.audio().set_muted(true), ERR_UNAVAILABLE, "mute")
		assert_equal(registry.scenes().change_scene("res://never.tscn"), ERR_UNAVAILABLE, "scene")
		assert_equal(
			registry.runtime_state().write_state(&"phase", "changed"), ERR_UNAVAILABLE, "state"
		)
		assert_equal(registry.runtime_state().read_state(&"phase").error(), ERR_UNAVAILABLE, "read")
		assert_equal(registry.runtime_state().read_state(&"phase").value(), null, "no value")
	assert_equal(tree.root.get_child_count(), root_child_count, "root child count unchanged")
	assert_equal(AudioServer.get_bus_count(), audio_bus_count, "audio bus count unchanged")
	assert_equal(
		ResourceLoader.exists("user://settings.json"), settings_exists, "settings file unchanged"
	)


func test_unavailable_results_are_repeatedly_deterministic() -> void:
	var registry := ServiceRegistryType.unavailable()
	var first_result := registry.save_settings().load_settings()
	var second_result := registry.save_settings().load_settings()
	assert_equal(first_result.error(), ERR_UNAVAILABLE, "first load error")
	assert_equal(second_result.error(), ERR_UNAVAILABLE, "second load error")
	assert_equal(first_result.value(), null, "first load value")
	assert_equal(second_result.value(), null, "second load value")
	assert_equal(registry.missing_service_ids(), [], "missing IDs stay empty")


func test_registry_reports_only_null_service_id() -> void:
	var complete_registry := ServiceRegistryType.unavailable()
	var registry := ServiceRegistryType.new(
		complete_registry.save_settings(),
		null,
		complete_registry.scenes(),
		complete_registry.runtime_state()
	)
	assert_equal(registry.missing_service_ids(), [&"audio"], "audio is the only missing service")
	assert_true(not registry.is_complete(), "registry incomplete")


func test_service_result_copies_collection_values() -> void:
	var source := {"nested": ["original"]}
	var result := ServiceResultType.new(OK, source)
	source["nested"].append("input mutation")
	var returned_value: Variant = result.value()
	returned_value["nested"].append("output mutation")
	assert_equal(result.error(), OK, "result error")
	assert_equal(result.value(), {"nested": ["original"]}, "result value remains copied")
