#!/usr/bin/python3

"""Button test."""

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
			orc.VGroup([
				orc.Button("Clic me!", on_click=self.click),
				orc.HGroup([
					orc.Button(image = orc.Icon(orc.IconType.PLAY), on_click=self.click),
					orc.Button(image = orc.Icon(orc.IconType.FAST_FORWARD), on_click=self.click),
					orc.Button(image = orc.Icon(orc.IconType.SKIP_END), on_click=self.click),
					orc.Button(image = orc.Icon(orc.IconType.SKIP_FORWARD), on_click=self.click),
					orc.Button(image = orc.Icon(orc.IconType.STOP), on_click=self.click),
					orc.Button(image = orc.Icon(orc.IconType.RECORD), on_click=self.click),
					self.star
				]),
				orc.Button("Button with tool tip!", help="The tooltip!"),
				orc.HGroup([self.checkbox, orc.Button("invert", on_click=self.invert_checkbox)]),
				orc.HGroup([self.radio, orc.Button("next", on_click=self.next)])
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


orc.Application("Buttons Test", first=MyPage).run(debug=True)

