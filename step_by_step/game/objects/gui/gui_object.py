from __future__ import annotations

from typing import Dict, Optional

from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import DrawnGameObject, GameObject
from step_by_step.game.objects.gui.settings import LayoutStyleCompatibilityError, LayoutStyle, POSSIBLE_LAYOUTS
from step_by_step.game.objects.settings import SpriteType
from step_by_step.graphics.sprites.sprite import Sprite


class GUIObject(DrawnGameObject):

	_base_name = 'GUI Object'

	_layout_style: LayoutStyle = None

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		sprites: Dict[SpriteType, Sprite] = None,
		orientation_vec: Vector2f = None,
		layout_style: LayoutStyle = None,
	):
		super(GUIObject, self).__init__(
			pos=pos,
			size=size,
			sprites=sprites,
			orientation_vec=orientation_vec
		)
		self._layout_style = layout_style if layout_style else LayoutStyle.ABSOLUTE

	@property
	def layout_style(self) -> LayoutStyle:
		return self._layout_style

	def _change_parent_logic_check(self, parent: Optional[GameObject]):
		super(GUIObject, self)._change_parent_logic_check(parent=parent)
		if parent and isinstance(parent, GUIObject):
			par_cls_name = type(parent).__name__
			if self.layout_style not in POSSIBLE_LAYOUTS[par_cls_name]:
				raise LayoutStyleCompatibilityError(
					f"Object with layout style '{self._layout_style}' can't be a child of '{par_cls_name}'!\n"
					f"Possible values: {POSSIBLE_LAYOUTS[par_cls_name]}"
				)
