#!/usr/bin/env python3

from orchid import *

MODEL = Model(
	"my-button",
	script = """
		console.log("my-button loaded!");
	""",
	style = """
.my-style {
	background-color: red;
}
"""
)

class MyButton(Button):

	def __init__(self):
		Button.__init__(self, "Hello!", model = MODEL)
		self.add_class("my-style")


class MyPage(Page):

	def __init__(self, app):
		self.group = HGroup([
				Button("run", on_click=self.run)
			])
		Page.__init__(
			self,
			self.group,
			app = app
		)

	def run(self):
		self.group.insert(MyButton())


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Model Update Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

