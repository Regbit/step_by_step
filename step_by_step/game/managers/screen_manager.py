import collections
import typing
from typing import List

from pyglet.graphics import Batch

from step_by_step.common.helpers import vertex_in_zone
from step_by_step.common.vector import Vector2f
from step_by_step.game.managers.settings import ScreenScrollFlag
from step_by_step.game.objects.game_object import DrawnGameObject
from step_by_step.graphics.camera import Camera
from step_by_step.graphics.objects.settings import BatchGroup


class ScreenManager:

	_camera: Camera
	_scroll_flags = set()
	batches: typing.OrderedDict[str, Batch]

	def __init__(self, screen_width: int, screen_height: int):
		self._camera = Camera(Vector2f(0, 0), Vector2f(screen_width, screen_height))
		self.batches = collections.OrderedDict()
		self._init_batches()

	def _init_batches(self):
		for b in BatchGroup:
			self.batches[b.value] = Batch()

	def refresh_draw_data(self, world_object_list: List[DrawnGameObject]):
		self._init_batches()
		for o in world_object_list:
			for v in o.visibility_vertices:
				cam_pos = self._camera.pos + (self._camera.size / 2)
				if vertex_in_zone(v.x, v.y, cam_pos, self._camera.size):
					for draw_data in o.draw_data:
						self.batches[draw_data.batch].add(
							draw_data.count,
							draw_data.mode,
							draw_data.group,
							*draw_data.shifted_draw_data(self._camera.pos)
						)
					break

	def draw(self):
		for b in reversed(self.batches.values()):
			b.draw()

	def check_mouse_over_object(self, mouse_x: int, mouse_y: int, obj: DrawnGameObject) -> bool:
		pos, size = obj.screen_data
		return vertex_in_zone(mouse_x, mouse_y, pos - self._camera.pos, size)

	def camera_drag(self, dx: float, dy: float):
		move_vec = Vector2f(dx, dy)
		self._camera.move(move_vec)

	def camera_scroll_flag(self, x: int, y: int):
		self._scroll_flags = set()
		if x <= self._camera.scroll_border_width:
			self._scroll_flags.add(ScreenScrollFlag.LEFT)
		elif x >= self._camera.size.x - self._camera.scroll_border_width:
			self._scroll_flags.add(ScreenScrollFlag.RIGHT)

		if y <= self._camera.scroll_border_width:
			self._scroll_flags.add(ScreenScrollFlag.DOWN)
		elif y >= self._camera.size.y - self._camera.scroll_border_width:
			self._scroll_flags.add(ScreenScrollFlag.UP)

	def camera_scroll_action(self):
		move_vec = Vector2f(0, 0)

		if ScreenScrollFlag.LEFT in self._scroll_flags:
			move_vec -= (self._camera.scroll_speed, 0)
		elif ScreenScrollFlag.RIGHT in self._scroll_flags:
			move_vec += (self._camera.scroll_speed, 0)

		if ScreenScrollFlag.DOWN in self._scroll_flags:
			move_vec -= (0, self._camera.scroll_speed)
		elif ScreenScrollFlag.UP in self._scroll_flags:
			move_vec += (0, self._camera.scroll_speed)

		self._camera.move(move_vec)
