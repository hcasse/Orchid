#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		ed1 = Editor("I'm an editor!\nOk!")
		ed2 = Editor("I'm a second editor!\nko!\ntwice first editor!")
		ed2.weight = (2, 1)
		Page.__init__(
			self,
			VGroup([
				HGroup([
					Button("Button"),
					ed1,
					Button("interval"),
					ed2,
					Label("at end")
				]),
			]),
			app = app
		)

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Expand HGroup")

	def first(self):
		return MyPage(self)

run(MyApp())

