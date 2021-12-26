from enum import Enum

from step_by_step.common.vector import Vector3i


class Color(Enum):
	WHITE = Vector3i(255, 255, 255)
	BLACK = Vector3i(0, 0, 0)
	RED = Vector3i(255, 0, 0)
	GREEN = Vector3i(0, 255, 0)
	BLUE = Vector3i(0, 0, 255)
