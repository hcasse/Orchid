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

from orchid.base import Subject, Observer, AbstractComponent
from orchid.util import STANDARD_CONSOLE

def is_python_type(t):
	return isinstance(t, type)

class Type:
	"""Represent a type."""
	MAP = {}

	def __init__(self):
		self.type = None
		self.null = None

	def record(type, object):
		Type.MAP[type] = object

	def find(type):
		try:
			return Type.MAP[type]
		except KeyError:
			return None

class BaseType(Type):
	"""Type for Python base types."""

	def __init__(self, type, null):
		self.type = type
		self.null = null

BOOL_TYPE = BaseType(bool, False)
INT_TYPE = BaseType(int, 0)
FLOAT_TYPE = BaseType(float, 0.)
STR_TYPE = BaseType(str, "")

Type.record(bool, BOOL_TYPE)
Type.record(int, INT_TYPE)
Type.record(float, FLOAT_TYPE)
Type.record(str, STR_TYPE)

class EnumType(Type):
	"""Type for enumerated values."""

	def __init__(self, values, null=None):
		assert len(values) >= 1
		self.values = values
		self.type = int
		if null is None:
			null = values[0]
		self.null = 0

	def labelFor(self, i):
		return self.values[i]

	def indexOf(self, value):
		return self.values.index(value)

	def get_values(self):
		return self.values


class RangeType(Type):
	"""Type for a range."""

	def __init__(self, min, max, null=None):
		assert min <= max
		self.min = min
		self.max = max
		self.type = int
		if null is None:
			null = min
		self.null = null


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
			type = value.__class__
		if isinstance(type, Type):
			self.type = type
		else:
			self.type = Type.find(type)

	def get_type(self):
		return self.type

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

	def __invert__(self):
		"""Get the value of the variable."""
		return self.value

	def __and__(self, x):
		return and_(not_null(self), x)

	def __or__(self, x):
		return or_(not_null(self), x)


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
		self.context = None

	def set_context(self, context):
		"""Set the context of the action (component using it)."""
		self.context = context

	def get_console(self):
		"""Get the console for the action."""
		if self.context == None:
			return STANDARD_CONSOLE
		else:
			return self.context.get_console()

	def is_enabled(self):
		"""Test if the action is enabled. Default implementation returns
		True."""
		return True

	def perform(self):
		"""Perform the action with the given console.
		Default implementation does nothing."""
		pass


class PredicateHandler(EnableSubject, Observer):
	"""Manage the predicate by observing the used variables. If a variable is changed and the predicate value is changed, update its observers."""

	def __init__(self, pred):
		EnableSubject.__init__(self)
		self.pred = pred
		self.vars = set()
		self.pred.collect_vars(self.vars)
		self.value = None
		self.context = None

	def enable(self):
		self.value = None
		for var in self.vars:
			var.add_observer(self)

	def disable(self):
		for var in self.vars:
			var.remove_observer(self)
		self.value = None

	def get(self):
		"""Get the predicate value. Component is the component calling this function."""
		if self.value is None:
			self.value = self.pred.check(self)
		return self.value

	def update(self, subject):
		new_value = self.pred.check(self)
		if new_value != self.value:
			self.value = new_value
			self.update_observers()

	def set_context(self, context):
		"""Connect the handler to the given component (typically to benefit from the component context information like console)."""
		self.context = context

	def get_console(self):
		if self.context == None:
			return STANDARD_CONSOLE
		else:
			return self.context.get_console()


class AbstractPredicate:
	"""A formula that depends on variables and that may be True or
	False. In turn, a predicate may be observed for changes."""

	def collect_vars(self, vars):
		"""Called to collect variables used in the predicate that has to be
		stored in the var set."""
		pass

	def check(self, context):
		"""Check if the predicate is true or false and return it.
		Default implementation returns True."""
		return True

	def get_handler(self):
		"""Get the handler for the predicate."""
		try:
			return self.handler
		except AttributeError:
			self.handler = PredicateHandler(self)
			return self.handler

	def __and__(self, x):
		if isinstance(x, Var):
			x = not_null(x)
		return and_(self, x)

	def __or__(self, x):
		if isinstance(x, Var):
			x = not_null(x)
		return or_(self, x)

	def __invert__(self):
		return not_(self)


class Predicate(AbstractPredicate):
	"""A predicate that lsiten to a set of variables and check with a function."""

	def __init__(self, vars = [], fun = lambda: True ):
		AbstractPredicate.__init__(self)
		self.vars = set(vars)
		self.fun = fun

	def collect_vars(self, vars):
		vars |= self.vars

	def check(self, handler):
		return self.fun()


TRUE = AbstractPredicate()


class MultiPredicate(AbstractPredicate):
	"""Base class of composed predicates."""

	def __init__(self, preds):
		AbstractPredicate.__init__(self)
		self.preds = preds

	def collect_vars(self, vars):
		for pred in self.preds:
			pred.collect_vars(vars)


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
		self.enable_pred = enable.get_handler()
		self.fun = fun

	def set_context(self, context):
		AbstractAction.set_context(self, context)
		self.enable_pred.set_context(context)

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

def get_value(x):
	if isinstance(x, Var):
		return ~x
	else:
		return x

def not_null(var):
	"""Generate a predicate that test if the variable is not None, 0, empty text, empty list, etc."""
	return Predicate(vars=[var], fun=lambda: bool(~var))

def equals(x, y):
	"""Predicate testing if x = y. x and y may be any value and specially variables that will be observed."""
	return Predicate(
		[v for v in [x, y] if isinstance(v, Var)],
		fun=lambda: get_value(x) == get_value(y)
	)

def not_(pred):
	"""Predicate inverting the result of another predicate."""
	class NotPredicate(MultiPredicate):
		def __init__(self):
			MultiPredicate.__init__(self, [pred])
		def check(self):
			return not pred.check()
	return NotPredicate()

def and_(*preds):
	"""Predicate performing an AND with the given predicates."""
	class AndPredicate(MultiPredicate):
		def __init__(self):
			MultiPredicate.__init__(self, preds)
		def check(self, handler):
			for pred in preds:
				if not pred.check(handler):
					return False
			return True
	return AndPredicate()

def or_(*preds):
	"""Predicate performing an OR with the given predicates."""
	class OrPredicate(MultiPredicate):
		def __init__(self):
			MultiPredicate.__init__(self, preds)
		def check(self, handler):
			return any([pred.check(handler) for pred in preds])
	return OrPredicate()

def is_password(var, size=8, lower=1, upper=1, digit=1, other=1):
	"""Test if the variable contains at least size characters with lower lowercase letter, upper uppercase letters, digit characters and other characters."""
	def is_other(c):
		return not (c.islower() or c.isupper() or c.isdigit())
	def count(i):
		c = 0
		for x in i:
			c += 1
		return c
	return Predicate([var], fun=lambda:
		len(~var) >= size and \
		count(filter(str.islower, ~var)) >= lower and \
		count(filter(str.isupper, ~var)) >= upper and \
		count(filter(str.isdigit, ~var)) >= digit and \
		count(filter(is_other, ~var)) >= other
	)

def if_error(pred, msg):
	"""If the predicate is false, display the message as an error to the displayer."""
	class IfError(MultiPredicate):
		def __init__(self):
			MultiPredicate.__init__(self, [pred])
			self.displayed = False
		def check(self, context):
			res = pred.check(context)
			if res:
				if self.displayed:
					context.get_console().clear_message()
					self.displayed = False
			else:
				if not self.displayed:
					context.get_console().show_error(msg)
					self.displayed = True
			return res
	return IfError()


