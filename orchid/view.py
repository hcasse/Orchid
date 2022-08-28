"""Module imlementing components allowing to view comple data."""

from orchid.base import *

class ExplorerViewModel(Model):

	def __init__(self, parent = None):
		Model.__init__(parent)

	def gen_script(self, out):
		out.write("""
function download(id) {
}
""")

EXPLORER_VIEW_MODEL = ExplorerViewModel()


class ExplorerView(Component):
	"""View structured data with move/zoom actions."""

	def __init__(self,
		init = None,
		path = None,
		mime = None,
		model = EXPLORER_VIEW_MODEL
	):
		Component.__init__(model)
		if init != None:
			self.set_text(init, mime)
		elif path != None:
			self.set_path(path, mime)
		else:
			self.text = None
			self.path = None
			self.mime = mime
		self.add_class("explorer-view")
		self.pref = "/explorer-view/" + self.get_id()

	def download(self):
		self.send({
			"type": "download",
			"id": self.get_id(),
			"path": self.pref
		})

	def set_path(self, path, mime = None):
		"""Set the content of a view from a file."""
		self.path = path
		self.text = None
		if mime != None:
			self.mime = mime
		self.download()

	def set_text(self, text, mime = None):
		"""Set the content of a view from a text."""
		self.text = text
		self.path = None
		if mime != None:
			self.mime = mime
		elif self.mime == None:
			self.mime = "text/plain"
		self.download()

	def gen(self, out):
		out.write("<div")
		self.gen_attrs(out)
		out.write("/>\n")
