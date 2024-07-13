#!/usr/bin/python3

"""Message dialog test."""

import orchid as orc
from orchid import dialog

class MyPage(orc.Page):

	def __init__(self, app):
		self.console = orc.Console(init = "<b>Welcome !</b>")
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.HGroup([
					orc.Button("Warning", on_click=self.on_warning),
					orc.Button("Error", on_click=self.on_error),
					orc.Button("Info", on_click=self.on_info),
				]),
			]),
			app = app
		)

	def on_warning(self):
		d = dialog.Message(self, "This is a warning!\nAnother line.",
			type="warning", title="My Warning", on_close=self.do_close)
		d.show()

	def on_error(self):
		d = dialog.Message(self, "There is an error:\nIt's joke!",
			type="error", title="Fatal Error", on_close=self.do_close)
		d.show()

	def on_info(self):
		d = dialog.Message(self, "Information.", type="info",
			title="Information", on_close=self.do_close)
		d.show()

	def do_close(self):
		print("Dialog closed!")

orc.Application("Message Dialog Test", first=MyPage).run()

