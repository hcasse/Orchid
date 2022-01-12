"""Group components."""

from orchid.base import *

class Group(Component):

	def __init__(self, model, comps):
		Component.__init__(self, model)
		self.children = list(comps)
		self.expandh = False
		self.expandv = False
		for c in self.children:
			c.parent = self
			if c.expands_horizontal():
				self.expandh = True
			if c.expands_vertical():
				self.expandv = True

	def get_children(self):
		return self.children

	def gen_resize(self, out):
		for child in self.children:
			child.gen_resize(out)

	def expands_horizontal(self):
		return self.expandh

	def expands_vertical(self):
		return self.expandv


# HGroup class
class HGroupModel(Model):

	def __init__(self):
		Model.__init__(self)

	def gen_style(self, out):
		out.write("""
.hgroup-item {
	display: inline-block;
	vertical-align: middle;
}

.hgroup {
	text-indent: 0;
	white-space: nowrap;
	overflow-x: clip;
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

	def gen(self, out):
		out.write('<div ')
		self.gen_attrs(out)
		out.write('>\n')
		for c in self.children:
			c.gen(out)
		out.write('</div>\n')	

	def gen_resize(self, out):

		# prepare generation
		sum = 0
		fixes = []
		expands = []
		for child in self.get_children():
			if child.expands_horizontal():
				expands.append(child)
				sum += child.get_weight()
			else:
				fixes.append(child)

		# generate child code
		Group.gen_resize(self, out)

		# generate the code
		out.write("\t\tfunction resize_%s(tw, th) {\n" % self.get_id())
		out.write('\t\t\tvar e = document.getElementById(%s);\n' % self.get_id())
		out.write('\t\t\ttw -= ui_left_offset(e) + ui_right_offset(e);\n')
		out.write('\t\t\tth -= ui_top_offset(e) + ui_bottom_offset(e);\n')
		#out.write('\t\t\tui_show_size(e);\n')
		if fixes != []:
			for child in fixes:
				out.write('\t\t\te = document.getElementById("%s");\n'
					% child.get_id());
				out.write('\t\t\ttw -= ui_full_width(e);\n');
				if child.expands_vertical():
					out.write("\t\t\tresize_%s(ui_content_width(e), th);\n" % child.get_id())
				#out.write('console.log("%s width = " + ui_full_width(e));\n' % child.get_id())
			
		for child in self.get_children():
			if child in expands:
				out.write('\t\t\tw = Math.floor(tw * %d / %d);\n'
					 % (child.get_weight(), sum))
				out.write("\t\t\tresize_%s(w, th);\n" % child.get_id())

		out.write("\t\t}\n")


# VGroup class
class VGroupModel(Model):

	def __init__(self):
		Model.__init__(self)

	def gen_style(self, out):
		out.write("""
.vgroup-item {
	display: block;
}

.vgroup {
	text-indent: 0;
	white-space: nowrap;
	overflow-y: clip;
}
""")

VGROUP_MODEL = VGroupModel()

class VGroup(Group):

	def __init__(self, comps, model = VGROUP_MODEL, align = None):
		Group.__init__(self, model, comps)
		self.align = align
		self.add_class("vgroup")
		for child in self.get_children():
			child.add_class("vgroup-item")

	def gen(self, out):
		out.write('<div ')
		self.gen_attrs(out)
		out.write('>\n')
		for c in self.children:
			c.gen(out)
		out.write('</div>\n')

	def gen_resize(self, out):

		# prepare generation
		sum = 0
		fixes = []
		expands = []
		for child in self.get_children():
			if child.expands_vertical():
				expands.append(child)
				sum += child.get_weight()
			else:
				fixes.append(child)

		# generate child code
		Group.gen_resize(self, out)

		# generate the code
		out.write("\t\tfunction resize_%s(tw, th) {\n" % self.get_id())
		out.write('\t\t\tvar e = document.getElementById(%s);\n' % self.get_id())
		out.write('\t\t\ttw -= ui_left_offset(e) + ui_right_offset(e);\n')
		out.write('\t\t\tth -= ui_top_offset(e) + ui_bottom_offset(e);\n')

		if fixes != []:
			for child in fixes:
				out.write('\t\t\te = document.getElementById("%s");\n'
					% child.get_id());
				out.write('\t\t\tth -= ui_full_height(e);\n');
				#out.write('console.log("%s height = " + ui_full_height(e));\n' % child.get_id())
				if child.expands_horizontal():
					out.write("\t\t\tresize_%s(tw, ui_content_height(e));\n" % child.get_id())
			
		for child in self.get_children():
			if child in expands:
				out.write('\t\t\th = th * %d / %d;\n'
					 % (child.get_weight(), sum))
				out.write("\t\t\tresize_%s(tw, h);\n" % child.get_id())

		out.write("\t\t}\n")


# Spring component
SPRING_MODEL = Model()

class Spring(ExpandableComponent):
	"""Invisible component taking as much place as possible.
	One parameter of hexpand or vexpand has to be defined else the
	component won't occupy any place."""

	def __init__(self, hexpand = False, vexpand = False, weight = 1):
		ExpandableComponent.__init__(self, SPRING_MODEL)
		self.hexpand = hexpand
		self.vexpand = vexpand
		self.weight = weight

	def expands_horizontal(self):
		return self.hexpand

	def expands_vertical(self):
		return self.vexpand

	def get_weight(self):
		return self.weight

	def gen(self, out):
		out.write("<div")
		self.gen_attrs(out)
		out.write(' style="display: inline-block;"')
		out.write("></div>\n")


