from enum import Enum

OSWALD_LIGHT = 'Oswald Light'
OSWALD_MEDIUM = 'Oswald Medium'

BASE_FONT = OSWALD_LIGHT
BASE_FONT_SIZE = 10


class Alignment(Enum):
	LEFT = 'left'
	CENTER = 'center'
	RIGHT = 'right'


class AnchorHorizontal(Enum):
	LEFT = 'left'
	CENTER = 'center'
	RIGHT = 'right'


class AnchorVertical(Enum):
	BOTTOM = 'bottom'
	BASELINE = 'baseline'
	CENTER = 'center'
	TOP = 'top'
