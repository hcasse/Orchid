#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		Page.__init__(
			self,
			VGroup([
				Banner("This is a banner!"),
				Label("Simple Label"),
				Label(AssetImage("basic/info.svg", width=64)),
				Button("Quit", on_click=self.close)
			]),
			app = app
		)

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Label Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

