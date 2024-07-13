#!/usr/bin/python3

"""Session test."""

import orchid as orc


class MySession(orc.Session):

	def __init__(self, app, man):
		orc.Session.__init__(self, app, man)
		self.cnt = 0
		self.label = None

	def get_index(self):
		self.label = orc.Label("0")
		return orc.Page(
			orc.VGroup([
				orc.Label(f"Session {self.get_number()}"),
				self.label,
				orc.Button("Increment", on_click=self.on_click)
			]),
			app = self.app
		)

	def on_click(self):
		self.cnt += 1
		self.label.set_text(str(self.cnt))


orc.Application("Session Test", session=MySession) \
	.run(server=True, debug=True)

