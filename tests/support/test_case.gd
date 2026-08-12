class_name TestCase
extends RefCounted

var _failure_messages: PackedStringArray = PackedStringArray()

func assert_true(value: bool, message: String) -> void:
	if not value:
		fail(message)

func assert_equal(actual: Variant, expected: Variant, message: String) -> void:
	if actual != expected:
		fail("%s: expected %s, got %s" % [message, str(expected), str(actual)])

func fail(message: String) -> void:
	_failure_messages.append(message)

func failure_count() -> int:
	return _failure_messages.size()

func failure_messages() -> PackedStringArray:
	return _failure_messages
