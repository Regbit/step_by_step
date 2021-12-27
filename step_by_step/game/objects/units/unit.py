from __future__ import annotations

from typing import Dict

from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import DrawnGameObject
from step_by_step.game.objects.settings import ALIGN_ANGLE_THRESHOLD, SpriteType
from step_by_step.graphics.sprites.sprite import Sprite


class Unit(DrawnGameObject):

	_base_name = 'Unit'

	is_movable: bool
	movement_velocity: float
	rotation_velocity: float

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		is_movable: bool,
		movement_velocity: float,
		rotation_velocity: float,
		sprites: Dict[SpriteType, Sprite],
		orientation_vec: Vector2f = None,
	):
		super(Unit, self).__init__(
			pos=pos,
			size=size,
			sprites=sprites,
			orientation_vec=orientation_vec
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
