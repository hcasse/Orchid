#!/usr/bin/env python3

from orchid import *

MODEL = Model(
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

class Counter(Component):

	def __init__(self, message):
		Component.__init__(self, MODEL)
		self.message = message;
		self.count = 0
		self.set_attr('onclick',
			f"counter_onclick('{self.get_id()}', event);")
		self.add_class('counter')

	def display(self):
		return f'{self.message} {self.count}'

	def gen(self, out):
		out.write('<div');
		self.gen_attrs(out);
		out.write('>')
		out.write(self.display())
		out.write('</div>')

	def receive(self, message, handler):
		if message['action'] == 'click':
			self.count = self.count + 1
			self.set_content(self.display())
		else:
			Component.receive(self, message, handler)


class MyPage(Page):

	def __init__(self, app):
		Page.__init__(
			self,
			VGroup([
				Counter("Counter 1:"),
				Counter("Counter 2:")
			]),
			app = app
		)


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Counter Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)
