#!/usr/bin/env python3

from orchid import *
from orchid.svg import Canvas
from orchid.util import Buffer
from orchid.server import Provider

class LED:

	def  __init__(self, x, y, image, color, canvas):
		self.color = color
		x -= 200
		num = canvas.inject("<g transform='scale(0.1)translate(%d, %d)'>%s" % (x, y, image), True)
		self.state = False
		self.id = canvas.get_object_id(num)
		self.page = canvas.get_page()

	def set(self, color1, color2):
		self.page.set_direct_attr(self.id + "_path", "fill", "#" + color1)
		self.page.set_direct_attr(self.id + "_s1", "style", "stop-color:#" + color2)
		self.page.set_direct_attr(self.id + "_s2", "style", "stop-color:#" + color2 + ";stop-opacity:0")

	def on(self):
		if not self.state:
			self.set(self.color, self.color)
			self.state = True

	def off(self):
		if self.state:
			self.set("CCCCCC", "FFFFFF")
			self.state = False

	def invert(self):
		if self.state:
			self.off()
		else:
			self.on()
	

class MyPage(Page):

	def __init__(self, app):
		self.on = False

		# build UI
		self.canvas = Canvas()
		Page.__init__(
			self,
			VGroup([
				HGroup([
					Button("show", on_click=self.show),
					Button("red", on_click=self.red),
					Button("green", on_click=self.green)
				]),
				self.canvas
			]),
			app = app)

		# prepare SVG
		buf = Buffer()
		with open("led.svg") as input:
			for i in range(0, 8):
				l = input.readline()
			while not l.startswith("</svg>"):
				buf.write(l)
				l = input.readline()
		self.image = str(buf)

	def show(self):
		self.red = LED(0, 0, self.image, "FF0000", self.canvas)
		self.green = LED(250, 0, self.image, "00FF00", self.canvas)

	def red(self):
		self.red.invert()

	def green(self):
		self.green.invert()


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "SVG Inject Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

