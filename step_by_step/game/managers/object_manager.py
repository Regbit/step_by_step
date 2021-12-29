from functools import cached_property
from typing import Dict, Optional, Set, List

from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import GameObject, DrawnGameObject
from step_by_step.game.objects.units import Building, ResourceNode, Vehicle
from step_by_step.game.objects.gui.gui_object import GUIObject


class ObjectManager:

	_next_object_id = -1
	_objects_dict: Dict[int, Optional[GameObject]] = dict()

	def __init__(self):
		self._test_init()

	@cached_property
	def drawn_object_list(self) -> List[DrawnGameObject]:
		return [o for o in self._objects_dict.values() if isinstance(o, DrawnGameObject)]

	@property
	def objects_dict(self) -> Dict[int, Optional[GameObject]]:
		return self._objects_dict

	def _test_init(self):
		# TODO remove
		self.add_all(
			{
				Building(pos=Vector2f(200, 100)),
				ResourceNode(pos=Vector2f(1000, 1000)),
				Vehicle(pos=Vector2f(100, 100))
			}
		)

	def next_object_id(self) -> int:
		self._next_object_id += 1
		return self._next_object_id

	def add_all(self, obj_list: Set[GameObject]) -> Set[GameObject]:
		return {self.add(obj) for obj in obj_list if isinstance(obj, GameObject)}

	def add(self, obj: GameObject) -> GameObject:
		if obj not in self.objects_dict.values():
			new_id = self.next_object_id()
			obj.object_id = new_id
			self.objects_dict[new_id] = obj

			if isinstance(obj, GUIObject):
				self.add_all(obj.all_children_in_hierarchy)

			return obj

	def trigger_self_destruct(self, object_id: int) -> bool:
		if object_id in self.objects_dict and self.objects_dict[object_id].self_destruct():
			self.objects_dict[object_id] = None
			return True
		return False
