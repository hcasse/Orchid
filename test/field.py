#!/usr/bin/python3

from orchid import *
from orchid.mind import *

class MyPage(Page):

	def __init__(self, app):
		self.my_field = Field("Set test", init="ok")
		self.my_text = Var("")
		self.my_text.add_observer(self.update_text)
		Page.__init__(
			self,
			VGroup([
				Field("Type text:", var=self.my_text),
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
				self.my_field,
				Button("Let's go!", on_click=self.go)
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

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "HGroup Test")

	def first(self):
		return MyPage(self)

run(MyApp(), debug=True)

