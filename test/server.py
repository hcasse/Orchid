#!/usr/bin/env python3

"""Server test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.Button("Close", on_click=self.close)
			]),
			app = app
		)


orc.Application("Server Test", first=MyPage).run(server=True, debug=True)

