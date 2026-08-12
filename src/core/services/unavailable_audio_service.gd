class_name UnavailableAudioService
extends "res://src/core/services/audio_service.gd"

const AudioServiceType := preload("res://src/core/services/audio_service.gd")

func service_id() -> StringName:
	return AudioServiceType.SERVICE_ID
