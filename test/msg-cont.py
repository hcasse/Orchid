#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		self.cont = MessageContainer(
				VGroup([
					Button("clear", on_click=self.clear),
					Button("show info", on_click=self.show_info),
					Button("show_warn", on_click=self.show_warn),
					Button("show_error", on_click=self.show_error),
					Button("hide info", on_click=self.hide_info),
					Button("hide warn", on_click=self.hide_warn),
					Button("hide error", on_click=self.hide_error),
				], align=Align.CENTER)
			)

		Page.__init__(
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


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "MessageContainer test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

