extends "res://tests/support/test_case.gd"

const TestCaseScript: Script = preload("res://tests/support/test_case.gd")


func test_failed_assertions_retain_order() -> void:
	var probe: TestCase = TestCaseScript.new()
	probe.assert_true(false, "first failure")
	probe.assert_equal(1, 2, "second failure")
	assert_equal(probe.failure_count(), 2, "failure count")
	assert_equal(
		probe.failure_messages(),
		PackedStringArray(["first failure", "second failure: expected 2, got 1"]),
		"failure order"
	)
