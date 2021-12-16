from __future__ import annotations

from typing import List, Set

from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import DrawnGameObject
from step_by_step.graphics.color import Color
from step_by_step.graphics.label_extension import LabelExtension
from step_by_step.graphics.objects.screen_object import ScreenObject
from step_by_step.graphics.objects.settings import BatchGroup


class GUIObject(DrawnGameObject):

	_base_name = 'GUI Object'
	_batch_group = BatchGroup.GUI_OBJECT
	_text_batch_group = BatchGroup.GUI_TEXT_OBJECT

	is_clickable: bool
	_is_visible: bool
	_main_drawable_highlighted: ScreenObject = None
	_main_drawable_clicked: ScreenObject = None
	_label: LabelExtension

	def self_destruct_clean_up(self):
		super(GUIObject, self).self_destruct_clean_up()
		self._main_drawable_highlighted = None
		self._main_drawable_clicked = None
		self._label = None

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		is_selectable: bool,
		is_clickable: bool,
		is_visible: bool = True,
		orientation_vec: Vector2f = None,
		background_drawable: ScreenObject = None,
		main_drawable: ScreenObject = None,
		foreground_drawable: ScreenObject = None,
		label: LabelExtension = None,
	):
		super(GUIObject, self).__init__(
			pos=pos,
			size=size,
			is_selectable=is_selectable,
			orientation_vec=orientation_vec,
			background_drawable=background_drawable,
			main_drawable=main_drawable,
			foreground_drawable=foreground_drawable,
		)
		self._children = set()

		self.is_clickable = is_clickable
		self._is_visible = is_visible

		if main_drawable:
			dif = (Color.WHITE.value - self._main_drawable.color)

			self._main_drawable_highlighted = main_drawable.copy
			self._main_drawable_highlighted.do_draw = False
			self._main_drawable_highlighted.color = self._main_drawable_highlighted.color + dif * 0.2

			self._main_drawable_clicked = main_drawable.copy
			self._main_drawable_clicked.do_draw = False
			self._main_drawable_clicked.color = self._main_drawable_clicked.color + dif * 0.4

		self._label = label

	@property
	def main_drawable(self) -> ScreenObject:
		if self._main_drawable_clicked.do_draw:
			return self._main_drawable_clicked
		elif self._main_drawable_highlighted.do_draw:
			return self._main_drawable_highlighted
		else:
			return self._main_drawable

	@property
	def drawable_list(self) -> List[ScreenObject]:
		out = []
		if self._background_drawable:
			out.append(self._background_drawable)
		if self._main_drawable:
			out.append(self._main_drawable)
		if self._main_drawable_highlighted:
			out.append(self._main_drawable_highlighted)
		if self._main_drawable_clicked:
			out.append(self._main_drawable_clicked)
		if self._foreground_drawable:
			out.append(self._foreground_drawable)
		return out

	@property
	def text_batch_group(self) -> BatchGroup:
		return self._text_batch_group

	@property
	def label(self) -> LabelExtension:
		return self._label

	@property
	def all_children(self) -> Set[GUIObject]:
		out = set()
		for c in self._children:
			if isinstance(c, GUIObject):
				out.add(c)
				out.update(c.all_children)

		return out

	def _set_drawable_pos(self, pos: Vector2f):
		super(GUIObject, self)._set_drawable_pos(pos)
		if self.label:
			self.label.x, self.label.y = pos.tuple

	def unset_parent(self):
		if self._parent and isinstance(self._parent, GUIObject):
			self.pos -= self._parent.pos

	def set_parent(self, obj: GUIObject):
		self.unset_parent()
		self._parent = obj
		self.pos += obj.pos

	def remove_child(self, obj: GUIObject):
		obj.unset_parent()
		self._children.remove(obj)

	def add_child(self, obj: GUIObject):
		obj.set_parent(self)
		self._children.add(obj)

	def add_children(self, obj_list: List[GUIObject]):
		for o in obj_list:
			self.add_child(o)

	@property
	def is_visible(self) -> bool:
		return self._is_visible

	@is_visible.setter
	def is_visible(self, is_visible: bool):
		self._is_visible = is_visible
		for ch in self._children:
			ch.is_visible = is_visible

	def highlight(self) -> bool:
		if self.is_clickable:
			self._main_drawable_highlighted.do_draw = True
			return True
		else:
			return False

	def dehighlight(self) -> bool:
		if self.is_clickable:
			self._main_drawable_highlighted.do_draw = False
			return True
		else:
			return False

	def click(self) -> bool:
		if self.is_clickable:
			self._main_drawable_clicked.do_draw = True
			return True
		else:
			return False

	def declick(self) -> bool:
		if self.is_clickable:
			self._main_drawable_clicked.do_draw = False
			return True
		else:
			return False
