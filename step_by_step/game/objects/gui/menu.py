import abc

from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.gui.elements.panel import Panel
from step_by_step.game.objects.gui.elements.label import Label
from step_by_step.game.objects.gui.elements.button import Button
from step_by_step.game.objects.gui.gui_object import GUIObject
from step_by_step.game.objects.gui.settings import GUIStyle
from step_by_step.graphics.objects.settings import BatchGroup
from step_by_step.graphics.settings import Alignment


class Menu(GUIObject, abc.ABC):

	_base_name = 'Menu'
	_batch_group = BatchGroup.GUI_OBJECT_BACKGROUND

	def __init__(
		self,
		pos: Vector2f,
		size: Vector2f,
		gui_style: GUIStyle,
	):
		super(Menu, self).__init__(
			pos=pos,
			size=size
		)
		self.gui_style = gui_style
		self._init_elements()

	@abc.abstractmethod
	def _init_elements(self):
		raise NotImplementedError()


class RightMenu(Menu):

	_base_name = 'Right Menu'

	def _init_elements(self):

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
					color=self.gui_style.label_color,
					text='Info',
					text_color=self.gui_style.label_text_color,
					border_width=self.gui_style.label_border_width,
					border_color=self.gui_style.label_border_color,
					align=Alignment.CENTER
				),
				Button(
					pos=Vector2f(0, p.y - 110),
					size=Vector2f(350, 50),
					color=self.gui_style.button_color,
					text='Select',
					align=Alignment.CENTER
				),
				Button(
					pos=Vector2f(0, p.y - 170),
					size=Vector2f(350, 50),
					color=self.gui_style.button_color,
					text='Delete',
					align=Alignment.CENTER
				),
				Button(
					pos=Vector2f(0, p.y - 230),
					size=Vector2f(350, 50),
					color=self.gui_style.button_color,
					text='Info',
					align=Alignment.CENTER
				)
			]
		)


class UpperBarMenu(Menu):

	_base_name = 'Upper Bar Menu'

	def _init_elements(self):

		p = Panel(
			pos=Vector2f(0, 0),
			size=self.size,
			color=self.gui_style.panel_color
		)
		self.add_child(p)
