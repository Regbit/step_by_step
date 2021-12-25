from typing import Dict

from step_by_step.common.vector import Vector3i
from step_by_step.game.objects.gui.elements.gui_element import GUIElement
from step_by_step.game.objects.settings import SpriteType
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.objects.sprites.gui.button import (
	ButtonDefaultSprite,
	ButtonHighlightedSprite,
	ButtonClickedSprite,
)
from step_by_step.graphics.objects.sprites.sprite import Sprite
from step_by_step.graphics.settings import AnchorHorizontal, AnchorVertical, Alignment


class Button(GUIElement):

	_base_name = 'Button'

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
				SpriteType.DEFAULT: ButtonDefaultSprite(
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
				SpriteType.HIGHLIGHTED: ButtonHighlightedSprite(
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
				),
				SpriteType.CLICKED: ButtonClickedSprite(
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