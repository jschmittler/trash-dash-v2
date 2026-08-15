class_name RenderObjectRef
extends Resource

## Schema for "every object has one owning layer" (RENDERING_LAYERS.md).
## Content data references layers symbolically by name; see
## RenderObjectRefValidator and RenderingLayer for resolution/validation.

const CURRENT_SCHEMA_VERSION := 1

@export var schema_version: int = CURRENT_SCHEMA_VERSION
@export var object_id: StringName = &""
@export var layer_name: StringName = &""
