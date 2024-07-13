#!/usr/bin/env python3

"""SVG injection test."""

import orchid as orc
from orchid.svg import Canvas, Content
from orchid.util import Buffer

# https://www.sarasoueidan.com/blog/svg-coordinate-systems/

class LED(Content):

	def  __init__(self, x, y, image, color, **args):
		Content.__init__(self, image, **args)
		self.color = color
		self.state = False
		self.scale(.1)
		self.translate(x, y)

	def finalize(self):
		Content.finalize(self)
		self.add_event("onclick", self.on_click)
		self.add_event("onmousedown", self.on_mouse_down)
		self.add_event("onmouseup", self.on_mouse_up)

	def on_click(self):
		print(f"Click {self.color}!" )
		self.invert()

	def on_mouse_down(self):
		print(f"Pushed {self.color}!")

	def on_mouse_up(self):
		print("Release {self.color}!")

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

class MyPage(orc.Page):

	def __init__(self, app):
		self.on = False

		# prepare SVG
		buf = Buffer()
		with open("led.svg", encoding="utf8") as input:
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
			buts.append(orc.Button(color, on_click=shape.invert))
			x = x + 50

		# build UI
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.HGroup(buts),
				self.canvas
			]),
			app = app)


orc.Application("SVG Inject Test", first=MyPage).run()

