from typing import Dict

from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.game.objects.settings import SpriteType
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.objects.sprites.gui.gui_element import GUIElementDefaultSprite, GUIElementSelectedSprite
from step_by_step.graphics.objects.sprites.sprite import Sprite
from step_by_step.graphics.settings import Alignment, AnchorHorizontal, AnchorVertical


class GUIElement(GUIObject):

	_base_name = 'GUI Element'

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		sprites: Dict[SpriteType, Sprite] = None,
		color: Vector3i = Vector3i(0, 0, 0),
		text: str = None,
		text_color: Vector3i = None,
		border_width: int = 0,
		border_color: Vector3i = None,
		anchor_x: AnchorHorizontal = AnchorHorizontal.CENTER,
		anchor_y: AnchorVertical = AnchorVertical.CENTER,
		align: Alignment = Alignment.LEFT
	):
		super(GUIElement, self).__init__(
			pos=pos,
			size=size,
		)
		self._sprites = self._make_sprites(
			sprites=sprites,
			color=color,
			text=text,
			text_color=text_color,
			border_width=border_width,
			border_color=border_color,
			anchor_x=anchor_x,
			anchor_y=anchor_y,
			align=align,
		)

	def _make_sprites(
		self,
		sprites: Dict[SpriteType, Sprite],
		color: Vector3i,
		text: str,
		text_color: Vector3i,
		border_width: int,
		border_color: Vector3i,
		anchor_x: AnchorHorizontal,
		anchor_y: AnchorVertical,
		align: Alignment
	) -> Dict[SpriteType, Sprite]:
		return sprites or {
				SpriteType.DEFAULT: GUIElementDefaultSprite(
					pos=self.pos,
					size=self.size,
					batch_group=BatchGroup.GUI_OBJECT,
					text_batch_group=BatchGroup.GUI_TEXT_OBJECT,
					do_draw=True,
					color=color,
					text=text,
					text_color=text_color,
					border_width=border_width,
					border_color=border_color,
					anchor_x=anchor_x,
					anchor_y=anchor_y,
					align=align
				),
				SpriteType.SELECTED: GUIElementSelectedSprite(
					pos=self.pos,
					size=self.size,
					batch_group=BatchGroup.GUI_OBJECT,
					text_batch_group=BatchGroup.GUI_TEXT_OBJECT,
					do_draw=False,
					color=color,
					text=text,
					text_color=text_color,
					border_width=border_width,
					border_color=border_color,
					anchor_x=anchor_x,
					anchor_y=anchor_y,
					align=align
				)
			}

