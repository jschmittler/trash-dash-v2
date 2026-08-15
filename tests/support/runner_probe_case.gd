extends "res://tests/support/test_case.gd"


func test_runner_probe() -> void:
	if OS.get_cmdline_args().has("--probe-fail"):
		fail("intentional runner probe failure")
