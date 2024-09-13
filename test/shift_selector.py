#!/usr/bin/python3

"""Shift selector test."""

import orchid as orc

class MyPage(orc.Page):
	NUM = 0

	def make_button(self):
		i = self.NUM
		self.NUM = self.NUM + 1
		def on_click():
			print("DEBUG: select", i)
		return orc.Button(f"Select {i}", on_click=on_click)

	def __init__(self, app):
		self.shift = orc.ShiftSelector([self.make_button(), self.make_button()])
		orc.Page.__init__(
			self,
			orc.VGroup([
				self.shift,
				orc.HGroup([
					orc.Button("Push", on_click=self.push),
					orc.Button("Pop", on_click=self.pop)
				])
			]),
			app = app
		)

	def push(self):
		self.shift.insert(self.make_button())

	def pop(self):
		children = self.shift.get_children()
		if children:
			self.shift.remove(len(children)-1)

orc.Application("ShiftSelector Test", first=MyPage).run()
