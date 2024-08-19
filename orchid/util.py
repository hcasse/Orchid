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

"""Utilty classes for Orchid."""

from enum import Enum, IntEnum
import sys

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


class Interface:
	"""An interface is the abstraction of an interface of the user. It
	allows to display messages and to ask the user for information.
	The way these information is really implemented depends on the
	application itself."""

	def clear_message(self):
		"""Clear the last message."""
		pass

	def show_info(self, message):
		"""Display generic information to the user."""
		pass

	def show_warning(self, message):
		""""Display warning to the user."""
		pass

	def show_error(self, message):
		"""Display erro message the user."""
		pass

	def ask_yes_or_no(self, message):
		""""Ask the user to answer by yes or no and return the value
		as a boolean (True for yes, False for no)."""
		pass

	def start_process(self, message):
		"""Display the start of a process with the given message.
		At startup is considered implemented at 0%."""
		pass

	def complete_process(self):
		"""End the current process."""
		pass

	def set_process(self, percent):
		"""Set the current status of the process. Percent is a number
		between 0 and 1."""
		pass


class StandardInterface(Interface):
	"""Console using standard input/output."""

	def show_info(self, message):
		sys.stderr.write(f"INFO: {message}\n")

	def show_warning(self, message):
		sys.stderr.write(f"WARNING: {message}\n")

	def show_error(self, message):
		sys.stderr.write(f"ERROR: {message}\n")

STANDARD_INTERFACE = StandardInterface()

class ProxyInterface(Interface):
	"""Interface redirecting the calls to another interface. Useful to specialize
	some methods of the interface. """

	def __init__(self, interface = STANDARD_INTERFACE):
		self.interface = interface

	def get_proxy(self):
		"""Get the proxy interface."""
		return self.interface

	def set_proxy(self, interface):
		"""Change the proxy interface."""
		self.interface = interface

	def clear_message(self):
		self.interface.clear_message()

	def show_info(self, message):
		self.interface.show_info(message)

	def show_warning(self, message):
		self.interface.show_warning(message)

	def show_error(self, message):
		self.interface.show_error(message)

	def ask_yes_or_no(self, message):
		self.interface.ask_yes_or_no(message)

	def start_process(self, message):
		self.interface.process(message)

	def complete_process(self):
		self.interface.complete_process()

	def set_process(self, percent):
		self.interface.set_process(percent)


class Observer:
	"""Observer for subject-observer pattern."""

	def update(self, subject):
		pass


class FunctionObserver(Observer):
	"""An observer implemented as a function."""

	def __init__(self, fun):
		self.fun = fun

	def update(self, subject):
		self.fun(subject)


class Subject:
	"""Observer for subject-observer pattern."""

	def __init__(self):
		self.observers = []

	def get_observers(self):
		"""Get the list of observers."""
		return self.observers

	def filter_observers(self, cls):
		"""Filter observers with the given class."""
		for obs in self.observers:
			if isinstance(obs, cls):
				yield obs

	def add_observer(self, observer):
		"""Add an observer to the subject. The observer may either implements
		Observer, or be callable (and will take the subject as parameter).

		Return the build observer that may be passed back to remove_observer()."""
		if callable(observer):
			observer = FunctionObserver(observer)
		self.observers.append(observer)
		return observer

	def remove_observer(self, observer):
		"""Remove an observer from the subject."""
		self.observers.remove(observer)

	def update_observers(self):
		"""Call the update function of the observers."""
		for observer in self.observers:
			observer.update(self)

# type of context

class Context(IntEnum):
	"""Enumeration of component context, mainly to fix lookup. The following
	contexts are supported:
	* NONE - no context.
	* TOOLBAR - window-level toolbar.
	* HEADERBAR - header of the application.
	* BUTTONBAR - buttonbar in window division.
	* STATUSBAR - status bar case.
	* MENU - popup menu.
	* MAIN - main window level.
	* ITEMBAR - level of items (typically appearing when mouse is over).
	"""
	NONE = 0
	TOOLBAR = 1
	HEADERBAR = 2
	BUTTONBAR = 3
	STATUSBAR = 4
	MENU = 5
	MAIN = 6
	ITEMBAR = 7

class Pos(IntEnum):
	"""Position of a component relatively to another one."""
	CENTER = 0
	BELOW = 1
	ABOVE = 2
	LEFT = 3
	RIGHT = 4

class Dir(IntEnum):
	"""Defines a direction."""
	NORTH = 0
	NORTH_EAST = 1
	EAST = 2
	SOUTH_EAST = 3
	SOUTH = 4
	SOUTH_WEST = 5
	WEST = 6
	NORTH_WEST = 7
	CENTER = 8

class Align(IntEnum):
	"""Define alignment of component inside its container."""
	NONE = 0
	LEFT = 1
	RIGHT = 2
	TOP = 1
	BOTTOM = 2
	CENTER = 3
	JUSTIFY = 4

class MessageType(Enum):
	"""Type of messages."""
	ERROR = "error"
	WARN = "warn"
	INFO = "info"
	SUCCESS = "success"
	FAILURE = "failure"

	def as_css(self):
		return self.value



