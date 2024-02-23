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
					Button("Show", on_click=self.open),
					Button("Not modal", on_click=self.bad),
				]),
				self.console
			]),
			app = app
		)
		print("DEBUG: after page")
		self.dialog = dialog.Base(
			self,
			VGroup([
				Label('First dialog!'),
				Button("Close", on_click=self.close),
				Button("Left", on_click=self.left)
			])
		)

	def open(self):
		self.dialog.show()

	def close(self):
		print("DEBUG: close")
		self.dialog.hide()

	def bad(self):
		print("DEBUG: not modal!")

	def left(self):
		self.dialog.set_style("left", "4px")

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "dialog test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug = True)

