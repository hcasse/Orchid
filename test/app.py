#!/usr/bin/python3

"""Simple application test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.Header(
					"app-test",
					[
						orc.Button("click here", on_click=self.clicked),
						orc.Button(image = orc.Icon(orc.IconType.QUIT), on_click=self.close)
					]
				),
				orc.Editor(init = "Hello, World!")
			]),
			app = app
		)

	def clicked(self):
		print("DEBUG: clicked!")

orc.Application("Application Test", first=MyPage).run()

