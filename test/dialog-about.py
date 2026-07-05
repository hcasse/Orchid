#!/usr/bin/python3

"""Test for about dialog."""

import orchid as orc
from orchid import dialog
from orchid.image import AssetImage
from orchid.base import People

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
			self.dialog = dialog.About(self,
				comment = "A simple comment! Type anything you want here!",
				contribs = [
					(AssetImage("images/python-logo-only.png", width=48), "Python", "https://www.python.org/")
				]
			)
		self.dialog.show()

orc.Application(
	"message dialog test",
	version="1.0.2",
	icon="images/orchid.svg",
	description="""
Incredible application.
Made by myself.
But in fact it's a test!
""",
	license="LGPL v3",
	copyright="Copyright (c) 2024, myself <myself@here.fr>",
	website="https://github.com/hcasse/Orchid",
	authors = [People("Burt", "Lancaster", links=[("email", "email:but.lancaster@here.us")])],
	first=MyPage
).run()

