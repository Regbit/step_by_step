from __future__ import annotations

from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.sprites.sprite import Sprite
from step_by_step.graphics.objects.square import Square, SelectionBorder


class BuildingDefaultSprite(Sprite):

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		batch_group: BatchGroup,
		do_draw: bool,
	):
		super(BuildingDefaultSprite, self).__init__(
			pos=pos,
			size=size,
			batch_group=batch_group,
			text_batch_group=BatchGroup.DEFAULT,
			screen_object_stack=[
				Square(
					pos=pos,
					size=size,
					color=Vector3i(240, 200, 200),
					base_batch_group=batch_group
				)
			],
			label_stack=[],
			do_draw=do_draw
		)


class BuildingSelectedSprite(Sprite):

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		batch_group: BatchGroup,
		do_draw: bool,
	):
		super(BuildingSelectedSprite, self).__init__(
			pos=pos,
			size=size,
			batch_group=batch_group,
			text_batch_group=BatchGroup.DEFAULT,
			screen_object_stack=[
				Square(
					pos=pos,
					size=size,
					color=Vector3i(240, 200, 200),
					base_batch_group=batch_group
				),
				SelectionBorder(
					pos=pos,
					size=size + Vector2f(4, 4),
					base_batch_group=batch_group
				)
			],
			label_stack=[],
			do_draw=do_draw
		)
