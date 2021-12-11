import pyglet

from step_by_step.game.managers.game_manager import GameManager
from step_by_step.game.managers.settings import KeyEvent


class App(pyglet.window.Window):

	w = 1920
	h = 1080

	print_info = True

	def __init__(self):
		super().__init__(self.w, self.h, caption='Step by Step')

		pyglet.gl.glClearColor(0, 0, 0, 1)

		self.alive = True

		GameManager.init(screen_width=self.w, screen_height=self.h)

	def render(self):
		# update game logic
		GameManager.game_update()

		# refresh draw data
		GameManager.refresh_draw_data()

		# draw
		self.clear()
		GameManager.draw()

		# postcode
		GameManager.post_code()

		self.flip()

	def on_draw(self):
		self.render()

	def on_close(self):
		self.alive = False

	def on_mouse_motion(self, x, y, dx, dy):
		GameManager.camera_scroll_flag(x, y)

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		GameManager.camera_drag(-dx, -dy)

	def on_mouse_press(self, x, y, button, modifiers):
		GameManager.key_update(button, KeyEvent.PRESSED, {'mouse': (x, y)})

	def on_mouse_release(self, x, y, button, modifiers):
		GameManager.key_update(button, KeyEvent.RELEASED, {'mouse': (x, y)})

	def on_key_press(self, symbol, modifiers):
		GameManager.key_update(symbol, KeyEvent.PRESSED)

	def on_key_release(self, symbol, modifiers):
		GameManager.key_update(symbol, KeyEvent.RELEASED)

	def run(self):
		while self.alive:
			event = self.dispatch_events()
			if event:
				print(event)
			self.render()


if __name__ == '__main__':
	App().run()
