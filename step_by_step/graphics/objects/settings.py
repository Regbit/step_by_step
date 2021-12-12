from enum import Enum

from pyglet.gl import (
	GL_QUADS,
	GL_LINE_LOOP,
	GL_TRIANGLES
)


class BatchGroup(Enum):
	GUI_POPUP_TEXT_OBJECT = 'GUI_POPUP_TEXT_OBJECT'
	GUI_POPUP_OBJECT = 'GUI_POPUP_OBJECT'
	GUI_TEXT_OBJECT = 'GUI_TEXT_OBJECT'
	GUI_OBJECT = 'GUI_OBJECT'
	SELECTED_OBJECT = 'SELECTED_OBJECT'
	WORLD_DYNAMIC_OBJECT = 'WORLD_DYNAMIC_OBJECT'
	WORLD_STATIC_OBJECT = 'WORLD_STATIC_OBJECT'
	PATH_OBJECT = 'PATH_OBJECT'
	DEFAULT = 'DEFAULT'
	WORLD_MAP = 'WORLD_MAP'


class DrawMode(Enum):
	QUADS = GL_QUADS
	TRIANGLE = GL_TRIANGLES
	LINES = GL_LINE_LOOP
