#!/usr/bin/env python3

from orchid import *
from orchid.svg import Canvas, Content
from orchid.util import Buffer
from orchid.server import Provider

# https://www.sarasoueidan.com/blog/svg-coordinate-systems/

class LED(Content):

	def  __init__(self, x, y, image, color, **args):
		Content.__init__(self, image, **args)
		self.color = color
		self.state = False
		self.scale(.1)
		self.translate(x, y)

	def set(self, color1, color2):
		if self.parent.online():
			id = self.get_id()
			self.set_direct_attr(id + "_path1", "fill", "#" + color1)
			self.set_direct_attr(id + "_path2", "fill", "#" + color1)
			self.set_direct_attr(id + "_stop1", "style", "stop-color:#" + color2)
			self.set_direct_attr(id + "_stop2", "style", "stop-color:#" + color2 + ";stop-opacity:0")

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
					Button("red", on_click=self.red),
					Button("green", on_click=self.green)
				]),
				self.canvas
			]),
			app = app)

		# prepare SVG
		buf = Buffer()
		with open("led.svg") as input:
			l = input.readline()
			while not l.startswith("<svg"):
				l = input.readline()
			buf.write(l)
			#while not l.endswith(">\n"):
			#	l = input.readline()
			l = input.readline()
			while not l.startswith("</svg>"):
				buf.write(l)
				l = input.readline()
		self.image = str(buf)

		self.red = self.canvas.record(LED(0, 0, self.image, "FF0000"))
		self.green = self.canvas.record(LED(50, 0, self.image, "00FF00"))

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

