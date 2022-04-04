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
		return self.pos.x if self.pos else None

	@property
	def y(self) -> float:
		return self.pos.y if self.pos else None

	@property
	def size(self) -> Vector2f:
		return self._size

	@size.setter
	def size(self, new_size: Vector2f):
		raise NotImplementedError()

	@property
	def w(self) -> float:
		return self.size.x if self.size else None

	@property
	def h(self) -> float:
		return self.size.y if self.size else None

	@property
	def left_bound_x(self) -> float:
		return self.pos.x - self.size.x / 2

	@property
	def right_bound_x(self) -> float:
		return self.pos.x + self.size.x / 2

	@property
	def upper_bound_y(self) -> float:
		return self.pos.y + self.size.y / 2

	@property
	def lower_bound_y(self) -> float:
		return self.pos.y - self.size.y / 2
