from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.objects.square import Rectangle


class Button(GUIObject):

	_base_name = 'Button'
	_batch_group = BatchGroup.GUI_OBJECT

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
				color=Vector3i(150, 50, 90),
				base_batch=self._batch_group
			)
		)
