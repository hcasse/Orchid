#!/usr/bin/python3

"""Split pane test."""

import orchid as orc
from orchid import split

class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			orc.HGroup([
				orc.Label("Here!"),
				split.Pane(
					orc.Editor(init = "Hello, World!"),
					split.Pane(
						orc.Editor(init = "second"),
						orc.Editor(init = "third"),
						vert=True
					),
					pos=30
				)
			]),
			app = app
		)


orc.Application("split.Pane Test", first=MyPage).run()


