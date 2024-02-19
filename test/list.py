#!/usr/bin/python3

from orchid import *
import orchid.list as list
import orchid.group as group

my_list = [
	"Rome",
	"Paris",
	"London",
	"Stockholm",
	"Berlin",
	"Madrid",
	"Washington",
	"Bucarest",
	"Prague",
	"Brussel",
	"Amsterdam"
]

class MyPage(Page):

	def __init__(self, app):
		self.count = 0
		self.component = list.View(my_list)
		self.items = self.component.get_items()
		Page.__init__(
			self,
			VGroup([
				self.component,
				HGroup([
					Button("clear", on_click=self.clear),
					Button("insert", on_click=self.insert),
					Button("remove", on_click=self.remove),
					Button("set", on_click=self.set),
				])
			]),
			app = app
		)

	def clear(self):
		pass

	def insert(self):
		item = "item %d" % self.count
		s = self.component.get_selection()
		if s:
			self.items.insert(s[0], item)
		else:
			self.items.append(item)
		self.count = self.count + 1

	def remove(self):
		s = self.component.get_selection()
		if s:
			self.items.remove(self.items.get(s[0]))

	def set(self):
		s = self.component.get_selection()
		if s:
			self.items.set(s[0], "???")


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "list-test")

	def first(self):
		return MyPage(self)

run(MyApp(), debug=True)

