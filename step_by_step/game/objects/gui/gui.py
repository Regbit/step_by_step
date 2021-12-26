from step_by_step.common.shaped import Shaped
from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.game_object import DrawnGameObject
from step_by_step.game.objects.gui.menu import RightMenu, UpperBarMenu
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.game.objects.gui.settings import GUIStyle, UPPER_BAR_MENU_HEIGHT, RIGHT_MENU_WIDTH
from step_by_step.game.objects.gui.viewport import Viewport
from step_by_step.graphics.objects.settings import BatchGroup


class GUI(GUIObject):

	_base_name = 'GUI'
	_batch_group = BatchGroup.GUI_OBJECT_BACKGROUND
	_screen: Shaped

	def self_destruct_clean_up(self):
		super(GUI, self).self_destruct_clean_up()
		self._screen = None

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		screen: Shaped,
		gui_style: GUIStyle
	):
		super(GUI, self).__init__(
			pos=pos,
			size=size
		)
		self.gui_style = gui_style
		self._screen = screen


class ViewportGUI(GUI):

	_base_name = 'Viewport GUI'
	_viewport: Viewport

	def self_destruct_clean_up(self):
		super(ViewportGUI, self).self_destruct_clean_up()
		self._viewport = None

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		screen: Shaped,
		gui_style: GUIStyle
	):
		super(ViewportGUI, self).__init__(
			pos=pos,
			size=size,
			screen=screen,
			gui_style=gui_style
		)

		self._init_viewport()

	@property
	def viewport(self) -> Viewport:
		return self._viewport

	@property
	def cam_world_pos(self) -> Vector2f:
		return self._viewport.camera.pos

	def _init_viewport(self):
		self._viewport = Viewport(
			pos=Vector2f(0, 0),
			size=self.size,
			screen=self._screen,
		)
		self.add_child(self._viewport)

	def is_object_in_frame(self, obj: DrawnGameObject) -> bool:
		return self._viewport.is_object_in_frame(obj)


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
		screen: Shaped,
		gui_style: GUIStyle
	):
		super(MainGameGUI, self).__init__(
			pos=pos,
			size=size,
			screen=screen,
			gui_style=gui_style
		)

		# self._init_upper_bar_menu()
		# self._init_right_menu()

	def _init_upper_bar_menu(self):
		self._upper_bar_menu = UpperBarMenu(
			pos=Vector2f(self.pos.x, self.pos.y * 2 - UPPER_BAR_MENU_HEIGHT / 2),
			size=Vector2f(self.size.x, UPPER_BAR_MENU_HEIGHT),
			gui_style=self.gui_style
		)
		self.add_child(self._upper_bar_menu)

	def _init_right_menu(self):
		self._right_menu = RightMenu(
			pos=Vector2f(self.pos.x * 2 - RIGHT_MENU_WIDTH / 2, self.pos.y) - self.camera_pos_shift,
			size=Vector2f(RIGHT_MENU_WIDTH, self.size.y) - self.camera_size_shift,
			gui_style=self.gui_style
		)
		self.add_child(self._right_menu)

	def switch_show_right_menu(self):
		self._right_menu.is_visible = not self._right_menu.is_visible
