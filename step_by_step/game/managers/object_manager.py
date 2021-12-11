from typing import Dict, Optional, List

from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.world_object import GameObject
from step_by_step.game.objects.path import Waypoint, Trajectory
from step_by_step.game.objects.unit import Building, ResourceNode, Vehicle


class ObjectManager:
	_next_object_id = -1
	objects_dict: Dict[int, Optional[GameObject]] = dict()

	def __init__(self):
		self.add_all(
			[
				Building(Vector2f(200, 100)),
				ResourceNode(Vector2f(1000, 1000)),
				Vehicle(Vector2f(100, 100)),
				Waypoint(Vector2f(300, 100)),
				Trajectory(Vector2f(100, 100), Vector2f(300, 100)),
			]
		)

	def next_object_id(self) -> int:
		self._next_object_id += 1
		return self._next_object_id

	def add_all(self, obj_list: List[GameObject]) -> List[GameObject]:
		return [self.add(obj) for obj in obj_list]

	def add(self, obj: GameObject) -> GameObject:
		new_id = self.next_object_id()
		obj.object_id = new_id
		self.objects_dict[new_id] = obj
		return obj

	def trigger_self_destruct(self, object_id: int) -> bool:
		if object_id in self.objects_dict and self.objects_dict[object_id].self_destruct():
			self.objects_dict[object_id] = None
			return True
		return False
