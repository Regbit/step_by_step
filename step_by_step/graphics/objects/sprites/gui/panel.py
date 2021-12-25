from __future__ import annotations

from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.objects.sprites.sprite import Sprite
from step_by_step.graphics.objects.square import Rectangle


class PanelDefaultSprite(Sprite):

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		batch_group: BatchGroup,
		do_draw: bool,
		color: Vector3i,
	):
		super(PanelDefaultSprite, self).__init__(
			pos=pos,
			size=size,
			batch_group=batch_group,
			text_batch_group=BatchGroup.GUI_TEXT_OBJECT,
			screen_object_stack=[
				Rectangle(
					pos=pos,
					size=size,
					color=color,
					base_batch=batch_group
				)
			],
			label_stack=[],
			do_draw=do_draw
		)
