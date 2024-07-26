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

from orchid.base import AbstractComponent, Component, Page, Model, Subject, \
	Observer, Session, Application, Pos, Dir, Align, Context, MessageType, Timer
from orchid.button import Button, CheckBox, RadioButton, TwoStateButton
from orchid.console import Console
from orchid.editor import Editor
from orchid.field import Field, ColorField, DateField, TimeField, \
	DateTimeField, PasswordField, EmailField, RangeField, \
	Select, as_natural, as_re, Form, ProposalField
from orchid.group import HGroup, VGroup, Spring, LayeredPane, hspring, vspring
from orchid.image import Icon, Image, AssetImage, IconType
from orchid.keygroup import Key, KeyGroup
from orchid.label import Label, MessageLabel, Banner
from orchid.listview import ListView
from orchid import mind
from orchid.mind import Type, Types, Entity, Var, \
	EnableObserver, AbstractPredicate, Predicate, AbstractAction, Action, \
	not_null, equals, not_, is_password, if_error, matches
from orchid.models import \
	ListObserver, ListModel, ListVar, \
	SetObserver, SetModel, SetVar, \
	TableObserver, TableModel, ListTableModel
from orchid.popup import Menu, MenuButton
from orchid.server import run
from orchid.split import SplitPane
from orchid.struct import Header, ToolBar, MessageContainer, StatusBar
from orchid.tabbedpane import TabbedPane, Tab
from orchid.table import TableView
from orchid.util import Interface, buffer
from orchid.view import InteractiveView

# deprecated
SUCCESS = MessageType.SUCCESS	# "success"
FAILED = MessageType.FAILURE	# "failed"
INFO = MessageType.INFO			# "info"
ERROR = MessageType.ERROR		# "error"

def text(mtype, content):
	"""Generate a text colored according to the type. MType may be one
	of MessageType enumeration value."""
	return f'<span class="text-{mtype.as_css()}">{content}</span>'


def var(val, type=None, **args):
	if isinstance(val, list) or isinstance(type, mind.ListType):
		return ListVar(val, type=type, **args)
	else:
		return mind.Var(val, type=type, **args)

