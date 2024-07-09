#!/usr/bin/python3

from orchid import *
import orchid.table as table
import orchid.group as group

my_table = [
	[ "Spain", "Madrid", 47325360, 505990 ],
	[ "France", "Paris", 68042591, 643801 ],
	[ "Germany", "Berlin", 84270625, 357592 ],
	[ "Italy", "Rome", 58853482, 301230 ]
]

class MyPage(Page):

	def __init__(self, app):
		self.table = table.TableView(
			my_table,
			parse=self.parse,
			headers = ["Country", "Capital", "Surface", "Population"]
		)
		Page.__init__(
			self,
			VGroup([
				self.table,
				HGroup([
					Button("clear", on_click=self.clear),
					Button("append", on_click=self.append),
					Button("insert", on_click=self.insert),
					Button("remove", on_click=self.remove)
				])
			]),
			app = app
		)
		self.pos = 0
		self.table.get_table_model().is_editable = self.is_editable

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

	def is_editable(self, row, col):
		return col >= 2

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "table-test")

	def first(self):
		return MyPage(self)

run(MyApp())

