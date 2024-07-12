#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		self.action = Action(fun=self.on_click,
			label = "Test", icon = Icon(IconType.MAGIC))
		Page.__init__(
			self,
			VGroup([
				Button(self.action),
				HGroup([
					Button("Change label", on_click=self.change_label),
					Button("Change icon", on_click=self.change_icon)
				])
			]),
			app = app
		)

	def on_click(self, interface):
		pass

	def change_label(self):
		self.action.set_label("Changed!")

	def change_icon(self):
		self.action.set_icon(Icon(IconType.BOX))


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Entity Update Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

