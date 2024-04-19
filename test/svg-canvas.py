#!/usr/bin/env python3

from orchid import *
from orchid.svg import Canvas

class MyPage(Page):

	def __init__(self, app):
		self.canvas = Canvas()
		self.objects = []
		self.reset()
		self.canvas.set_stroke("red")
		Page.__init__(
			self,
			VGroup([
				HGroup([
					Button("Start", on_click=self.start),
					Button("Stop", on_click=self.stop),
					Button("Reset", on_click=self.reset)
				]),
				self.canvas
			]),
			app = app)
		self.timer = Timer(self, self.step, period=250, started = True)

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
		self.objects.append(self.canvas.line(self.x1, 0, self.x2, 200))
		self.x1 += 10
		self.x2 -= 10


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "SVG Canvas Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

