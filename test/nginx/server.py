#!env python3

"""Hello World test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.Label("Hello, World!"),
				orc.Button("Quit", on_click=self.close)
			]),
			app = app
		)

orc.Application("Hello World", first=MyPage).run(
	debug=True,
	server=True,
	browser=False,
	port=4444,
	proxy="http://localhost/server")
