#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		Page.__init__(
			self,
			VGroup([
				Field("Type text:"),
				Field("Type natural:", validate=as_natural),
				Field("Type binary:", validate=as_re("[01]+")),
				Field("With place holder:", place_holder="a place holder"),
				Field("Help message:", help="the help message"),
				ColorField(label="Color:", help="ok", init="#00FF00"),
				DateField(label="Date"),
				TimeField(label="Time"),
				DateTimeField(label="Date, Time"),
				PasswordField(label="Password"),
				EmailField(label="EMail"),
				RangeField(0, 10, label="Range"),
				Button("Let's go!")
			]),
			app = app
		)

	def done(self):
		print("Done!")

	def give_up(self):
		print("Give up!")

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "HGroup Test")

	def first(self):
		return MyPage(self)

run(MyApp())
