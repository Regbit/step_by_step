import collections
import typing
from typing import List

from pyglet.graphics import Batch

from step_by_step.common.helpers import vertex_in_zone
from step_by_step.game.managers.settings import ScreenScrollFlag
from step_by_step.game.objects.world_object import WorldObject
from step_by_step.graphics.camera import Camera
from step_by_step.common.vector import Vector2f
from step_by_step.graphics.settings import BatchGroup


class ScreenManager:

	_camera: Camera
	_scroll_flags = set()
	batches: typing.OrderedDict[str, Batch]

	@classmethod
	def _init_batches(cls):
		for b in BatchGroup:
			cls.batches[b.value] = Batch()

	@classmethod
	def init(cls, screen_width: int, screen_height: int):
		cls._camera = Camera(Vector2f(0, 0), Vector2f(screen_width, screen_height))
		cls.batches = collections.OrderedDict()
		cls._init_batches()

	@classmethod
	def refresh_draw_data(cls, world_object_list: List[WorldObject]):
		cls._init_batches()
		for o in world_object_list:
			for v in o.visibility_vertices:
				cam_pos = cls._camera.pos + (cls._camera.size / 2)
				if vertex_in_zone(v.x, v.y, cam_pos, cls._camera.size):
					for draw_data in o.draw_data:
						cls.batches[draw_data.batch].add(
							draw_data.count,
							draw_data.mode,
							draw_data.group,
							*draw_data.shifted_draw_data(cls._camera.pos)
						)
					break

	@classmethod
	def draw(cls):
		for b in reversed(cls.batches.values()):
			b.draw()

	@classmethod
	def check_mouse_over_object(cls, mouse_x: int, mouse_y: int, obj: WorldObject) -> bool:
		pos, size = obj.screen_data
		return vertex_in_zone(mouse_x, mouse_y, pos - cls._camera.pos, size)

	@classmethod
	def camera_drag(cls, dx: float, dy: float):
		move_vec = Vector2f(dx, dy)
		cls._camera.move(move_vec)

	@classmethod
	def camera_scroll_flag(cls, x: int, y: int):
		cls._scroll_flags = set()
		if x <= cls._camera.scroll_border_width:
			cls._scroll_flags.add(ScreenScrollFlag.LEFT)
		elif x >= cls._camera.size.x - cls._camera.scroll_border_width:
			cls._scroll_flags.add(ScreenScrollFlag.RIGHT)

		if y <= cls._camera.scroll_border_width:
			cls._scroll_flags.add(ScreenScrollFlag.DOWN)
		elif y >= cls._camera.size.y - cls._camera.scroll_border_width:
			cls._scroll_flags.add(ScreenScrollFlag.UP)

	@classmethod
	def camera_scroll_action(cls):
		move_vec = Vector2f(0, 0)

		if ScreenScrollFlag.LEFT in cls._scroll_flags:
			move_vec -= (cls._camera.scroll_speed, 0)
		elif ScreenScrollFlag.RIGHT in cls._scroll_flags:
			move_vec += (cls._camera.scroll_speed, 0)

		if ScreenScrollFlag.DOWN in cls._scroll_flags:
			move_vec -= (0, cls._camera.scroll_speed)
		elif ScreenScrollFlag.UP in cls._scroll_flags:
			move_vec += (0, cls._camera.scroll_speed)

		cls._camera.move(move_vec)
