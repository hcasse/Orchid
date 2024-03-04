#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		self.star = Button(Icon("star-empty"), enabled = False)
		Page.__init__(
			self,
			VGroup([
				Button("Clic me!", on_click=self.click),
				HGroup([
					Button(image = Icon("play"), on_click=self.click),
					Button(image = Icon("fast-forward"), on_click=self.click),
					Button(image = Icon("skip-end"), on_click=self.click),
					Button(image = Icon("skip-forward"), on_click=self.click),
					Button(image = Icon("stop"), on_click=self.click),
					Button(image = Icon("record"), on_click=self.click),
					self.star
				]),
				Button("Button with tool tip!", help="The tooltip!"),
				CheckButton("check button", help="This is a check button!", on_change=self.on_checkbox_change)
			]),
			app = app
		)

	def click(self):
		print("Clicked!")

	def on_checkbox_change(self, value):
		print("Checkbox:", value)

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "buttons")

	def first(self):
		return MyPage(self)

run(MyApp(), debug=True)

