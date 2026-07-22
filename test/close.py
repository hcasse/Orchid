#!/usr/bin/python3

"""Application close test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.Label("Clock below to close:"),
				orc.Button("Close!", on_click=self.close)
			]),
			app = app
		)

orc.Application("Closing Test", first=MyPage).run()

