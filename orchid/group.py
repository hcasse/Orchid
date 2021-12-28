"""Group components."""

from orchid.base import *

class Group(Component):

	def __init__(self, model, *comps):
		Component.__init__(self, model)
		self.children = list(comps)
		for c in self.children:
			c.parent = self

	def get_children(self):
		return self.children


# HGroup class
HGROUP_MODEL = Model()

class HGroup(Group):

	def __init__(self, *comps):
		Group.__init__(self, HGROUP_MODEL, *comps)

	def gen(self, out):
		out.write('<div class=\"hgroup\">\n')
		for c in self.children:
			c.gen(out)
		out.write('</div>')	


# VGtoup class
VGROUP_MODEL = Model()

class VGroup(Group):

	def __init__(self, *comps):
		Group.__init__(self, VGROUP_MODEL, *comps)

	def gen(self, out):
		out.write('<div class=\"vgroup\">\n')
		for c in self.children:
			c.gen(out)
			out.write("<br/>\n")
		out.write('</div>')
