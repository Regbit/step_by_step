from step_by_step.common.helpers import vertex_in_zone
from step_by_step.common.shaped import Shaped
from step_by_step.common.vector import Vector2f
from step_by_step.game.managers.settings import ScreenScrollFlag
from step_by_step.game.objects.game_object import DrawnGameObject
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.game.objects.gui.settings import VIEWPORT_SCROLL_SPEED, VIEWPORT_SCROLL_BORDER_WIDTH
from step_by_step.game.objects.settings import SpriteType
from step_by_step.game.objects.gui.camera import Camera
from step_by_step.graphics.color import Color
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.sprites.gui.viewport import ViewportDefaultSprite


class Viewport(GUIObject):

	_base_name = 'Viewport'
	_camera: Camera
	_scroll_flags = set()
	_scroll_speed = VIEWPORT_SCROLL_SPEED
	_scroll_border_width = VIEWPORT_SCROLL_BORDER_WIDTH

	def self_destruct_clean_up(self):
		super(Viewport, self).self_destruct_clean_up()
		self._camera = None

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		screen: Shaped,
	):
		super(Viewport, self).__init__(
			pos=pos,
			size=size,
			sprites={
				SpriteType.DEFAULT: ViewportDefaultSprite(
					pos=pos,
					size=size,
					batch_group=BatchGroup.GUI_OBJECT_BACKGROUND,
					do_draw=True,
					color=Color.RED,
					screen=screen
				)
			}
		)

		self._camera = Camera(
			pos=Vector2f(0, 0),
			size=screen.size
		)
		self.add_child(self._camera)

	@property
	def camera(self) -> Camera:
		return self._camera

	def scroll_flag(self, x: int, y: int):
		self._scroll_flags = set()
		if vertex_in_zone(x, y, self.pos, self.size):
			if self.left_bound_x <= x <= self.left_bound_x + self._scroll_border_width:
				self._scroll_flags.add(ScreenScrollFlag.LEFT)
			elif self.right_bound_x >= x >= self.right_bound_x - self._scroll_border_width:
				self._scroll_flags.add(ScreenScrollFlag.RIGHT)

			if self.lower_bound_y <= y <= self.lower_bound_y + self._scroll_border_width:
				self._scroll_flags.add(ScreenScrollFlag.DOWN)
			elif self.upper_bound_y >= y >= self.upper_bound_y - self._scroll_border_width:
				self._scroll_flags.add(ScreenScrollFlag.UP)

	def scroll_action(self):
		move_vec = Vector2f(0, 0)

		if ScreenScrollFlag.LEFT in self._scroll_flags:
			move_vec -= (self._scroll_speed, 0)
		elif ScreenScrollFlag.RIGHT in self._scroll_flags:
			move_vec += (self._scroll_speed, 0)

		if ScreenScrollFlag.DOWN in self._scroll_flags:
			move_vec -= (0, self._scroll_speed)
		elif ScreenScrollFlag.UP in self._scroll_flags:
			move_vec += (0, self._scroll_speed)

		self.scroll(move_vec)

	def scroll(self, vec: Vector2f):
		self._camera.pos += vec

	def is_object_in_frame(self, obj: DrawnGameObject) -> bool:
		pos = self.pos + self._camera.pos
		if isinstance(obj, GUIObject):
			return obj.is_visible
		for v in obj.visibility_vertices:
			if vertex_in_zone(v.x, v.y, pos, self.size):
				return True
		return False
