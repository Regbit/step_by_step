import math


def calc_radius(x, y, precision):
	return round(math.sqrt(x ** 2 + y ** 2), precision)


def calc_angle(x, y, precision):
	return round(math.atan2(y, x), precision)


def calc_x(r, a, precision):
	return round(r * math.cos(a), precision)


def calc_y(r, a, precision):
	return round(r * math.sin(a), precision)
