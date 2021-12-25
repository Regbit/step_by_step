from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.game.objects.settings import SpriteType
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.objects.sprites.gui.panel import PanelDefaultSprite


class Panel(GUIObject):

	_base_name = 'Panel'

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		color: Vector3i
	):
		super(Panel, self).__init__(
			pos=pos,
			size=size,
			sprites={
				SpriteType.DEFAULT: PanelDefaultSprite(
					pos=pos,
					size=size,
					batch_group=BatchGroup.GUI_OBJECT_BACKGROUND,
					do_draw=True,
					color=color,
				)
			}
		)
