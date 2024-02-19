#!/usr/bin/env python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		Page.__init__(
			self,
			VGroup([
				Button("Close", on_click=self.close)
			]),
			app = app
		)


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Server Test")

	def first(self):
		return MyPage(self)

run(MyApp(), server=True, debug=True)

