#!/usr/bin/python3

"""Mind test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.login = orc.Var("", label="Login")
		self.pwd = orc.Var("", label="Password")
		self.repwd = orc.Var("", label="Retype")
		self.email = orc.Var("", label="EMail")
		apply_enable = \
			orc.if_error(orc.not_null(self.login), "Login required!") & \
			orc.if_error(orc.is_password(self.pwd), "Password must contains at \
			least 8 character, 1 uppercase, 1 lower case and 1 digit.") & \
			orc.if_error(orc.equals(self.pwd, self.repwd), "Password and re-typed different!") & \
			orc.if_error(orc.not_null(self.email), "EMail required!")

		apply_action = orc.Action(
			label="Apply",
			fun = self.apply,
			enable = apply_enable
		)

		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.Field(var=self.login),
				orc.PasswordField(var=self.pwd),
				orc.PasswordField(var=self.repwd),
				orc.EmailField(var=self.email),
				orc.MessageLabel([apply_enable]),
				orc.Button(action=apply_action)
			]),
			app = app
		)

	def apply(self, interface):
		print("DEBUG: create user", self.login.get(), self.pwd.get(), self.email.get())


orc.Application("Mind Module Test", first=MyPage).run()

