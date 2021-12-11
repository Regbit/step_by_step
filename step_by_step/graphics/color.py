from enum import Enum

from step_by_step.common.vector import Vector3i


class Color(Enum):
	WHITE = Vector3i(255, 255, 255)
	BLACK = Vector3i(0, 0, 0)
