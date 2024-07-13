#!/usr/bin/python3

"""Form test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.Label("Fulfill the form below:"),
				orc.Form([
					orc.Field(label="Name"),
					orc.EmailField(label="EMail"),
					orc.DateField(label="Birth date"),
					orc.DateTimeField(label="Now"),
					orc.TimeField(label="Time"),
					orc.PasswordField(label="Password"),
					orc.RangeField(0, 10, label="Range"),
					orc.ProposalField(propose=self.propose, label="Count"),
					orc.Select(["Frodon", "Sam", "Merry", "Pippin"], label="Hobbit"),
					orc.CheckBox(label="Pro Sauron?"),
					orc.RadioButton(["Aragorn", "Legolas", "Gimli"], label="Hero")
				]),
				orc.Button("Apply", on_click=self.apply)
			]),
			app = app
		)

	def apply(self):
		print("DEBUG: applying!")

	def propose(self, value):
		return ["one", "two", "three"]

orc.Application("Form Test", first=MyPage).run()

