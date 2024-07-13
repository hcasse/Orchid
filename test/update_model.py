#!/usr/bin/env python3

"""Testing for model updating."""

import orchid as orc

MODEL = orc.Model(
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

class MyButton(orc.Button):

	def __init__(self):
		orc.Button.__init__(self, "Hello!", model = MODEL)
		self.add_class("my-style")


class MyPage(orc.Page):

	def __init__(self, app):
		self.group = orc.HGroup([
				orc.Button("run", on_click=self.run)
			])
		orc.Page.__init__(
			self,
			self.group,
			app = app
		)

	def run(self):
		self.group.insert(MyButton())


orc.Application("Model Update Test", first=MyPage).run()

