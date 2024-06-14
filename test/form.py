#!/usr/bin/python3

from orchid import *
from orchid.field import *
from orchid.button import *

class MyPage(Page):

	def __init__(self, app):
		Page.__init__(
			self,
			VGroup([
				Label("Fulfill the form below:"),
				Form([
					Field(label="Name"),
					EmailField(label="EMail"),
					DateField(label="Birth date"),
					DateTimeField(label="Now"),
					TimeField(label="Time"),
					PasswordField(label="Password"),
					RangeField(0, 10, label="Range"),
					ProposalField(propose=self.propose, label="Count"),
					Select(["Frodon", "Sam", "Merry", "Pippin"], label="Hobbit"),
					CheckBox(label="Pro Sauron?"),
					RadioButton(["Aragorn", "Legolas", "Gimli"], label="Hero")
				]),
				Button("Apply", on_click=self.apply)
			]),
			app = app
		)

	def apply(self):
		print("DEBUG: applying!")

	def propose(self, value):
		return ["one", "two", "three"]

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Form Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

