from pyglet.text import Label as _Label

from step_by_step.common.vector import Vector3i, Vector2f


class Label(_Label):

	def __init__(
			self,
			pos: Vector2f,
			size: Vector2f,
			text: str = '',
			font_name: str = 'Oswald',
			font_size: int = 10,
			bold: bool = False,
			italic: bool = False,
			color: Vector3i = Vector3i(255, 255, 255),
			anchor_x: str = 'center',
			anchor_y: str = 'center',
			align: str = 'center',
			text_padding: int = 0
	):
		super(Label, self).__init__(
			text=text,
			font_name=font_name,
			font_size=font_size,
			bold=bold,
			italic=italic,
			color=tuple(color.list + [255]),
			x=pos.x,
			y=pos.y,
			width=size.x - text_padding,
			height=size.y - text_padding,
			anchor_x=anchor_x,
			anchor_y=anchor_y,
			align=align,
			multiline=True
		)
