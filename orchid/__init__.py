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

"""Data/Process-oriented user interface."""

from orchid.util import *
from orchid.base import *
from orchid.button import Button, CheckBox, RadioButton
from orchid.label import Label
from orchid.label import Banner
from orchid.field import Field, ColorField, DateField, TimeField, \
	DateTimeField, PasswordField, EmailField, RangeField, \
	as_natural, as_re
from orchid.group import HGroup, VGroup
from orchid.group import Spring
from orchid.group import LayeredPane
from orchid.tabbedpane import TabbedPane, Tab
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

POS_CENTER = 0
POS_BELOW = 1
POS_ABOVE = 2
POS_LEFT = 3
POS_RIGHT = 4

DIR_NORTH = 0
DIR_NORTH_EAST = 1
DIR_EAST = 2
DIR_SOUTH_EAST = 3
DIR_SOUTH = 4
DIR_SOUTH_WEST = 5
DIR_WEST = 6
DIR_NORTH_EAST = 7
DIR_CENTER = 8

