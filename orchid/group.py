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

	def gen_resize(self, out):
		for child in self.children:
			child.gen_resize(out)


# HGroup class
class HGroupModel(Model):

	def __init__(self):
		Model.__init__(self)

	def gen_style(self, out):
		out.write("""
.hgroup-item {
	display: inline-block;
}
""")

HGROUP_MODEL = HGroupModel()

class HGroup(Group):

	def __init__(self, *comps):
		Group.__init__(self, HGROUP_MODEL, *comps)
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

		if fixes != []:
			for child in fixes:
				out.write('\t\t\te = document.getElementById("%s");\n'
					% child.get_id());
				out.write('\t\t\ttw -= ui_full_width(e);\n');
				#out.write('console.log("%s width = " + ui_full_width(e));\n' % child.get_id())
			
		for child in self.get_children():
			if child in expands:
				out.write('\t\t\tw = tw * %d / %d;\n'
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
""")

VGROUP_MODEL = VGroupModel()

class VGroup(Group):

	def __init__(self, *comps):
		Group.__init__(self, VGROUP_MODEL, *comps)
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

		if fixes != []:
			for child in fixes:
				out.write('\t\t\te = document.getElementById("%s");\n'
					% child.get_id());
				out.write('\t\t\tth -= ui_full_height(e);\n');
				#out.write('console.log("%s height = " + ui_full_height(e));\n' % child.get_id())
			
		for child in self.get_children():
			if child in expands:
				out.write('\t\t\th = th * %d / %d;\n'
					 % (child.get_weight(), sum))
				out.write("\t\t\tresize_%s(tw, h);\n" % child.get_id())

		out.write("\t\t}\n")
