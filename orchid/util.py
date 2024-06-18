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

	def show_info(self, msg):
		sys.stderr.write("INFO: %s\n" % msg)

	def show_warning(self, msg):
		sys.stderr.write("WARNING: %s\n" % msg)

	def show_error(self, msg):
		sys.stderr.write("ERROR: %s\n" % msg)

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
