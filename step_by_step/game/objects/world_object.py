from __future__ import annotations

import abc
import logging
from typing import Optional, List, Tuple, Union

from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.settings import NO_BASE_NAME
from step_by_step.graphics.draw_data import DrawData
from step_by_step.graphics.screen_object import ScreenObject
from step_by_step.graphics.settings import BatchGroup


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


class WorldObject(GameObject):

	_base_name = 'World Object'

	is_selectable: bool
	is_movable: bool
	world_pos: Vector2f
	size: Vector2f
	movement_velocity: float
	rotation_velocity: float
	orientation_vec: Vector2f
	_batch_group: BatchGroup = BatchGroup.DEFAULT
	_background_drawable: ScreenObject = None
	_main_drawable: ScreenObject = None
	_foreground_drawable: ScreenObject = None

	@property
	def drawable_list(self) -> List[ScreenObject]:
		out = []
		if self._background_drawable:
			out.append(self._background_drawable)
		if self._main_drawable:
			out.append(self._main_drawable)
		if self._foreground_drawable:
			out.append(self._foreground_drawable)
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
			Vector2f(self.world_pos.x - self.size.x, self.world_pos.y - self.size.y),
			Vector2f(self.world_pos.x - self.size.x, self.world_pos.y + self.size.y),
			Vector2f(self.world_pos.x + self.size.x, self.world_pos.y + self.size.y),
			Vector2f(self.world_pos.x + self.size.x, self.world_pos.y - self.size.y),
		]

	@property
	def x(self) -> float:
		return self.world_pos.x

	@property
	def y(self) -> float:
		return self.world_pos.y

	@property
	def screen_data(self) -> Tuple[Vector2f, Vector2f]:
		return self._main_drawable.screen_data

	def rotate(self, rad: float):
		self.orientation_vec.rotate(rad)
		for drawable in self.drawable_list:
			drawable.rotate(rad)

	def rotate_towards(self, destination: Vector2f):
		vec = destination - self.world_pos
		angle = self.orientation_vec.angle_between(vec)
		if abs(angle) > 0.001:
			mul = 1 if angle > 0 else -1
			to_rotate = self.rotation_velocity * mul if abs(angle) > self.rotation_velocity else angle
			self.rotate(to_rotate)

	def move(self, vec: Union[Vector2f, float]):
		if isinstance(vec, (int, float)):
			dist = vec
			vec = self.orientation_vec.copy()
			vec.set_len(dist)
		self.world_pos += vec
		for drawable in self.drawable_list:
			drawable.move(dir_vec=vec)

	def move_towards(self, destination: Vector2f):
		dist = self.world_pos.dist(destination)
		to_travel = self.movement_velocity if dist > self.movement_velocity else dist
		self.move(Vector2f(r=to_travel, a=self.orientation_vec.a))

	def select(self) -> bool:
		if self.is_selectable and self._foreground_drawable:
			self._foreground_drawable.do_draw = True
			self._foreground_drawable.set_batch(BatchGroup.SELECTED_OBJECT)
			return True
		else:
			return False

	def deselect(self) -> bool:
		if self.is_selectable and self._foreground_drawable:
			self._foreground_drawable.do_draw = False
			self._foreground_drawable.set_batch(None)
			return True
		else:
			return False

	def self_destruct_clean_up(self):
		self.world_pos = None
		self.size = None
		self.orientation_vec = None
		self._background_drawable = None
		self._main_drawable = None
		self._foreground_drawable = None

	def __init__(
		self,
		world_pos: Vector2f,
		size: Vector2f,
		is_selectable: bool,
		is_movable: bool,
		movement_velocity: float,
		rotation_velocity: float,
		orientation_vec: Vector2f = None,
		background_drawable: ScreenObject = None,
		main_drawable: ScreenObject = None,
		foreground_drawable: ScreenObject = None
	):
		super(WorldObject, self).__init__()
		self.world_pos = world_pos
		self.size = size
		self.is_selectable = is_selectable
		self.is_movable = is_movable
		self.movement_velocity = movement_velocity
		self.rotation_velocity = rotation_velocity
		self.orientation_vec = orientation_vec if orientation_vec else Vector2f(0, 1)
		self._background_drawable = background_drawable
		self._main_drawable = main_drawable
		self._foreground_drawable = foreground_drawable
