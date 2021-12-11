from typing import Dict, Optional, TYPE_CHECKING
if TYPE_CHECKING:
	from step_by_step.game.objects.world_object import GameObject


class ObjectManager:
	_next_object_id = -1
	objects_dict: Dict[int, Optional['GameObject']] = dict()

	@classmethod
	def next_object_id(cls) -> int:
		cls._next_object_id += 1
		return cls._next_object_id

	@classmethod
	def add(cls, obj: 'GameObject') -> int:
		new_id = cls.next_object_id()
		cls.objects_dict[new_id] = obj
		return new_id

	@classmethod
	def trigger_self_destruct(cls, object_id: int) -> bool:
		if object_id in cls.objects_dict and cls.objects_dict[object_id].self_destruct():
			cls.objects_dict[object_id] = None
			return True
		return False
