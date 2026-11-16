#!/usr/bin/python3

"""Status bar test."""

from orchid.label import MessageLabel
from orchid.button import Button
import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.counter = orc.Var(0)
		self.twostate = orc.Var(True, icon=orc.Icon(orc.IconType.FLOWER))
		self.tscomp = orc.TwoStateButton(self.twostate, icon2=orc.Icon(orc.IconType.FIRE))
		self.msg = MessageLabel(content = "Hi, folks!", time=5000)
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.HGroup([
					orc.Button("Increment", on_click=self.increment),
					orc.Button("Decrement", on_click=self.decrement),
					orc.Button("Disable", on_click=self.tscomp.disable),
					orc.Button("Enabled", on_click=self.tscomp.enable),
					Button("Info", on_click=lambda: self.msg.show_info("New info!")),
					Button("Warning", on_click=lambda: self.msg.show_warning("Warning: Warning!")),
					Button("Error", on_click=lambda: self.msg.show_error("Error! Error!"))
				]),
				orc.Editor(init="MyEditor!"),
				orc.StatusBar([
					self.msg,
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

