#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		self.hgroup = HGroup([
			Button("Add", on_click=self.add),
			Button("Remove", on_click=self.remove)
		])
		self.edit = None
		Page.__init__(
			self,
			VGroup([
				self.hgroup,
				Editor(init = "Basic editor")
			]),
			app = app
		)

	def add(self):
		self.edit = Editor(init="Second editor.")
		self.hgroup.insert(self.edit)

	def remove(self):
		self.hgroup.remove(self.edit)

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Group Dynamic Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

