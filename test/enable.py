#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		self.target = Button("Target", on_click=self.close)
		Page.__init__(
			self,
			VGroup([
				self.target,
				Button("Enable", on_click=self.do_enable),
				Button("Disable", on_click=self.do_disable),
			]),
			app = app
		)

	def do_enable(self):
		self.target.enable()

	def do_disable(self):
		self.target.disable()


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "MyApp")

	def first(self):
		return MyPage(self)

run(MyApp())

