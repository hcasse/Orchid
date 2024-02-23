#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		self.edit1 = Editor(init = "Hello, World!")
		self.edit2 = Editor(init = "<b>first</b>")
		self.edit3 = Editor(init = "second")
		Page.__init__(
			self,
			VGroup([
				HGroup([
					Label("Editor test"),
					Button("Get 1", on_click=self.get_edit1),
					Button("Get 2", on_click=self.get_edit2),
					Button("Get 3", on_click=self.get_edit3)
				]),
				self.edit1,
				HGroup([
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


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Editor Test")

	def first(self):
		return MyPage(self)

run(MyApp())

