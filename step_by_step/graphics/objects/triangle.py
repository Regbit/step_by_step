from typing import List

from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.graphics.objects._helpers import rotate_triangle_coordinates
from step_by_step.graphics.objects.screen_object import ScreenObject
from step_by_step.graphics.objects.settings import BatchGroup, DrawMode


class ReverseTriangle(ScreenObject):

	def __init__(
			self,
			pos: Vector2f,
			size: Vector2f,
			color: Vector3i,
			base_batch_group: BatchGroup,
			shift: Vector2f = Vector2f(0, 0),
	):
		super(ReverseTriangle, self).__init__(
			vertex_count=3,
			pos=pos,
			shift=shift,
			size=size,
			color=color,
			mode=DrawMode.TRIANGLE,
			base_batch_group=base_batch_group,
			do_draw=True,
		)

	def __copy__(self):
		return ReverseTriangle(
			self.pos,
			self.size,
			self.color,
			self._base_batch_group,
			self.shift
		)

	def __deepcopy__(self):
		return ReverseTriangle(
			self.pos.copy,
			self.size.copy,
			self.color.copy,
			self._base_batch_group,
			self.shift.copy
		)

	@property
	def vertex_coordinates(self) -> List[int]:
		return rotate_triangle_coordinates(
			pos=self.pos + self.shift,
			size=(self.size.x, 0),
			rotation_angle=self.orientation_rad,
			vertex_angles=(1, 1 / 3, -1 / 3),
			vertex_radius_multiplier=(1, 1, 1),
		)
