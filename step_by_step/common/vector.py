from __future__ import annotations

import copy
import math
from typing import Optional, List, Tuple


class Vector2f:

	def __init__(
			self,
			x: Optional[float] = None,
			y: Optional[float] = None,
			r: Optional[float] = None,
			a: Optional[float] = None,
	):
		self._x = None
		self._y = None
		self._r = None
		self._a = None

		if x is not None and y is not None:
			self._x = x
			self._y = y
			self._update_polar()
		elif r is not None and a is not None:
			self._r = r
			self._a = a
			self._update_cartesian()
		else:
			ValueError(f'{self.__class__.__name__} needs ether "x" and "y" pair or "r" and "a" pair to be initialized!')

	def _update_polar(self):
		self._r = round(math.sqrt(self._x ** 2 + self._y ** 2), 4)
		self._a = round(math.atan2(self._y, self._x), 4)

	def _update_cartesian(self):
		self._x = round(self._r * math.cos(self._a), 4)
		self._y = round(self._r * math.sin(self._a), 4)

	def __add__(self, other):
		if isinstance(other, Vector2f):
			return Vector2f(self._x + other._x, self._y + other._y)
		elif isinstance(other, (list, tuple)) and len(other) == 2:
			return Vector2f(self._x + other[0], self._y + other[1])
		else:
			raise NotImplementedError(f"__add__ is not implemented for pair ({type(self)}, {type(other)})")

	def __iadd__(self, other):
		return self + other

	def __sub__(self, other):
		if isinstance(other, Vector2f):
			return Vector2f(self._x - other._x, self._y - other._y)
		elif isinstance(other, (list, tuple)) and len(other) == 2:
			return Vector2f(self._x - other[0], self._y - other[1])
		else:
			raise NotImplementedError(f"__sub__ is not implemented for pair ({type(self)}, {type(other)})")

	def __isub__(self, other):
		return self - other

	def __mul__(self, other):
		if isinstance(other, (int, float)):
			return Vector2f(round(self._x * other, 4), round(self._y * other, 4))
		elif isinstance(other, Vector2f):
			return self._x * other._x + self._y * other._y
		else:
			raise NotImplementedError(f"__mul__ is not implemented for pair ({type(self)}, {type(other)})")

	def __truediv__(self, other):
		if isinstance(other, (int, float)):
			return Vector2f(round(self._x / other, 4), round(self._y / other, 4))
		else:
			raise NotImplementedError(f"__truediv__ is not implemented for pair ({type(self)}, {type(other)})")

	def __str__(self):
		return f'({self.x, self.y})({self.r, self.a})'

	def __repr__(self):
		return f'{type(self).__name__}{self.x, self.y}'

	def __copy__(self):
		return Vector2f(self._x, self._y)

	def __invert__(self):
		return Vector2f(-self._x, -self._y)

	@property
	def copy(self) -> Vector2f:
		return copy.copy(self)

	@property
	def x(self) -> float:
		return round(self._x, 4)

	@property
	def y(self) -> float:
		return round(self._y, 4)

	@property
	def r(self) -> float:
		return round(self._r, 4)

	@property
	def a(self) -> float:
		return round(self._a, 4)

	@property
	def list(self) -> List[float]:
		return [self._x, self._y]

	@property
	def tuple(self) -> Tuple[float, float]:
		return self._x, self._y

	@property
	def len(self) -> float:
		return self.r

	@property
	def angle(self) -> float:
		return self.a

	def dist(self, other: Vector2f) -> float:
		return (other - self).len

	def angle_between(self, other: Vector2f) -> float:
		return round(other.a - self.a, 4)

	def set_angle(self, new_angle: float):
		if new_angle < 0:
			new_angle = new_angle + math.pi * 2
		elif new_angle > math.pi * 2:
			new_angle = new_angle - math.pi * 2
		else:
			new_angle = new_angle
		self._a = new_angle
		self._update_cartesian()

	def set_len(self, new_l: float):
		self._r = new_l
		self._update_cartesian()

	def rotate(self, rad: float):
		self.set_angle(self.angle + rad)


class Vector3i:

	def __init__(
			self,
			x: int,
			y: int,
			z: int
	):
		self._x = x
		self._y = y
		self._z = z

	@property
	def list(self) -> List[int]:
		return [self._x, self._y, self._z]

	def __add__(self, other):
		if isinstance(other, Vector3i):
			return Vector3i(self._x + other._x, self._y + other._y, self._z + other._z)
		elif isinstance(other, (list, tuple)) and len(other) == 3:
			return Vector3i(self._x + other[0], self._y + other[1], self._z + other[2])
		else:
			raise NotImplementedError(f"__add__ is not implemented for pair ({type(self)}, {type(other)})")

	def __iadd__(self, other):
		return self + other

	def __sub__(self, other):
		if isinstance(other, Vector3i):
			return Vector3i(self._x - other._x, self._y - other._y, self._z - other._z)
		elif isinstance(other, (list, tuple)) and len(other) == 3:
			return Vector3i(self._x - other[0], self._y - other[1], self._z - other[2])
		else:
			raise NotImplementedError(f"__sub__ is not implemented for pair ({type(self)}, {type(other)})")

	def __isub__(self, other):
		return self - other

	def __mul__(self, other):
		if isinstance(other, (int, float)):
			return Vector3i(round(self._x * other), round(self._y * other), round(self._z * other))
		elif isinstance(other, Vector3i):
			return self._x * other._x + self._y * other._y + self._z * other._z
		else:
			raise NotImplementedError(f"__mul__ is not implemented for pair ({type(self)}, {type(other)})")

	def __copy__(self):
		return Vector3i(self._x, self._y, self._z)

	@property
	def copy(self) -> Vector3i:
		return copy.copy(self)
