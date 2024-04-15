#!/usr/bin/python3

from orchid import *

class MyTab(Editor):

	def __init__(self, title, text):
		Editor.__init__(self, text)
		self.title = title

	def get_title(self):
		return self.title


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
					Button("remove", on_click=self.remove)
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

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "TabbedPane Test")

	def first(self):
		return MyPage(self)

run(MyApp())

