from __future__ import annotations

import abc
import logging
from typing import Optional, List, Tuple, Union, Dict, Set

from step_by_step.common.shaped import Shaped
from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.settings import NO_BASE_NAME, SpriteType
from step_by_step.graphics.draw_data import DrawData
from step_by_step.graphics.label_extension import LabelExtension
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.objects.sprites.sprite import Sprite

log = logging.getLogger('Game Object')


class _BaseGameObject(abc.ABC):

	_base_name: str = NO_BASE_NAME
	_name: Optional[str] = None

	object_id: int

	@property
	def name(self) -> str:
		return self._name if self._name else self._base_name

	def rename(self, new_name: str):
		if new_name:
			self._name = new_name

	def self_destruct(self) -> bool:
		try:
			self.self_destruct_clean_up()
			del self
			return True
		except Exception as e:
			log.error(e)
			return False

	@abc.abstractmethod
	def self_destruct_clean_up(self):
		raise NotImplementedError()


class GameObject(_BaseGameObject, Shaped):

	_base_name = 'Game Object'

	_parent: Optional[GameObject] = None
	_children: Optional[List[GameObject]] = None

	def self_destruct_clean_up(self):
		self._parent = None
		self._children = None

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
	):
		super(GameObject, self).__init__(
			pos=pos,
			size=size
		)

		self._children = list()

	def __str__(self):
		return f'{self.name}({self.__class__.__name__}) #{self.object_id}'

	@property
	def all_children(self) -> Set[GameObject]:
		out = set()
		for c in self._children:
			if isinstance(c, GameObject):
				out.add(c)
				out.update(c.all_children)

		return out

	def unset_parent(self):
		if self._parent and isinstance(self._parent, GameObject):
			self._unset_parent_dimensions_change(self._parent)
			self._parent = None

	def _unset_parent_dimensions_change(self, parent_obj: GameObject):
		self.pos -= parent_obj.pos

	def set_parent(self, parent_obj: GameObject):
		self.unset_parent()
		self._parent = parent_obj
		self._set_parent_dimensions_change(parent_obj=parent_obj)

	def _set_parent_dimensions_change(self, parent_obj: GameObject):
		self.pos += parent_obj.pos

	def remove_child(self, obj: GameObject):
		obj.unset_parent()
		self._children.remove(obj)

	def add_child(self, obj: GameObject):
		obj.set_parent(self)
		if obj not in self._children:
			self._children.append(obj)

	def add_children(self, obj_list: List[GameObject]):
		for o in obj_list:
			self.add_child(o)


class DrawnGameObject(GameObject):

	_base_name = 'Drawn Game Object'

	_state: SpriteType
	_sprites: Dict[SpriteType, Sprite] = None
	_is_visible: bool

	orientation_vec: Vector2f

	def self_destruct_clean_up(self):
		self._sprites = None
		self.orientation_vec = None

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		orientation_vec: Vector2f = None,
		sprites: Dict[SpriteType, Sprite] = None,
		state: SpriteType = SpriteType.DEFAULT,
		is_visible: bool = True,
	):
		super(DrawnGameObject, self).__init__(
			pos=pos,
			size=size
		)

		self._sprites = sprites or {}
		self._state = state
		self._is_visible = is_visible
		self.orientation_vec = orientation_vec if orientation_vec else Vector2f(0, 1)

	@property
	def state(self) -> SpriteType:
		return self._state

	@state.setter
	def state(self, new_state: SpriteType):
		if new_state in self.sprites:
			self.drawn_sprite.do_draw = False
			self._state = new_state
			self.drawn_sprite.do_draw = True

	@property
	def sprites(self) -> Dict[SpriteType, Sprite]:
		return self._sprites

	@property
	def drawn_sprite(self) -> Sprite:
		return self._sprites.get(self._state)

	@property
	def is_highlightable(self) -> bool:
		return SpriteType.HIGHLIGHTED in self.sprites

	@property
	def is_clickable(self) -> bool:
		return SpriteType.CLICKED in self.sprites

	@property
	def is_selectable(self) -> bool:
		return SpriteType.SELECTED in self.sprites

	@property
	def draw_data(self) -> List[DrawData]:
		out = []
		if self.drawn_sprite and self.drawn_sprite.do_draw:
			for drawable in self.drawn_sprite.screen_object_stack:
				out.append(drawable.draw_data)
		return out

	@property
	def labels(self) -> List[LabelExtension]:
		return self.drawn_sprite.label_stack

	@property
	def visibility_vertices(self) -> List[Vector2f]:
		return self.drawn_sprite.visibility_vertices

	@property
	def pos(self) -> Vector2f:
		return self._pos

	@pos.setter
	def pos(self, pos: Vector2f):
		self._pos = pos
		self._set_sprite_pos(pos)

	@property
	def screen_data(self) -> Tuple[Vector2f, Vector2f]:
		return self.drawn_sprite.screen_data

	@property
	def batch_group(self) -> BatchGroup:
		return self.drawn_sprite.batch_group

	@property
	def text_batch_group(self) -> BatchGroup:
		return self.drawn_sprite.text_batch_group

	@property
	def is_visible(self) -> bool:
		return self._is_visible

	@is_visible.setter
	def is_visible(self, is_visible: bool):
		self._is_visible = is_visible
		for ch in self._children:
			ch.is_visible = is_visible

	def _set_sprite_pos(self, pos: Vector2f):
		for sprite in self.sprites.values():
			sprite.set_pos(pos=pos)

	def rotate(self, rad: float):
		self.orientation_vec.rotate(rad)
		for sprite in self.sprites.values():
			sprite.rotate(rad=rad)

	def move(self, vec: Union[Vector2f, float]):
		if isinstance(vec, (int, float)):
			dist = vec
			vec = self.orientation_vec.copy
			vec.set_len(dist)
		self.pos += vec

	def select(self) -> bool:
		if self.is_selectable:
			self.state = SpriteType.SELECTED
			# TODO check batch change
			return True
		else:
			return False

	def deselect(self) -> bool:
		if self.is_selectable:
			if self.is_highlightable:
				self.state = SpriteType.HIGHLIGHTED
			else:
				self.state = SpriteType.DEFAULT
			return True
		else:
			return False

	def highlight(self) -> bool:
		if self.is_highlightable:
			self.state = SpriteType.HIGHLIGHTED
			return True
		else:
			return False

	def dehighlight(self) -> bool:
		if self.is_highlightable:
			self.state = SpriteType.DEFAULT
			return True
		else:
			return False

	def click(self) -> bool:
		if self.is_clickable:
			self.state = SpriteType.CLICKED
			return True
		else:
			return False

	def declick(self) -> bool:
		if self.is_clickable:
			if self.is_highlightable:
				self.state = SpriteType.HIGHLIGHTED
			else:
				self.state = SpriteType.DEFAULT
			return True
		else:
			return False
