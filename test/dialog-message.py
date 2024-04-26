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
					Button("Error", on_click=self.on_error),
					Button("Info", on_click=self.on_info),
				]),
			]),
			app = app
		)

	def on_warning(self):
		d = dialog.Message(self, "This is a warning!\nAnother line.", type="warning", title="My Warning", on_close=self.do_close)
		d.show()

	def on_error(self):
		d = dialog.Message(self, "There is an error:\nIt's joke!", type="error", title="Fatal Error", on_close=self.do_close)
		d.show()

	def on_info(self):
		d = dialog.Message(self, "Information.", type="info", title="Information", on_close=self.do_close)
		d.show()

	def do_close(self):
		print("Dialog closed!")

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "message dialog test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug = True)

