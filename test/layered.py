#!/usr/bin/python3

"""Layered pane test."""

import orchid as orc
from orchid import svg
from orchid.button import Button
from orchid.group import VGroup

class MyPage(orc.Page):

	def __init__(self, app):

		self.canvas = svg.Canvas()
		self.circle = self.canvas.circle(50, 50, 100)
		self.canvas2 = svg.Canvas()
		self.canvas2.circle(200, 200, 50)
		self.layer = orc.LayeredPane([
			orc.Editor(init = "Layer 0!"),
			orc.Editor(init = "Layer 1!"),
			orc.Console(init = "coucou!"),
			self.canvas,
			VGroup([Button("Test"), self.canvas2])
		])

		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.HGroup([
					orc.Button("Layer 0", on_click=self.set_zero),
					orc.Button("Layer 1", on_click=self.set_one),
					orc.Button("Layer 2", on_click=self.set_two),
					orc.Button("SVG", on_click=lambda: self.layer.set_layer(3)),
					orc.Button("SVG2", on_click=lambda: self.layer.set_layer(4)),
					orc.Button("SVG size", on_click=self.show_svg_size),
					orc.Button("circle size", on_click=self.show_circle_size)
				]),
				self.layer,
				orc.Label("below")
			]),
			app = app
		)

	def show_circle_size(self):
		def get_size(width, height):
			print(f"circle size: {width}x{height}")
		self.canvas.get_size(get_size, self.circle.get_id())

	def show_svg_size(self):
		def get_size(width, height):
			print(f"canvas size: {width}x{height}")
		self.canvas.get_size(get_size)

	def set_zero(self):
		self.layer.set_layer(0)

	def set_one(self):
		self.layer.set_layer(1)

	def set_two(self):
		self.layer.set_layer(2)


orc.Application("Layered Pane Test", first=MyPage).run()

