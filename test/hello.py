#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		Page.__init__(
			self,
			VGroup([
				Label("Hello, World!"),
				Button("Quit", on_click=self.close)
			]),
			app = app
		)

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "MyApp")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

