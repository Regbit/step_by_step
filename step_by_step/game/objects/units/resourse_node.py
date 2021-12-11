from step_by_step.game.objects.units.world_object import WorldObject
from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.graphics.objects.square import Square, SelectionBorder
from step_by_step.graphics.objects.settings import BatchGroup


class ResourceNode(WorldObject):

	_base_name = 'Resource Node'
	_batch_group = BatchGroup.WORLD_STATIC_OBJECT

	def __init__(
		self,
		pos: Vector2f,
	):
		super(ResourceNode, self).__init__(
			pos=pos,
			size=Vector2f(50, 50),
			is_selectable=True,
			is_movable=False,
			movement_velocity=0,
			rotation_velocity=0,
			main_drawable=Square(
				pos=pos,
				size=Vector2f(50, 50),
				color=Vector3i(100, 80, 50),
				base_batch=self._batch_group
			),
			foreground_drawable=SelectionBorder(
				pos=pos,
				size=Vector2f(50, 50) + Vector2f(4, 4),
				base_batch=self._batch_group
			)
		)
