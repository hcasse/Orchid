#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		self.target = HGroup([
			Button("Button 0"),
			Button("Button 1")
		])
		Page.__init__(
			self,
			VGroup([
				HGroup([
					Button("Add", on_click=self.add),
					Button("Remove", on_click=self.remove),
					Button("Middle", on_click=self.middle)
				]),
				self.target
			]),
			app = app
		)

	def add(self):
		n = len(self.target.get_children())
		self.target.insert(Button("Button %d" % n))

	def middle(self):
		n = len(self.target.get_children())
		self.target.insert(Button("Button X"), n//2)

	def remove(self):
		n = len(self.target.get_children())
		self.target.remove(n - 1)

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Change Group Test")

	def first(self):
		return MyPage(self)

run(MyApp())

