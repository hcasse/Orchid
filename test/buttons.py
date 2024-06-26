#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		self.star = Button(Icon("star-empty"), enabled = False)

		self.checkbox = CheckBox("check box",
			help="This is a check box!")

		self.radio = RadioButton(
			["choice 1", "choice 2", "choice 3"])

		Page.__init__(
			self,
			VGroup([
				Button("Clic me!", on_click=self.click),
				HGroup([
					Button(image = Icon("play"), on_click=self.click),
					Button(image = Icon("fast-forward"), on_click=self.click),
					Button(image = Icon("skip-end"), on_click=self.click),
					Button(image = Icon("skip-forward"), on_click=self.click),
					Button(image = Icon("stop"), on_click=self.click),
					Button(image = Icon("record"), on_click=self.click),
					self.star
				]),
				Button("Button with tool tip!", help="The tooltip!"),
				HGroup([self.checkbox, Button("invert", on_click=self.invert_checkbox)]),
				HGroup([self.radio, Button("next", on_click=self.next)])
			]),
			app = app
		)

	def next(self):
		i = self.radio.get_choice() + 1
		if i >= 3:
			i = 0
		print("DEBUG: next =", i)
		self.radio.set_choice(i)

	def invert_checkbox(self):
		self.checkbox.set_value(not self.checkbox.get_value())

	def click(self):
		print("Clicked!")


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "buttons")

	def first(self):
		return MyPage(self)

run(MyApp(), debug=True)

