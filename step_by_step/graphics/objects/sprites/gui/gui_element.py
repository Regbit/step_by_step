from __future__ import annotations

import abc
from typing import List

from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.graphics.color import Color
from step_by_step.graphics.label_extension import LabelExtension
from step_by_step.graphics.objects.screen_object import ScreenObject
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.objects.sprites.sprite import Sprite
from step_by_step.graphics.objects.square import SelectionBorder, Rectangle
from step_by_step.graphics.settings import AnchorHorizontal, AnchorVertical, Alignment


class BaseGUIElementSprite(Sprite):

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		batch_group: BatchGroup,
		text_batch_group: BatchGroup,
		do_draw: bool,
		color: Vector3i,
		border_width: int,
		border_color: Vector3i,
		text: str,
		text_color: Vector3i,
		anchor_x: AnchorHorizontal,
		anchor_y: AnchorVertical,
		align: Alignment
	):
		super(BaseGUIElementSprite, self).__init__(
			pos=pos,
			size=size,
			batch_group=batch_group,
			text_batch_group=text_batch_group,
			screen_object_stack=[],
			label_stack=[],
			do_draw=do_draw,
		)

		self._screen_object_stack = self._make_screen_object_stack(
			color=color,
			border_width=border_width,
			border_color=border_color,
		)
		self._label_stack = self._make_label_stack(
			color=color,
			text=text,
			text_color=text_color,
			anchor_x=anchor_x,
			anchor_y=anchor_y,
			align=align,
		)

	@abc.abstractmethod
	def _make_screen_object_stack(
			self,
			color: Vector3i,
			border_width: int,
			border_color: Vector3i,
	) -> List[ScreenObject]:
		raise NotImplementedError()

	def _make_label_stack(
		self,
		color: Vector3i,
		text: str,
		text_color: Vector3i,
		anchor_x: AnchorHorizontal,
		anchor_y: AnchorVertical,
		align: Alignment
	) -> List[LabelExtension]:
		return [
			LabelExtension(
					pos=self.pos,
					size=self.size,
					text=text,
					font_size=round(self.size.y * 0.5),
					color=text_color if text_color else color / 3,
					anchor_x=anchor_x,
					anchor_y=anchor_y,
					align=align
				)
			]


class GUIElementDefaultSprite(BaseGUIElementSprite):

	def _make_screen_object_stack(
			self,
			border_width: int,
			border_color: Vector3i,
			color: Vector3i,
	) -> List[ScreenObject]:
		screen_object_stack = []
		if border_width:
			screen_object_stack.append(
				Rectangle(
					pos=self.pos,
					size=self.size,
					color=border_color,
					base_batch=self.batch_group,
				)
			)

		screen_object_stack.append(
			Rectangle(
				pos=self.pos,
				size=self.size - (Vector2f(border_width * 2, border_width * 2) if border_width else Vector2f(0, 0)),
				color=color,
				base_batch=self.batch_group
			)
		)
		return screen_object_stack


class GUIElementSelectedSprite(BaseGUIElementSprite):

	def _make_screen_object_stack(
			self,
			border_width: int,
			border_color: Vector3i,
			color: Vector3i,
	) -> List[ScreenObject]:
		screen_object_stack = []
		if border_width:
			screen_object_stack.append(
				Rectangle(
					pos=self.pos,
					size=self.size,
					color=border_color,
					base_batch=self.batch_group,
				)
			)

		screen_object_stack.append(
			Rectangle(
				pos=self.pos,
				size=self.size - (Vector2f(border_width * 2, border_width * 2) if border_width else Vector2f(0, 0)),
				color=color,
				base_batch=self.batch_group
			)
		)

		screen_object_stack.append(
			SelectionBorder(
				pos=self.pos,
				size=self.size + Vector2f(4, 4),
				base_batch=self.batch_group
			)
		)

		return screen_object_stack


class GUIElementHighlightedSprite(BaseGUIElementSprite):

	def _make_screen_object_stack(
			self,
			border_width: int,
			border_color: Vector3i,
			color: Vector3i,
	) -> List[ScreenObject]:
		diff = Color.WHITE.value - color
		screen_object_stack = []
		if border_width:
			screen_object_stack.append(
				Rectangle(
					pos=self.pos,
					size=self.size,
					color=border_color,
					base_batch=self.batch_group,
				)
			)
		screen_object_stack.append(
			Rectangle(
				pos=self.pos,
				size=self.size - (Vector2f(border_width * 2, border_width * 2) if border_width else Vector2f(0, 0)),
				color=color + diff * 0.2,
				base_batch=self.batch_group
			)
		)

		return screen_object_stack


class GUIElementClickedSprite(BaseGUIElementSprite):

	def _make_screen_object_stack(
			self,
			border_width: int,
			border_color: Vector3i,
			color: Vector3i,
	) -> List[ScreenObject]:
		diff = Color.WHITE.value - color
		screen_object_stack = []
		if border_width:
			screen_object_stack.append(
				Rectangle(
					pos=self.pos,
					size=self.size,
					color=border_color,
					base_batch=self.batch_group,
				)
			)

		screen_object_stack.append(
			Rectangle(
				pos=self.pos,
				size=self.size - (Vector2f(border_width * 2, border_width * 2) if border_width else Vector2f(0, 0)),
				color=color + diff * 0.4,
				base_batch=self.batch_group
			)
		)

		return screen_object_stack
