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

	def __str__(self):
		return "var(%s: %s)" % (self.value, self.type)


class EnableSubject(Subject):
	"""A subject that calls enable() or disable() if there is or not observers."""

	def __init__(self):
		Subject.__init__(self)

	def add_observer(self, observer):
		if not self.observers:
			self.enable()
		Subject.add_observer(self, observer)

	def remove_observer(self, observer):
		Subject.remove_observer(self, observer)
		if not self.observers:
			self.disable()

	def enable(self):
		"""Called as soon as there is an observer."""
		pass

	def disable(self):
		"""Called when there is no more observer."""
		pass


class AbstractAction(EnableSubject, Entity):
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


class AbstractPredicate(EnableSubject, Observer):
	"""A formula that depends on variables and that may be True or
	False. In turn, a predicate may be observed for changes."""

	def __init__(self):
		EnableSubject.__init__(self)
		self.value = None

	def enable(self):
		"""Called to enable the predicate."""
		pass

	def disable(self):
		"""Called to disable the predicate."""
		self.value = None

	def get(self):
		"""Get the value of the predicate."""
		if self.value is None:
			self.value = self.check()
		return self.value

	def check(self):
		"""Check if the predicate is true or false and return it.
		Default implementation returns True."""
		return True


class Predicate(AbstractPredicate):
	"""A predicate that lsiten to a set of variables and check with a function."""

	def __init__(self, vars = [], fun = lambda: True ):
		AbstractPredicate.__init__(self)
		self.vars = vars
		self.fun = fun

	def enable(self):
		AbstractPredicate.enable(self)
		for var in self.vars:
			var.add_observer(self)

	def disable(self):
		for var in self.vars:
			var.remove_observer(self)
		AbstractPredicate.disable(self)
		self.value = None

	def check(self):
		return self.fun()

	def update(self, subject):
		value = self.check()
		if value != self.value:
			self.value = value
			self.update_observers()


TRUE = AbstractPredicate()


class EnableObserver(Observer):
	"""Observer supporting activation of actions."""

	def enable(self):
		pass

	def disable(self):
		pass


class Action(AbstractAction, Observer):
	"""Default implementation of an action. An action basically
	perform an action (method action()) when it is invoked.
	In addition, an action may ne enabled or not depending on
	an enable predication (default to TRUE - the predicate).
	The observer must implement EnableObserver."""

	def __init__(self, fun, enable=TRUE, **args):
		AbstractAction.__init__(self, **args)
		self.enable_pred = enable
		self.fun = fun

	def enable(self):
		self.enable_pred.add_observer(self)

	def disable(self):
		self.enable_pred.remove_observer(self)

	def update(self, subject):
		if self.is_enabled():
			for observer in self.filter_observers(EnableObserver):
				observer.enable()
		else:
			for observer in self.filter_observers(EnableObserver):
				observer.disable()

	def is_enabled(self):
		return self.enable_pred.get()

	def perform(self, console):
		self.fun(console)


def not_null(var):
	"""Generate a predicate that test if the variable is not None, 0, empty text, empty list, etc."""
	return Predicate(vars=[var], fun=lambda: bool(var.get()))


def not_(pred):
	"""Predicate inverting the result of another predicate."""
	class NotPredicate(AbstractPredicate):
		def enable(self):
			pred.enable()
		def disable(self):
			pred.disable()
		def check(self):
			return not pred.check()
	return NotPredicate()

def and_(preds):
	"""Predicate performing an AND with the given predicates."""
	class AndPredicate(AbstractPredicate):
		def enable(self):
			for pred in preds:
				pred.enable()
		def disable(self):
			for pred in preds:
				pred.disable()
		def check(self):
			return all([pred.check() for pred in preds])
	return AndPredicate()

def or_(preds):
	"""Predicate performing an OR with the given predicates."""
	class AndPredicate(AbstractPredicate):
		def enable(self):
			for pred in preds:
				pred.enable()
		def disable(self):
			for pred in preds:
				pred.disable()
		def check(self):
			return any([pred.check() for pred in preds])
	return AndPredicate()
