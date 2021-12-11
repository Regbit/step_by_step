from typing import List

from step_by_step.graphics.objects.screen_object import ScreenObject
from step_by_step.graphics.objects.settings import BatchGroup, DrawMode
from step_by_step.common.vector import Vector2f, Vector3i


class Line(ScreenObject):

	def __init__(
			self,
			vertex_1: Vector2f,
			vertex_2: Vector2f,
			base_batch: BatchGroup,
			shift: Vector2f = Vector2f(0, 0),
	):
		super(Line, self).__init__(
			vertex_count=2,
			pos=vertex_2-vertex_1,
			shift=shift,
			size=Vector2f(1, 1),
			color=Vector3i(50, 200, 50),
			mode=DrawMode.LINES,
			base_batch=base_batch,
			do_draw=True,
		)
		self.vertex_1 = vertex_1
		self.vertex_2 = vertex_2

	@property
	def vertex_coordinates(self) -> List[int]:
		return [
			int(self.vertex_1.x),
			int(self.vertex_1.y),
			int(self.vertex_2.x),
			int(self.vertex_2.y)
		]
