import logging
from time import time
from typing import Optional, Dict, Any, List

from pyglet.window import key, mouse

from step_by_step.game.managers import KeyEvent, ObjectManager, ScreenManager
from step_by_step.game.objects.path import Waypoint, Trajectory
from step_by_step.game.objects.world_object import WorldObject
from step_by_step.game.objects.unit import Building, ResourceNode, Vehicle
from step_by_step.game.objects.jobs.task import MoveToTask
from step_by_step.common.vector import Vector2f

log = logging.getLogger('Game Manager')


class GameManager:

	_print_info = False
	_pressed_keys = set()
	_window_data = dict()
	_frame_rate = 0, time()
	selected_object: Optional[WorldObject] = None

	@classmethod
	def init(cls, screen_width: int, screen_height: int):
		ScreenManager.init(screen_width, screen_height)

		b = Building(Vector2f(200, 100))
		rn = ResourceNode(Vector2f(1000, 1000))
		v = Vehicle(Vector2f(100, 100))
		w = Waypoint(Vector2f(300, 100))
		t = Trajectory(Vector2f(100, 100), Vector2f(300, 100))
		MoveToTask(actor=v, destination=rn)

	@classmethod
	def world_object_list(cls) -> List[WorldObject]:
		return [o for o in ObjectManager.objects_dict.values() if isinstance(o, WorldObject)]

	@classmethod
	def select(cls, mouse_x: int, mouse_y: int):
		if cls.selected_object:
			cls.selected_object.deselect()

		cls.selected_object = None
		for obj in cls.world_object_list():
			if obj.is_selectable:
				if ScreenManager.check_mouse_over_object(mouse_x, mouse_y, obj):
					if obj.select():
						cls.selected_object = obj
						break
					else:
						log.warning(f'Could not select object under cursor! {obj}')

	@classmethod
	def delete_selected_object(cls) -> bool:
		return ObjectManager.trigger_self_destruct(object_id=cls.selected_object.object_id)

	@classmethod
	def key_update(cls, key: int, event_type: KeyEvent, data: Dict[str, Any] = None):
		if event_type == KeyEvent.PRESSED:
			cls._pressed_keys.add(key)
		if event_type == KeyEvent.RELEASED:
			cls._pressed_keys.remove(key)
		if data:
			cls._window_data.update(data)

	@classmethod
	def _key_action(cls):
		if key.SPACE in cls._pressed_keys:
			cls._print_info = not cls._print_info
		if key.DELETE in cls._pressed_keys:
			cls.delete_selected_object()
		if mouse.LEFT in cls._pressed_keys:
			pos = cls._window_data.get('mouse')
			if pos:
				cls.select(*pos)

	@classmethod
	def game_update(cls):
		cls._key_action()
		cls._camera_scroll_action()

	@classmethod
	def camera_drag(cls, dx: float, dy: float):
		if mouse.MIDDLE in cls._pressed_keys:
			ScreenManager.camera_drag(dx, dy)

	@classmethod
	def camera_scroll_flag(cls, x: int, y: int):
		ScreenManager.camera_scroll_flag(x, y)

	@classmethod
	def _camera_scroll_action(cls):
		if mouse.MIDDLE not in cls._pressed_keys:
			ScreenManager.camera_scroll_action()

	@classmethod
	def refresh_draw_data(cls):
		ScreenManager.refresh_draw_data(cls.world_object_list())

	@classmethod
	def draw(cls):
		ScreenManager.draw()

	@classmethod
	def post_code(cls):
		if time() - cls._frame_rate[1] > 1:
			if cls._print_info:
				print('-' * 25)
				print('fps:', cls._frame_rate)
				print('Selected object:', cls.selected_object)
				print('Window data', cls._window_data)
				print('Keys pressed', cls._pressed_keys)
				print('-' * 25)
				print()

			cls._frame_rate = 0, time()
		else:
			cls._frame_rate = cls._frame_rate[0] + 1, cls._frame_rate[1]
