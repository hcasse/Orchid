#!/usr/bin/python3

"""Tabbed pane test."""

import orchid as orc

class MyTab(orc.Tab):

	def __init__(self, label, text):
		self.component = orc.Editor(text)
		self.label = label

	def get_label(self):
		return self.label

	def get_component(self):
		return self.component

	def on_show(self):
		print("Shown", self.label)

	def on_hide(self):
		print("Hidden", self.label)

	def on_release(self):
		print("Released", self.label)


class MyPage(orc.Page):

	def __init__(self, app):
		self.num = 0
		self.cnt = 3

		self.tab = orc.TabbedPane([
			MyTab("one", "One !\nHere\n"),
			MyTab("two", "Another tab!"),
			MyTab("three", "Last tab!")
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
		self.tab.insert(MyTab(f"new {self.num}", "another text {self.num}"))
		self.num = self.num + 1
		self.cnt = self.cnt + 1

	def remove(self):
		self.cnt = self.cnt - 1
		self.tab.remove(self.cnt)

	def first(self):
		self.tab.select(self.tab.get_tab(0))


orc.Application("TabbedPane Test", first=MyPage).run()

