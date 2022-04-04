import abc
from typing import List, Optional, Dict, Tuple

from step_by_step.common.helpers import between
from step_by_step.common.shaped import Shaped
from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import GameObject
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.game.objects.gui.settings import LayoutStyle, SnapLayoutZone
from step_by_step.game.objects.settings import SpriteType
from step_by_step.graphics.sprites.sprite import Sprite


class Layout(GUIObject, abc.ABC):

	_base_name = 'Layout'

	def _resolve(self):
		raise NotImplementedError(f"Method '_resolve' was not implemented in class '{type(self).__name__}'")

	@property
	def size(self) -> Vector2f:
		return super(GUIObject, self).size

	@size.setter
	def size(self, new_size: Vector2f):
		self._size = new_size
		self._resolve()


class AbsoluteLayout(Layout):

	_base_name = 'Absolute Layout'

	def _resolve(self):
		pass


class DynamicLayout(Layout, abc.ABC):

	_base_name = 'Dynamic Layout'

	_padding: int
	_border: int

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		sprites: Dict[SpriteType, Sprite] = None,
		orientation_vec: Vector2f = None,
		layout_style: LayoutStyle = None,
		padding: int = 0,
		border: int = 0,
	):
		super(DynamicLayout, self).__init__(
			pos=pos,
			size=size,
			sprites=sprites,
			orientation_vec=orientation_vec,
			layout_style=layout_style
		)
		self._padding = padding if padding >= 0 else 0
		self._border = border if border >= 0 else 0

	@property
	def padding(self) -> int:
		return self._padding

	@padding.setter
	def padding(self, new_padding: int):
		self._padding = new_padding if new_padding >= 0 else 0
		self._resolve()

	@property
	def border(self) -> int:
		return self._border

	@border.setter
	def border(self, new_border: int):
		self._border = new_border if new_border >= 0 else 0
		self._resolve()


class GridLayout(DynamicLayout):

	_base_name = 'Grid Layout'

	_grid: List[List[Optional[GUIObject]]] = None

	def self_destruct_clean_up(self):
		super(GridLayout, self).self_destruct_clean_up()
		self._grid = None

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		rows: int,
		columns: int,
		sprites: Dict[SpriteType, Sprite] = None,
		orientation_vec: Vector2f = None,
		layout_style: LayoutStyle = None,
		padding: int = 0,
		border: int = 0,
	):
		super(GridLayout, self).__init__(
			pos=pos,
			size=size,
			sprites=sprites,
			orientation_vec=orientation_vec,
			layout_style=layout_style,
			padding=padding,
			border=border
		)
		self._grid = [[None for _ in range(columns)] for _ in range(rows)] if rows > 0 and columns > 0 else []

	def _check_input_row_column(self, row: int, col: int) -> bool:
		if between(row, 0, self.rows_count) and between(col, 0, self.columns_count):
			return True
		else:
			raise IndexError(
				f"Index out of range!\n"
				f"Requested object: {row, col}\n"
				f"Grid dimensions: {self.rows_count, self.columns_count}\n"
			)

	@property
	def grid(self) -> List[List[GUIObject]]:
		return self._grid

	@property
	def rows_count(self) -> int:
		return len(self._grid)

	@property
	def columns_count(self) -> int:
		return len(self._grid[0]) if self.rows_count > 0 else 0

	@property
	def default_cell_dimensions(self) -> Optional[Shaped]:
		if self.rows_count > 0 and self.columns_count > 0:
			size = Vector2f(
				x=round(self.w / self.columns_count),
				y=round(self.h / self.rows_count)
			)

			pos = Vector2f(
				x=round(self.left_bound_x + size.x / 2),
				y=round(self.upper_bound_y - size.y / 2)
			)

			return Shaped(pos=pos, size=size)

	def get_cell(self, row: int, col: int) -> Optional[GUIObject]:
		if self._check_input_row_column(row=row, col=col):
			return self._grid[row][col]

	def set_cell(self, row: int, col: int, new_obj: Optional[GUIObject]):
		if self._check_input_row_column(row=row, col=col):

			stored_obj = self.get_cell(row=row, col=col)
			if stored_obj:
				stored_obj.change_parent(parent=None)

			if new_obj:
				new_obj.change_parent(parent=self)

			self._grid[row][col] = new_obj
			self._resolve()

	def add_child(self, obj: GameObject):
		raise NotImplementedError(
			f"Can not explicitly add child to a {type(self).__name__}!\n"
			f"Use 'set_cell(..)' method instead.\n"
		)


class SnapLayout(DynamicLayout):

	_base_name = 'Snap Layout'

	_zones: Dict[SnapLayoutZone, Optional[GUIObject]] = None

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		sprites: Dict[SpriteType, Sprite] = None,
		orientation_vec: Vector2f = None,
		layout_style: LayoutStyle = None,
		padding: int = 0,
		border: int = 0,
	):
		super(SnapLayout, self).__init__(
			pos=pos,
			size=size,
			sprites=sprites,
			orientation_vec=orientation_vec,
			layout_style=layout_style,
			padding=padding,
			border=border,
		)
		self._zones = {
			SnapLayoutZone.TOP: None,
			SnapLayoutZone.BOTTOM: None,
			SnapLayoutZone.LEFT: None,
			SnapLayoutZone.RIGHT: None,
			SnapLayoutZone.CENTER: None,
		}

	def _set_zone(self, zone: SnapLayoutZone, new_obj: Optional[GUIObject]):
		if self._zones[zone]:
			self._zones[zone].change_parent(parent=None)

		if new_obj:
			new_obj.change_parent(parent=self)

		self._zones[zone] = new_obj

		self._resolve()

	@property
	def top(self) -> GUIObject:
		return self._zones[SnapLayoutZone.TOP]

	@top.setter
	def top(self, new_top: Optional[GUIObject]):
		self._set_zone(zone=SnapLayoutZone.TOP, new_obj=new_top)

	@property
	def bottom(self) -> GUIObject:
		return self._zones[SnapLayoutZone.BOTTOM]

	@bottom.setter
	def bottom(self, new_bottom: Optional[GUIObject]):
		self._set_zone(zone=SnapLayoutZone.BOTTOM, new_obj=new_bottom)

	@property
	def left(self) -> GUIObject:
		return self._zones[SnapLayoutZone.LEFT]

	@left.setter
	def left(self, new_left: Optional[GUIObject]):
		self._set_zone(zone=SnapLayoutZone.LEFT, new_obj=new_left)

	@property
	def right(self) -> GUIObject:
		return self._zones[SnapLayoutZone.RIGHT]

	@right.setter
	def right(self, new_right: Optional[GUIObject]):
		self._set_zone(zone=SnapLayoutZone.RIGHT, new_obj=new_right)

	@property
	def center(self) -> GUIObject:
		return self._zones[SnapLayoutZone.CENTER]

	@center.setter
	def center(self, new_center: Optional[GUIObject]):
		self._set_zone(zone=SnapLayoutZone.CENTER, new_obj=new_center)

	def add_child(self, obj: GameObject):
		raise NotImplementedError(
			f"Can not explicitly add child to a {type(self).__name__}!\n"
			f"Set 'top', 'bottom', 'left', 'right', 'center' via assignment operator ('top = ...') instead.\n"
		)


class StackLayout(DynamicLayout):

	_base_name = 'Stack Layout'

	_stack: List[Tuple[GUIObject]] = None

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		sprites: Dict[SpriteType, Sprite] = None,
		orientation_vec: Vector2f = None,
		layout_style: LayoutStyle = None,
		padding: int = 0,
		border: int = 0,
	):
		super(StackLayout, self).__init__(
			pos=pos,
			size=size,
			sprites=sprites,
			orientation_vec=orientation_vec,
			layout_style=layout_style,
			padding=padding,
			border=border,
		)
		self._stack = []

	def __len__(self):
		return len(self._stack)

	def _resolve(self):
		for row in self._stack:
			self._resolve_row(row)

	def _resolve_row(self, row: Tuple[GUIObject]):
		raise NotImplementedError()

	def _check_input_stack_index(self, i: int) -> bool:
		if between(i, 0, len(self) - 1):
			return True
		else:
			raise IndexError(
				f"Index out of range!\n"
				f"Requested object: {i}\n"
				f"Stack depth: {len(self)}\n"
			)

	def add(self, obj: Tuple[GUIObject]):
		for o in obj:
			o.change_parent(parent=self)

		self._stack.append(obj)

		self._resolve()

	def remove(self, stack_index: int):
		if len(self) > 0 and self._check_input_stack_index(stack_index):
			for o in self._stack[stack_index]:
				o.change_parent(parent=None)

		self._stack.pop(stack_index)

		self._resolve()

	def add_child(self, obj: GameObject):
		raise NotImplementedError(
			f"Can not explicitly add child to a {type(self).__name__}!\n"
			f"Use 'add' method instead.\n"
		)
