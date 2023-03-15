"""Editor class."""

from orchid.base import *

class EditorModel(Model):

	def gen_script(self, out):
		out.write("""

	function editor_content(args) {
		id = args.id
		n = document.getElementById(id);
		ui_post({id: id, action: "content", content: n.value})
	}

""")

EDITOR_MODEL = EditorModel()

class Editor(ExpandableComponent):

	def __init__(self, init = "", enabled = True, readonly = False):
		ExpandableComponent.__init__(self, EDITOR_MODEL)
		self.value = init
		self.add_class("editor")
		self.content_getters = []
		if enabled:
			self.enable()
		else:
			self.disable()
		self.readonly = readonly
		if readonly:
			self.set_attr("readonly", "true")
		self.weight = (1, 1)
		self.set_style("align-self", "stretch")
		self.add_class("editor")

	def gen(self, out):
		#out.write('<textarea oninput="editor_input(this, event)"')
		out.write('<textarea')
		self.gen_attrs(out)
		out.write(">\n")
		out.write(self.value)
		out.write('\n</textarea>')

	def enable(self):
		self.remove_attr("disabled")
		self.enabled = True

	def disable(self):
		self.set_attr("disabled", "true")
		self.enabled = False

	def expands_horizontal(self):
		return True

	def expands_vertical(self):
		return True

	def get_content(self, f):
		"""Asynchronously look up for the content of the editor.
		Function f is called once the content is obtained."""
		self.content_getters.append(f)
		self.call("editor_content", {"id": self.get_id()})

	def receive(self, msg, handler):
		if msg["action"] == "content":
			content = msg["content"]
			for f in self.content_getters:
				f(self, content)
			self.content_getters = []
		else:
			ExpandableComponent.receive(self, msg, handler)
