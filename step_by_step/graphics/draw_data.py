from typing import Optional, List, Tuple

from step_by_step.common.vector import Vector2f
from step_by_step.graphics.objects.settings import BatchGroup, DrawMode


class DrawData:

	def __init__(
			self,
			batch: BatchGroup,
			count: int,
			mode: DrawMode,
			group: Optional[str],
			data: List[Tuple[str, List[int]]]
	):
		self._batch = batch
		self._count = count
		self._mode = mode
		self._group = group
		self._data = data

	@property
	def batch_value(self) -> str:
		return self._batch.value

	@property
	def count(self) -> int:
		return self._count

	@property
	def mode_value(self) -> int:
		return self._mode.value

	@property
	def group(self) -> Optional[str]:
		return self._group

	@property
	def data(self) -> List[Tuple]:
		return self._data

	def shifted_draw_data(self, camera_pos: Vector2f) -> List[Tuple[str, List[int]]]:
		out = []
		for d in self._data:
			vertex_list = d[1]
			if d[0] == 'v2i':
				vertex_list = []
				for i in range(self._count):
					mul = 0 if 'GUI' in self._batch.value else -1
					vertex_list.extend(
						[
							d[1][i*2] + mul * int(camera_pos.x),
							d[1][i*2+1] + mul * int(camera_pos.y)
						]
					)
			out.append((d[0], vertex_list))
		return out
