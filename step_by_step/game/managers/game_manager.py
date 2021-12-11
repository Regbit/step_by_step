import logging
from time import time
from typing import Optional, Dict, Any, List

from pyglet.window import key, mouse

from step_by_step.game.managers import KeyEvent, ObjectManager, ScreenManager, JobManager
from step_by_step.game.objects.units.world_object import WorldObject


log = logging.getLogger('Game Manager')


class GameManager:

	_print_info = False
	_pressed_keys = set()
	_window_data = dict()
	_frame_rate = 0, time()

	_screen_manager: ScreenManager
	_object_manager: ObjectManager
	_job_manager: JobManager

	selected_object: Optional[WorldObject] = None

	def __init__(self, screen_width: int, screen_height: int):
		self._screen_manager = ScreenManager(screen_width, screen_height)
		self._object_manager = ObjectManager()
		self._job_manager = JobManager()

	def world_object_list(self) -> List[WorldObject]:
		return [o for o in self._object_manager.objects_dict.values() if isinstance(o, WorldObject)]

	def select(self, mouse_x: int, mouse_y: int):
		if self.selected_object:
			self.selected_object.deselect()

		self.selected_object = None
		for obj in self.world_object_list():
			if obj.is_selectable:
				if self._screen_manager.check_mouse_over_object(mouse_x, mouse_y, obj):
					if obj.select():
						self.selected_object = obj
						break
					else:
						log.warning(f'Could not select object under cursor! {obj}')

	def delete_selected_object(self) -> bool:
		if self.selected_object:
			object_id = self.selected_object.object_id
			self.selected_object.object_id = None
			self._object_manager.trigger_self_destruct(object_id=object_id)
			return True
		return False

	def key_update(self, key: int, event_type: KeyEvent, data: Dict[str, Any] = None):
		if event_type == KeyEvent.PRESSED:
			self._pressed_keys.add(key)
		if event_type == KeyEvent.RELEASED:
			self._pressed_keys.remove(key)
		if data:
			self._window_data.update(data)

	def _key_action(self):
		if key.SPACE in self._pressed_keys:
			self._print_info = not self._print_info
		if key.DELETE in self._pressed_keys:
			self.delete_selected_object()
		if mouse.LEFT in self._pressed_keys:
			pos = self._window_data.get('mouse')
			if pos:
				self.select(*pos)

	def game_update(self):
		self._key_action()
		self._camera_scroll_action()

	def camera_drag(self, dx: float, dy: float):
		if mouse.MIDDLE in self._pressed_keys:
			self._screen_manager.camera_drag(dx, dy)

	def camera_scroll_flag(self, x: int, y: int):
		self._screen_manager.camera_scroll_flag(x, y)

	def _camera_scroll_action(self):
		if mouse.MIDDLE not in self._pressed_keys:
			self._screen_manager.camera_scroll_action()

	def refresh_draw_data(self):
		self._screen_manager.refresh_draw_data(self.world_object_list())

	def draw(self):
		self._screen_manager.draw()

	def post_code(self):
		if time() - self._frame_rate[1] > 1:
			if self._print_info:
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
