from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.gui.elements import Panel, Label, Button
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.game.objects.gui.settings import GUIStyle
from step_by_step.graphics.objects.settings import BatchGroup


class Menu(GUIObject):

	_base_name = 'Menu'
	_batch_group = BatchGroup.GUI_OBJECT_BACKGROUND

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		gui_style: GUIStyle
	):
		super(Menu, self).__init__(
			pos=pos,
			size=size,
			is_selectable=False,
			is_clickable=False,
			is_visible=True
		)
		self.gui_style = gui_style


class RightMenu(Menu):

	_base_name = 'Right Menu'

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		gui_style: GUIStyle
	):
		super(RightMenu, self).__init__(
			pos=pos,
			size=size,
			gui_style=gui_style
		)

		p = Panel(
			pos=Vector2f(0, 0),
			size=self.size,
			color=self.gui_style.panel_color
		)
		self.add_child(p)

		p.add_children(
			[
				Label(
					pos=Vector2f(0, p.y - 50),
					size=Vector2f(350, 50),
					text='Info',
					color=self.gui_style.label_color,
					text_color=self.gui_style.label_text_color,
					border_width=self.gui_style.label_border_width,
					border_color=self.gui_style.label_border_color,
				),
				Button(
					pos=Vector2f(0, p.y - 110),
					size=Vector2f(350, 50),
					color=self.gui_style.button_color,
					text='Select'
				),
				Button(
					pos=Vector2f(0, p.y - 170),
					size=Vector2f(350, 50),
					color=self.gui_style.button_color,
					text='Delete'
				),
				Button(
					pos=Vector2f(0, p.y - 230),
					size=Vector2f(350, 50),
					color=self.gui_style.button_color,
					text='Info'
				)
			]
		)
