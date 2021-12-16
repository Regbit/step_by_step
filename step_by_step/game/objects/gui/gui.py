from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.gui.menu import RightMenu
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.game.objects.gui.settings import RIGHT_MENU_BAR_WIDTH, GUIStyle
from step_by_step.graphics.objects.settings import BatchGroup


class GUI(GUIObject):

	_base_name = 'GUI'
	_batch_group = BatchGroup.GUI_OBJECT_BACKGROUND
	_camera_pos_shift: Vector2f = None
	_camera_size_shift = None

	def self_destruct_clean_up(self):
		super(GUI, self).self_destruct_clean_up()
		self._camera_pos_shift = None
		self._camera_size_shift = None

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		gui_style: GUIStyle
	):
		super(GUI, self).__init__(
			pos=pos,
			size=size,
			is_selectable=False,
			is_clickable=False,
			is_visible=True
		)
		self.gui_style = gui_style
		self._camera_pos_shift = Vector2f(0, 0)
		self._camera_size_shift = Vector2f(0, 0)

	@property
	def camera_pos_shift(self) -> Vector2f:
		return self._camera_pos_shift if self.is_visible else Vector2f(0, 0)

	@camera_pos_shift.setter
	def camera_pos_shift(self, vec: Vector2f):
		self._camera_pos_shift = vec

	@property
	def camera_size_shift(self) -> Vector2f:
		return self._camera_size_shift if self.is_visible else Vector2f(0, 0)

	@camera_size_shift.setter
	def camera_size_shift(self, vec: Vector2f):
		self._camera_size_shift = vec


class MainGameGUI(GUI):

	_base_name = 'Main Game GUI'

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		gui_style: GUIStyle
	):
		super(MainGameGUI, self).__init__(
			pos=pos,
			size=size,
			gui_style=gui_style
		)

		right_menu = RightMenu(
			pos=Vector2f(self.pos.x * 2 - RIGHT_MENU_BAR_WIDTH / 2, self.pos.y),
			size=Vector2f(RIGHT_MENU_BAR_WIDTH, self.size.y),
			gui_style=gui_style
		)

		self.add_child(right_menu)

		self.camera_pos_shift += Vector2f(RIGHT_MENU_BAR_WIDTH / 2, 0)
		self.camera_size_shift += Vector2f(RIGHT_MENU_BAR_WIDTH, 0)

