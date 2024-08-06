#!/usr/bin/python3

"""Hello World test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.field1 = orc.Field("Field 1")
		self.field2 = orc.Field("Field 2")
		self.field3 = orc.Field("Field 3")
		orc.Page.__init__(
			self,
			orc.VGroup([
				self.field1,
				self.field2,
				self.field3,
				orc.HGroup([
					orc.Button("Focus 1", on_click=self.focus1),
					orc.Button("Focus 2", on_click=self.focus2),
					orc.Button("Focus 3", on_click=self.focus3),
				])
			]).key(orc.Key.ENTER, lambda: self.next_focus()),
			app = app
		)

	def focus1(self):
		self.field1.grab_focus()

	def focus2(self):
		self.field2.grab_focus()

	def focus3(self):
		self.field3.grab_focus()

orc.Application("Focus test", first=MyPage).run(debug = True)

