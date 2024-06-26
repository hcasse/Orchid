#!/usr/bin/python3

from orchid import *
from orchid import struct

class MyPage(Page):

	def __init__(self, app):
		Page.__init__(
			self,
			VGroup([
				struct.Header(
					"app-test",
					[
						Button("click here", on_click=self.clicked),
						Button(image = Icon("quit"), on_click=self.close)
					]
				),
				Editor(init = "Hello, World!")
			]),
			app = app
		)

	def clicked(self):
		print("DEBUG: clicked!")

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "app-test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

