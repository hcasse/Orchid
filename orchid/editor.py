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

#	function editor_input(editor, event) {
#		console.log("editor " + editor.id
#			+ ": type=" + event.inputType
#			+ ", data=" + event.data
#			+ ", transfer=" + event.dataTransfer
#			+ ", ranges=" + event.getTargetRanges());
#	}

EDITOR_MODEL = EditorModel()

class Editor(ExpandableComponent):

	def __init__(self, init = "", enabled = True, readonly = False):
		ExpandableComponent.__init__(self, EDITOR_MODEL)
		self.value = init
		self.enabled = enabled
		self.readonly = readonly
		self.add_class("editor")
		self.content_getters = []

	def gen(self, out):
		#out.write('<textarea oninput="editor_input(this, event)"')
		out.write('<textarea')
		self.gen_attrs(out)
		if not self.enabled:
			out.write(' disabled')
		if self.readonly:
			out.write(' readonly')
		out.write(">\n")
		out.write(self.value)
		out.write('\n</textarea>')

	def enable(enabled = True):
		pass

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
