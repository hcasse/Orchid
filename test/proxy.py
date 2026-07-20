#!/usr/bin/python3

"""Proxy Test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.Label("Hello, World!"),
				orc.Button("Click", on_click=self.click)
			]),
			app = app
		)

	def click(self):
		print("Clicked!")


orc.Application("Proxy Test", first=MyPage).run(
	host="localhost",
	port=8888,
	proxy="http://localhost:8888/here",
	browser=False,
	server=True,
	debug=True)


