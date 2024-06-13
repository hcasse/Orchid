#!/usr/bin/python3

from orchid import *
from orchid.mind import *
from orchid.field import *

class MyPage(Page):

	def __init__(self, app):
		self.login = Var("", label="Login")
		self.pwd = Var("", label="Password")
		self.repwd = Var("", label="Retype")
		self.email = Var("", label="EMail")
		self.message = MessageLabel("")
		apply_enable = \
			if_error(not_null(self.login), "Login required!") & \
			if_error(is_password(self.pwd), "Password must contains at least 8 character, 1 uppercase, 1 lower case and 1 digit.") & \
			if_error(equals(self.pwd, self.repwd), "Password and re-typed different!") & \
			if_error(not_null(self.email), "EMail required!")

		apply_action = Action(
			label="Apply",
			fun = self.apply,
			enable = apply_enable
		)

		Page.__init__(
			self,
			VGroup([
				Field(var=self.login),
				PasswordField(var=self.pwd),
				PasswordField(var=self.repwd),
				EmailField(var=self.email),
				self.message,
				Button(action=apply_action)
			]),
			app = app
		)

	def apply(self, console):
		print("DEBUG: create user", self.login.get(), self.pwd.get(), self.email.get())


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Mind Module Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

