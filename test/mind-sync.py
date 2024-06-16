#!/usr/bin/python3

from orchid import *
from orchid.mind import *

class MyPage(Page):

	def __init__(self, app):
		self.val = Var("123", label="Value")

		Page.__init__(
			self,
			VGroup([
				Field(var = self.val),
				Field(var = self.val)
			]),
			app = app
		)

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Mind Synchronisation Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

