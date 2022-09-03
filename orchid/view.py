"""Module imlementing components allowing to view comple data."""

from orchid.base import *

class InteractiveViewModel(Model):

	def __init__(self, parent = None):
		Model.__init__(self, parent)

INTERACTIVE_VIEW_MODEL = InteractiveViewModel()


class InteractiveView(Component):
	"""View structured data with move/zoom actions."""

	def __init__(self,
		init = None,
		path = None,
		mime = None,
		model = INTERACTIVE_VIEW_MODEL
	):
		Component.__init__(self, model)
		if init != None:
			self.set_text(init, mime)
		elif path != None:
			self.set_path(path, mime)
		else:
			self.text = None
			self.path = None
			self.mime = mime
		self.add_class("interactive-view")
		self.url = "/interactive-view/" + self.get_id()

	def show(self, path = None, text = None, mime = None):
		"""Set the content of a view. If neither path,
		nor text is given, the view is cleared."""

		# set the state
		self.mime = mime
		if path != None:
			self.path = path
			self.text = None
		elif text != None:
			self.text = text
			self.path = None
			if self.mime == None:
				self.mime = "text/plain"
		else:
			self.path = None
			self.text = ""
			self.mime = None

		# show the content
		self.publish()
		self.send({
			"type": "download",
			"id": self.get_id(),
			"path": self.url
		})

	def publish(self):
		if self.text != None:
			self.get_page().publish_text(self.url, self.text)
		elif self.path != None:
			self.get_page().publish_file(self.url, self.path)

	def gen(self, out):
		out.write("<div")
		self.gen_attrs(out)
		out.write("></div>\n")
		self.publish()

	def expands_horizontal(self):
		return True

	def expands_vertical(self):
		return True
