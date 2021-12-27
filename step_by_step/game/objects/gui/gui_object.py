from __future__ import annotations

from typing import Dict

from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import DrawnGameObject
from step_by_step.game.objects.settings import SpriteType
from step_by_step.graphics.sprites.sprite import Sprite


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


