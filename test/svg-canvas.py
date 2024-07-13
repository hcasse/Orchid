#!/usr/bin/env python3

"""SVG canvas test."""

import orchid as orc
from orchid.svg import Canvas

class MyPage(orc.Page):

	def __init__(self, app):
		self.canvas = Canvas()
		self.canvas.circle(50, 50, 30,
			stroke="green", fill="yellow", stroke_width=4)
		self.objects = []
		self.reset()
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.HGroup([
					orc.Button("Start", on_click=self.start),
					orc.Button("Stop", on_click=self.stop),
					orc.Button("Reset", on_click=self.reset),
					orc.Button("Picture", on_click=self.picture)
				]),
				self.canvas
			]),
			app = app)
		self.timer = orc.Timer(self, self.step, period=250, started = False)

	def reset(self):
		self.x1 = 0
		self.x2 = 400
		for obj in self.objects:
			self.canvas.remove(obj)
		self.objects = []

	def start(self):
		self.timer.start()

	def stop(self):
		self.timer.stop()

	def step(self):
		self.objects.append(self.canvas.line(
			self.x1, 0, self.x2, 200, stroke="red"))
		self.x1 += 10
		self.x2 -= 10

	def picture(self):
		self.canvas.image("led.svg", 100, 10)


orc.Application("SVG Canvas Test", first=MyPage).run()

