#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		Page.__init__(
			self,
			HGroup([
				Label("Label..."),
				Field("Type text here!", size=10),
				Field(size = 2),
				Button("Done", on_click=self.done),
				Button("Give up", on_click=self.give_up)
			]),
			app = app
		)

	def done(self):
		print("Done!")

	def give_up(self):
		print("Give up!")

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "HGroup Test")

	def first(self):
		return MyPage(self)

run(MyApp())

