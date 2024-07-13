#!/usr/bin/python3


"""Menu test."""

import orchid as orc

class MyPage(orc.Page):

	def make_menu(self):
		return orc.MenuButton(
			orc.Menu([
				orc.Button("Menu 1", on_click=self.menu1),
				orc.Button("Menu 2", on_click=self.menu2),
				orc.Button("Menu 3 long")
			])
		)

	def __init__(self, app):
		orc.Page.__init__(self,
			orc.VGroup([
				orc.HGroup([
					self.make_menu(),
					orc.Spring(hexpand=True),
					self.make_menu()
				]),
				orc.Editor(),
				orc.HGroup([
					self.make_menu(),
					orc.Spring(hexpand=True),
					self.make_menu()
				])
			]),
			app = app)

	def menu1(self):
		print("DEBUG: menu1!")

	def menu2(self):
		print("DEBUG: menu2!")


orc.Application("Lenu Test", first=MyPage).run()


