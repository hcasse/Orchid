#!/usr/bin/python3

"""Label test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.Banner("This is a banner!"),
				orc.Label("Simple Label"),
				orc.Label(orc.AssetImage("basic/info.svg", width=64)),
				orc.Button("Quit", on_click=self.close)
			]),
			app = app
		)

orc.Application("Label Test", first=MyPage).run()

