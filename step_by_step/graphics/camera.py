from step_by_step.common.helpers import vertex_in_zone
from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import DrawnGameObject
from step_by_step.graphics.objects.settings import BatchGroup


class Camera:

	_pos: Vector2f
	_world_pos: Vector2f
	_screen_pos: Vector2f
	size: Vector2f
	scroll_speed = 7
	scroll_border_width = 20

	def __init__(self, world_pos: Vector2f, screen_pos: Vector2f, size: Vector2f):
		self._world_pos = world_pos
		self._screen_pos = screen_pos
		self._update_pos()
		self.size = size

	@property
	def pos(self) -> Vector2f:
		return self._pos

	@property
	def world_pos(self) -> Vector2f:
		return self._world_pos

	@world_pos.setter
	def world_pos(self, new_world_pos: Vector2f):
		self._world_pos = new_world_pos
		self._update_pos()

	@property
	def screen_pos(self) -> Vector2f:
		return self._screen_pos

	@screen_pos.setter
	def screen_pos(self, new_screen_pos: Vector2f):
		self._screen_pos = new_screen_pos
		self._update_pos()

	def _update_pos(self):
		self._pos = self._screen_pos + self._world_pos

	def scroll(self, vec: Vector2f):
		self._world_pos += vec
		self._update_pos()

	def is_object_in_frame(self, obj: DrawnGameObject) -> bool:
		for v in obj.visibility_vertices:
			if obj.batch_group == BatchGroup.GUI_OBJECT or vertex_in_zone(v.x, v.y, self.pos, self.size):
				return True
		return False
