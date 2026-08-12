class_name BuildIdentity
extends RefCounted

const BuildIdentityType := preload("res://src/core/build/build_identity.gd")

var _version: String
var _revision: String

func _init(version_value: String, revision_value: String) -> void:
	assert(not version_value.is_empty(), "Build identity version must not be empty")
	assert(not revision_value.is_empty(), "Build identity revision must not be empty")
	_version = version_value
	_revision = revision_value

static func development() -> BuildIdentityType:
	return BuildIdentityType.new("0.1.0-foundation", "development")

func version() -> String:
	return _version

func revision() -> String:
	return _revision

func text() -> String:
	return "%s (%s)" % [_version, _revision]
