from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.game.objects.gui.settings import LayoutStyle


def test__gui_object__init__ok_1():
	o = GUIObject(
		pos=Vector2f(1, 1),
		size=Vector2f(1, 1),
	)

	assert o is not None
	assert o._layout_style == LayoutStyle.ABSOLUTE
	assert o.layout_style == LayoutStyle.ABSOLUTE
