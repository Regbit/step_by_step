from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.graphics.objects.square import Rectangle


class Panel(GUIObject):

	_base_name = 'Panel'

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f
	):
		super(Panel, self).__init__(
			pos=pos,
			size=size,
			is_selectable=False,
			is_clickable=False,
			main_drawable=Rectangle(
				pos=pos,
				size=size,
				color=Vector3i(5, 5, 18),
				base_batch=self._batch_group
			)
		)
