from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.gui.menu import RightMenu, UpperBarMenu
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.game.objects.gui.settings import GUIStyle, UPPER_BAR_MENU_HEIGHT, RIGHT_MENU_WIDTH
from step_by_step.graphics.objects.settings import BatchGroup


class GUI(GUIObject):

	_base_name = 'GUI'
	_batch_group = BatchGroup.GUI_OBJECT_BACKGROUND

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


class ViewportGUI(GUI):

	_base_name = 'Viewport GUI'
	_camera_pos_shift: Vector2f = None
	_camera_size_shift: Vector2f = None

	def self_destruct_clean_up(self):
		super(ViewportGUI, self).self_destruct_clean_up()
		self._camera_pos_shift = None
		self._camera_size_shift = None

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		gui_style: GUIStyle
	):
		super(ViewportGUI, self).__init__(
			pos=pos,
			size=size,
			gui_style=gui_style
		)
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


class MainGameGUI(ViewportGUI):

	_base_name = 'Main Game GUI'
	_upper_bar_menu: UpperBarMenu = None
	_right_menu: RightMenu = None

	def self_destruct_clean_up(self):
		super(ViewportGUI, self).self_destruct_clean_up()
		self._upper_bar_menu = None
		self._right_menu = None

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
		self._init_upper_bar_menu()
		self._init_right_menu()

	def _init_upper_bar_menu(self):
		self._upper_bar_menu = UpperBarMenu(
			pos=Vector2f(self.pos.x, self.pos.y * 2 - UPPER_BAR_MENU_HEIGHT / 2),
			size=Vector2f(self.size.x, UPPER_BAR_MENU_HEIGHT),
			gui_style=self.gui_style
		)
		self.add_child(self._upper_bar_menu)
		self.camera_pos_shift += Vector2f(0, UPPER_BAR_MENU_HEIGHT / 2)
		self.camera_size_shift += Vector2f(0, UPPER_BAR_MENU_HEIGHT)

	def _init_right_menu(self):
		self._right_menu = RightMenu(
			pos=Vector2f(self.pos.x * 2 - RIGHT_MENU_WIDTH / 2, self.pos.y) - self.camera_pos_shift,
			size=Vector2f(RIGHT_MENU_WIDTH, self.size.y) - self.camera_size_shift,
			gui_style=self.gui_style
		)
		self.add_child(self._right_menu)
		self.camera_pos_shift += Vector2f(RIGHT_MENU_WIDTH / 2, 0)
		self.camera_size_shift += Vector2f(RIGHT_MENU_WIDTH, 0)

	def switch_hide_right_menu(self):
		self._right_menu.is_visible = not self._right_menu.is_visible
