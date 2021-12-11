from typing import List

from step_by_step.graphics.objects._helpers import rotate_quad_coordinates
from step_by_step.graphics.objects.screen_object import ScreenObject
from step_by_step.graphics.objects.settings import BatchGroup, DrawMode
from step_by_step.common.vector import Vector2f, Vector3i


class Square(ScreenObject):

	def __init__(
			self,
			pos: Vector2f,
			size: Vector2f,
			color: Vector3i,
			base_batch: BatchGroup,
			shift: Vector2f = Vector2f(0, 0),
			mode: DrawMode = DrawMode.QUADS,
			do_draw: bool = True
	):
		super(Square, self).__init__(
			vertex_count=4,
			pos=pos,
			shift=shift,
			size=size,
			color=color,
			mode=mode,
			base_batch=base_batch,
			do_draw=do_draw,
		)

	@property
	def vertex_coordinates(self) -> List[int]:
		return rotate_quad_coordinates(
			pos=self.pos + self.shift,
			size=self.size,
			vertex_angles=(3 / 4, -3 / 4, -1 / 4, 1 / 4),
			rotation_angle=self.orientation_rad,
		)


class Diamond(Square):

	@property
	def vertex_coordinates(self) -> List[int]:
		return rotate_quad_coordinates(
			pos=self.pos + self.shift,
			size=(self.size.x, 0),
			vertex_angles=(0, 1 / 2, 1, -1 / 2),
			rotation_angle=self.orientation_rad,
		)


class SelectionBorder(Square):

	def __init__(
			self,
			pos: Vector2f,
			size: Vector2f,
			base_batch: BatchGroup,
			shift: Vector2f = Vector2f(0, 0),
	):
		super(SelectionBorder, self).__init__(
			pos=pos,
			shift=shift,
			size=size,
			color=Vector3i(255, 255, 255),
			base_batch=base_batch,
			mode=DrawMode.LINES,
			do_draw=False
		)