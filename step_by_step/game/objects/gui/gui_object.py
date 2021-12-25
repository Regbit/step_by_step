from __future__ import annotations

from typing import List, Set, Dict

from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import DrawnGameObject
from step_by_step.game.objects.settings import SpriteType
from step_by_step.graphics.objects.sprites.sprite import Sprite


class GUIObject(DrawnGameObject):

	_base_name = 'GUI Object'

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		sprites: Dict[SpriteType, Sprite] = None,
		orientation_vec: Vector2f = None,
	):
		super(GUIObject, self).__init__(
			pos=pos,
			size=size,
			sprites=sprites,
			orientation_vec=orientation_vec
		)

		self._children = list()

	@property
	def all_children(self) -> Set[GUIObject]:
		out = set()
		for c in self._children:
			if isinstance(c, GUIObject):
				out.add(c)
				out.update(c.all_children)

		return out

	def unset_parent(self):
		if self._parent and isinstance(self._parent, GUIObject):
			self._unset_parent_dimensions_change(self._parent)
			self._parent = None

	def _unset_parent_dimensions_change(self, parent_obj: GUIObject):
		self.pos -= parent_obj.pos

	def set_parent(self, parent_obj: GUIObject):
		self.unset_parent()
		self._parent = parent_obj
		self._set_parent_dimensions_change(parent_obj=parent_obj)

	def _set_parent_dimensions_change(self, parent_obj: GUIObject):
		self.pos += parent_obj.pos

	def remove_child(self, obj: GUIObject):
		obj.unset_parent()
		self._children.remove(obj)

	def add_child(self, obj: GUIObject):
		obj.set_parent(self)
		if obj not in self._children:
			self._children.append(obj)

	def add_children(self, obj_list: List[GUIObject]):
		for o in obj_list:
			self.add_child(o)
