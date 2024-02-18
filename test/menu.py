#!/usr/bin/python3

from orchid import *
from orchid import popup

class MyPage(Page):

	def __init__(self, app):
		self.menu = popup.MenuButton(
			popup.Menu([
				Button("Menu 1", on_click=self.menu1),
				Button("Menu 2", on_click=self.menu2)
			])
		)

		Page.__init__(self,
			VGroup([
				HGroup([
					self.menu,
					Spring(hexpand=True)
				]),
				Editor()
			]),
			app = app)

	def menu1(self):
		print("DEBUG: menu1!")

	def menu2(self):
		print("DEBUG: menu2!")


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "MyApp")

	def first(self):
		return MyPage(self)

run(MyApp())

