"""Component providing a console with scrolling text."""

from orchid.base import Component, Model

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

CONSOLE_MODEL = Model()

class Console(Component):

	def __init__(self, init = "", max = None):
		Component.__init__(self, CONSOLE_MODEL)
		self.init = init
		self.max = max
		self.add_class("console")

	def gen(self, out):
		out.write('<div')
		self.gen_attrs(out)
		out.write(">\n")
		out.write(self.init)
		out.write('\n</div>\n')

	def expands_horizontal(self):
		return True

	def expands_vertical(self):
		return True

	def append(self, line):
		"""Append the given line to the console. The line may use any text
		formatting HTML tag."""
		self.append_content(f"<p>{line}</p>")
		self.show_last()

	def clear(self):
		"""Clear the content of the console."""
		self.clear_content()
