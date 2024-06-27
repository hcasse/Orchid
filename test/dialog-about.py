#!/usr/bin/python3

from orchid import *
from orchid import dialog

class MyPage(Page):

	def __init__(self, app):
		self.console = Console(init = "<b>Welcome !</b>")
		Page.__init__(
			self,
			VGroup([
				HGroup([
					Button("About", on_click=self.about),
				]),
			]),
			app = app
		)
		self.dialog = None

	def about(self):
		if self.dialog is None:
			self.dialog = dialog.About(self)
		self.dialog.show()


class MyApp(Application):

	def __init__(self):
		Application.__init__(self,
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
			website="https://github.com/hcasse/Orchid"
		)
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug = True)

