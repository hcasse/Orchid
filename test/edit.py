#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		Page.__init__(
			self,
			VGroup([
				Label("Editor test"),
				Editor(init = "Hello, World!"),
				HGroup([
					Editor(init = "<b>first</b>"),
					Editor(init = "second")
				])
			]),
			app = app
		)

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Editor Test")

	def first(self):
		return MyPage(self)

run(MyApp())

