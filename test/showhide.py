#!/usr/bin/python3

"""Show/hide test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.lookup = orc.HGroup([
			orc.Field("Lookup"),
			orc.Button("Close", on_click=self.end_lookup)
		])
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.Button("Lookup", on_click=self.do_lookup),
				orc.Editor(init = "Edit something."),
				self.lookup
			]),
			app = app
		)
		self.lookup.hide()

	def do_lookup(self):
		self.lookup.show()

	def end_lookup(self):
		self.lookup.hide()


orc.Application("Show/Hide Test", first=MyPage).run()

