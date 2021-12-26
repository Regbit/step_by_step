from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import GameObject


class Camera(GameObject):

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f
	):
		super(Camera, self).__init__(
			pos=pos,
			size=size
		)

	@property
	def pos(self) -> Vector2f:
		return self._pos

	@pos.setter
	def pos(self, new_pos: Vector2f):
		self._pos = new_pos

	@property
	def size(self) -> Vector2f:
		return self._size

	@size.setter
	def size(self, new_size: Vector2f):
		self._size = new_size
