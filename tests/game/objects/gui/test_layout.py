import pytest

from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.game.objects.gui.layout import GridLayout, SnapLayout, StackLayout
from step_by_step.game.objects.gui.settings import LayoutStyle, SnapLayoutZone


test_dummy = GUIObject(pos=Vector2f(0, 0), size=Vector2f(0, 0))


def test__grid_layout__init__ok_1():
	layout = GridLayout(
		pos=Vector2f(1, 2),
		size=Vector2f(3, 4),
		rows=0,
		columns=0,
		padding=0,
		border=0,
	)

	assert layout.pos == Vector2f(1, 2)
	assert layout.size == Vector2f(3, 4)

	assert layout.padding == 0
	assert layout.border == 0

	assert layout.rows_count == 0
	assert layout.columns_count == 0
	assert layout.grid is not None
	assert len(layout.grid) == 0


def test__grid_layout__init__ok_2():
	layout = GridLayout(
		pos=Vector2f(1, 1),
		size=Vector2f(1, 1),
		rows=1,
		columns=1,
		padding=0,
		border=0,
	)

	assert layout.padding == 0
	assert layout.border == 0

	assert layout.rows_count == 1
	assert layout.columns_count == 1
	assert layout.grid is not None
	assert len(layout.grid) == 1
	assert len(layout.grid[0]) == 1
	assert layout.grid[0][0] is None


def test__grid_layout__init__ok_3():
	layout = GridLayout(
		pos=Vector2f(1, 1),
		size=Vector2f(1, 1),
		rows=1,
		columns=2,
		padding=10,
		border=20,
	)

	assert layout.padding == 10
	assert layout.border == 20

	assert layout.rows_count == 1
	assert layout.columns_count == 2
	assert layout.grid is not None
	assert len(layout.grid) == 1
	assert len(layout.grid[0]) == 2
	assert layout.grid[0][0] is None
	assert layout.grid[0][1] is None


def test__grid_layout__add_child__fail_1():
	layout = GridLayout(
		pos=Vector2f(1, 1),
		size=Vector2f(1, 1),
		rows=1,
		columns=1,
		padding=0,
		border=0,
	)

	with pytest.raises(NotImplementedError):
		layout.add_child(test_dummy)


def test__grid_layout__set_cell__add__ok_1():
	layout = GridLayout(
		pos=Vector2f(0, 0),
		size=Vector2f(10, 10),
		rows=1,
		columns=2,
		padding=0,
		border=0,
	)

	o = GUIObject(
		pos=Vector2f(0, 0),
		size=Vector2f(1, 1),
		layout_style=LayoutStyle.FILL
	)

	layout.set_cell(0, 0, o)

	assert layout._grid[0][0] is o
	assert layout._grid[0][1] is None

	assert o.parent is layout


def test__grid_layout__set_cell__add__ok_2():
	layout = GridLayout(
		pos=Vector2f(0, 0),
		size=Vector2f(10, 10),
		rows=1,
		columns=2,
		padding=0,
		border=0,
	)

	o1 = GUIObject(
		pos=Vector2f(0, 0),
		size=Vector2f(1, 1),
		layout_style=LayoutStyle.FILL
	)

	o2 = GUIObject(
		pos=Vector2f(0, 0),
		size=Vector2f(1, 1),
		layout_style=LayoutStyle.FILL
	)

	layout.set_cell(0, 0, o1)
	layout.set_cell(0, 1, o2)

	assert layout._grid[0][0] is o1
	assert layout._grid[0][1] is o2

	assert o1.parent is layout
	assert o2.parent is layout


def test__grid_layout__set_cell__add__fail_1():
	layout = GridLayout(
		pos=Vector2f(0, 0),
		size=Vector2f(10, 10),
		rows=1,
		columns=2,
		padding=0,
		border=0,
	)

	o = GUIObject(
		pos=Vector2f(0, 0),
		size=Vector2f(1, 1),
		layout_style=LayoutStyle.FILL
	)

	with pytest.raises(IndexError):
		layout.set_cell(0, 2, o)

	assert layout._grid[0][0] is None
	assert layout._grid[0][1] is None


def test__grid_layout__set_cell__update__ok_1():
	layout = GridLayout(
		pos=Vector2f(0, 0),
		size=Vector2f(10, 10),
		rows=1,
		columns=2,
		padding=0,
		border=0,
	)

	o1 = GUIObject(
		pos=Vector2f(0, 0),
		size=Vector2f(1, 1),
		layout_style=LayoutStyle.FILL
	)

	o2 = GUIObject(
		pos=Vector2f(0, 0),
		size=Vector2f(1, 1),
		layout_style=LayoutStyle.FILL
	)

	layout.set_cell(0, 0, o1)

	assert layout._grid[0][0] is o1
	assert layout._grid[0][1] is None

	layout.set_cell(0, 0, o2)

	assert layout._grid[0][0] is o2
	assert layout._grid[0][1] is None

	assert o1.parent is None
	assert o2.parent is layout


def test__grid_layout__set_cell__update__ok_2():
	layout = GridLayout(
		pos=Vector2f(0, 0),
		size=Vector2f(10, 10),
		rows=1,
		columns=2,
		padding=0,
		border=0,
	)

	o = GUIObject(
		pos=Vector2f(0, 0),
		size=Vector2f(1, 1),
		layout_style=LayoutStyle.FILL
	)

	layout.set_cell(0, 0, o)

	assert layout._grid[0][0] is o
	assert layout._grid[0][1] is None

	layout.set_cell(0, 0, None)

	assert layout._grid[0][0] is None
	assert layout._grid[0][1] is None

	assert o.parent is None


def test__grid_layout__default_cell_dimensions__ok_1():
	layout = GridLayout(
		pos=Vector2f(0, 0),
		size=Vector2f(10, 10),
		rows=1,
		columns=1,
		padding=0,
		border=0,
	)

	dim = layout.default_cell_dimensions

	assert dim
	assert dim.pos == layout.pos
	assert dim.size == layout.size


def test__grid_layout__default_cell_dimensions__ok_2():
	layout = GridLayout(
		pos=Vector2f(0, 0),
		size=Vector2f(10, 10),
		rows=1,
		columns=2,
		padding=0,
		border=0,
	)

	dim = layout.default_cell_dimensions

	assert dim
	assert dim.x == round(layout.x - round(layout.w / layout.columns_count) / 2)
	assert dim.y == layout.y
	assert dim.w == round(layout.w / layout.columns_count)
	assert dim.h == layout.h


def test__grid_layout__default_cell_dimensions__ok_3():
	layout = GridLayout(
		pos=Vector2f(0, 0),
		size=Vector2f(10, 10),
		rows=2,
		columns=1,
		padding=0,
		border=0,
	)

	dim = layout.default_cell_dimensions

	assert dim
	assert dim.x == layout.x
	assert dim.y == round(layout.y + round(layout.h / layout.rows_count) / 2)
	assert dim.w == layout.w
	assert dim.h == round(layout.h / layout.rows_count)


def test__grid_layout__default_cell_dimensions__ok_4():
	layout = GridLayout(
		pos=Vector2f(0, 0),
		size=Vector2f(10, 10),
		rows=2,
		columns=2,
		padding=0,
		border=0,
	)

	dim = layout.default_cell_dimensions

	assert dim
	assert dim.x == round(layout.x - round(layout.w / layout.columns_count) / 2)
	assert dim.y == round(layout.y + round(layout.h / layout.rows_count) / 2)
	assert dim.w == round(layout.w / layout.columns_count)
	assert dim.h == round(layout.h / layout.rows_count)


def test__grid_layout__default_cell_dimensions__ok_5():
	layout = GridLayout(
		pos=Vector2f(0, 0),
		size=Vector2f(90, 90),
		rows=3,
		columns=7,
		padding=0,
		border=0,
	)

	dim = layout.default_cell_dimensions

	assert dim
	assert dim.x == round(layout.left_bound_x + round(layout.w / layout.columns_count) / 2)
	assert dim.y == round(layout.upper_bound_y - round(layout.h / layout.rows_count) / 2)
	assert dim.w == round(layout.w / layout.columns_count)
	assert dim.h == round(layout.h / layout.rows_count)


def test__snap_layout__init__ok_1():
	layout = SnapLayout(
		pos=Vector2f(1, 2),
		size=Vector2f(3, 4),
		padding=5,
		border=6,
	)

	assert layout.pos == Vector2f(1, 2)
	assert layout.size == Vector2f(3, 4)

	assert layout.padding == 5
	assert layout.border == 6

	expected_zones = {_ for _ in SnapLayoutZone}
	assert layout._zones is not None
	assert type(layout._zones) is dict
	assert len(layout._zones) > 0
	assert len(layout._zones) == len(expected_zones)
	assert set(layout._zones.keys()) == expected_zones
	assert set(layout._zones.values()) == {None}


def test__snap_layout__add_child__fail_1():
	layout = SnapLayout(
		pos=Vector2f(1, 1),
		size=Vector2f(1, 1),
	)

	with pytest.raises(NotImplementedError):
		layout.add_child(test_dummy)


def test__snap_layout__resolve__center_fill__ok_1():
	layout = SnapLayout(
		pos=Vector2f(5, 10),
		size=Vector2f(15, 20),
		padding=0,
		border=0,
	)

	obj = GUIObject(
		pos=Vector2f(0, 0),
		size=Vector2f(1, 1),
		layout_style=LayoutStyle.FILL
	)

	obj.change_parent(layout)
	layout._zones[SnapLayoutZone.CENTER] = obj

	layout._resolve()

	assert obj.pos == Vector2f(5, 10)
	assert obj.pos == layout.pos
	assert obj.size == Vector2f(15, 20)
	assert obj.size == layout.size


def test__snap_layout__resolve__center_fill_vertical__ok_1():
	layout = SnapLayout(
		pos=Vector2f(5, 10),
		size=Vector2f(15, 20),
		padding=0,
		border=0,
	)

	obj = GUIObject(
		pos=Vector2f(0, 0),
		size=Vector2f(1, 1),
		layout_style=LayoutStyle.FILL_VERTICAL
	)

	obj.change_parent(layout)
	layout._zones[SnapLayoutZone.CENTER] = obj

	layout._resolve()

	assert obj.pos == Vector2f(5, 10)
	assert obj.pos == layout.pos
	assert obj.size == Vector2f(1, 20)
	assert obj.w != layout.w
	assert obj.h == layout.h


def test__snap_layout__resolve__center_fill_horizontal__ok_1():
	layout = SnapLayout(
		pos=Vector2f(5, 10),
		size=Vector2f(15, 20),
		padding=0,
		border=0,
	)

	obj = GUIObject(
		pos=Vector2f(0, 0),
		size=Vector2f(1, 1),
		layout_style=LayoutStyle.FILL_HORIZONTAL
	)

	obj.change_parent(layout)
	layout._zones[SnapLayoutZone.CENTER] = obj

	layout._resolve()

	assert obj.pos == Vector2f(5, 10)
	assert obj.pos == layout.pos
	assert obj.size == Vector2f(15, 1)
	assert obj.w == layout.w
	assert obj.h != layout.h


def test__snap_layout__set_zone__ok_1():
	layout = SnapLayout(
		pos=Vector2f(1, 1),
		size=Vector2f(1, 1),
		padding=0,
		border=0,
	)

	assert layout.top is None

	obj = GUIObject(
		pos=Vector2f(0, 0),
		size=Vector2f(1, 1),
		layout_style=LayoutStyle.FILL
	)

	layout._set_zone(zone=SnapLayoutZone.TOP, new_obj=obj)

	assert layout.top is obj


def test__stack_layout__init__ok_1():
	layout = StackLayout(
		pos=Vector2f(1, 2),
		size=Vector2f(3, 4),
		padding=5,
		border=6,
	)

	assert layout.pos == Vector2f(1, 2)
	assert layout.size == Vector2f(3, 4)

	assert layout.padding == 5
	assert layout.border == 6

	assert layout._stack is not None
	assert type(layout._stack) is list
	assert len(layout._stack) == 0


def test__stack_layout__add_child__fail_1():
	layout = StackLayout(
		pos=Vector2f(1, 1),
		size=Vector2f(1, 1),
	)

	with pytest.raises(NotImplementedError):
		layout.add_child(test_dummy)
