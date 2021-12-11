import math
from typing import List, Tuple, Union

from step_by_step.common.vector import Vector2f


def _rotate_coordinates(
	pos: Union[Vector2f, Tuple[Union[int, float], Union[int, float]]],
	size: Union[Vector2f, Tuple[Union[int, float], Union[int, float]]],
	rotation_angle: float,
	vertex_angles: List[float],
	vertex_radius_multiplier: List[float]
) -> List[int]:
	x, y = pos.list if isinstance(pos, Vector2f) else pos
	w, h = size.list if isinstance(size, Vector2f) else size

	r = math.sqrt((w / 2) ** 2 + (h / 2) ** 2)

	out = []

	for a, r_m in zip(vertex_angles, vertex_radius_multiplier):
		out.append(int(x + r * r_m * math.cos(rotation_angle + math.pi * a)))
		out.append(int(y + r * r_m * math.sin(rotation_angle + math.pi * a)))

	return out


def rotate_quad_coordinates(
	pos: Union[Vector2f, Tuple[Union[int, float], Union[int, float]]],
	size: Union[Vector2f, Tuple[Union[int, float], Union[int, float]]],
	rotation_angle: float,
	vertex_angles: Tuple[float, float, float, float],
	vertex_radius_multiplier: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
) -> List[int]:
	return _rotate_coordinates(pos, size, rotation_angle, list(vertex_angles), list(vertex_radius_multiplier))


def rotate_triangle_coordinates(
	pos: Union[Vector2f, Tuple[Union[int, float], Union[int, float]]],
	size: Union[Vector2f, Tuple[Union[int, float], Union[int, float]]],
	rotation_angle: float,
	vertex_angles: Tuple[float, float, float],
	vertex_radius_multiplier: Tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> List[int]:
	return _rotate_coordinates(pos, size, rotation_angle, list(vertex_angles), list(vertex_radius_multiplier))
