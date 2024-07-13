#!/usr/bin/python3

"""Message container test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.cont = orc.MessageContainer(
				orc.VGroup([
					orc.Button("clear", on_click=self.clear),
					orc.Button("show info", on_click=self.show_info),
					orc.Button("show_warn", on_click=self.show_warn),
					orc.Button("show_error", on_click=self.show_error),
					orc.Button("hide info", on_click=self.hide_info),
					orc.Button("hide warn", on_click=self.hide_warn),
					orc.Button("hide error", on_click=self.hide_error),
				], align=orc.Align.CENTER)
			)
		self.info = None
		self.warn = None
		self.error = None

		orc.Page.__init__(
			self,
			self.cont,
			app = app
		)

	def clear(self):
		self.cont.clear()

	def show_info(self):
		self.info = self.cont.info("One information!")

	def show_warn(self):
		self.warn = self.cont.warn("A warning is now displayed!")

	def show_error(self):
		self.error = self.cont.error("There is an error!")

	def hide_info(self):
		self.cont.hide_message(self.info)

	def hide_warn(self):
		self.cont.hide_message(self.warn)

	def hide_error(self):
		self.cont.hide_message(self.error)


orc.Application("MessageContainer test", first=MyPage).run()

