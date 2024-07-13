#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		self.counter = Var(0)
		self.twostate = Var(True, icon=Icon(IconType.FLOWER))
		self.tscomp = TwoStateButton(self.twostate, icon2=Icon(IconType.FIRE))
		Page.__init__(
			self,
			VGroup([
				HGroup([
					Button("Increment", on_click=self.increment),
					Button("Decrement", on_click=self.decrement),
					Button("Disable", on_click=self.tscomp.disable),
					Button("Enabled", on_click=self.tscomp.enable)
				]),
				Editor(init="MyEditor!"),
				StatusBar([
					hspring(),
					Field(self.counter),
					self.tscomp
				])
			]),
			app = app
		)

	def set_twostate(self):
		self.twostate.set(self.counter.get() < 3)

	def increment(self):
		self.counter.set(self.counter.get() + 1)
		self.set_twostate()

	def decrement(self):
		self.counter.set(self.counter.get() - 1)
		self.set_twostate()


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "StatusBar Test")

	def first(self):
		return MyPage(self)

run(MyApp())

