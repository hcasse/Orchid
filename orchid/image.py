#
#	This file is part of Orchid.
#
#    Orchid is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Lesser General Public License as
#	published by the Free Software Foundation, either version 3 of the
#	License, or (at your option) any later version.
#
#	Orchid is distributed in the hope that it will be useful, but
#	WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#	GNU Lesser General Public License for more details.
#
#	You should have received a copy of the GNU Lesser General Public
#	License along with Orchid. If not, see <https://www.gnu.org/licenses/>.
#

"""Management of images."""

from orchid.base import *

class Image(Displayable):
	"""Base class to represent an image (according different sources:
	file to download, standard icon, etc)."""

	def __init__(self, model):
		self.model = model

	def gen(self, out, type = CONTEXT_NONE):
		"""Generate the code for the image."""
		pass

	def finalize(self, page):
		page.add_model(self.model)


ICON_MODEL = Model(name="icon-model")

class Icon(Image):

	def __init__(self, name, color = None):
		global ICON_MODEL
		Image.__init__(self, ICON_MODEL)
		self.name = name
		self.color = color

	def finalize(self, page):
		Image.finalize(self, page)
		self.icon = page.get_theme().get_icon(self.name, self.color)

	def gen(self, out, context = CONTEXT_NONE):
		self.icon.gen(out, context)


ASSET_IMAGE_MODEL = Model("asset-image")

class AssetImage(Image):
	"""Image from the assets of the application or from Orchid."""

	def __init__(self, path, width=None, height=None):
		Image.__init__(self, model=ASSET_IMAGE_MODEL)
		self.path = path
		self.width = width
		self.height = height

	def gen(self, out, type = CONTEXT_NONE):
		out.write('<img src="%s"' % self.path)
		if self.width != None:
			out.write(' width="%d"' % self.width)
		if self.height != None:
			out.write(' width="%d"' % self.height)
		out.write(">")
