#!/usr/bin/env python3

from orchid import *
from orchid.svg import Canvas

class MyPage(Page):

	def __init__(self, app):
		self.canvas = Canvas()
		self.canvas.circle(50, 50, 30,
			stroke="green", fill="yellow", stroke_width=4)
		self.objects = []
		self.reset()
		Page.__init__(
			self,
			VGroup([
				HGroup([
					Button("Start", on_click=self.start),
					Button("Stop", on_click=self.stop),
					Button("Reset", on_click=self.reset),
					Button("Picture", on_click=self.picture)
				]),
				self.canvas
			]),
			app = app)
		self.timer = Timer(self, self.step, period=250, started = False)

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


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "SVG Canvas Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

