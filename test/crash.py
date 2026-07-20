#!/usr/bin/python3

"""Crash test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.star = orc.Button(orc.Icon(orc.IconType.STAR_EMPTY), enabled = False)

		self.checkbox = orc.CheckBox("check box",
			help="This is a check box!")

		self.radio = orc.RadioButton(
			["choice 1", "choice 2", "choice 3"])

		orc.Page.__init__(
			self,
			orc.Button("Do crash!", on_click=self.click),
			app = app
		)

	def click(self):
		print("Prepare to crash")
		x = {}
		y = x[3]
		print("This should be not displayed!")

orc.Application("Crash Test", first=MyPage).run(debug=True)
