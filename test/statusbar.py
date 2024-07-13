#!/usr/bin/python3

"""Status bar test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.counter = orc.Var(0)
		self.twostate = orc.Var(True, icon=orc.Icon(orc.IconType.FLOWER))
		self.tscomp = orc.TwoStateButton(self.twostate, icon2=orc.Icon(orc.IconType.FIRE))
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.HGroup([
					orc.Button("Increment", on_click=self.increment),
					orc.Button("Decrement", on_click=self.decrement),
					orc.Button("Disable", on_click=self.tscomp.disable),
					orc.Button("Enabled", on_click=self.tscomp.enable)
				]),
				orc.Editor(init="MyEditor!"),
				orc.StatusBar([
					orc.hspring(),
					orc.Field(self.counter),
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


orc.Application("StatusBar Test", first=MyPage).run()

