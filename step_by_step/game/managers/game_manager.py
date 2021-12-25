import logging
from time import time
from typing import Optional, Dict, Any, List

from pyglet.window import key, mouse

from step_by_step.game.managers import KeyEvent, ObjectManager, ScreenManager, JobManager
from step_by_step.game.objects.game_object import DrawnGameObject
from step_by_step.game.objects.gui.gui import MainGameGUI
from step_by_step.game.objects.gui.settings import GUIStyle


log = logging.getLogger('Game Manager')


class GameManager:

	_print_info = False
	_pressed_keys = set()
	_pressed_keys_previous = set()
	_window_data = dict()
	_frame_rate = 0, time()

	_object_manager: ObjectManager
	_screen_manager: ScreenManager
	_job_manager: JobManager

	_gui: MainGameGUI

	highlighted_object: Optional[DrawnGameObject] = None
	clicked_object: Optional[DrawnGameObject] = None
	selected_object: Optional[DrawnGameObject] = None

	def __init__(self, screen_width: int, screen_height: int):
		self._object_manager = ObjectManager()
		self._screen_manager = ScreenManager(screen_width, screen_height)
		self._job_manager = JobManager()

		self._gui = MainGameGUI(
			pos=self._screen_manager.screen_center,
			size=self._screen_manager.screen_size,
			gui_style=GUIStyle.BLUE
		)
		self._object_manager.add(self._gui)
		self._screen_manager.camera_shift(self._gui.camera_pos_shift, self._gui.camera_size_shift)

	def drawn_object_list(self) -> List[DrawnGameObject]:
		return [o for o in self._object_manager.objects_dict.values() if isinstance(o, DrawnGameObject)]

	def highlight(self, mouse_x: int, mouse_y: int) -> bool:
		if self.highlighted_object:
			self.highlighted_object.dehighlight()

		self.highlighted_object = None
		for obj in self.drawn_object_list():
			if obj.is_visible and obj.is_highlightable:
				if self._screen_manager.check_mouse_over_object(mouse_x, mouse_y, obj):
					if obj.highlight():
						self.highlighted_object = obj
						return True
					else:
						log.warning(f'Could not highlight object under cursor! {obj}')
		return False

	def click(self, mouse_x: int, mouse_y: int) -> bool:
		if self.clicked_object:
			self.clicked_object.declick()

		self.clicked_object = None
		for obj in self.drawn_object_list():
			if obj.is_visible and obj.is_clickable:
				if self._screen_manager.check_mouse_over_object(mouse_x, mouse_y, obj):
					if obj.click():
						self.clicked_object = obj
						return True
					else:
						log.warning(f'Could not click object under cursor! {obj}')
		return False

	def select(self, mouse_x: int, mouse_y: int) -> bool:
		if self.selected_object:
			self.selected_object.deselect()

		self.selected_object = None
		for obj in self.drawn_object_list():
			if obj.is_visible and obj.is_selectable:
				if self._screen_manager.check_mouse_over_object(mouse_x, mouse_y, obj):
					if obj.select():
						self.selected_object = obj
						return True
					else:
						log.warning(f'Could not select object under cursor! {obj}')
		return False

	def delete_selected_object(self) -> bool:
		if self.selected_object:
			object_id = self.selected_object.object_id
			self.selected_object.object_id = None
			self._object_manager.trigger_self_destruct(object_id=object_id)
			return True
		return False

	def key_update(self, key_code: int, event_type: KeyEvent, data: Dict[str, Any] = None):
		if event_type == KeyEvent.PRESSED:
			self._pressed_keys.add(key_code)
		if event_type == KeyEvent.RELEASED:
			self._pressed_keys.remove(key_code)
		if data:
			self._window_data.update(data)

	def _key_action(self):
		if key.SPACE in self._pressed_keys and key.SPACE not in self._pressed_keys_previous:
			self._print_info = not self._print_info
			self._switch_hide_right_menu()
		if key.DELETE in self._pressed_keys:
			self.delete_selected_object()
		if mouse.LEFT in self._pressed_keys:
			pos = self._window_data.get('mouse')
			if pos:
				res = self.click(*pos)
				if not res:
					res = self.select(*pos)
		else:
			if self.clicked_object:
				self.clicked_object.declick()
				self.clicked_object = None

		self._pressed_keys_previous = self._pressed_keys.copy()

	def _switch_hide_right_menu(self):
		self._gui.switch_hide_right_menu()
		self._screen_manager.camera_shift(self._gui.camera_pos_shift, self._gui.camera_size_shift)

	def game_update(self):
		self._key_action()
		self._camera_scroll_action()

	def camera_drag(self, x: int, y: int, dx: float, dy: float):
		if mouse.MIDDLE in self._pressed_keys:
			self._screen_manager.camera_drag(x, y, dx, dy)

	def camera_scroll_flag(self, x: int, y: int):
		self._screen_manager.camera_scroll_flag(x, y)

	def _camera_scroll_action(self):
		if mouse.MIDDLE not in self._pressed_keys:
			self._screen_manager.camera_scroll_action()

	def refresh_draw_data(self):
		self._screen_manager.refresh_draw_data(self.drawn_object_list())

	def draw(self):
		self._screen_manager.draw()

	def post_code(self):
		if time() - self._frame_rate[1] > 1:
			if self._print_info and False:
				print('-' * 25)
				print('[FPS]:', self._frame_rate)
				print('[Selected object]:', self.selected_object)
				print('[Window data]:', self._window_data)
				print('[Keys pressed]:', self._pressed_keys)
				print('[Objects]:')
				for obj_id, obj in self._object_manager.objects_dict.items():
					print('\t', obj_id, obj)
				print('-' * 25)
				print()

			self._frame_rate = 0, time()
		else:
			self._frame_rate = self._frame_rate[0] + 1, self._frame_rate[1]
