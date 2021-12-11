from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.objects.square import Square


class Label(GUIObject):

	_base_name = 'Label'
	_batch_group = BatchGroup.GUI_OBJECT

	def __init__(
		self,
		pos: Vector2f,
	):
		super(Label, self).__init__(
			pos=pos,
			size=Vector2f(25, 25),
			is_selectable=False,
			is_clickable=True,
			main_drawable=Square(
				pos=pos,
				size=Vector2f(25, 25),
				color=Vector3i(150, 50, 90),
				base_batch=self._batch_group
			)
		)
