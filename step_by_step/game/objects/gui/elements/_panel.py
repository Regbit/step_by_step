from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.objects.square import Rectangle


class Panel(GUIObject):

	_base_name = 'Panel'
	_batch_group = BatchGroup.GUI_OBJECT_BACKGROUND

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		color: Vector3i
	):
		super(Panel, self).__init__(
			pos=pos,
			size=size,
			is_selectable=False,
			is_clickable=False,
			main_drawable=Rectangle(
				pos=pos,
				size=size,
				color=color,
				base_batch=self._batch_group
			)
		)
