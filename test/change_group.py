#!/usr/bin/python3

"""Test on-line group  changes."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.target = orc.HGroup([
			orc.Button("Button 0"),
			orc.Button("Button 1")
		])
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.HGroup([
					orc.Button("Add", on_click=self.add),
					orc.Button("Remove", on_click=self.remove),
					orc.Button("Middle", on_click=self.middle)
				]),
				self.target
			]),
			app = app
		)

	def add(self):
		n = len(self.target.get_children())
		self.target.insert(orc.Button(f"Button {n}"))

	def middle(self):
		n = len(self.target.get_children())
		self.target.insert(orc.Button("Button X"), n//2)

	def remove(self):
		n = len(self.target.get_children())
		self.target.remove(n - 1)

orc.Application("Change Group Test", first=MyPage).run()

