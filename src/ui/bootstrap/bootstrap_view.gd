class_name BootstrapView
extends MarginContainer

const FoundationStatusType := preload("res://src/core/bootstrap/foundation_status.gd")

@onready var _project_title: Label = $StatusColumn/ProjectTitle
@onready var _foundation_status: Label = $StatusColumn/FoundationStatus
@onready var _build_identity: Label = $StatusColumn/BuildIdentity
@onready var _runtime_policy: Label = $StatusColumn/RuntimePolicy
@onready var _content_status: Label = $StatusColumn/ContentStatus

func present(status: FoundationStatusType) -> void:
	_project_title.text = status.title()
	_foundation_status.text = "%s — %s" % [status.subtitle(), _state_text(status.state())]
	_build_identity.text = status.identity().text()
	_runtime_policy.text = "%d×%d / %s" % [
		status.logical_size().x,
		status.logical_size().y,
		status.renderer(),
	]
	_content_status.text = status.content()
	var messages := status.messages()
	if status.state() == FoundationStatusType.State.FOUNDATION_ERROR and not messages.is_empty():
		_content_status.text += "\n%s" % "\n".join(messages)

func _state_text(state: FoundationStatusType.State) -> String:
	return (
		"FOUNDATION_READY"
		if state == FoundationStatusType.State.FOUNDATION_READY
		else "FOUNDATION_ERROR"
	)
