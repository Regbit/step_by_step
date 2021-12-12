from __future__ import annotations

from typing import Union

from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import DrawnGameObject
from step_by_step.game.objects.settings import ALIGN_ANGLE_THRESHOLD
from step_by_step.graphics.objects.screen_object import ScreenObject


class WorldObject(DrawnGameObject):

	_base_name = 'World Object'

	is_movable: bool
	movement_velocity: float
	rotation_velocity: float

	def __init__(
		self,
		pos: Vector2f,
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
		super(WorldObject, self).__init__(
			pos=pos,
			size=size,
			is_selectable=is_selectable,
			orientation_vec=orientation_vec,
			background_drawable=background_drawable,
			main_drawable=main_drawable,
			foreground_drawable=foreground_drawable,
		)
		self.is_movable = is_movable
		self.movement_velocity = movement_velocity
		self.rotation_velocity = rotation_velocity

	def rotate_towards(self, destination: Vector2f):
		vec = destination - self._pos
		angle = self.orientation_vec.angle_between(vec)
		if abs(angle) > ALIGN_ANGLE_THRESHOLD:
			mul = 1 if angle > 0 else -1
			to_rotate = self.rotation_velocity * mul if abs(angle) > self.rotation_velocity else angle
			self.rotate(to_rotate)

	def move_towards(self, destination: Vector2f):
		dist = self._pos.dist(destination)
		to_travel = self.movement_velocity if dist > self.movement_velocity else dist
		self.move(Vector2f(r=to_travel, a=self.orientation_vec.a))
