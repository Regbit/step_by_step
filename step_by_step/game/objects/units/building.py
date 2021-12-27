from step_by_step.game.objects.settings import SpriteType
from step_by_step.game.objects.units.unit import Unit
from step_by_step.common.vector import Vector2f
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.sprites.units.building import (
	BuildingDefaultSprite,
	BuildingSelectedSprite,
)


class Building(Unit):

	_base_name = 'Building'

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f = Vector2f(50, 50)
	):
		super(Building, self).__init__(
			pos=pos,
			size=size,
			is_movable=False,
			movement_velocity=0,
			rotation_velocity=0,
			sprites={
				SpriteType.DEFAULT: BuildingDefaultSprite(
					pos=pos,
					size=size,
					batch_group=BatchGroup.WORLD_STATIC_OBJECT,
					do_draw=True
				),
				SpriteType.SELECTED: BuildingSelectedSprite(
					pos=pos,
					size=size,
					batch_group=BatchGroup.SELECTED_OBJECT,
					do_draw=False
				)
			}
		)
