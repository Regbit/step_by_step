import collections
import typing
from typing import List

from pyglet.graphics import Batch

from step_by_step.common.helpers import vertex_in_zone
from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import DrawnGameObject
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.graphics.camera import Camera
from step_by_step.graphics.objects.settings import BatchGroup


class ScreenManager:

	_camera: Camera
	batches: typing.OrderedDict[str, Batch]
	screen_size: Vector2f
	screen_center: Vector2f

	def __init__(self, screen_width: int, screen_height: int):
		self.screen_size = Vector2f(screen_width, screen_height)
		self.screen_center = self.screen_size / 2

		self._camera = Camera(
			world_pos=Vector2f(0, 0),
			screen_pos=self.screen_center,
			size=self.screen_size
		)

		self.batches = collections.OrderedDict()
		self._init_batches()

	def _init_batches(self):
		for b in BatchGroup:
			self.batches[b.value] = Batch()

	def refresh_draw_data(self, drawn_object_list: List[DrawnGameObject]):
		self._init_batches()
		for o in drawn_object_list:
			if o.drawn_sprite and self._camera.is_object_in_frame(o):
				for draw_data in o.draw_data:
					self.batches[draw_data.batch_value].add(
						draw_data.count,
						draw_data.mode_value,
						draw_data.group,
						*draw_data.shifted_draw_data(self._camera.world_pos)
					)
				for label in o.labels:
					label.batch = self.batches[o.text_batch_group.value]

	def draw(self):
		for b in reversed(self.batches.values()):
			b.draw()

	def check_mouse_over_object(self, mouse_x: int, mouse_y: int, obj: DrawnGameObject) -> bool:
		pos, size = obj.screen_data
		mul = 0 if isinstance(obj, GUIObject) else -1
		return vertex_in_zone(mouse_x, mouse_y, pos + self._camera.world_pos * mul, size)

	def camera_drag(self, x: int, y: int, dx: float, dy: float):
		if vertex_in_zone(x, y, self._camera.screen_pos, self._camera.size):
			move_vec = Vector2f(dx, dy)
			self._camera.scroll(move_vec)

	def camera_scroll_flag(self, x: int, y: int):
		self._camera.scroll_flag(x, y)

	def camera_scroll_action(self):
		self._camera.scroll_action()

	def camera_shift(self, pos: Vector2f, size: Vector2f):
		self._camera.screen_pos = self.screen_center - pos
		self._camera.size = self.screen_size - size
