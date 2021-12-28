"""Updater classes."""

import orchid.base as base

class Updater:
	"""A connector performs an action according to conditions."""

	def __init__(self, condition):
		self.condition = condition
		condition.parent = self
		self.test = None

	def trigger(self):
		"""Function called when a condition is triggerred."""
		test = self.condition.test()
		if test != self.test:
			self.test = test
			self.apply(test)

	def apply(self, test):
		"""Called to apply the action."""
		pass
	

class Condition:
	"""A condition test the state of a component."""

	def __init__(self):
		self.parent = None

	def test(self):
		return True


class EmbedCondition(Condition):

	def __init__(self, cond):
		Condition.__init__(self)
		self.cond = cond
		cond.parent = self

	def trigger(self):
		self.parent.trigger()


class Not(EmbedCondition):
	"""Condition that inverts its sub-condition."""

	def __init__(self, cond):
		EmbedCondition.__init__(self, cond)

	def test(self):
		return not self.cond.test()


class GroupCondition(Condition):

	def __init__(self, *conds):
		self.conds = conds
		for cond in self.conds:
			cond.parent = self

	def trigger(self):
		self.parent.trigger()


class And(GroupCondition):
	"""Condition that test if all sub-conditions are true together."""

	def __init__(self, *conds):
		GroupCondition.__init__(self, *conds)

	def test(self):
		for cond in self.conds:
			if not cond.test():
				return False
		return True


class Or(GroupCondition):
	"""Condition that test if one of sub-conditions is true."""

	def __init__(self, *conds):
		GroupCondition.__init__(self, *conds)

	def test(self):
		for cond in self.conds:
			if cond.test():
				return True
		return False


class IsValid(Condition, base.Observer):
	"""Test if the argument is valid."""

	def __init__(self, component):
		Condition.__init__(self)
		self.component = component
		component.add_observer(self)

	def test(self):
		return self.component.is_valid(self.component.get_content())

	def update(self, subject):
		self.parent.trigger()


class EnableIf(Updater):
	"""Updater for enabling/idsabling a component."""

	def __init__(self, condition, *components):
		Updater.__init__(self, condition)
		self.components = components

	def apply(self, test):
		for component in self.components:
			component.enable(test)
