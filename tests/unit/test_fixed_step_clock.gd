extends "res://tests/support/test_case.gd"

const FixedStepClockType := preload("res://src/core/time/fixed_step_clock.gd")


func test_tick_seconds_matches_tick_rate() -> void:
	var clock := FixedStepClockType.new(60)
	assert_equal(clock.tick_hz(), 60, "tick rate")
	assert_true(is_equal_approx(clock.tick_seconds(), 1.0 / 60.0), "tick seconds")


func test_advance_consumes_whole_ticks_and_keeps_remainder() -> void:
	var clock := FixedStepClockType.new(60)
	var consumed := clock.advance(1.0 / 60.0)
	assert_equal(consumed, 1, "single tick consumed")
	assert_equal(clock.elapsed_ticks(), 1, "elapsed ticks")
	assert_true(is_equal_approx(clock.accumulated_seconds(), 0.0), "no remainder")


func test_advance_accumulates_partial_seconds_across_calls() -> void:
	var clock := FixedStepClockType.new(60)
	var step := clock.tick_seconds()
	assert_equal(clock.advance(step * 0.5), 0, "half tick consumes nothing")
	assert_equal(clock.advance(step * 0.5), 1, "remaining half completes one tick")
	assert_equal(clock.elapsed_ticks(), 1, "elapsed ticks after two partial advances")


func test_advance_consumes_multiple_ticks_in_one_call() -> void:
	var clock := FixedStepClockType.new(60)
	var consumed := clock.advance(clock.tick_seconds() * 3.5)
	assert_equal(consumed, 3, "ticks consumed in one call")
	assert_equal(clock.elapsed_ticks(), 3, "elapsed ticks")
	assert_true(
		is_equal_approx(clock.accumulated_seconds(), clock.tick_seconds() * 0.5),
		"remainder retained"
	)


func test_reset_clears_elapsed_ticks_and_remainder() -> void:
	var clock := FixedStepClockType.new(60)
	clock.advance(clock.tick_seconds() * 2.5)
	clock.reset()
	assert_equal(clock.elapsed_ticks(), 0, "elapsed ticks reset")
	assert_true(is_equal_approx(clock.accumulated_seconds(), 0.0), "remainder reset")


func test_supports_alternate_tick_rates() -> void:
	var clock := FixedStepClockType.new(30)
	assert_true(is_equal_approx(clock.tick_seconds(), 1.0 / 30.0), "30hz tick seconds")
	assert_equal(clock.advance(1.0 / 30.0), 1, "30hz single tick")
