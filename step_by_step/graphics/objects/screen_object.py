from __future__ import annotations

import abc
import copy
import math
from typing import List, Optional

from step_by_step.common.shaped import Shaped
from step_by_step.graphics.draw_data import DrawData
from step_by_step.graphics.objects.settings import DrawMode, BatchGroup
from step_by_step.common.vector import Vector2f, Vector3i


class _BaseScreenObject(Shaped):

	_vertex_count: int
	_draw_data: DrawData = None
	_base_batch_group: BatchGroup
	_batch_group: Optional[BatchGroup] = None
	_shift: Vector2f
	mode: DrawMode
	color: Vector3i
	orientation_rad: float = math.pi / 2

	@abc.abstractmethod
	def vertex_coordinates(self) -> List[int]:
		raise NotImplementedError()

	@property
	def shift(self) -> Vector2f:
		return self._shift

	@property
	def shifted_pos(self) -> Vector2f:
		return self._pos + self._shift

	@property
	def draw_data(self) -> DrawData:
		if not self._draw_data:
			self._update_draw_data()
		return self._draw_data

	@property
	def batch_group(self) -> BatchGroup:
		return self._batch_group if self._batch_group else self._base_batch_group

	def _update_draw_data(self):
		self._draw_data = DrawData(
				batch=self.batch_group,
				count=self._vertex_count,
				mode=self.mode,
				group=None,
				data=[
					('v2i', self.vertex_coordinates),
					('c3B', self.color.list * self._vertex_count)
				]
			)

	def set_batch_group(self, new_batch_group: Optional[BatchGroup]):
		self._batch_group = new_batch_group

	def set_pos(self, pos: Vector2f):
		self._pos = pos
		self._update_draw_data()

	def set_shift(self, shift: Vector2f):
		self._shift = shift
		self._update_draw_data()

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
			base_batch_group: BatchGroup,
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
		self._base_batch_group = base_batch_group
		self._shift = shift
		self.mode = mode
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
