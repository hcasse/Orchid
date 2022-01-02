"""Label component."""

from orchid.base import *

LABEL_MODEL = Model()

class Label(Component):

	def __init__(self, label):
		Component.__init__(self, LABEL_MODEL)
		self.label = label
		self.add_class("label")

	def gen(self, out):
		out.write('<div')
		self.gen_attrs(out)
		out.write('>')
		out.write(self.label)
		out.write('</div>\n')

