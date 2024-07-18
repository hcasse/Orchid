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

from orchid.base import Subject, Observer
from orchid.mind import Var, Types

class ListObserver(Observer):
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

	def on_clear(self):
		"""Called when the list is cleared."""
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
		for obs in self.get_observers():
			if isinstance(obs, ListObserver):
				obs.on_append(x)
			else:
				obs.update(self)

	def insert(self, i, x):
		""""Insert an element at given position."""
		for obs in self.get_observers():
			if isinstance(obs, ListObserver):
				obs.on_insert(i, x)
			else:
				obs.update(self)

	def remove(self, x):
		"""Remove the given element."""
		for obs in self.filter_observers(ListObserver):
			if isinstance(obs, ListObserver):
				obs.on_remove(x)
			else:
				obs.update(self)

	def set(self, i, x):
		"""Change the value of an element."""
		for obs in self.filter_observers(ListObserver):
			if isinstance(obs, ListObserver):
				obs.on_set(i, x)
			else:
				obs.update(self)

	def clear(self):
		"""Clear the list."""
		for obs in self.filter_observers(ListObserver):
			if isinstance(obs, ListObserver):
				obs.on_clear()
			else:
				obs.update(self)


class ListVar(Var, ListModel):
	"""Variable containg a list."""

	def __init__(self, list=None, type=None, item_type=None, **args):
		ListModel.__init__(self)
		if list is None:
			list = []
		if type is None:
			if item_type is not None:
				type = Types.list(Types.of(item_type))
			else:
				type = Types.of(list)
		Var.__init__(self, list, type, **args)

	def size(self):
		return len(~self)

	def index(self, x):
		return (~self).find(x)

	def get_index(self, i):
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

	def set_index(self, i, x):
		(~self)[i] = x
		ListModel.set(self, i, x)

	def clear(self):
		(~self).clear()
		ListModel.clear(self)

	def __iter__(self):
		return iter(~self)

	def __len__(self):
		return len(~self)

	def __getitem__(self, i):
		return self.get_index(i)

	def __setitem__(self, i, x):
		self.set_index(i, x)


class TableObserver(Observer):
	"""Observer of a table."""

	def on_table_set(self, table):
		"""Called the whole table is changed."""
		pass

	def on_cell_set(self, table, row, col, val):
		"""Called each time a cell is changed."""
		pass

	def on_row_append(self, table, vals):
		"""Called each time a row is appended. Values is the cell values
		of the appended row."""
		pass

	def on_row_insert(self, table, row, vals):
		"""Called each time a row is inserted at position row. Values is
		the cell values of inserted row."""
		pass

	def on_row_remove(self, table, row):
		"""Called each time a row is removed."""
		pass



class TableModel(Subject):
	"""The model is used to define the lookup of the table in function
	the displayed cell. The returned value may be components, simple
	strings or None if there is nothing to display.

	The table the models applies to is stored in the table attribute.

	Notice that, after being displayed, all modifications to the table
	has to be performed throught the Model object."""

	def __init__(self):
		Subject.__init__(self)

	def get_column_count(self):
		"""Get the column count."""
		return 0

	def get_row_count(self):
		""""Get the row count."""
		return 0

	def get_cell(self, row, column):
		"""Get the lookup of the given cell."""
		return None

	def set_table(self, table):
		"""Called to change the table object."""
		for observer in self.filter_observers(TableObserver):
			observer.on_table_set(self)

	def set_cell(self, row, col, val):
		"""Change the value of a table element."""
		for observer in self.filter_observers(TableObserver):
			observer.on_cell_set(self, row, col, val)

	def set(self, row, col, value):
		return self.set_cell(row, col, value)

	def append_row(self, vals):
		"""Append a new row to the table."""
		for observer in self.filter_observers(TableObserver):
			observer.on_row_append(self, vals)

	def insert_row(self, row, vals):
		"""Insert the content at row position."""
		for observer in self.filter_observers(TableObserver):
			observer.on_row_insert(self, row, vals)

	def remove_row(self, row):
		"""Remove the given row."""
		for observer in self.filter_observers(TableObserver):
			observer.on_row_remove(self, row)


class ListTableModel(TableModel):
	"""Table for a model based on Python list."""

	def __init__(self, table = None, column_count = None):
		TableModel.__init__(self)
		self.table = table
		if column_count is None and table is not None and table != []:
			self.column_count = len (table[0])
		else:
			self.column_count = column_count

	def get_column_count(self):
		return self.column_count

	def get_row_count(self):
		return len(self.table)

	def get_cell(self, row, column):
		return str(self.table[row][column])

	def set_table(self, table):
		self.table = table
		super().set_table(self)

	def set_cell(self, row, col, val):
		self.table[row][col] = val
		super().set_cell(row, col, val)

	def append_row(self, vals):
		self.table.append(vals)
		super().append_row(vals)

	def insert_row(self, row, vals):
		self.table.insert(row, vals)
		super().insert_row(row, vals)

	def remove_row(self, row):
		del self.table[row]
		super().remove_row(row)


class SetObserver(Observer):
	"""Observer on set operations."""

	def on_clear(self, set):
		"""Called when the set is cleared."""
		pass

	def on_change(self, set):
		"""Called when the set is completely changed."""
		pass

	def on_add(self, set, item):
		"""Called when an item is added to the set."""
		pass

	def on_remove(self, set, item):
		"""Called when an element is removed from the set."""
		pass


class SetModel(Subject):
	"""Model for sets."""

	def __init__(self):
		Subject.__init__(self)

	def clear(self):
		"""Called to clear the set."""
		for observer in self.filter_observers(SetObserver):
			observer.on_clear(self)

	def change(self, set):
		"""Called to change the set."""
		for observer in self.filter_observers(SetObserver):
			observer.on_change(self, set)

	def add(self, item):
		"""Add an item to the set."""
		for observer in self.filter_observers(SetObserver):
			observer.on_add(self, item)

	def remove(self, item):
		"""Remove an item from the set."""
		for observer in self.filter_observers(SetObserver):
			observer.on_remove(self, item)

	def contains(self, item):
		"""Test if the set contains the item."""
		return False

	def __contains__(self, item):
		return self.contains(item)


class SetVar(Var, SetModel):
	"""Variable containing a set (or any container with same methods as sets
	i.e. clear, add, remove)."""

	def __init__(self, set, item_type=None, type=None, **args):
		if type is None:
			if item_type is not None:
				type = Types.set(Types.of(item_type))
			elif type is None:
				type = Types.of(set)
		Var.__init__(self, set, type=type, **args)
		SetModel.__init__(self)

	def set(self, value):
		Var.set(self, value)
		SetModel.change(self, value)

	def change(self, set):
		self.set(set)

	def clear(self):
		SetModel.clear(self)
		(~self).clear()

	def add(self, item):
		if item not in ~self:
			(~self).add(item)
			SetModel.add(self, item)

	def remove(self, item):
		if item in ~self:
			(~self).remove(item)
			SetModel.remove(self, item)

	def contains(self, item):
		return item in ~self

