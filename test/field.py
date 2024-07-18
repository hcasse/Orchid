#!/usr/bin/python3

"""Field tests."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.my_field = orc.Field("Set test", init="ok")
		self.my_text = orc.Var("")
		self.my_text.add_observer(self.update_text)
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.Field("Type text:", var=self.my_text),
				orc.Field("Type natural:", parse=orc.as_natural),
				orc.Field("Type binary:", parse=orc.as_re("[01]+")),
				orc.Field("With place holder:", place_holder="a place holder"),
				orc.Field("Help message:", help="the help message"),
				orc.ColorField(label="Color:", help="ok", init="#00FF00"),
				orc.DateField(label="Date"),
				orc.TimeField(label="Time"),
				orc.DateTimeField(label="Date, Time"),
				orc.PasswordField(label="Password"),
				orc.EmailField(label="EMail"),
				orc.RangeField(0, 10, label="Range"),
				self.my_field,
				orc.Button("Let's go!", on_click=self.go)
			]),
			app = app
		)

	def update_text(self, subject):
		print("DEBUG: updated", self.my_text.get())

	def go(self):
		self.my_field.set_value("ko!")

	def done(self):
		print("Done!")

	def give_up(self):
		print("Give up!")

orc.Application("Field Test", first=MyPage).run()

