#!/usr/bin/python3

"""Hello World test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.user = orc.Var("", label="User")
		self.password = orc.Var("", label="Password")
		action = orc.Action(self.login, label="Login",
			enable=orc.not_null(self.user) & orc.not_null(self.password))
		orc.Page.__init__(
			self,
			orc.KeyGroup(
				orc.VGroup([
					orc.Field(self.user),
					orc.Field(self.password),
					orc.Button(action)
				]),
				[orc.Key(orc.Key.ENTER, action)]
			),
			app = app
		)

	def login(self, interface):
		print("DEBUG; login. User:", ~self.user, "Password:",
			~self.password)

orc.Application("Key Group Test", first=MyPage).run(debug=True)

