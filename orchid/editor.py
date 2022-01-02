"""Editor class."""

from orchid.base import *

class EditorModel(Model):
	pass

EDITOR_MODEL = EditorModel()

class Editor(ExpandableComponent):

	def __init__(self, init = "", enabled = True, readonly = False):
		ExpandableComponent.__init__(self, EDITOR_MODEL)
		self.value = init
		self.enabled = enabled
		self.readonly = readonly
		self.add_class("editor")

	def gen(self, out):
		out.write('<textarea')
		self.gen_attrs(out)
		if not self.enabled:
			out.write(' disabled')
		if self.readonly:
			out.write(' readonly')
		out.write(">\n")
		out.write(self.value)
		out.write('\n</textarea>\n')

	def enable(enabled = True):
		pass

	def expands_horizontal(self):
		return True

	def expands_vertical(self):
		return True
