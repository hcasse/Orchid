"""Management of images."""

from orchid.base import Model, CONTEXT_HEADERBAR, CONTEXT_NONE

class Image:
	"""Base class to represent an image (according different sources:
	file to download, standard icon, etc)."""

	def __init__(self, model):
		self.model = model

	def get_model(self):
		return self.model

	def gen(self, out, type = CONTEXT_NONE):
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

	def gen(self, out, context):
		out.write('<i class="bi bi-%s' % self.name)
		if context == CONTEXT_HEADERBAR:
			out.write(' headerbar-icon')
		out.write('"></i>')
