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

	def finalize(self, page):
		Content.finalize(self, page)
		self.add_event("onclick", self.on_click)
		self.add_event("onmousedown", self.on_mouse_down)
		self.add_event("onmouseup", self.on_mouse_up)

	def on_click(self):
		print("Click %s!" % self.color)
		self.invert()

	def on_mouse_down(self):
		print("Pushed %s!" % self.color)

	def on_mouse_up(self):
		print("Release %s!" % self.color)

	def set(self, color1, color2):
		if self.parent.online():
			id = self.get_id()
			self.set_direct_attr(id + "_path1", "fill", color1)
			self.set_direct_attr(id + "_path2", "fill", color1)
			self.set_direct_attr(id + "_stop1", "style", "stop-color:" + color2)
			self.set_direct_attr(id + "_stop2", "style", "stop-color:" + color2 + ";stop-opacity:0")

	def on(self):
		if not self.state:
			self.set(self.color, self.color)
			self.state = True

	def off(self):
		if self.state:
			self.set("#CCCCCC", "#FFFFFF")
			self.state = False

	def invert(self):
		if self.state:
			self.off()
		else:
			self.on()
	

COLORS = ["red", "green", "Gold", "MediumPurple", "YellowGreen"]

class MyPage(Page):

	def __init__(self, app):
		self.on = False

		# prepare SVG
		buf = Buffer()
		with open("led.svg") as input:
			l = input.readline()
			while not l.startswith("<svg"):
				l = input.readline()
			#buf.write(l)
			while not l.endswith(">\n"):
				l = input.readline()
			l = input.readline()
			while not l.startswith("</svg>"):
				buf.write(l)
				l = input.readline()
		self.image = str(buf)

		# build colors
		self.canvas = Canvas()
		buts = []
		x = 0
		for color in COLORS:
			shape = self.canvas.record(LED(x, 0, self.image, color))
			buts.append(Button(color, on_click=shape.invert))
			x = x + 50

		# build UI
		Page.__init__(
			self,
			VGroup([
				HGroup(buts),
				self.canvas
			]),
			app = app)


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "SVG Inject Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

