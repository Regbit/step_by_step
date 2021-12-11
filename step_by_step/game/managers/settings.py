from enum import Enum


class KeyEvent(Enum):
	PRESSED = 'pressed'
	RELEASED = 'released'


class ScreenScrollFlag(Enum):
	UP = 'up'
	DOWN = 'down'
	LEFT = 'left'
	RIGHT = 'right'
