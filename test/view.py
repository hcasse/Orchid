#!/usr/bin/python3

"""View test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.view = orc.InteractiveView()
		orc.Page.__init__(
			self,
			orc.VGroup([
				self.view,
				orc.Button("Pikachu", on_click=self.do_pikachu),
				orc.Button("Ninetales", on_click=self.do_ninetales)
			]),
			app = app
		)

	def do_pikachu(self):
		self.view.display(path = "pikachu.svg")

	def do_ninetales(self):
		self.view.display(path = "ninetales.svg")


orc.Application("View Test", first=MyPage).run()

