#!/usr/bin/env python3

"""Custom component test."""

import orchid as orc

class Counter(orc.Component):

	MODEL = orc.Model(
		script = """
		function counter_onclick(id, event) {
			if(event.button == 0)
				ui_send({id: id, action: "click"});
		}
	""",
		style = """
		.counter {
			border: 2px solid red;
			padding: 4px;
		}

		.counter:hover {
			background: yellow;
		}
	"""
	)

	def __init__(self, message):
		orc.Component.__init__(self, self.MODEL)
		self.message = message
		self.count = 0
		self.set_attr('onclick',
			f"counter_onclick('{self.get_id()}', event);")
		self.add_class('counter')

	def display(self):
		return f'{self.message} {self.count}'

	def gen(self, out):
		out.write('<div')
		self.gen_attrs(out)
		out.write('>')
		out.write(self.display())
		out.write('</div>')

	def receive(self, msg, handler):
		if msg['action'] == 'click':
			self.count = self.count + 1
			self.set_content(self.display())
		else:
			orc.Component.receive(self, msg, handler)


class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			orc.VGroup([
				Counter("Counter 1:"),
				Counter("Counter 2:")
			]),
			app = app
		)


orc.Application("Counter Test", first=MyPage).run()
