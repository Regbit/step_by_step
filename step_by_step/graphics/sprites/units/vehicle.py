from __future__ import annotations

from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.sprites.sprite import Sprite
from step_by_step.graphics.objects.square import SelectionBorder, Diamond


class VehicleDefaultSprite(Sprite):

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		batch_group: BatchGroup,
		do_draw: bool,
	):
		super(VehicleDefaultSprite, self).__init__(
			pos=pos,
			size=size,
			batch_group=batch_group,
			text_batch_group=BatchGroup.DEFAULT,
			screen_object_stack=[
				Diamond(
					pos=pos,
					size=size,
					color=Vector3i(240, 50, 90),
					base_batch_group=batch_group
				)
			],
			label_stack=[],
			do_draw=do_draw
		)


class VehicleSelectedSprite(Sprite):

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		batch_group: BatchGroup,
		do_draw: bool,
	):
		super(VehicleSelectedSprite, self).__init__(
			pos=pos,
			size=size,
			batch_group=batch_group,
			text_batch_group=BatchGroup.DEFAULT,
			screen_object_stack=[
				Diamond(
					pos=pos,
					size=size,
					color=Vector3i(240, 50, 90),
					base_batch_group=batch_group
				),
				SelectionBorder(
					pos=pos,
					size=size + Vector2f(2, 2),
					base_batch_group=batch_group
				)
			],
			label_stack=[],
			do_draw=do_draw
		)
