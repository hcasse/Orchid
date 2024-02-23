#!/usr/bin/python3

from orchid import *
from orchid import dialog
from orchid.group import VGroup

class MyPage(Page):

	def __init__(self, app):
		self.console = Console(init = "<b>Welcome !</b>")
		Page.__init__(
			self,
			VGroup([
				HGroup([
					Button("Show base", on_click=self.open),
					Button("Show answer", on_click=self.open2)
				]),
				self.console
			]),
			app = app
		)

		self.dialog = dialog.Base(
			self,
			VGroup([
				Label('First dialog!'),
				Button("Close", on_click=self.close)
			])
		)

		self.dialog2 = dialog.Answer(
			self,
			"This is an anwer dialog!",
			title = "Answer Dialog",
			buttons = ["Zero", "One", "Two"],
			on_close=self.on_close2
		)

	def open(self):
		self.dialog.show()

	def open2(self):
		self.dialog2.show()

	def on_close2(self, dialog, i):
		print("DEBUG: got", i, "from", dialog)

	def close(self):
		print("DEBUG: close")
		self.dialog.hide()


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "dialog test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug = True)

