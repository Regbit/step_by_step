from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.graphics.objects.settings import BatchGroup


class GUI(GUIObject):

	_base_name = 'GUI'
	_batch_group = BatchGroup.GUI_OBJECT_BACKGROUND

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f
	):
		super(GUI, self).__init__(
			pos=pos,
			size=size,
			is_selectable=False,
			is_clickable=False,
			is_visible=True
		)
