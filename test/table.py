#!/usr/bin/python3

from orchid import *
import orchid.table as table

my_table = [
	[ "Spain", "Madrid", 47325360, 505990 ],
	[ "France", "Paris", 68042591, 643801 ],
	[ "Germany", "Berlin", 84270625, 357592 ],
	[ "Italy", "Rome", 58853482, 301230 ]
]

class MyPage(Page):

	def __init__(self, app):
		Page.__init__(
			self,
			table.View(my_table),
			app = app
		)

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "table-test")

	def first(self):
		return MyPage(self)

run(MyApp())

