#!/usr/bin/env python3

"""SVG canvas test."""

import orchid as orc
from orchid.control import ClickNMove, MouseWheel
from orchid.svg import Canvas, Translate, Scale


class MyPage(orc.Page):

	def __init__(self, app):
		self.canvas = Canvas()
		self.canvas.add_control(ClickNMove(on_move = self.on_move))
		self.canvas.add_control(MouseWheel(on_change = self.on_wheel_change))
		self.circle = self.canvas.circle(50, 50, 30,
			stroke="green", fill="yellow", stroke_width=4)
		self.circle_scale = Scale(1.)
		self.circle.add_transformation(self.circle_scale)
		self.circle_trans = Translate(0, 0)
		self.circle.add_transformation(self.circle_trans)
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

		def show_size(width: int, height: int) -> None:
			print(f"size = {width} x {height}")
		self.canvas.get_size(show_size)

	def on_wheel_change(self, delta: int) -> None:
		print(f"DEBUG: wheel {delta}")
		if delta >= 0:
			self.circle_scale.zoom(.1)
		else:
			self.circle_scale.unzoom(.1)

	def on_move(self, dx: int, dy: int) -> None:
		print(f"DEBUG: move {dx}, {dy}")
		self.circle_trans.move(dx, dy)

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

