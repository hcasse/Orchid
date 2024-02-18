#!/usr/bin/python3

from orchid import *
import orchid.list as list
import orchid.group as group

my_list = [
	"Rome",
	"Paris",
	"London",
	"Stockholm"
]

class MyPage(Page):

	def __init__(self, app):
		self.count = 0
		self.list = list.View(my_list)
		Page.__init__(
			self,
			VGroup([
				self.list,
				HGroup([
					Button("clear", on_click=self.clear),
					Button("insert", on_click=self.insert),
					Button("remove", on_click=self.remove)
				])
			]),
			app = app
		)

	def clear(self):
		pass

	def insert(self):
		item = "item %d" % self.count
		s = self.list.get_selection()
		if s:
			self.list.get_items().insert(s[0], item)
		else:
			self.list.get_items().append(item)
		self.count = self.count + 1

	def remove(self):
		s = self.list.get_selection()
		if s:
			self.list.get_items().remove(self.list.get_items().get(s[0]))


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "list-test")

	def first(self):
		return MyPage(self)

run(MyApp())

