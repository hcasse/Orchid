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
		self.message = Label("")

		apply_action = Action(
				label="Apply",
				fun = self.apply,
				enable = Predicate(
					[self.login, self.pwd, self.email],
					fun=self.check
				)
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

	def is_password_valid(self, pwd):
		return \
			len(pwd) >= 8 and \
			any([c.islower() for c in pwd]) and \
			any([c.isupper() for c in pwd]) and \
			any([c.isdigit() for c in pwd])

	def check(self):
		msg = ""
		if not self.login.get():
			msg = "Login required!"
		elif not self.pwd.get():
			msg = "Empty password forbidden!"
		elif not self.is_password_valid(self.pwd.get()):
			msg = "Password must contains at least 8 character, 1 uppercase, 1 lower case and 1 digit"
		elif self.pwd.get() != self.repwd.get():
			msg = "Password and retyped password different!"
		elif not self.email.get():
			msg = "Email required!"
		self.message.set_text(msg)
		return not msg

	def apply(self, console):
		print("DEBUG: create user", self.login.get(), self.pwd.get(), self.email.get())


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Mind Module Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

