#!/usr/bin/python3

from orchid import *

CHOICES1 = [
	"choice 1",
	"choice 2",
	"choice 3"
]
CHOICES2 = [
	"red",
	"green",
	"blue"
]

class MyPage(Page):

	def __init__(self, app):
		self.select = Select(CHOICES1)
		Page.__init__(
			self,
			VGroup([
				HGroup([
					Button("Choices 1", on_click=self.set_choice1),
					Button("Choices 2", on_click=self.set_choice2),
					Button("Append", on_click=self.do_append),
					Button("Remvoe last", on_click=self.do_remove)
				]),
				self.select
			]),
			app = app
		)

	def set_choice1(self):
		self.select.set_choices(CHOICES1)

	def set_choice2(self):
		self.select.set_choices(CHOICES2)

	def do_append(self):
		self.select.add_choice("added")

	def do_remove(self):
		self.select.remove_choice(len(self.select.choices)-1)


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Select Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug = True)


