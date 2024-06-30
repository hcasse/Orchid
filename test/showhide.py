#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		self.lookup = HGroup([
			Field("Lookup"),
			Button("Close", on_click=self.end_lookup)
		])
		Page.__init__(
			self,
			VGroup([
				Button("Lookup", on_click=self.do_lookup),
				Editor(init = "Edit something."),
				self.lookup
			]),
			app = app
		)
		self.lookup.hide()

	def do_lookup(self):
		self.lookup.show()

	def end_lookup(self):
		self.lookup.hide()


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Show/Hide Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

