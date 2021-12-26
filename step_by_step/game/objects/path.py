from step_by_step.game.objects.units.unit import Unit
from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.graphics.objects.line import Line
from step_by_step.graphics.objects.square import SelectionBorder
from step_by_step.graphics.objects.triangle import ReverseTriangle
from step_by_step.graphics.objects.settings import BatchGroup


class Waypoint(Unit):

	_base_name = "Waypoint"
	_batch_group = BatchGroup.PATH_OBJECT

	def __init__(
		self,
		pos: Vector2f,
	):
		super(Waypoint, self).__init__(
			pos=pos,
			size=Vector2f(25, 25),
			is_selectable=False,
			is_movable=False,
			movement_velocity=0,
			rotation_velocity=0,
			background_drawable=ReverseTriangle(
				pos=pos,
				shift=Vector2f(0, 16),
				size=Vector2f(28, 28),
				color=Vector3i(150, 240, 190),
				base_batch_group=self._batch_group
			),
			main_drawable=ReverseTriangle(
				pos=pos,
				shift=Vector2f(0, 16),
				size=Vector2f(25, 25),
				color=Vector3i(10, 60, 40),
				base_batch_group=self._batch_group
			),
			foreground_drawable=SelectionBorder(
				pos=pos,
				shift=Vector2f(0, 13),
				size=Vector2f(28, 28),
				base_batch_group=self._batch_group
			)
		)


class Trajectory(Unit):

	_base_name = "Trajectory"
	_batch_group = BatchGroup.PATH_OBJECT

	def __init__(
		self,
		vertex_1: Vector2f,
		vertex_2: Vector2f,
	):
		super(Trajectory, self).__init__(
			pos=(vertex_1 + vertex_2) / 2,
			size=vertex_2-vertex_1 + Vector2f(1, 1),
			is_selectable=False,
			is_movable=False,
			movement_velocity=0,
			rotation_velocity=0,
			main_drawable=Line(
				vertex_1=vertex_1,
				vertex_2=vertex_2,
				base_batch_group=self._batch_group
			)
		)
