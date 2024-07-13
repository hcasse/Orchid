#!/usr/bin/python3

"""Layered pane test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):

		self.layer = orc.LayeredPane([
			orc.Editor(init = "Layer 0!"),
			orc.Editor(init = "Layer 1!"),
			orc.Console(init = "coucou!")
		])

		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.HGroup([
					orc.Button("Layer 0", on_click=self.set_zero),
					orc.Button("Layer 1", on_click=self.set_one),
					orc.Button("Layer 2", on_click=self.set_two),
				]),
				self.layer,
				orc.Label("below")
			]),
			app = app
		)

	def set_zero(self):
		self.layer.set_layer(0)

	def set_one(self):
		self.layer.set_layer(1)

	def set_two(self):
		self.layer.set_layer(2)


orc.Application("Layered Pane Test", first=MyPage).run()

