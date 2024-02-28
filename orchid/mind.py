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

"""Module to define UI in a semantic way, making the application
concept as first-class citizen and then build around it the UI.

It defines variables that can be obserbed, action instead of buttons, etc.
An application, and its different views, can be seen as a set of data on which actions applies. This structure may also be used to provide external interface to the application."""

from orchid.base import Subject, Observer

class Console:
	"""A console is the abstraction of an interface of the user. It
	allows to display messages and to ask the user for information.
	The way these information is really implemented depends on the
	application itself."""

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
	

def observer(f):
	"""Build an observer from a simple function."""

	class IndirectObserver(Observer):

		def __init__(self, f):
			self.f = f

		def update(self, subject):
			self.f(subject)

	return IndirectObserver(f)
	

class Entity:
	"""An entity is an object (action, variable) of an application
	that may be displayed or used by the human user. It is defined
	with a logic name, a label, help information, dmentation, icon, etc."""

	def __init__(self, name=None, label=None, help=None, doc=None, icon=None):
		"""Type of parameters must be:
		* name -- string,
		* label -- human-readable string,
		* help -- string with HTML tags,
		* doc -- URL to documentation,
		* icon -- orchid.image.Image object."""
		self.name = name
		self.label = label
		self.help = help
		self.doc = doc
		self.icon = icon

	def __str__(self):
		if self.name is not None:
			return self.name
		else:
			return self.label

	def __repr__(self):
		if self.label is not None:
			return self.label
		else:
			return self.name


class Var(Subject, Entity):
	"""A variable that contains a vlue that can be observed.
	As Python is not strict about types, a type ma also be given.
	This includes basic types of Python like bool, int, float, str
	but more types derived from Type can be given. This type may be used to derive automatically consistent UI."""

	def __init__(self, value, type = None, **args):
		Subject.__init__(self)
		Entity.__init__(self, **args)
		self.value = value
		if type is None:
			self.type = value.__class__
		else:
			self.type = type

	def get(self):
		"""Get the current value."""
		return self.value

	def set(self, value):
		"""Change the value in the variable."""
		self.value = value
		self.update_observers()

	def __repr__(self):
		return "var(%s: %s)" % (self.value, self.type)


class AbstractAction(Subject, Entity):
	"""An action represents a command, a procedure that can be applied
	on the current data set of the application.

	Mainly, an action can be enabled or not depending on the data set.
	An action may be observed to detect changes in enabling/disabling."""

	def __init__(self, **args):
		Subject.__init__(self)
		Entity.__init__(self, **args)

	def is_enabled(self):
		"""Test if the action is enabled. Default implementation returns
		True."""
		return True

	def perform(self, console):
		"""Perform the action with the given console.
		Default implementation does nothing."""
		pass


class Predicate(Subject, Observer):
	"""A formula that depends on variables and that may be True or
	False. In turn, a predicate may be observed for changes."""

	def __init__(self, vars = []):
		Subject.__init__(self)
		self.vars = vars
		for var in vars:
			var.add_observer(self)
		self.value = self.check()

	def get(self):
		"""Get the value of the predicate."""
		return self.value

	def check(self):
		"""Check if the predicate is true or false and return it.
		Default implementation returns True."""
		return True

	def update(self, subject):
		value = self.check()
		if value != self.value:
			self.value = value
			self.update_observers()

TRUE = Var(True)
FALSE = Var(False)

class Action(AbstractAction, Observer):
	"""Default implementation of an action with a predication and
	a function as action. Notice that the predicate may inherit from
	Predicate but may be also a boolean Var (or anything implementing
	Subject and evaluating to a boolean)."""

	def __init__(self, action, pred=True, **args):
		AbstractAction.__init__(**args)
		self.pred = pred
		pred.add_observer(self)
		self.action = action

	def is_enabled(self):
		return self.pred.get()

	def perform(self, console):
		self.action(console)

			
		

	
