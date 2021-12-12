from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import DrawnGameObject
from step_by_step.graphics.color import Color
from step_by_step.graphics.label import Label
from step_by_step.graphics.objects.screen_object import ScreenObject
from step_by_step.graphics.objects.settings import BatchGroup


class GUIObject(DrawnGameObject):

	_base_name = 'GUI Object'
	_batch_group = BatchGroup.GUI_OBJECT
	_text_batch_group = BatchGroup.GUI_TEXT_OBJECT

	is_clickable: bool
	_main_drawable_highlighted: ScreenObject
	_main_drawable_clicked: ScreenObject
	_label: Label

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
		orientation_vec: Vector2f = None,
		background_drawable: ScreenObject = None,
		main_drawable: ScreenObject = None,
		foreground_drawable: ScreenObject = None,
		label: Label = None,
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
		self.is_clickable = is_clickable

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
	def text_batch_group(self) -> BatchGroup:
		return self._text_batch_group

	@property
	def label(self) -> Label:
		return self._label

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
