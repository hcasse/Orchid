#!/usr/bin/python3

"""Hello World test."""

import orchid as orc
from orchid.struct import Center

class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			orc.VGroup([
				Center(orc.Label("Hello, World!")),
				orc.Button("Quit", on_click=self.close)
			]),
			app = app
		)

orc.Application("Center", first=MyPage).run()

