from step_by_step.game.objects.units.world_object import WorldObject
from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.graphics.objects.square import Diamond, SelectionBorder
from step_by_step.graphics.objects.settings import BatchGroup


class Vehicle(WorldObject):

	_base_name = 'Vehicle'
	_batch_group = BatchGroup.WORLD_DYNAMIC_OBJECT

	def __init__(
		self,
		pos: Vector2f,
	):
		super(Vehicle, self).__init__(
			pos=pos,
			size=Vector2f(25, 25),
			is_selectable=True,
			is_movable=True,
			movement_velocity=2,
			rotation_velocity=0.03,
			main_drawable=Diamond(
				pos=pos,
				size=Vector2f(25, 25),
				color=Vector3i(240, 50, 90),
				base_batch=self._batch_group
			),
			foreground_drawable=SelectionBorder(
				pos=pos,
				size=Vector2f(25, 25) + Vector2f(2, 2),
				base_batch=self._batch_group
			)
		)
