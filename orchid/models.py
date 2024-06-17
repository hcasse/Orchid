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

"""Classes representing models, observers and variables for complex data structures."""

from orchid.mind import *

class ListObserver:
	"""Observer of a list model."""

	def on_set(self, i, x):
		"""Called when a value of the list is changed."""
		pass

	def on_append(self, x):
		"""Called when an item is appended."""
		pass

	def on_remove(self, i):
		"""Called when an item is removed."""
		pass

	def on_insert(self, i, x):
		"""Called when item is inserted at position i."""
		pass

	def on_reset(self):
		"""Called when the list is reset."""
		pass


class ListModel(Subject):
	"""Model used to display a list."""

	def __init__(self):
		Subject.__init__(self)

	def size(self):
		"""Get the size of the list."""
		return 0

	def index(self, x):
		"""Get the index of a value."""
		raise ValueError()

	def get(self, index):
		"""Get the value at the given index."""
		return None

	def append(self, x):
		"""Append a value."""
		for obs in self.filter_observers(Observer):
			obs.on_append(x)

	def insert(self, i, x):
		""""Insert an element at given position."""
		for obs in self.filter_observers(Observer):
			obs.on_insert(i, x)

	def remove(self, x):
		"""Remove the given element."""
		for obs in self.filter_observers(Observer):
			obs.on_remove(x)

	def set(self, i, x):
		"""Change the value of an element."""
		for obs in self.filter_observers(Observer):
			obs.on_set(i, x)

	def reset(self):
		"""Reset the list."""
		for obs in self.filter_observers(Observer):
			obs.on_reset()


class ListVar(Var, ListModel):
	"""Variable containg a list."""

	def __init__(self, list = [], item_type = None, **args):
		ListModel.__init__(self)
		if item_type is not None:
			type = ListType(make_type(item_type))
		else:
			type = type_of_data(list)
		Var.__init__(self, list, type, **args)

	def size(self):
		return len(~self)

	def index(self, x):
		return (~self).find(x)

	def get(self, i):
		return (~self)[i]

	def append(self, x):
		(~self).append(x)
		ListModel.append(self, x)

	def insert(self, i, x):
		(~self).insert(i, x)
		ListModel.insert(self, i, x)

	def remove(self, x):
		(~self).remove(x)
		ListModel.remove(self, x)

	def set(self, i, x):
		(~self)[i] = x
		ListModel.set(self, i, x)

	def on_reset(self):
		(~self).clear()
		ListModel.reset(self)
