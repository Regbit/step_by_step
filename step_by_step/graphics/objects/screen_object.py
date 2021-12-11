from __future__ import annotations

import abc
import copy
import math
from typing import List, Tuple, Optional

from step_by_step.graphics.draw_data import DrawData
from step_by_step.graphics.objects.settings import DrawMode, BatchGroup
from step_by_step.common.vector import Vector2f, Vector3i


class _BaseScreenObject(abc.ABC):

	_vertex_count: int
	_draw_data: DrawData = None
	_base_batch: BatchGroup
	_batch: Optional[BatchGroup] = None
	mode: DrawMode
	pos: Vector2f
	shift: Vector2f
	size: Vector2f
	color: Vector3i
	do_draw: bool
	orientation_rad: float = math.pi / 2

	@property
	def x(self) -> float:
		return self.pos.x

	@property
	def y(self) -> float:
		return self.pos.y

	@property
	def w(self) -> float:
		return self.size.x

	@property
	def h(self) -> float:
		return self.size.y

	@abc.abstractmethod
	def vertex_coordinates(self) -> List[int]:
		raise NotImplementedError()

	@property
	def draw_data(self) -> DrawData:
		if not self._draw_data:
			self._update_draw_data()
		return self._draw_data

	@property
	def screen_data(self) -> Tuple[Vector2f, Vector2f]:
		return self.pos + self.shift, self.size

	@property
	def batch(self) -> BatchGroup:
		return self._batch if self._batch else self._base_batch

	def _update_draw_data(self):
		self._draw_data = DrawData(
				batch=self.batch,
				count=self._vertex_count,
				mode=self.mode,
				group=None,
				data=[
					('v2i', self.vertex_coordinates),
					('c3B', self.color.list * self._vertex_count)
				]
			)

	def set_batch(self, new_batch: Optional[BatchGroup]):
		self._batch = new_batch

	def set_pos(self, x: int, y: int):
		if self.pos and isinstance(self.pos, Vector2f):
			self.pos._x, self.pos._y = x, y
			self._update_draw_data()

	def move(self, dir_x: int = None, dir_y: int = None, dir_vec: Vector2f = None):
		if dir_x and dir_y:
			self.pos += (dir_x, dir_y)
			self._update_draw_data()
		elif dir_vec:
			self.pos += dir_vec
			self._update_draw_data()
		else:
			raise NotImplementedError(f'Not enough args passed!\n\targs: ({dir_x, dir_y, dir_vec})')

	def rotate(self, rad: float):
		self.orientation_rad += rad
		self._update_draw_data()


class ScreenObject(_BaseScreenObject):

	def __init__(
			self,
			vertex_count: int,
			base_batch: BatchGroup,
			mode: DrawMode,
			pos: Vector2f,
			shift: Vector2f,
			size: Vector2f,
			color: Vector3i,
			do_draw: bool,
	):
		self._vertex_count = vertex_count
		self._base_batch = base_batch
		self.mode = mode
		self.pos = pos
		self.shift = shift
		self.size = size
		self.color = color
		self.do_draw = do_draw

	@property
	def copy(self) -> ScreenObject:
		return copy.copy(self)

	@property
	def deepcopy(self) -> ScreenObject:
		return copy.deepcopy(self)

	@abc.abstractmethod
	def __copy__(self):
		raise NotImplementedError()

	@abc.abstractmethod
	def __deepcopy__(self):
		raise NotImplementedError()

	@abc.abstractmethod
	def vertex_coordinates(self) -> List[int]:
		raise NotImplementedError()
