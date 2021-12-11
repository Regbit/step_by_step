from __future__ import annotations

import abc
import logging
from typing import Optional, List, Tuple

from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.settings import NO_BASE_NAME
from step_by_step.graphics.draw_data import DrawData
from step_by_step.graphics.objects.screen_object import ScreenObject
from step_by_step.graphics.objects.settings import BatchGroup

log = logging.getLogger('Game Object')


class _BaseGameObject(abc.ABC):

	_base_name: str = NO_BASE_NAME
	_name: Optional[str] = None
	object_id: int
	parent: Optional[_BaseGameObject] = None
	children: Optional[List[_BaseGameObject]] = None

	@property
	def name(self) -> str:
		return self._name if self._name else self._base_name

	def rename(self, new_name: str):
		if new_name:
			self._name = new_name

	def self_destruct(self) -> bool:
		try:
			if self.parent:
				self.parent = None
			if self.children:
				self.children = None
			self.self_destruct_clean_up()
			del self
			return True
		except Exception as e:
			log.error(e)
			return False

	@abc.abstractmethod
	def self_destruct_clean_up(self):
		raise NotImplementedError()


class GameObject(_BaseGameObject):

	def __str__(self):
		return f'{self.name}({self.__class__.__name__}) #{self.object_id}'


class DrawnGameObject(GameObject):

	_base_name = 'Game Object'

	is_selectable: bool
	pos: Vector2f
	size: Vector2f
	orientation_vec: Vector2f
	_batch_group: BatchGroup = BatchGroup.DEFAULT
	_background_drawable: ScreenObject = None
	_main_drawable: ScreenObject = None
	_foreground_drawable: ScreenObject = None

	def self_destruct_clean_up(self):
		self.pos = None
		self.size = None
		self.orientation_vec = None
		self._background_drawable = None
		self._main_drawable = None
		self._foreground_drawable = None

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		is_selectable: bool,
		orientation_vec: Vector2f = None,
		background_drawable: ScreenObject = None,
		main_drawable: ScreenObject = None,
		foreground_drawable: ScreenObject = None
	):
		super(DrawnGameObject, self).__init__()
		self.pos = pos
		self.size = size
		self.is_selectable = is_selectable
		self.orientation_vec = orientation_vec if orientation_vec else Vector2f(0, 1)
		self._background_drawable = background_drawable
		self._main_drawable = main_drawable
		self._foreground_drawable = foreground_drawable

	@property
	def background_drawable(self) -> ScreenObject:
		return self._background_drawable

	@property
	def main_drawable(self) -> ScreenObject:
		return self._main_drawable

	@property
	def foreground_drawable(self) -> ScreenObject:
		return self._foreground_drawable

	@property
	def drawable_list(self) -> List[ScreenObject]:
		out = []
		if self.background_drawable:
			out.append(self.background_drawable)
		if self.main_drawable:
			out.append(self.main_drawable)
		if self.foreground_drawable:
			out.append(self.foreground_drawable)
		return out

	@property
	def draw_data(self) -> List[DrawData]:
		out = []
		for drawable in self.drawable_list:
			if drawable.do_draw:
				out.append(drawable.draw_data)
		return out

	@property
	def visibility_vertices(self) -> List[Vector2f]:
		return [
			Vector2f(self.pos.x - self.size.x, self.pos.y - self.size.y),
			Vector2f(self.pos.x - self.size.x, self.pos.y + self.size.y),
			Vector2f(self.pos.x + self.size.x, self.pos.y + self.size.y),
			Vector2f(self.pos.x + self.size.x, self.pos.y - self.size.y),
		]

	@property
	def x(self) -> float:
		return self.pos.x

	@property
	def y(self) -> float:
		return self.pos.y

	@property
	def screen_data(self) -> Tuple[Vector2f, Vector2f]:
		return self._main_drawable.screen_data

	@property
	def batch_group(self) -> BatchGroup:
		return self._batch_group

	def rotate(self, rad: float):
		self.orientation_vec.rotate(rad)
		for drawable in self.drawable_list:
			drawable.rotate(rad)

	def select(self) -> bool:
		if self.is_selectable and self.foreground_drawable:
			self.foreground_drawable.do_draw = True
			self.foreground_drawable.set_batch(BatchGroup.SELECTED_OBJECT)
			return True
		else:
			return False

	def deselect(self) -> bool:
		if self.is_selectable and self.foreground_drawable:
			self.foreground_drawable.do_draw = False
			self.foreground_drawable.set_batch(None)
			return True
		else:
			return False
