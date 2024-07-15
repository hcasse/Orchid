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
An application, and its different views, can be seen as a set of data on which
actions applies. This structure may also be used to provide external interface
to the application."""

import re

from orchid.base import Subject, Observer


def is_python_type(t):
	return isinstance(t, type)

class Type:
	"""Represent a type."""
	MAP = {}

	def __init__(self):
		self.type = None
		self.null = None

	def get_null(self):
		"""Get the null value."""
		return self.null

	def parse(self, text):
		"""Parse a value of the type as a text.
		Return the value or None if the parsing fails."""
		return None

	def as_text(self, value):
		"""Transform the value of the type as text.
		Default implementation use str()."""
		return str(value)

	@staticmethod
	def record(type, object):
		Type.MAP[type] = object

	@staticmethod
	def find(type):
		try:
			return Type.MAP[type]
		except KeyError:
			return None

class BaseType(Type):
	"""Type for Python base types."""

	def __init__(self, type, null, parser=None):
		Type.__init__(self)
		self.type = type
		self.null = null
		self.parser = parser
		self.record(type, self)

	def parse(self, text):
		return self.parser(text)

	def __str__(self):
		return str(self.type)

def parse_bool(text):
	text = text.lowercase()
	if text in ["true", "on", "yes"]:
		return True
	elif text in ["false", "off", "no"]:
		return False
	else:
		return None

class ListType(Type):
	"""Type for lists."""

	def __init__(self, item_type):
		Type.__init__(self)
		self.type = list
		self.null = []
		self.item_type = item_type

	def get_item_type(self):
		"""Get the type of items in the list."""
		return self.get_item_type

	def get_null(self):
		return []

class EnumType(Type):
	"""Type for enumerated values."""

	def __init__(self, values, null=None):
		assert len(values) >= 1
		Type.__init__(self)
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
		Type.__init__(self)
		self.min = min
		self.max = max
		self.type = int
		if null is None:
			null = min
		self.null = null

class Types:
	"""Record all existing types."""

	BOOL = BaseType(bool, False, parser=parse_bool)
	INT = BaseType(int, 0, parser=int)
	FLOAT = BaseType(float, 0., parser=float)
	STR = BaseType(str, "", parser=str)
	LIST = ListType
	ENUM = EnumType
	RANGE = RangeType

	@staticmethod
	def list(item_type):
		return ListType(item_type)

	@staticmethod
	def enum(values, null=None):
		return EnumType(values, null=null)

	@staticmethod
	def range(min, max, null=None):
		return RangeType(min, max, null=null)

	@staticmethod
	def type_of(x):
		if isinstance(x, type):
			return Type.find(type)
		elif isinstance(x, Type):
			return x
		elif isinstance(x, list):
			if len(x) == 0:
				return ListType(Types.STR)
			else:
				return ListType(Types.type_of(x[0]))
		else:
			return Type.find(x.__class__)


class EntityObserver(Observer):
	"""Entity to detect changes in label, help, doc or icon."""

	def on_label_change(self, new_label):
		"""Called when the label is changed."""
		pass

	def on_help_change(self, new_help):
		"""Called when the help is changed."""
		pass

	def on_doc_change(self, new_doc):
		"""Called when the doc URL is changed."""
		pass

	def on_icon_change(self, new_icon):
		"""Called when the icon is changed."""
		pass


class Entity(Subject):
	"""An entity is an object (action, variable) of an application
	that may be displayed or used by the human user. It is defined
	with:
	* logic name,
	* label for human reader,
	* help information often displayed as tooltip,
	* documentation URL,
	* icon (Image class)."""

	def __init__(self, name=None, label=None, help=None, doc=None, icon=None):
		"""Type of parameters must be:
		* name -- string,
		* label -- human-readable string,
		* help -- string with HTML tags,
		* doc -- URL to documentation,
		* icon -- orchid.image.Image object.
		"""
		Subject.__init__(self)
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

	def set_label(self, label):
		"""Change the label of the entity."""
		self.label = label
		for observer in self.filter_observers(EntityObserver):
			observer.on_label_change(label)

	def set_help(self, help):
		"""Change the help of the entity."""
		self.help = help
		for observer in self.filter_observers(EntityObserver):
			observer.on_help_change(help)

	def set_doc(self, doc):
		"""Change the doc of the entity."""
		self.doc = doc
		for observer in self.filter_observers(EntityObserver):
			observer.on_doc_change(doc)

	def set_icon(self, icon):
		"""Change the icon of the entity."""
		self.icon = icon
		for observer in self.filter_observers(EntityObserver):
			observer.on_icon_change(icon)


class Var(Entity):
	"""A variable that contains a vlue that can be observed.
	As Python is not strict about types, a type ma also be given.
	This includes basic types of Python like bool, int, float, str
	but more types derived from Type can be given. This type may be used
	to derive automatically consistent UI."""

	def __init__(self, value, type = None, **args):
		Entity.__init__(self, **args)
		self.value = value
		if type is None:
			self.type = Types.type_of(value)
		else:
			self.type = Types.type_of(type)

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
		return f"var({self.value}: {self.type})"

	def __str__(self):
		return f"var({self.value}: {self.type})"

	def __invert__(self):
		"""Get the value of the variable."""
		return self.value

	def __and__(self, x):
		return and_(not_null(self), x)

	def __or__(self, x):
		return or_(not_null(self), x)


class PredicateError(Exception):
	"""Raised as soon as there is a predicate error."""

	def __init__(self, message):
		Exception.__init__(self)
		self.msg = message

	def message(self):
		return self.msg

	def __str__(self):
		return self.msg


class EnableObserver(Observer):
	"""Observer for enabling/disabling."""

	def enable(self):
		"""Called to enable."""
		pass

	def disable(self):
		"""Called to disable."""
		pass


class PredicateHandler(Subject, Observer):
	"""Manage the predicate by observing the used variables. If a variable is
	changed and the predicate value is changed, update its observers."""

	def __init__(self, pred):
		Subject.__init__(self)
		Observer.__init__(self)
		self.pred = pred
		self.vars = set()
		self.pred.collect_vars(self.vars)
		self.value = None

	def add_observer(self, observer):
		if not self.get_observers():
			for var in self.vars:
				var.add_observer(self)
		Subject.add_observer(self, observer)

	def remove_observer(self, observer):
		Subject.remove_observer(self, observer)
		if not self.get_observers():
			for var in self.vars:
				var.remove_observer(self)
			self.value = None

	def check(self):
		"""Check and return the value of the pedicate."""
		self.value = self.pred.check()
		return self.value

	def update(self, subject):
		old_value = self.value
		self.check()
		if old_value != self.value:
			for observer in self.get_observers():
				observer.update(self.pred)

	def get_value(self):
		"""Get the value of the pedicate."""
		if self.value is None:
			self.check()
		return self.value


class AbstractPredicate:
	"""A formula that depends on variables and that may be True or
	False. In turn, a predicate may be observed for changes."""

	def __init__(self):
		self.handler = None

	def collect_vars(self, vars):
		"""Called to collect variables used in the predicate that has to be
		stored in the var set."""
		pass

	def check(self):
		"""Check if the predicate is true or false and return it.
		Default implementation returns True."""
		return True

	def get_handler(self):
		"""Get the handler for the predicate."""
		if self.handler is None:
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

	def add_observer(self, observer):
		"""Add an observer to the predicate."""
		self.get_handler().add_observer(observer)

	def remove_observer(self, observer):
		"""Add an observer to the predicate."""
		self.get_handler().remove_observer(observer)

	def get_value(self):
		"""Get the value of the predicate, True or False."""
		return self.get_handler().get_value()

	def add_error_observer(self, observer):
		"""For predicate displaying an error, add an observer."""
		pass

	def remove_error_observer(self, observer):
		"""Remove an error observer."""
		pass


class Predicate(AbstractPredicate):
	"""A predicate that lsiten to a set of variables and check with a function."""

	def __init__(self, vars = None, fun = lambda: True ):
		AbstractPredicate.__init__(self)
		if vars is None:
			self.vars = set()
		else:
			self.vars = set(vars)
		self.fun = fun

	def collect_vars(self, vars):
		vars |= self.vars

	def check(self):
		return self.fun()


TRUE = AbstractPredicate()


class MultiPredicate(AbstractPredicate):
	"""Base class of composed predicates."""

	def __init__(self, preds):
		AbstractPredicate.__init__(self)
		self.preds = []
		for pred in preds:
			if isinstance(pred, Var):
				pred = not_null(pred)
			self.preds.append(pred)

	def collect_vars(self, vars):
		for pred in self.preds:
			pred.collect_vars(vars)

	def add_error_observer(self, observer):
		for pred in self.preds:
			pred.add_error_observer(observer)

	def remove_error_observer(self, observer):
		for pred in self.preds:
			pred.remove_error_observer(observer)


class AbstractAction(Entity):
	"""An action represents a command, a procedure that can be applied
	on the current data set of the application.

	Mainly, an action can be enabled or not depending on the data set.
	An action may be observed to detect changes in enabling/disabling."""

	def __init__(self, **args):
		Entity.__init__(self, **args)
		self.context = None

	def is_enabled(self):
		"""Test if the action is enabled. Default implementation returns
		True."""
		return True

	def add_enable_observer(self, observer):
		"""Add an enable observer that must implement EnableObserver.
		Default implementation does nothing."""
		pass

	def remove_enable_observer(self, observer):
		"""Remove an enable observer.
		Default implementation does nothing."""
		pass

	def perform(self, interface):
		"""Perform the action with the given interface.
		Default implementation does nothing."""
		pass

	def __str__(self):
		return f"<action {self.label}>"


class Action(AbstractAction):
	"""Default implementation of an action. An action basically
	perform an action (method action()) when it is invoked.
	In addition, an action may ne enabled or not depending on
	an enable predication (default to TRUE - the predicate).
	The observer must implement EnableObserver."""

	def __init__(self, fun, enable=TRUE, **args):
		AbstractAction.__init__(self, **args)
		if isinstance(enable, Var):
			enable = not_null(enable)
		self.enable_pred = enable
		self.enable_count = 0
		self.fun = fun

	def add_enable_observer(self, observer):
		if self.enable_count == 0:
			self.enable_pred.add_observer(self)
			self.enable_count += 1
		self.add_observer(observer)

	def remove_enable_observer(self, observer):
		self.remove_observer(observer)
		self.enable_count -= 1
		if self.enable_count == 0:
			self.enable_pred.remove_observer(self)

	def is_enabled(self):
		return self.enable_pred.get_value()

	def perform(self, interface):
		self.fun(interface)

	def update(self, subject):
		if self.enable_pred.get_value():
			for observer in self.filter_observers(EnableObserver):
				observer.enable()
		else:
			for observer in self.filter_observers(EnableObserver):
				observer.disable()


def get_value(x):
	"""Get the value of a constant or from a variable."""
	if isinstance(x, Var):
		return ~x
	else:
		return x

def not_null(var):
	"""Generate a predicate that test if the variable is not None, 0,
	empty text, empty list, etc."""
	return Predicate(vars=[var], fun=lambda: bool(~var))

def equals(x, y):
	"""Predicate testing if x = y. x and y may be any value and specially
	variables that will be observed."""
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
			return not self.preds[0].check()
	return NotPredicate()

def and_(*preds):
	"""Predicate performing an AND with the given predicates."""
	class AndPredicate(MultiPredicate):
		def __init__(self):
			MultiPredicate.__init__(self, preds)
		def check(self):
			for pred in preds:
				if not pred.check():
					return False
			return True
	return AndPredicate()

def or_(*preds):
	"""Predicate performing an OR with the given predicates."""
	class OrPredicate(MultiPredicate):
		def __init__(self):
			MultiPredicate.__init__(self, preds)
		def check(self):
			return any(pred.check() for pred in preds)
	return OrPredicate()

def is_password(var, size=8, lower=1, upper=1, digit=1, other=1):
	"""Test if the variable contains at least size characters with lower
	lowercase letter, upper uppercase letters, digit characters and other
	characters."""
	def is_other(c):
		return not (c.islower() or c.isupper() or c.isdigit())
	def count(i):
		c = 0
		for _ in i:
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
	class IfError(AbstractPredicate, Subject):

		def __init__(self):
			AbstractPredicate.__init__(self)
			Subject.__init__(self)

		def add_error_observer(self, observer):
			Subject.add_observer(self, observer)

		def remove_error_observer(self, observer):
			Subject.remove_observer(self, observer)

		def collect_vars(self, vars):
			pred.collect_vars(vars)

		def check(self):
			res = pred.check()
			if res:
				for observer in self.get_observers():
					observer.clear_message()
			else:
				for observer in self.get_observers():
					observer.show_error(msg)
			return res

	return IfError()


def matches(var, expr):
	"""Check if the variable matches the given regular expression."""
	r = re.compile(expr)
	class Match(Predicate):
		def check(self):
			return r.fullmatch(~var) is not None
	return Match()




