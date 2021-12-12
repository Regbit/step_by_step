from step_by_step.common.helpers import vertex_in_zone
from step_by_step.common.vector import Vector2f
from step_by_step.game.managers.settings import ScreenScrollFlag
from step_by_step.game.objects.game_object import DrawnGameObject
from step_by_step.game.objects.gui.gui_object import GUIObject


class Camera:

	_pos: Vector2f
	_world_pos: Vector2f
	_screen_pos: Vector2f
	_scroll_flags = set()
	size: Vector2f
	scroll_speed = 7
	scroll_border_width = 15

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

	def scroll_flag(self, x: int, y: int):
		self._scroll_flags = set()
		if self.screen_pos.x - self.size.x / 2 <= x <= self.scroll_border_width:
			self._scroll_flags.add(ScreenScrollFlag.LEFT)
		elif self.screen_pos.x + self.size.x / 2 >= x >= self.size.x - self.scroll_border_width:
			self._scroll_flags.add(ScreenScrollFlag.RIGHT)

		if self.screen_pos.y - self.size.y / 2 <= y <= self.scroll_border_width:
			self._scroll_flags.add(ScreenScrollFlag.DOWN)
		elif self.screen_pos.y + self.size.y / 2 >= y >= self.size.y - self.scroll_border_width:
			self._scroll_flags.add(ScreenScrollFlag.UP)

	def scroll_action(self):
		move_vec = Vector2f(0, 0)

		if ScreenScrollFlag.LEFT in self._scroll_flags:
			move_vec -= (self.scroll_speed, 0)
		elif ScreenScrollFlag.RIGHT in self._scroll_flags:
			move_vec += (self.scroll_speed, 0)

		if ScreenScrollFlag.DOWN in self._scroll_flags:
			move_vec -= (0, self.scroll_speed)
		elif ScreenScrollFlag.UP in self._scroll_flags:
			move_vec += (0, self.scroll_speed)

		self.scroll(move_vec)

	def _update_pos(self):
		self._pos = self._screen_pos + self._world_pos

	def scroll(self, vec: Vector2f):
		self._world_pos += vec
		self._update_pos()

	def is_object_in_frame(self, obj: DrawnGameObject) -> bool:
		for v in obj.visibility_vertices:
			if isinstance(obj, GUIObject) or vertex_in_zone(v.x, v.y, self.pos, self.size):
				return True
		return False
