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

DIR_NORTH = 0
DIR_NORTH_EAST = 1
DIR_EAST = 2
DIR_SOUTH_EAST = 3
DIR_SOUTH = 4
DIR_SOUTH_WEST = 5
DIR_WEST = 6
DIR_NORTH_EAST = 7
DIR_CENTER = 8

def text(type, text):
	return '<span class="text-%s">%s</span>' % (type, text)
