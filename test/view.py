#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		self.view = InteractiveView()
		Page.__init__(
			self,
			VGroup([
				self.view,
				Button("Pikachu", on_click=self.do_pikachu),
				Button("Ninetales", on_click=self.do_ninetales)
			]),
			app = app
		)

	def do_pikachu(self):
		self.view.display(path = "pikachu.svg")

	def do_ninetales(self):
		self.view.display(path = "ninetales.svg")


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "MyApp")

	def first(self):
		return MyPage(self)

run(MyApp())

