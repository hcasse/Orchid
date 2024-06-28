#!/usr/bin/python3

from orchid import *
from orchid.list import *
import orchid.group as group
from orchid import popup

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

alt_list = [
	"Italy",
	"France",
	"England",
	"Sweden",
	"Germany"
]

class MyPage(Page):

	def __init__(self, app):
		self.count = 0
		self.selection = []

		self.menu = popup.Menu([
				Button("Menu 1", on_click=self.menu1),
				Button("Menu 2", on_click=self.menu2)
			])

		self.component = ListView(my_list,
			selection = self.selection,
			context_menu = self.menu)
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
					Button("change", on_click=self.change)
				])
			]),
			app = app
		)

	def clear(self):
		print("DEBUG: clear clicked!")
		self.component.get_items().clear()

	def insert(self):
		item = "item %d" % self.count
		if self.selection:
			self.items.insert(self.selection[0], item)
		else:
			self.items.append(item)
		self.count = self.count + 1

	def remove(self):
		if self.selection:
			self.items.remove(self.items.get(self.selection[0]))

	def set(self):
		if self.selection:
			self.items.set_index(self.selection[0], "???")

	def change(self):
		self.component.set_items(alt_list)

	def menu1(self):
		print("DEBUG: menu1!")

	def menu2(self):
		print("DEBUG: menu2!")


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "list-test")

	def first(self):
		return MyPage(self)

run(MyApp(), debug=True)

