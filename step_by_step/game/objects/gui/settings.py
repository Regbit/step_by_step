from enum import Enum

from step_by_step.common.vector import Vector3i

RIGHT_MENU_BAR_WIDTH = 400


class GUIStyle(Enum):

	def __new__(cls, *args, **kwds):
		value = len(cls.__members__) + 1
		obj = object.__new__(cls)
		obj._value_ = value
		return obj

	def __init__(
		self,
		panel_color,
		label_color,
		label_text_color,
		label_border_color,
		label_border_width,
		label_background_color,
		button_color,
	):
		self.panel_color: Vector3i = panel_color
		self.label_color: Vector3i = label_color
		self.label_text_color: Vector3i = label_text_color
		self.label_border_color: Vector3i = label_border_color
		self.label_border_width: int = label_border_width
		self.label_background_color: Vector3i = label_background_color
		self.button_color: Vector3i = button_color

	BLUE = (
		Vector3i(5, 5, 18),
		Vector3i(5, 5, 18),
		Vector3i(120, 140, 220),
		Vector3i(120, 140, 220),
		1,
		None,
		Vector3i(60, 70, 180),
	)
