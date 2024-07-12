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

from enum import IntEnum, auto

from orchid.base import Displayable, Model, Context

class IconType(IntEnum):
	"""Type of icons."""

	# actions
	ABOUT = auto()
	ADD = auto()
	ALIGN_LEFT = auto()
	ALIGN_RIGHT = auto()
	CENTER = auto()
	CHAT = auto()
	CHECK = auto()
	CHECK_ALL = auto()
	CONFIGURE = auto()
	CONTEXT_MENU = auto()
	CUT = auto()
	DEBUG = auto()
	DOWNLOAD = auto()
	EJECT = auto()
	ENTER = auto()
	ERASE = auto()
	FAST_FORWARD = auto()
	GO_BACK = auto()
	GO_FORWARD = auto()
	GO_FRONT = auto()
	GO_HOME = auto()
	INDENT = auto()
	JUSTIFY = auto()
	LEAVE = auto()
	MENU = auto()
	PAINT = auto()
	PAUSE = auto()
	PICK = auto()
	PIN = auto()
	PLAY = auto()
	PRINT = auto()
	PROCESS = auto()
	PROTECT = auto()
	QUIT = auto()
	RECORD = auto()
	REMOVE = auto()
	REPEAT = auto()
	REPLY = auto()
	RESET = auto()
	REWIND = auto()
	SEARCH = auto()
	SEND = auto()
	SHOW = auto()
	SHUFFLE = auto()
	SKIP_BACKWARD = auto()
	SKIP_END = auto()
	SKIP_FORWARD = auto()
	SKIP_START = auto()
	SORT_DOWN = auto()
	SORT_UP = auto()
	STOP = auto()
	UNINDENT = auto()
	UPLOAD = auto()
	WORK = auto()
	ZOOM_IN = auto()
	ZOOM_OUT = auto()

	# decorators
	ADD_DECO = auto()
	REMOVE_DECO = auto()

	# symbols
	ANGRY = auto()
	FEMALE = auto()
	HAPPY = auto()
	HELP = auto()
	INFO = auto()
	LAYERS = auto()
	MALE = auto()
	NEUTRAL = auto()
	QUESTION = auto()
	QUOTE = auto()
	WARNING = auto()

	# keys
	ARROW_DOWN = auto()
	ARROW_LEFT = auto()
	ARROW_RIGHT = auto()
	ARROW_UP = auto()
	BACKSPACE = auto()
	BRACES = auto()
	SHIFT = auto()

	# objects
	ALARM = auto()
	BOOKMARK = auto()
	BOOKMARKS = auto()
	BOX = auto()
	CALENDAR = auto()
	CAMERA = auto()
	CLOCK = auto()
	DOC = auto()
	DROP = auto()
	EVENT = auto()
	FIRE = auto()
	FLAG = auto()
	FLOWER = auto()
	FULLSCREEN = auto()
	GRAPH = auto()
	HOURGLASS = auto()
	IDEA = auto()
	IMAGE = auto()
	KEY = auto()
	LOCK = auto()
	MAGIC = auto()
	MAP = auto()
	MESSAGE = auto()
	MONEY = auto()
	MUSIC = auto()
	PEOPLE = auto()
	PALETTE = auto()
	PAPERCLIP = auto()
	PENCIL = auto()
	PERSON = auto()
	PIECE = auto()
	PLUG = auto()
	POINT = auto()
	STACK = auto()
	STAR_EMPTY = auto()
	STAR_FULL = auto()
	STATS = auto()
	STOPWATCH = auto()
	TAG = auto()
	TARGET = auto()
	TRASHCAN = auto()
	TODO = auto()
	WALL = auto()
	VIRUS = auto()

	# technology
	CODE = auto()
	CPU = auto()
	DATABASE = auto()
	DESKTOP = auto()
	ETHERNET = auto()
	FILE = auto()
	FOLDER = auto()
	HARDDISK = auto()
	HEADPHONES = auto()
	KEYBOARD = auto()
	LAPTOP = auto()
	LINK = auto()
	MICRO = auto()
	MOUSE = auto()
	PRINTER = auto()
	SCREEN = auto()
	TERMINAL = auto()
	USBKEY = auto()
	WIFI = auto()
	WINDOW = auto()


class Image(Displayable):
	"""Base class to represent an image (according different sources:
	file to download, standard icon, etc)."""

	def __init__(self, model):
		self.model = model

	def gen(self, out):
		"""Generate the code for the image."""
		pass

	def gen_in_context(self, out, context):
		"""Generate the image in the given context.
		Default implementation call gen()."""
		self.gen(out)

	def finalize(self, page):
		page.add_model(self.model)


ICON_MODEL = Model(name="icon-model")

class Icon(Image):
	"""A standard icon. type must be an enumration constant from IconType
	or "!" prefixed string to use custom icon."""

	def __init__(self, type, color=None):
		Image.__init__(self, ICON_MODEL)
		self.type = type
		self.color = color
		self.icon = None

	def finalize(self, page):
		Image.finalize(self, page)
		self.icon = page.get_theme().get_icon(self.type, self.color)

	def gen(self, out):
		self.gen_in_context(out, Context.NONE)

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
