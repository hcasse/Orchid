#!/usr/bin/python3

"""Mind synchronization test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.val = orc.Var("123", label="Value")

		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.Field(var = self.val),
				orc.Field(var = self.val)
			]),
			app = app
		)

orc.Application("Mind Synchronisation Test", first=MyPage).run()

