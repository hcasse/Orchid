#!/usr/bin/python3

from orchid import *

class MyTab(Tab):

	def __init__(self, label, text):
		self.component = Editor(text)
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


class MyPage(Page):

	def __init__(self, app):
		self.num = 0
		self.cnt = 3

		self.tab = TabbedPane([
			MyTab("one", "One !\nHere\n"),
			MyTab("two", "Another tab!"),
			MyTab("three", "Last tab!")
		])

		Page.__init__(
			self,
			VGroup([
				HGroup([
					Button("add", on_click=self.add),
					Button("remove", on_click=self.remove),
					Button("first", on_click=self.first)
				]),
				self.tab
			]),
			app = app
		)

	def add(self):
		self.tab.insert(MyTab("new %d" % self.num, "another text %d" % self.num))
		self.num = self.num + 1
		self.cnt = self.cnt + 1

	def remove(self):
		self.cnt = self.cnt - 1
		self.tab.remove(self.cnt)

	def first(self):
		self.tab.select(self.tab.get_tab(0))


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "TabbedPane Test")

	def first(self):
		return MyPage(self)

run(MyApp())

