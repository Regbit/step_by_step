from step_by_step.game.objects.world_object import WorldObject
from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.graphics.square import Square, SelectionBorder
from step_by_step.graphics.settings import BatchGroup


class Building(WorldObject):

	_base_name = 'Building'
	_batch_group = BatchGroup.WORLD_STATIC_OBJECT

	def __init__(
		self,
		world_pos: Vector2f,
	):
		super(Building, self).__init__(
			world_pos=world_pos,
			size=Vector2f(50, 50),
			is_selectable=True,
			is_movable=False,
			movement_velocity=0,
			rotation_velocity=0,
			main_drawable=Square(
				pos=world_pos,
				size=Vector2f(50, 50),
				color=Vector3i(240, 200, 200),
				base_batch=self._batch_group
			),
			foreground_drawable=SelectionBorder(
				pos=world_pos,
				size=Vector2f(50, 50) + Vector2f(4, 4),
				base_batch=self._batch_group
			)
		)
