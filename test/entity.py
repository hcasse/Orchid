#!/usr/bin/python3

"""Entity change test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.action = orc.Action(fun=self.on_click,
			label = "Test", icon = orc.Icon(orc.IconType.MAGIC))
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.Button(self.action),
				orc.HGroup([
					orc.Button("Change label", on_click=self.change_label),
					orc.Button("Change icon", on_click=self.change_icon)
				])
			]),
			app = app
		)

	def on_click(self, interface):
		pass

	def change_label(self):
		self.action.set_label("Changed!")

	def change_icon(self):
		self.action.set_icon(orc.Icon(orc.IconType.BOX))


orc.Application("Entity Update Test", first=MyPage).run()

