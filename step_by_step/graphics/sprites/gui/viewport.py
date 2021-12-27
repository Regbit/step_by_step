from __future__ import annotations

from typing import Union

from step_by_step.common.shaped import Shaped
from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.graphics.color import Color
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.sprites.sprite import Sprite
from step_by_step.graphics.objects.square import Rectangle


class ViewportDefaultSprite(Sprite):

	_screen: Shaped
	_left_band: Rectangle = None
	_right_band: Rectangle = None
	_upper_band: Rectangle = None
	_lower_band: Rectangle = None

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		batch_group: BatchGroup,
		do_draw: bool,
		color: Union[Vector3i, Color],
		screen: Shaped,
	):
		color = color.value if isinstance(color, Color) else color

		self._left_band = Rectangle(
			pos=screen.pos,
			size=screen.size,
			color=color,
			base_batch_group=batch_group
		)

		self._right_band = Rectangle(
			pos=screen.pos,
			size=screen.size,
			color=color,
			base_batch_group=batch_group
		)

		self._upper_band = Rectangle(
			pos=screen.pos,
			size=screen.size,
			color=color,
			base_batch_group=batch_group
		)

		self._lower_band = Rectangle(
			pos=screen.pos,
			size=screen.size,
			color=color,
			base_batch_group=batch_group
		)

		super(ViewportDefaultSprite, self).__init__(
			pos=pos,
			size=size,
			batch_group=batch_group,
			text_batch_group=BatchGroup.GUI_TEXT_OBJECT,
			screen_object_stack=[
				self._left_band,
				self._right_band,
				self._upper_band,
				self._lower_band
			],
			label_stack=[],
			do_draw=do_draw
		)

		self._screen = screen
		self._update_bands()

	def _update_bands(self):
		diff = self.left_bound_x - self._screen.left_bound_x
		self._left_band.set_shift(Vector2f(-self._screen.w + diff, 0))

		diff = self._screen.right_bound_x - self.right_bound_x
		self._right_band.set_shift(Vector2f(self._screen.w - diff, 0))

		diff = self._screen.upper_bound_y - self.upper_bound_y
		self._upper_band.set_shift(Vector2f(0, self._screen.h - diff))

		diff = self.lower_bound_y - self._screen.lower_bound_y
		self._lower_band.set_shift(Vector2f(0, -self._screen.h + diff))

	def set_pos(self, pos: Vector2f):
		super(ViewportDefaultSprite, self).set_pos(pos=pos)
		self._update_bands()
