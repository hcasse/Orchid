"""Label component."""

from orchid.base import *

LABEL_MODEL = Model()

class Label(Component):

	def __init__(self, label):
		Component.__init__(self, LABEL_MODEL)
		self.label = label

	def gen(self, out):
		out.write('<span id="%s">%s</span>\n' % (self.get_id(), self.label))

