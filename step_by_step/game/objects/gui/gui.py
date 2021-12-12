from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.gui import Button, Panel
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

		p = Panel(pos=Vector2f(self.size.x / 2 - 200, 0), size=Vector2f(400, self.size.y))
		self.add_child(p)

		p.add_child(Button(pos=Vector2f(0, 500), size=Vector2f(350, 50)))
		p.add_child(Button(pos=Vector2f(0, 440), size=Vector2f(350, 50)))
		p.add_child(Button(pos=Vector2f(0, 380), size=Vector2f(350, 50)))
