#!/usr/bin/python3

"""Dynamic group changes."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.hgroup = orc.HGroup([
			orc.Button("Add", on_click=self.add),
			orc.Button("Remove", on_click=self.remove)
		])
		self.edit = None
		orc.Page.__init__(
			self,
			orc.VGroup([
				self.hgroup,
				orc.Editor(init = "Basic editor")
			]),
			app = app
		)

	def add(self):
		self.edit = orc.Editor(init="Second editor.")
		self.hgroup.insert(self.edit)

	def remove(self):
		self.hgroup.remove(self.edit)

orc.Application("Group Dynamic Test", first=MyPage).run()

