#!/usr/bin/python3

from orchid import *
from orchid.split import SplitPane

class MyPage(Page):

	def __init__(self, app):
		Page.__init__(
			self,
			SplitPane(
				Editor(init = "Hello, World!"),
				Editor(init = "second"),
				pos=30
			),
			app = app
		)


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "SplitPane Test")

	def first(self):
		return MyPage(self)

run(MyApp())


