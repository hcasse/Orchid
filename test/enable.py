#!/usr/bin/python3

"""Enabling test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.target = orc.Button("Target", on_click=self.close)
		orc.Page.__init__(
			self,
			orc.VGroup([
				self.target,
				orc.Button("Enable", on_click=self.do_enable),
				orc.Button("Disable", on_click=self.do_disable),
			]),
			app = app
		)

	def do_enable(self):
		self.target.enable()

	def do_disable(self):
		self.target.disable()


orc.Application("Enable Test", first=MyPage).run()

