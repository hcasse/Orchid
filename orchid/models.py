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

from orchid.base import Subject
from orchid.mind import Var, ListType, make_type, type_of_data

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
				type = ListType(make_type(item_type))
			else:
				type = type_of_data(list)
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


class TableModel(Subject):
	"""The model is used to define the lookup of the table in function
	the displayed cell. The returned value may be components, simple
	strings or None if there is nothing to display.

	The table the models applies to is stored in the table attribute.

	Notice that, after being displayed, all modifications to the table
	has to be performed throught the Model object."""

	def __init__(self):
		Subject.__init__(self)
		self.component = None

	def get_header(self, column):
		"""Get the lookup of the given column header."""
		return None

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
		if self.component is not None:
			self.component.update_all()

	def set(self, row, column, value):
		"""Change the value of a table element."""
		if self.component is not None:
			self.component.update_cell(row, column)

	def append_row(self, content):
		"""Append a new row to the table."""
		pass

	def insert_row(self, row, content):
		"""Insert the content at row position."""
		pass

	def remove_row(self, row):
		"""Remove the given row."""
		pass

	def is_editable(self, row, col):
		"""Test if the cell at given row and column is editable."""
		return True


class ListTableModel(TableModel):
	"""Table for a model based on Python list."""

	def __init__(self, table = None, column_count = None):
		TableModel.__init__(self)
		self.table = table
		self.component = None
		if column_count is None and table is not None and table != []:
			self.column_count = len (table[0])
		else:
			self.column_count = column_count

	def get_header(self, column):
		return f"Column {column}"

	def get_column_count(self):
		return self.column_count

	def get_row_count(self):
		return len(self.table)

	def get_cell(self, row, column):
		return str(self.table[row][column])

	def set_table(self, table):
		self.table = table
		for obs in self.observers:
			obs.update_all()

	def set(self, row, column, value):
		self.table[row][column] = value
		for obs in self.observers:
			obs.update_cell(row, column)

	def append_row(self, content):
		self.table.append(content)
		for obs in self.observers:
			obs.update_append(content)

	def insert_row(self, row, content):
		self.table.insert(row, content)
		for obs in self.observers:
			obs.update_insert(row, content)

	def remove_row(self, row):
		del self.table[row]
		for obs in self.observers:
			obs.update_remove(row)

