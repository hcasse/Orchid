#!/usr/bin/python3

"""Expading horizontal group test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		ed1 = orc.Editor("I'm an editor!\nOk!")
		ed2 = orc.Editor("I'm a second editor!\nko!\ntwice first editor!")
		ed2.weight = (2, 1)
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.HGroup([
					orc.Button("Button"),
					ed1,
					orc.Button("interval"),
					ed2,
					orc.Label("at end")
				]),
			]),
			app = app
		)

orc.Application("Expand HGroup", first=MyPage).run()

