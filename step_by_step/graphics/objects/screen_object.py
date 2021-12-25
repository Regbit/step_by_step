from __future__ import annotations

import abc
import copy
import math
from typing import List, Tuple, Optional

from step_by_step.common.shaped import Shaped
from step_by_step.graphics.draw_data import DrawData
from step_by_step.graphics.objects.settings import DrawMode, BatchGroup
from step_by_step.common.vector import Vector2f, Vector3i


class _BaseScreenObject(Shaped):

	_vertex_count: int
	_draw_data: DrawData = None
	_base_batch: BatchGroup
	_batch: Optional[BatchGroup] = None
	mode: DrawMode
	shift: Vector2f
	color: Vector3i
	do_draw: bool
	orientation_rad: float = math.pi / 2

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
		return self._pos + self.shift, self._size

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

	def set_pos(self, x: int = None, y: int = None, pos: Vector2f = None):
		if self._pos and isinstance(self._pos, Vector2f):
			if x is not None and y is not None:
				self._pos._x, self._pos._y = x, y
				self._update_draw_data()
			elif pos:
				self._pos = pos
				self._update_draw_data()
			else:
				raise NotImplementedError(f'Not enough args passed!\n\targs: ({x, y, pos})')

	def move(self, dir_x: int = None, dir_y: int = None, dir_vec: Vector2f = None):
		if dir_x is not None and dir_y is not None:
			self._pos += (dir_x, dir_y)
			self._update_draw_data()
		elif dir_vec:
			self._pos += dir_vec
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
		super(ScreenObject, self).__init__(
			pos=pos,
			size=size
		)
		self._vertex_count = vertex_count
		self._base_batch = base_batch
		self.mode = mode
		self.shift = shift
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
