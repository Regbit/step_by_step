import pytest

from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import (
	GameObject,
	SelfParenthoodError,
	CircularParenthoodError,
	ExistingParenthoodError
)


def test__game_object__init__ok_1():
	o = GameObject(pos=Vector2f(1, 2), size=Vector2f(3, 4))
	assert o
	assert isinstance(o, GameObject)
	assert o.pos == Vector2f(1, 2)
	assert o.size == Vector2f(3, 4)
	assert o._base_name == 'Game Object'
	assert o._children is not None
	assert o._children == list()
	assert o._parent is None
	assert str(o) == f'Game Object(GameObject) #None'


def test__game_object__init__no_args__fail_1():
	with pytest.raises(TypeError):
		GameObject()


def test__game_object__init__not_enough__fail_1():
	with pytest.raises(TypeError):
		GameObject(pos=Vector2f(1, 2))


def test__game_object__init__not_enough__fail_2():
	with pytest.raises(TypeError):
		GameObject(size=Vector2f(1, 2))


def test__game_object__change_parent__set__ok_1():
	parent_pos = Vector2f(1, 2)
	child_pos = Vector2f(3, 4)

	parent_o = GameObject(parent_pos, Vector2f(1, 1))
	child_o = GameObject(child_pos, Vector2f(1, 1))

	assert parent_o.pos == parent_pos
	assert child_o.pos == child_pos

	child_o.change_parent(parent=parent_o)

	assert child_o._parent == parent_o
	assert child_o.parent == child_o._parent

	assert len(parent_o._children) == 1
	assert len(parent_o.children) == 1

	assert parent_o._children[0] == child_o
	assert parent_o.children == parent_o._children

	assert child_o.pos == parent_pos + child_pos
	assert child_o._pos == child_pos


def test__game_object__change_parent__set__fail_1():
	o = GameObject(Vector2f(1, 1), Vector2f(1, 1))

	with pytest.raises(SelfParenthoodError):
		o.change_parent(parent=o)


def test__game_object__change_parent__set__fail_2():
	par_o = GameObject(Vector2f(1, 1), Vector2f(1, 1))
	ch_o = GameObject(Vector2f(1, 1), Vector2f(1, 1))

	ch_o.change_parent(par_o)

	with pytest.raises(CircularParenthoodError):
		par_o.change_parent(parent=ch_o)


def test__game_object__change_parent__set__fail_3():
	par_o = GameObject(Vector2f(1, 1), Vector2f(1, 1))
	ch_o = GameObject(Vector2f(1, 1), Vector2f(1, 1))

	ch_o.change_parent(par_o)

	with pytest.raises(ExistingParenthoodError):
		ch_o.change_parent(par_o)


def test__game_object__change_parent__unset__ok_1():
	parent_pos = Vector2f(1, 2)
	child_pos = Vector2f(3, 4)

	parent_o = GameObject(parent_pos, Vector2f(1, 1))
	child_o = GameObject(child_pos, Vector2f(1, 1))

	child_o.change_parent(parent=parent_o)

	assert child_o.parent == parent_o
	assert len(parent_o.children) == 1
	assert parent_o.children[0] == child_o

	child_o.change_parent(parent=None)

	assert child_o.parent is None
	assert len(parent_o.children) == 0

	assert child_o.pos == child_pos
	assert child_o._pos == child_pos


def test__game_object__change_parent__change__ok_1():
	parent_1_pos = Vector2f(1, 2)
	parent_2_pos = Vector2f(5, 6)
	child_pos = Vector2f(3, 4)

	parent_1_o = GameObject(parent_1_pos, Vector2f(1, 1))
	child_o = GameObject(child_pos, Vector2f(1, 1))

	child_o.change_parent(parent=parent_1_o)

	assert child_o.parent == parent_1_o
	assert len(parent_1_o.children) == 1
	assert parent_1_o.children[0] == child_o

	parent_o2 = GameObject(parent_2_pos, Vector2f(1, 1))

	assert child_o.parent != parent_o2
	assert len(parent_o2.children) == 0

	child_o.change_parent(parent=parent_o2)

	assert child_o._parent == parent_o2
	assert len(parent_o2.children) == 1
	assert parent_o2.children[0] == child_o
	assert len(parent_1_o.children) == 0

	assert child_o.pos == parent_2_pos + child_pos
	assert child_o._pos == child_pos
