from step_by_step.common.shaped import Shaped
from step_by_step.common.vector import Vector2f, Vector3i
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.objects.square import Rectangle
from step_by_step.graphics.sprites.gui.viewport import ViewportDefaultSprite


def test__viewport_default_sprite__init__ok_1():
	s = ViewportDefaultSprite(
		pos=Vector2f(1, 2),
		size=Vector2f(3, 4),
		batch_group=BatchGroup.GUI_OBJECT,
		do_draw=True,
		color=Vector3i(1, 2, 3),
		screen=Shaped(pos=Vector2f(5, 6), size=Vector2f(7, 8))
	)

	assert s is not None
	assert s.pos == Vector2f(1, 2)
	assert s.size == Vector2f(3, 4)
	assert s.batch_group == BatchGroup.GUI_OBJECT
	assert s.do_draw is True

	assert s._screen is not None
	assert s._screen.pos == Vector2f(5, 6)
	assert s._screen.size == Vector2f(7, 8)

	assert s._left_band is not None
	assert type(s._left_band) is Rectangle

	assert s._right_band is not None
	assert type(s._right_band) is Rectangle

	assert s._upper_band is not None
	assert type(s._upper_band) is Rectangle

	assert s._lower_band is not None
	assert type(s._lower_band) is Rectangle


def test__viewport_default_sprite__update_bands__ok_1():
	screen = Shaped(pos=Vector2f(5, 5), size=Vector2f(10, 10))
	s = ViewportDefaultSprite(
		pos=Vector2f(5, 5),
		size=Vector2f(10, 10),
		batch_group=BatchGroup.GUI_OBJECT,
		do_draw=True,
		color=Vector3i(0, 0, 0),
		screen=screen
	)

	assert s.left_bound_x == screen.left_bound_x
	assert s.right_bound_x == screen.right_bound_x
	assert s.upper_bound_y == screen.upper_bound_y
	assert s.lower_bound_y == screen.lower_bound_y

	assert s._left_band.pos == s.pos
	assert s._right_band.pos == s.pos
	assert s._upper_band.pos == s.pos
	assert s._lower_band.pos == s.pos

	assert s._left_band.shift == Vector2f(-screen.w, 0)
	assert s._right_band.shift == Vector2f(screen.w, 0)
	assert s._upper_band.shift == Vector2f(0, screen.h)
	assert s._lower_band.shift == Vector2f(0, -screen.h)


def test__viewport_default_sprite__update_bands__ok_2():
	screen = Shaped(pos=Vector2f(5, 5), size=Vector2f(10, 10))
	s = ViewportDefaultSprite(
		pos=Vector2f(5, 5),
		size=Vector2f(8, 8),
		batch_group=BatchGroup.GUI_OBJECT,
		do_draw=True,
		color=Vector3i(0, 0, 0),
		screen=screen
	)

	assert s.left_bound_x == screen.left_bound_x + 1
	assert s.right_bound_x == screen.right_bound_x - 1
	assert s.upper_bound_y == screen.upper_bound_y - 1
	assert s.lower_bound_y == screen.lower_bound_y + 1

	assert s._left_band.pos == s.pos
	assert s._right_band.pos == s.pos
	assert s._upper_band.pos == s.pos
	assert s._lower_band.pos == s.pos

	assert s._left_band.shift == Vector2f(-screen.w + 1, 0)
	assert s._right_band.shift == Vector2f(screen.w - 1, 0)
	assert s._upper_band.shift == Vector2f(0, screen.h - 1)
	assert s._lower_band.shift == Vector2f(0, -screen.h + 1)


def test__viewport_default_sprite__update_bands__ok_3():
	screen = Shaped(pos=Vector2f(5, 5), size=Vector2f(10, 10))
	s = ViewportDefaultSprite(
		pos=Vector2f(6, 5),
		size=Vector2f(10, 10),
		batch_group=BatchGroup.GUI_OBJECT,
		do_draw=True,
		color=Vector3i(0, 0, 0),
		screen=screen
	)

	assert s.pos == screen.pos + Vector2f(1, 0)

	assert s.left_bound_x == screen.left_bound_x + 1
	assert s.right_bound_x == screen.right_bound_x + 1
	assert s.upper_bound_y == screen.upper_bound_y
	assert s.lower_bound_y == screen.lower_bound_y

	assert s._left_band.pos == s.pos
	assert s._right_band.pos == s.pos
	assert s._upper_band.pos == s.pos
	assert s._lower_band.pos == s.pos

	assert s._left_band.shift == Vector2f(-screen.w, 0)
	assert s._right_band.shift == Vector2f(screen.w, 0)
	assert s._upper_band.shift == Vector2f(0, screen.h)
	assert s._lower_band.shift == Vector2f(0, -screen.h)


def test__viewport_default_sprite__update_bands__ok_4():
	screen = Shaped(pos=Vector2f(5, 5), size=Vector2f(10, 10))
	s = ViewportDefaultSprite(
		pos=Vector2f(6, 7),
		size=Vector2f(8, 8),
		batch_group=BatchGroup.GUI_OBJECT,
		do_draw=True,
		color=Vector3i(0, 0, 0),
		screen=screen
	)

	assert s.pos == screen.pos + Vector2f(1, 2)

	assert s.left_bound_x == screen.left_bound_x + 1 + 1
	assert s.right_bound_x == screen.right_bound_x + 1 - 1
	assert s.upper_bound_y == screen.upper_bound_y + 2 - 1
	assert s.lower_bound_y == screen.lower_bound_y + 2 + 1

	assert s._left_band.pos == s.pos
	assert s._right_band.pos == s.pos
	assert s._upper_band.pos == s.pos
	assert s._lower_band.pos == s.pos

	assert s._left_band.shift == Vector2f(-screen.w + 1, 0)
	assert s._right_band.shift == Vector2f(screen.w - 1, 0)
	assert s._upper_band.shift == Vector2f(0, screen.h - 1)
	assert s._lower_band.shift == Vector2f(0, -screen.h + 1)
