"""Label component."""

from orchid.base import *

LABEL_MODEL = Model()

class Label(Component):
	"""Display a single HTML text."""

	def __init__(self, text):
		Component.__init__(self, LABEL_MODEL)
		self.text = text
		self.add_class("label")

	def gen(self, out):
		out.write('<div')
		self.gen_attrs(out)
		out.write('>')
		out.write(self.text)
		out.write('</div>\n')

	def set_text(self, text):
		self.text = text
		self.set_content(text)


BANNER_MODEL = Model()

class Banner(ExpandableComponent):
	"""Display an HTML text that occupies the whole avaiable width,
	like a banner."""
	
	def __init__(self, text):
		ExpandableComponent.__init__(self, BANNER_MODEL)
		self.add_class("banner")
		self.text = text

	def expands_horizontal(self):
		return True

	def gen(self, out):
		out.write('<div')
		self.gen_attrs(out)
		out.write('>')
		out.write(self.text)
		out.write('</div>\n')

		
