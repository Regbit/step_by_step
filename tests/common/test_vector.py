import pytest

from step_by_step.common.vector import Vector2f
from step_by_step.common.settings import MATH_ROUND_PRECISION
from tests.helpers import (
	calc_angle,
	calc_radius,
	calc_x,
	calc_y,
)


def test__v2f_init__fail_1():
	with pytest.raises(ValueError):
		Vector2f()


def test__v2f_init_cartesian__ok_1():
	v = Vector2f(x=0, y=1)

	expected_x = 0
	assert v._x == expected_x
	assert v.x == expected_x

	expected_y = 1
	assert v._y == expected_y
	assert v.y == expected_y

	expected_r = 1
	assert v._r == expected_r
	assert v.r == expected_r

	expected_a = calc_angle(expected_x, expected_y, MATH_ROUND_PRECISION)
	assert v._a == expected_a
	assert v.a == expected_a
	assert v.angle == expected_a


def test__v2f_init_cartesian__ok_2():
	v = Vector2f(x=3, y=4)

	expected_x = 3
	assert v._x == expected_x
	assert v.x == expected_x

	expected_y = 4
	assert v._y == expected_y
	assert v.y == expected_y

	expected_r = 5
	assert v._r == expected_r
	assert v.r == expected_r

	expected_a = calc_angle(expected_x, expected_y, MATH_ROUND_PRECISION)
	assert v._a == expected_a
	assert v.a == expected_a
	assert v.angle == expected_a


def test__v2f_init_polar__ok_1():
	v = Vector2f(r=1, a=0)

	expected_x = 1
	assert v._x == expected_x
	assert v.x == expected_x

	expected_y = 0
	assert v._y == expected_y
	assert v.y == expected_y

	expected_r = 1
	assert v._r == expected_r
	assert v.r == expected_r

	expected_a = calc_angle(expected_x, expected_y, MATH_ROUND_PRECISION)
	assert v._a == expected_a
	assert v.a == expected_a
	assert v.angle == expected_a


def test__v2f_init_polar__ok_2():
	v = Vector2f(r=5, a=calc_angle(3, 4, MATH_ROUND_PRECISION))

	expected_x = 3
	assert v._x == expected_x
	assert v.x == expected_x

	expected_y = 4
	assert v._y == expected_y
	assert v.y == expected_y

	expected_r = 5
	assert v._r == expected_r
	assert v.r == expected_r

	expected_a = calc_angle(expected_x, expected_y, MATH_ROUND_PRECISION)
	assert v._a == expected_a
	assert v.a == expected_a
	assert v.angle == expected_a


def test__v2f_init_polar__ok_3():
	v = Vector2f(r=7, a=1.5)

	expected_r = 7
	assert v._r == expected_r
	assert v.r == expected_r

	expected_a = 1.5
	assert v._a == expected_a
	assert v.a == expected_a
	assert v.angle == expected_a

	expected_x = calc_x(7, 1.5, MATH_ROUND_PRECISION)
	assert v._x == expected_x
	assert v.x == expected_x

	expected_y = calc_y(7, 1.5, MATH_ROUND_PRECISION)
	assert v._y == expected_y
	assert v.y == expected_y


def test__v2f_add_v2f__ok_1():
	v1 = Vector2f(x=1, y=0)
	v2 = Vector2f(x=0, y=1)

	v3 = v1 + v2

	assert v3.x == v1.x + v2.x
	assert v3.y == v1.y + v2.y
	assert v3.r == calc_radius(v1.x + v2.x, v1.y + v2.y, MATH_ROUND_PRECISION)
	assert v3.a == calc_angle(v1.x + v2.x, v1.y + v2.y, MATH_ROUND_PRECISION)


def test__v2f_add_v2f__ok_2():
	v1 = Vector2f(x=-1, y=2)
	v2 = Vector2f(x=3, y=-1)

	v3 = v1 + v2

	assert v3.x == v1.x + v2.x
	assert v3.y == v1.y + v2.y
	assert v3.r == calc_radius(v1.x + v2.x, v1.y + v2.y, MATH_ROUND_PRECISION)
	assert v3.a == calc_angle(v1.x + v2.x, v1.y + v2.y, MATH_ROUND_PRECISION)


def test__v2f_add_list__ok_1():
	v1 = Vector2f(x=1, y=0)
	v2 = [0, 1]

	v3 = v1 + v2

	assert v3.x == v1.x + v2[0]
	assert v3.y == v1.y + v2[1]
	assert v3.r == calc_radius(v1.x + v2[0], v1.y + v2[1], MATH_ROUND_PRECISION)
	assert v3.a == calc_angle(v1.x + v2[0], v1.y + v2[1], MATH_ROUND_PRECISION)


def test__v2f_add_list__fail_1():
	v1 = Vector2f(x=1, y=0)
	v2 = [0, 1, 3]

	with pytest.raises(NotImplementedError):
		v1 + v2


def test__v2f_add_tuple__ok_1():
	v1 = Vector2f(x=-1, y=2)
	v2 = (0, 1)

	v3 = v1 + v2

	assert v3.x == v1.x + v2[0]
	assert v3.y == v1.y + v2[1]
	assert v3.r == calc_radius(v1.x + v2[0], v1.y + v2[1], MATH_ROUND_PRECISION)
	assert v3.a == calc_angle(v1.x + v2[0], v1.y + v2[1], MATH_ROUND_PRECISION)


def test__v2f_add_tuple__fail_1():
	v1 = Vector2f(x=1, y=0)
	v2 = (0, 1, 3)

	with pytest.raises(NotImplementedError):
		v1 + v2


def test__v2f_add__fail_1():
	v1 = Vector2f(x=1, y=0)
	v2 = '3, 4'

	with pytest.raises(NotImplementedError):
		v1 + v2
