from __future__ import annotations

import abc
import logging
from typing import Optional, List, Tuple, Union, Dict, Set, OrderedDict

from pyglet.graphics import Batch

from step_by_step.common.shaped import Shaped
from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.settings import NO_BASE_NAME, SpriteType
from step_by_step.graphics.draw_data import DrawData
from step_by_step.graphics.label_extension import LabelExtension
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.sprites.sprite import Sprite

log = logging.getLogger('Game Object')


class ParenthoodError(Exception):
	pass


class SelfParenthoodError(ParenthoodError):
	pass


class CircularParenthoodError(ParenthoodError):
	pass


class ExistingParenthoodError(ParenthoodError):
	pass


class ClassParenthoodError(ParenthoodError):
	pass


class _BaseGameObject(abc.ABC):

	_name: Optional[str] = None

	object_id: int = None

	@property
	def _base_name(self) -> str:
		return NO_BASE_NAME

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
		self.change_parent(None)
		for _ in self._children:
			del _
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
		self._parent_pos = None

	def __str__(self):
		return f'{self.name}({self.__class__.__name__}) #{self.object_id}'

	@property
	def children(self) -> List[GameObject]:
		return self._children

	@property
	def parent(self) -> GameObject:
		return self._parent

	@property
	def pos(self) -> Vector2f:
		if self._parent:
			return self._pos + self._parent.pos
		else:
			return self._pos

	@pos.setter
	def pos(self, pos: Vector2f):
		self._pos = pos

	@property
	def size(self) -> Vector2f:
		return super(GameObject, self).size

	@size.setter
	def size(self, new_size: Vector2f):
		self._size = new_size

	@property
	def all_children_in_hierarchy(self) -> Set[GameObject]:
		out = set()
		for c in self._children:
			if isinstance(c, GameObject):
				out.add(c)
				out.update(c.all_children_in_hierarchy)

		return out

	def _change_parent_logic_check(self, parent: Optional[GameObject]):
		if parent:
			child = self

			if parent is child:
				raise SelfParenthoodError(
					f"Object can't be a parent of itself!"
					f"Object: '{child}'"
				)
			if parent in child._children:
				raise CircularParenthoodError(
					f"Object can't be a parent of it's parent!"
					f"Object: '{parent}'"
					f"Parent: '{child}'"
				)
			if child in parent._children:
				raise ExistingParenthoodError(
					f"Object is already a child of the parent!"
					f"Object: '{child}'"
					f"Parent: '{parent}'"
				)

	def change_parent(self, parent: Optional[GameObject]):
		child = self

		# Logic checks
		self._change_parent_logic_check(parent=parent)

		# Action
		if parent:
			parent.children.append(child)
			if child.parent:
				child.parent._children.remove(child)
			child._parent = parent
		else:
			child.parent.children.remove(child)
			child._parent = None

	def add_child(self, obj: GameObject):
		obj.change_parent(self)

	def add_children(self, obj_list: List[GameObject]):
		for o in obj_list:
			o.change_parent(self)


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
	def draw_data_list(self) -> List[DrawData]:
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

	def change_parent(self, parent: Optional[GameObject]):
		super(DrawnGameObject, self).change_parent(parent=parent)
		self._set_sprite_pos(self.pos)

	def enrich_batches(self, batches: OrderedDict[str, Batch], cam_world_pos: Vector2f):
		for draw_data in self.draw_data_list:
			batches[draw_data.batch.value].add(
				draw_data.count,
				draw_data.mode.value,
				draw_data.group,
				*draw_data.camera_adjusted_draw_data(cam_world_pos=cam_world_pos)
			)
		for label in self.labels:
			label.batch = batches[self.text_batch_group.value]

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
