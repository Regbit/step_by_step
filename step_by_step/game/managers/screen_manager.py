import collections
from typing import List, OrderedDict

from pyglet.graphics import Batch

from step_by_step.common.helpers import vertex_in_zone
from step_by_step.common.shaped import Shaped
from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import DrawnGameObject
from step_by_step.game.objects.gui.gui import MainGameGUI, ViewportGUI
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.game.objects.gui.settings import GUIStyle
from step_by_step.graphics.objects.settings import BatchGroup


class ScreenManager:

	_screen: Shaped
	_active_gui: ViewportGUI = None
	_batches: OrderedDict[str, Batch]

	def __init__(self, screen_width: int, screen_height: int):
		screen_size = Vector2f(screen_width, screen_height)
		screen_center = screen_size / 2
		self._screen = Shaped(screen_center, screen_size)
		self._batches = collections.OrderedDict()

	@property
	def screen(self) -> Shaped:
		return self._screen

	@property
	def active_gui(self) -> ViewportGUI:
		if not self._active_gui:
			self._active_gui = MainGameGUI(
				pos=self.screen.pos,
				size=self.screen.size,
				screen=self.screen,
				gui_style=GUIStyle.BLUE
			)
		return self._active_gui

	def _init_batches(self):
		for b in BatchGroup:
			self._batches[b.value] = Batch()

	def refresh_draw_data(self, drawn_object_list: List[DrawnGameObject]):
		if self._active_gui:
			self._init_batches()
			for o in drawn_object_list:
				if o.drawn_sprite and self._active_gui.is_object_in_frame(o):
					o.enrich_batches(batches=self._batches, cam_world_pos=self._active_gui.cam_world_pos)

	def draw(self):
		for b in reversed(self._batches.values()):
			b.draw()

	def check_mouse_over_object(self, mouse_x: int, mouse_y: int, obj: DrawnGameObject) -> bool:
		if self._active_gui:
			pos, size = obj.screen_data
			mul = 0 if isinstance(obj, GUIObject) else -1
			return vertex_in_zone(mouse_x, mouse_y, pos + self._active_gui.cam_world_pos * mul, size)
		else:
			return False

	def camera_drag(self, x: int, y: int, dx: float, dy: float):
		if self._active_gui:
			if vertex_in_zone(x, y, self._active_gui.viewport.pos, self._active_gui.viewport.size):
				move_vec = Vector2f(dx, dy)
				self._active_gui.viewport.scroll(move_vec)

	def camera_scroll_flag(self, x: int, y: int):
		if self._active_gui:
			self._active_gui.viewport.scroll_flag(x, y)

	def camera_scroll_action(self):
		if self._active_gui:
			self._active_gui.viewport.scroll_action()
