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

from orchid.base import Displayable, Model, CONTEXT_NONE

class Image(Displayable):
	"""Base class to represent an image (according different sources:
	file to download, standard icon, etc)."""

	def __init__(self, model):
		self.model = model

	def gen(self, out):
		"""Generate the code for the image. Context is one of
		CONTEXT_XXX constant."""
		pass

	def gen_in_context(self, out, context):
		"""Generate the image in the given context.
		Default implementation call gen()."""
		self.gen(out)

	def finalize(self, page):
		page.add_model(self.model)


ICON_MODEL = Model(name="icon-model")

class Icon(Image):

	def __init__(self, name, color=None):
		Image.__init__(self, ICON_MODEL)
		self.name = name
		self.color = color
		self.icon = None

	def finalize(self, page):
		Image.finalize(self, page)
		self.icon = page.get_theme().get_icon(self.name, self.color)

	def gen(self, out):
		self.gen_in_context(out, CONTEXT_NONE)

	def gen_in_context(self, out, context):
		self.icon.gen_in_context(out, context)


ASSET_IMAGE_MODEL = Model("asset-image")

class AssetImage(Image):
	"""Image from the assets of the application or from Orchid."""

	def __init__(self, path, width=None, height=None):
		Image.__init__(self, model=ASSET_IMAGE_MODEL)
		self.path = path
		self.width = width
		self.height = height

	def gen(self, out):
		out.write(f'<img src="{self.path}"')
		if self.width is not None:
			out.write(f' width="{self.width}"')
		if self.height is not None:
			out.write(f' width="{self.height}"')
		out.write(">")
