"""Data/Process-oriented user interface."""

from orchid.base import *
from orchid.button import Button
from orchid.label import Label
from orchid.label import Banner
from orchid.field import Field, is_valid_number
from orchid.group import HGroup, VGroup
from orchid.group import Spring
from orchid.group import LayeredPane
from orchid.updater import *
from orchid.editor import Editor
from orchid.console import Console
from orchid.struct import Header, ToolBar
from orchid.image import Icon, Image
from orchid.server import run
from orchid.view import InteractiveView

SUCCESS = "success"
FAILED = "failed"
INFO = "info"

def text(type, text):
	"""Generate a text colored according to the type. Type may be one
	of SUCCESS, FAILED or INFO."""
	return '<span class="text-%s">%s</span>' % (type, text)


DIR_NORTH = 0
DIR_NORTH_EAST = 1
DIR_EAST = 2
DIR_SOUTH_EAST = 3
DIR_SOUTH = 4
DIR_SOUTH_WEST = 5
DIR_WEST = 6
DIR_NORTH_EAST = 7
DIR_CENTER = 8

class Buffer:
	"""Text buffer supporting write function."""

	def __init__(self, text = ""):
		self.text = text

	def write(self, text):
		self.text = self.text + text

	def __str__(self):
		return self.text

def buffer(fun):
	"""Call function with a buffer to generate a text content and return
	the produced text."""
	buf = Buffer()
	fun(buf)
	return str(buf)

