#!/usr/bin/python3

"""Test for console."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.cnt = 0
		self.console = orc.Console(init = "<b>Welcome !</b>")
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.HGroup([
					orc.Button("One more", on_click=self.append),
					orc.Button("Clear", on_click=self.clear)
				]),
				self.console
			]),
			app = app
		)

	def append(self):
		self.console.append(f"One line <b>{self.cnt}</b> !!!!")
		self.cnt += 1

	def clear(self):
		self.console.clear()

orc.Application("Console Test", first=MyPage).run()

