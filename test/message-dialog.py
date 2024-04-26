#!/usr/bin/python3

from orchid import *
from orchid import dialog

class MyPage(Page):

	def __init__(self, app):
		self.console = Console(init = "<b>Welcome !</b>")
		Page.__init__(
			self,
			VGroup([
				HGroup([
					Button("Warning", on_click=self.on_warning),
				]),
			]),
			app = app
		)

	def on_warning(self):
		d = dialog.Message(self, "This is a warning!", type="warning", title="My Warning")
		d.show()

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "message dialog test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug = True)

