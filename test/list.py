#!/usr/bin/python3

"""List view test."""

import orchid as orc

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

class MyPage(orc.Page):

	def __init__(self, app):
		self.count = 0
		self.selection = []

		self.menu = orc.Menu([
				orc.Button("Menu 1", on_click=self.menu1),
				orc.Button("Menu 2", on_click=self.menu2)
			])

		self.component = orc.ListView(my_list,
			selection = self.selection,
			context_menu = self.menu)
		self.items = self.component.get_items()
		orc.Page.__init__(
			self,
			orc.VGroup([
				self.component,
				orc.HGroup([
					orc.Button("clear", on_click=self.clear),
					orc.Button("insert", on_click=self.insert),
					orc.Button("remove", on_click=self.remove),
					orc.Button("set", on_click=self.set),
					orc.Button("change", on_click=self.change)
				])
			]),
			app = app
		)

	def clear(self):
		print("DEBUG: clear clicked!")
		self.component.get_items().clear()

	def insert(self):
		item = f"item {self.count}"
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


orc.Application("ListView Test", first=MyPage).run()


