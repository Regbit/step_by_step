from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.graphics.label_extension import LabelExtension
from step_by_step.graphics.objects.square import Rectangle


class Label(GUIObject):

	_base_name = 'Label'

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		text: str,
		color: Vector3i = Vector3i(0, 0, 0),
		text_color: Vector3i = None,
		border_width: int = 0,
		border_color: Vector3i = None,
	):
		super(Label, self).__init__(
			pos=pos,
			size=size,
			is_selectable=False,
			is_clickable=False,
			background_drawable=Rectangle(
				pos=pos,
				size=size,
				color=border_color,
				base_batch=self._batch_group
			) if border_width else None,
			main_drawable=Rectangle(
				pos=pos,
				size=size - Vector2f(border_width * 2, border_width * 2) if border_width else Vector2f(0, 0),
				color=color,
				base_batch=self._batch_group
			),
			label=LabelExtension(
				pos=pos,
				size=size,
				text=text,
				font_size=round(size.y * 0.5),
				color=text_color if text_color else color / 3,
			)
		)
