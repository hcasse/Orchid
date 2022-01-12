"""Component providing a console with scrolling text."""

from orchid.base import *

class ConsoleModel(Model):

	def gen_script(self, out):
		out.write("""

	function console_clear(args) {
		var n = document.getElementById(args.id);
		n.value = "";
	}

	function console_append(args) {
		var n = document.getElementById(args.id);
		n.value = n.value + args.line + "\\n";
        n.scrollTop = (n.scrollTop + 100000);
	}
""")

CONSOLE_MODEL = ConsoleModel()

class Console(ExpandableComponent):

	def __init__(self, init = "", max = None):
		ExpandableComponent.__init__(self, CONSOLE_MODEL)
		self.init = init
		self.max = max

	def gen(self, out):
		out.write('<textarea readonly')
		self.gen_attrs(out)
		out.write(">\n")
		out.write(self.init)
		out.write('\n</textarea>\n')

	def expands_horizontal(self):
		return True

	def expands_vertical(self):
		return True

	def append(self, line):
		"""Append the given line to the console."""
		self.call("console_append", {"id": self.get_id(), "line": line})

	def clear(self):
		"""Clear the content of the console."""
		self.call("console_clear", {"id": self.get_id()})
