class_name FixedStepClock
extends RefCounted

var _tick_hz: int
var _accumulated_seconds: float = 0.0
var _elapsed_ticks: int = 0


func _init(tick_hz: int) -> void:
	assert(tick_hz > 0, "Fixed step clock requires a positive tick rate")
	_tick_hz = tick_hz


func tick_hz() -> int:
	return _tick_hz


func tick_seconds() -> float:
	return 1.0 / float(_tick_hz)


func elapsed_ticks() -> int:
	return _elapsed_ticks


func accumulated_seconds() -> float:
	return _accumulated_seconds


func advance(delta_seconds: float) -> int:
	assert(delta_seconds >= 0.0, "Fixed step clock cannot advance by a negative duration")
	_accumulated_seconds += delta_seconds
	var step := tick_seconds()
	var ticks_this_advance := 0
	while _accumulated_seconds >= step:
		_accumulated_seconds -= step
		_elapsed_ticks += 1
		ticks_this_advance += 1
	return ticks_this_advance


func reset() -> void:
	_accumulated_seconds = 0.0
	_elapsed_ticks = 0
