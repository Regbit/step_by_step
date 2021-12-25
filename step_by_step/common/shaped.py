import abc

from step_by_step.common.vector import Vector2f


class Shaped(abc.ABC):

	_pos: Vector2f = None
	_size: Vector2f = None

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
	):
		self._pos = pos
		self._size = size

	@property
	def pos(self) -> Vector2f:
		return self._pos

	@pos.setter
	def pos(self, new_pos: Vector2f):
		raise NotImplementedError()

	@property
	def x(self) -> float:
		return self._pos.x if self._pos else None

	@property
	def y(self) -> float:
		return self._pos.y if self._pos else None

	@property
	def size(self) -> Vector2f:
		return self._size

	@size.setter
	def size(self, new_pos: Vector2f):
		raise NotImplementedError()

	@property
	def w(self) -> float:
		return self._size.x if self._size else None

	@property
	def h(self) -> float:
		return self._size.y if self._size else None
