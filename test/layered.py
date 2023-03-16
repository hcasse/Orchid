#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):

		self.layer = LayeredPane([
			Editor(init = "Layer 0!"),
			Editor(init = "Layer 1!"),
			Console(init = "coucou!")
		])
		
		Page.__init__(
			self,
			VGroup([
				HGroup([
					Button("Layer 0", on_click=self.set_zero),
					Button("Layer 1", on_click=self.set_one),
					Button("Layer 2", on_click=self.set_two),
				]),
				self.layer,
				Label("below")
			]),
			app = app
		)

	def set_zero(self):
		self.layer.set_layer(0)

	def set_one(self):
		self.layer.set_layer(1)

	def set_two(self):
		self.layer.set_layer(2)


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "layered-test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp())

