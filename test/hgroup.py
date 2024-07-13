#!/usr/bin/python3

"""Horizontal group test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			orc.HGroup([
				orc.Label("Label..."),
				orc.Field("Type text here!", size=10),
				orc.Field(size = 2),
				orc.Button("Done", on_click=self.done),
				orc.Button("Give up", on_click=self.give_up)
			]),
			app = app
		)

	def done(self):
		print("Done!")

	def give_up(self):
		print("Give up!")

orc.Application("HGroup Test", first=MyPage).run()


