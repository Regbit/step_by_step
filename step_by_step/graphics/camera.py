from step_by_step.common.vector import Vector2f


class Camera:

	pos: Vector2f
	size: Vector2f
	scroll_speed = 7
	scroll_border_width = 20

	def __init__(self, pos: Vector2f, size: Vector2f):
		self.pos = pos
		self.size = size

	def move(self, vec: Vector2f):
		self.pos += vec
