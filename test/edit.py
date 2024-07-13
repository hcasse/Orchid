#!/usr/bin/python3

"""Editor test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		self.edit1 = orc.Editor(init = "Hello, World!")
		self.edit2 = orc.Editor(init = "<b>first</b>")
		self.edit3 = orc.Editor(init = "second")
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.HGroup([
					orc.Label("Editor test"),
					orc.Button("Get 1", on_click=self.get_edit1),
					orc.Button("Get 2", on_click=self.get_edit2),
					orc.Button("Get 3", on_click=self.get_edit3)
				]),
				self.edit1,
				orc.HGroup([
					self.edit2,
					self.edit3
				])
			]),
			app = app
		)
		print("DEBUG: edit1.id =", self.edit1.get_id())
		print("DEBUG: edit2.id =", self.edit2.get_id())
		print("DEBUG: edit3.id =", self.edit3.get_id())

	def get_edit1(self):
		self.edit1.get_content(self.got)

	def get_edit2(self):
		self.edit2.get_content(self.got)

	def get_edit3(self):
		self.edit3.get_content(self.got)

	def got(self, editor, content):
		print("DEBUG: got", content, "from", editor.get_id())


orc.Application("Editor Test", first=MyPage).run()

