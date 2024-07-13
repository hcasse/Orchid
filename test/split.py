#!/usr/bin/python3

"""Split pane test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			orc.SplitPane(
				orc.Editor(init = "Hello, World!"),
				orc.Editor(init = "second"),
				pos=30
			),
			app = app
		)


orc.Application("SplitPane Test", first=MyPage).run()


