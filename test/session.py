#!/usr/bin/python3

from orchid import *


class MySession(Session):

	def __init__(self, app, man):
		Session.__init__(self, app, man)
		self.cnt = 0

	def get_index(self):
		self.label = Label("0")
		return Page(
			VGroup([
				self.label,
				Button("Increment", on_click=self.on_click)
			]),
			app = self.app
		)

	def on_click(self):
		self.cnt += 1
		self.label.set_text(str(self.cnt))


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "session-test")

	def new_session(self, man):
		return MySession(self, man)

run(MyApp(), server = True)

