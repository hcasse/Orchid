#!/usr/bin/python3

"""Table test."""

import orchid as orc

my_table = [
	[ "Spain", "Madrid", 47325360, 505990 ],
	[ "France", "Paris", 68042591, 643801 ],
	[ "Germany", "Berlin", 84270625, 357592 ],
	[ "Italy", "Rome", 58853482, 301230 ]
]

class MyPage(orc.Page):

	def __init__(self, app):
		context_toolbar = orc.MenuButton(orc.Menu([
				orc.Button("Choice 1", on_click=self.do_choice1),
				orc.Button("Choice 2", on_click=self.do_choice2)
			]))
		self.table = orc.TableView(
			my_table,
			parse=self.parse,
			is_editable=self.is_editable,
			headers = ["Country", "Capital", "Surface", "Population"],
			context_toolbar=context_toolbar
		)
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.Label("Table test!"),
				self.table,
				orc.HGroup([
					orc.Button("clear", on_click=self.clear),
					orc.Button("append", on_click=self.append),
					orc.Button("insert", on_click=self.insert),
					orc.Button("remove", on_click=self.remove)
				])
			]),
			app = app
		)
		self.pos = 0
		self.table.get_table_model().is_editable = self.is_editable

	def do_choice1(self):
		print("DEBUG: choice 1 on row", self.table.get_context_row())

	def do_choice2(self):
		print("DEBUG: choice 2 on row", self.table.get_context_row())

	def is_editable(self, row, col):
		return col >= 2

	def parse(self, row, col, val):
		try:
			return int(val)
		except ValueError:
			return None

	def clear(self):
		self.table.get_table_model().set(self.pos//4, self.pos%4, str(self.pos))
		self.pos = self.pos + 1

	def append(self):
		self.table.get_table_model().append_row(["?", "?", "?", "?"])

	def insert(self):
		self.table.get_table_model().insert_row(2, ["?", "?", "?", "?"])
	def remove(self):
		self.table.get_table_model().remove_row(2)

orc.Application("Table Test", first=MyPage).run()

