#!/usr/bin/python3

"""Field tests."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.field = orc.Field("Value")
		orc.Page.__init__(self,
			orc.VGroup([
				self.field,
				orc.Button("Click", on_click=self.update)
			]),
			app=app
		)

	def update(self):
		self.field.set_value("Hello!")

orc.Application("Field Update Test", first=MyPage).run(debug=True)


