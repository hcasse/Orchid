"""Group components."""

from orchid.base import *

class Group(Component):
	"""Groups allows to display several components together. The place
	associated to each group component depends on its weight
	(obtained by calling Component.get_weight())."""

	def __init__(self, model, comps):
		Component.__init__(self, model)
		self.children = list(comps)
		self.expandh = False
		self.expandv = False
		hw, vw = (0 ,0)
		for c in self.children:
			c.parent = self
			if c.expands_horizontal():
				self.expandh = True
				hw = 1;
			if c.expands_vertical():
				self.expandv = True
				vw = 1;
		self.weight = (hw, vw)

	def get_children(self):
		return self.children

	def expands_horizontal(self):
		return self.expandh

	def expands_vertical(self):
		return self.expandv

	def get_context(self):
		"""Get the group context (one of CONTEXT_* constants)."""
		return CONTEXT_NONE


# HGroup class
class HGroupModel(Model):
	"""Represents a group of component horizontally arranged."""

	def __init__(self):
		Model.__init__(self)

	def gen_style(self, out):
		out.write("""
.hgroup-item {
}
.hgroup-expand {
	align-self: stretch;
}

.hgroup {
	display: flex;
	vertical-align: middle;
	flex-wrap: nowrap;
	column-gap: 4px;
	align-self: stretch;
	overflow: hidden;
	align-items: center;
}
""")

HGROUP_MODEL = HGroupModel()

class HGroup(Group):

	def __init__(self, comps = [], model = HGROUP_MODEL, align = None):
		Group.__init__(self, model, comps)
		self.align = align
		self.add_class("hgroup")
		for child in self.get_children():
			child.add_class("hgroup-item")
			w  = child.get_weight()[0]
			if w == 0 and child.expands_horizontal():
				w = 1
			if w != 0:
				child.set_style("flex", str(w))
			if child.expands_vertical():
				child.add_class("hgroup-expand")

	def gen(self, out):
		out.write('<div ')
		self.gen_attrs(out)
		out.write('>\n')
		for c in self.children:
			c.gen(out)
		out.write('</div>\n')	


# VGroup class
class VGroupModel(Model):
	"""Represents a group of component vertically arranged."""

	def __init__(self):
		Model.__init__(self)

	def gen_style(self, out):
		out.write("""
.vgroup-item {
	align-self: center;
}
.vgroup-expand {
	align-self: stretch;
}

.vgroup {
	display: flex;
	flex-wrap: nowrap;
	flex-direction: column;
	row-gap: 4px;
	align-self: stretch;
	overflow: hidden;
	align-items: center;
}
""")
# 	white-space: nowrap;


VGROUP_MODEL = VGroupModel()

class VGroup(Group):

	def __init__(self, comps, model = VGROUP_MODEL, align = None):
		Group.__init__(self, model, comps)
		self.align = align
		self.add_class("vgroup")
		for child in self.get_children():
			child.add_class("vgroup-item")
			w = child.get_weight()[1]
			if w == 0 and child.expands_vertical():
				w = 1
			if w != 0:
				child.set_style("flex", str(w))
			if child.expands_horizontal():
				child.add_class("vgroup-expand")

	def gen(self, out):
		out.write('<div ')
		self.gen_attrs(out)
		out.write('>\n')
		for c in self.children:
			c.gen(out)
		out.write('</div>\n')


# Spring component
SPRING_MODEL = Model()

class Spring(ExpandableComponent):
	"""Invisible component taking as much place as possible.
	One parameter of hexpand or vexpand has to be defined else the
	component won't occupy any place."""

	def __init__(self, hexpand = False, vexpand = False, weight = 1):
		ExpandableComponent.__init__(self, SPRING_MODEL)
		self.hexpand = hexpand
		hw = weight if hexpand else 0
		self.vexpand = vexpand
		vw = weight if vexpand else 0
		self.weight = (hw, vw)

	def expands_horizontal(self):
		return self.hexpand

	def expands_vertical(self):
		return self.vexpand

	def gen(self, out):
		out.write("<div")
		self.gen_attrs(out)
		out.write("></div>\n")
		self.set_style("display", "inline-block")


