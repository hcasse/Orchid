#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		self.cnt = 0
		self.console = Console(init = "<b>Welcome !</b>")
		Page.__init__(
			self,
			VGroup([
				HGroup([
					Button("One more", on_click=self.append),
					Button("Clear", on_click=self.clear)
				]),
				self.console
			]),
			app = app
		)

	def append(self):
		self.console.append("One line <b>%d</b> !!!!" % self.cnt)
		self.cnt += 1

	def clear(self):
		self.console.clear()


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "console-test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp())

