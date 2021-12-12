from typing import Dict, Optional, List

from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import DrawnGameObject
from step_by_step.game.objects.units import Building, ResourceNode, Vehicle
from step_by_step.game.objects.gui import Button, Panel


class ObjectManager:

	_next_object_id = -1
	objects_dict: Dict[int, Optional[DrawnGameObject]] = dict()

	def __init__(self):
		self._test_init()

	def _test_init(self):
		# TODO remove
		self.add_all(
			[
				Building(pos=Vector2f(200, 100)),
				ResourceNode(pos=Vector2f(1000, 1000)),
				Vehicle(pos=Vector2f(100, 100)),
				Button(pos=Vector2f(0, 400), size=Vector2f(350, 50)),
				Button(pos=Vector2f(0, 340), size=Vector2f(350, 50)),
				Button(pos=Vector2f(0, 280), size=Vector2f(350, 50)),
				Panel(pos=Vector2f(1920-400/2, 1080/2), size=Vector2f(400, 1080)),
			]
		)

		p = None
		for o in self.objects_dict.values():
			if isinstance(o, Panel):
				p = o
				break

		for o in self.objects_dict.values():
			if isinstance(o, Button):
				o.set_parent(p)

	def next_object_id(self) -> int:
		self._next_object_id += 1
		return self._next_object_id

	def add_all(self, obj_list: List[DrawnGameObject]) -> List[DrawnGameObject]:
		return [self.add(obj) for obj in obj_list]

	def add(self, obj: DrawnGameObject) -> DrawnGameObject:
		new_id = self.next_object_id()
		obj.object_id = new_id
		self.objects_dict[new_id] = obj
		return obj

	def trigger_self_destruct(self, object_id: int) -> bool:
		if object_id in self.objects_dict and self.objects_dict[object_id].self_destruct():
			self.objects_dict[object_id] = None
			return True
		return False
