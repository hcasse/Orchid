#!/usr/bin/python3

"""Tabbed pane test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.num = 0
		self.cnt = 3

		self.tab = orc.TabbedPane([
			("one", orc.Editor("One !\nHere\n")),
			("two", orc.Editor("Another tab!")),
			("three", orc.Editor("Last tab!"))
		])

		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.HGroup([
					orc.Button("add", on_click=self.add),
					orc.Button("remove", on_click=self.remove),
					orc.Button("first", on_click=self.first)
				]),
				self.tab
			]),
			app = app
		)

	def add(self):
		self.tab.insert_tab(orc.Editor("another text {self.num}"), label=f"new {self.num}")
		self.num = self.num + 1
		self.cnt = self.cnt + 1

	def remove(self):
		self.cnt = self.cnt - 1
		self.tab.remove_tab(self.cnt)

	def first(self):
		self.tab.select(self.tab.get_tab(0))


orc.Application("TabbedPane Test", first=MyPage).run()

