#!/usr/bin/python3

"""Test for about dialog."""

import orchid as orc
from orchid import dialog

class MyPage(orc.Page):

	def __init__(self, app):
		self.console = orc.Console(init = "<b>Welcome !</b>")
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.HGroup([
					orc.Button("About", on_click=self.about),
				]),
			]),
			app = app
		)
		self.dialog = None

	def about(self):
		if self.dialog is None:
			self.dialog = dialog.About(self)
		self.dialog.show()

orc.Application(
	"message dialog test",
	version="1.0.2",
	icon="orchid.svg",
	description="""
Incredible application.
Made by myself.
But in fact it's a test!
""",
	license="LGPL v3",
	copyright="Copyright (c) 2024, myself <myself@here.fr>",
	website="https://github.com/hcasse/Orchid",
	first=MyPage
).run()

