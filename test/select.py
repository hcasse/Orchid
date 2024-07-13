#!/usr/bin/python3

"""Select list test."""

import orchid as orc

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

class MyPage(orc.Page):

	def __init__(self, app):
		self.select = orc.Select(CHOICES1)
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.HGroup([
					orc.Button("Choices 1", on_click=self.set_choice1),
					orc.Button("Choices 2", on_click=self.set_choice2),
					orc.Button("Append", on_click=self.do_append),
					orc.Button("Remvoe last", on_click=self.do_remove)
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


orc.Application("Select Test", first=MyPage).run()


