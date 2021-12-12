from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.graphics.label import Label
from step_by_step.graphics.objects.square import Rectangle


class Button(GUIObject):

	_base_name = 'Button'

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f
	):
		super(Button, self).__init__(
			pos=pos,
			size=size,
			is_selectable=False,
			is_clickable=True,
			main_drawable=Rectangle(
				pos=pos,
				size=size,
				color=Vector3i(60, 70, 180),
				base_batch=self._batch_group
			),
			label=Label(
				pos=pos,
				size=size,
				text='Button',
				font_size=20,
				color=Vector3i(30, 20, 90),
			)
		)
