from step_by_step.game.objects.settings import SpriteType
from step_by_step.game.objects.units.unit import Unit
from step_by_step.common.vector import Vector2f
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.objects.sprites.units.vehicle import (
	VehicleDefaultSprite,
	VehicleSelectedSprite,
)


class Vehicle(Unit):

	_base_name = 'Vehicle'

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f = Vector2f(25, 25),
	):
		super(Vehicle, self).__init__(
			pos=pos,
			size=Vector2f(25, 25),
			is_movable=True,
			movement_velocity=2,
			rotation_velocity=0.03,
			sprites={
				SpriteType.DEFAULT: VehicleDefaultSprite(
					pos=pos,
					size=size,
					batch_group=BatchGroup.WORLD_DYNAMIC_OBJECT,
					do_draw=True
				),
				SpriteType.SELECTED: VehicleSelectedSprite(
					pos=pos,
					size=size,
					batch_group=BatchGroup.SELECTED_OBJECT,
					do_draw=False
				)
			}
		)
