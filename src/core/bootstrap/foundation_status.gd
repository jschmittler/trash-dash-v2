class_name FoundationStatus
extends RefCounted

const BuildIdentityType := preload("res://src/core/build/build_identity.gd")
const FoundationStatusType := preload("res://src/core/bootstrap/foundation_status.gd")

enum State {
	FOUNDATION_READY,
	FOUNDATION_ERROR,
}

var _state: State
var _identity: BuildIdentityType
var _title: String
var _subtitle: String
var _logical_size: Vector2i
var _renderer: String
var _content: String
var _messages: PackedStringArray


func _init(
	state_value: State,
	identity_value: BuildIdentityType,
	title_value: String,
	subtitle_value: String,
	logical_size_value: Vector2i,
	renderer_value: String,
	content_value: String,
	messages_value: PackedStringArray
) -> void:
	assert(identity_value != null, "Foundation status identity must not be null")
	_state = state_value
	_identity = identity_value
	_title = title_value
	_subtitle = subtitle_value
	_logical_size = logical_size_value
	_renderer = renderer_value
	_content = content_value
	_messages = messages_value.duplicate()


static func ready(identity: BuildIdentityType) -> FoundationStatusType:
	return FoundationStatusType.new(
		State.FOUNDATION_READY,
		identity,
		"Trash Dash 2.0",
		"macOS prototype foundation",
		Vector2i(960, 540),
		"Compatibility",
		"prototype content not loaded",
		PackedStringArray()
	)


static func error(identity: BuildIdentityType, messages: PackedStringArray) -> FoundationStatusType:
	return FoundationStatusType.new(
		State.FOUNDATION_ERROR,
		identity,
		"Trash Dash 2.0",
		"macOS prototype foundation",
		Vector2i(960, 540),
		"Compatibility",
		"prototype content not loaded",
		messages
	)


func state() -> State:
	return _state


func identity() -> BuildIdentityType:
	return _identity


func title() -> String:
	return _title


func subtitle() -> String:
	return _subtitle


func logical_size() -> Vector2i:
	return _logical_size


func renderer() -> String:
	return _renderer


func content() -> String:
	return _content


func messages() -> PackedStringArray:
	return _messages.duplicate()
