from __future__ import annotations

from typing import List, Tuple

from step_by_step.common.shaped import Shaped
from step_by_step.common.vector import Vector2f
from step_by_step.graphics.label_extension import LabelExtension
from step_by_step.graphics.objects.screen_object import ScreenObject
from step_by_step.graphics.objects.settings import BatchGroup


class Sprite(Shaped):

	_batch_group: BatchGroup = BatchGroup.DEFAULT
	_text_batch_group = BatchGroup.DEFAULT
	_screen_object_stack: List[ScreenObject]
	_label_stack: List[LabelExtension]

	do_draw: bool

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		batch_group: BatchGroup,
		text_batch_group: BatchGroup,
		screen_object_stack: List[ScreenObject],
		label_stack: List[LabelExtension],
		do_draw: bool
	):
		super(Sprite, self).__init__(
			pos=pos,
			size=size
		)

		self._batch_group = batch_group
		self._text_batch_group = text_batch_group
		self._screen_object_stack = screen_object_stack or []
		self._label_stack = label_stack or []

		self.do_draw = do_draw

	@property
	def batch_group(self) -> BatchGroup:
		return self._batch_group

	@property
	def text_batch_group(self) -> BatchGroup:
		return self._text_batch_group

	@property
	def screen_object_stack(self) -> List[ScreenObject]:
		return self._screen_object_stack

	@property
	def label_stack(self) -> List[LabelExtension]:
		return self._label_stack

	@property
	def screen_data(self) -> Tuple[Vector2f, Vector2f]:
		return self.pos, self.size

	@property
	def visibility_vertices(self) -> List[Vector2f]:
		return [
			Vector2f(self.pos.x - self.size.x, self.pos.y - self.size.y),
			Vector2f(self.pos.x - self.size.x, self.pos.y + self.size.y),
			Vector2f(self.pos.x + self.size.x, self.pos.y + self.size.y),
			Vector2f(self.pos.x + self.size.x, self.pos.y - self.size.y),
		]

	def set_pos(self, pos: Vector2f):
		self._pos = pos
		for screen_object in self.screen_object_stack:
			screen_object.set_pos(pos=pos)
		for label in self.label_stack:
			label.x, label.y = pos.tuple

	def rotate(self, rad: float):
		# TODO maybe needs self.orientation_rad
		for screen_object in self.screen_object_stack:
			screen_object.rotate(rad=rad)
