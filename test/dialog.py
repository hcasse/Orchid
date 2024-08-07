#!/usr/bin/python3

"""Dialog test."""

import orchid as orc
from orchid import dialog, Key

class CustomDialog(dialog.Base):

	def __init__(self, page):
		dialog.Base.__init__(self, page, title="Custom")
		self.set_main(orc.VGroup([
			orc.Label("Custom list"),
			orc.ListView(["one", "two", "three"]),
			orc.Button("Close", on_click=self.hide)
		]).key(Key.ESCAPE, self.test).key('a', self.test))
		self.set_style("min-width", "400px")
		self.set_style("min-height", "300px")
		#self.key(Key.ESCAPE, self.test)

	def test(self):
		print("DEBUG: Escape entered!")
		self.hide()

	def hide(self):
		print("DEBIG: hiding!")
		dialog.Base.hide(self)


class MyPage(orc.Page):

	def __init__(self, app):
		self.console = orc.Console(init = "<b>Welcome !</b>")

		def on_escape():
			print("DEBUG: escape!")

		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.HGroup([
					orc.Button("Show base", on_click=self.do_open),
					orc.Button("Show answer", on_click=self.open2),
					orc.Button("Show custom", on_click=self.open3)
				]),
				self.console
			]).key(Key.ESCAPE, on_escape),
			app = app
		)

		self.dialog = dialog.Base(
			self,
			orc.VGroup([
				orc.Label('First dialog!'),
				orc.Button("Close", on_click=self.close)
			])
		)

		self.dialog2 = dialog.Answer(
			self,
			"This is an anwer dialog!",
			title = "Answer Dialog",
			buttons = ["Zero", "One", "Two"],
			on_close=self.on_close2
		)

		self.dialog3 = None

	def do_open(self):
		print("DEBUG: open first dialog!")
		self.dialog.show()

	def open2(self):
		self.dialog2.show()

	def open3(self):
		if self.dialog3 is None:
			self.dialog3 = CustomDialog(self)
		self.dialog3.show()

	def on_close2(self, dialog, i):
		print("DEBUG: got", i, "from", dialog)

	def close(self):
		print("DEBUG: close")
		self.dialog.hide()

orc.Application("Dialog Test", first=MyPage).run(debug=True)

