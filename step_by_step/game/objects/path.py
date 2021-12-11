from step_by_step.game.objects.world_object import WorldObject
from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.graphics.line import Line
from step_by_step.graphics.square import SelectionBorder
from step_by_step.graphics.triangle import ReverseTriangle
from step_by_step.graphics.settings import BatchGroup


class Waypoint(WorldObject):

	_base_name = "Waypoint"
	_batch_group = BatchGroup.PATH_OBJECT

	def __init__(
		self,
		world_pos: Vector2f,
	):
		super(Waypoint, self).__init__(
			world_pos=world_pos,
			size=Vector2f(25, 25),
			is_selectable=False,
			is_movable=False,
			movement_velocity=0,
			rotation_velocity=0,
			background_drawable=ReverseTriangle(
				pos=world_pos,
				shift=Vector2f(0, 16),
				size=Vector2f(28, 28),
				color=Vector3i(150, 240, 190),
				base_batch=self._batch_group
			),
			main_drawable=ReverseTriangle(
				pos=world_pos,
				shift=Vector2f(0, 16),
				size=Vector2f(25, 25),
				color=Vector3i(10, 60, 40),
				base_batch=self._batch_group
			),
			foreground_drawable=SelectionBorder(
				pos=world_pos,
				shift=Vector2f(0, 13),
				size=Vector2f(28, 28),
				base_batch=self._batch_group
			)
		)


class Trajectory(WorldObject):

	_base_name = "Trajectory"
	_batch_group = BatchGroup.PATH_OBJECT

	def __init__(
		self,
		vertex_1: Vector2f,
		vertex_2: Vector2f,
	):
		super(Trajectory, self).__init__(
			world_pos=(vertex_1 + vertex_2) / 2,
			size=vertex_2-vertex_1 + Vector2f(1, 1),
			is_selectable=False,
			is_movable=False,
			movement_velocity=0,
			rotation_velocity=0,
			main_drawable=Line(
				vertex_1=vertex_1,
				vertex_2=vertex_2,
				base_batch=self._batch_group
			)
		)
