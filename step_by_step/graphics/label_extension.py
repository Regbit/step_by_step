from pathlib import Path

from pyglet import font
from pyglet.text import Label

from step_by_step.common.vector import Vector3i, Vector2f
from step_by_step.graphics.settings import (
	Alignment,
	AnchorHorizontal,
	AnchorVertical,
	BASE_FONT,
	BASE_FONT_SIZE,
)
from step_by_step.graphics.color import Color

path = Path(__file__).parent.parent.absolute().joinpath('resources/fonts/')
font.add_directory(Path.joinpath(path))
oswald = font.load('Oswald')


class LabelExtension(Label):

	def __init__(
			self,
			pos: Vector2f,
			size: Vector2f,
			text: str = '',
			font_name: str = BASE_FONT,
			font_size: int = BASE_FONT_SIZE,
			bold: bool = False,
			italic: bool = False,
			color: Vector3i = Color.WHITE.value,
			anchor_x: AnchorHorizontal = AnchorHorizontal.CENTER,
			anchor_y: AnchorVertical = AnchorVertical.CENTER,
			align: Alignment = Alignment.CENTER,
			text_padding: int = 0
	):
		super(LabelExtension, self).__init__(
			text=text,
			font_name=font_name,
			font_size=font_size,
			bold=bold,
			italic=italic,
			color=tuple(color.list + [255]),
			x=pos.x,
			y=pos.y,
			width=size.x - text_padding * 2,
			height=size.y - text_padding * 2,
			anchor_x=anchor_x.value,
			anchor_y=anchor_y.value,
			align=align.value,
			multiline=True
		)
