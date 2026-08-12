class_name AudioService
extends RefCounted

const SERVICE_ID: StringName = &"audio"

func service_id() -> StringName:
	return StringName()

func play_music(_track_id: StringName) -> Error:
	return ERR_UNAVAILABLE

func stop_music() -> Error:
	return ERR_UNAVAILABLE

func set_muted(_muted: bool) -> Error:
	return ERR_UNAVAILABLE
