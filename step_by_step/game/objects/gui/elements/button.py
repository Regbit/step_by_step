from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.graphics.label_extension import LabelExtension
from step_by_step.graphics.objects.square import Rectangle


class Button(GUIObject):

	_base_name = 'Button'

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		color: Vector3i,
		text: str
	):
		super(Button, self).__init__(
			pos=pos,
			size=size,
			is_selectable=False,
			is_clickable=True,
			main_drawable=Rectangle(
				pos=pos,
				size=size,
				color=color,
				base_batch=self._batch_group
			),
			label=LabelExtension(
				pos=pos,
				size=size,
				text=text,
				font_size=round(size.y * 0.5),
				color=color / 3,
			)
		)
