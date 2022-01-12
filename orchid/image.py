"""Management of images."""

from orchid.base import Model

PICTURE = 0
TOOL = 1

class Image:
	"""Base class to represent an image (according different sources:
	file to download, standard icon, etc)."""

	def __init__(self, model):
		self.model = model

	def get_model(self):
		return self.model

	def gen(self, out, type = PICTURE):
		"""Generate the code for the image."""
		pass


class IconModel(Model):

	def get_style_paths(self):
		return ["bootstrap-icons/bootstrap-icons.css"]
		

ICON_MODEL = IconModel()

class Icon(Image):
	"""An image using standard icons."""

	def __init__(self, name):
		Image.__init__(self, ICON_MODEL)
		self.name = name

	def gen(self, out, type):
		out.write('<i class="bi bi-%s' % self.name)
		if type == TOOL:
			out.write(' tool-icon')
		out.write('"></i>')
