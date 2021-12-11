from step_by_step.common.vector import Vector2f


def between(val, left, right) -> bool:
	return left <= val <= right


def around(val, other_val, d) -> bool:
	return other_val - d / 2 <= val <= other_val + d / 2


def vertex_in_zone(x: float, y: float, zone_pos: Vector2f, zone_size: Vector2f) -> bool:
	return around(x, zone_pos.x, zone_size.x) and around(y, zone_pos.y, zone_size.y)


