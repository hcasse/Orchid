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

"""List components."""

from orchid import buffer
from orchid.base import *
from orchid.label import Label

SELECT_NONE = 0
SELECT_SINGLE = 1
SELECT_MUTLI = 2

MODEL = Model(
	script_paths = [ "list.js" ],
)

class Model:
	"""Model used to display a list."""

	def __init__(self):
		self.views = []

	def size(self):
		"""Get the size of the list."""
		return 0

	def get(self, index):
		"""Get the value at the given index."""
		return None

	def append(self, x):
		"""Append a value."""
		for view in self.views:
			view.append_item(x)

	def insert(self, i, x):
		""""Insert an element at given position."""
		for view in self.views:
			view.insert_item(i, x)

	def remove(self, x):
		"""Remove the given element."""
		for view in self.views:
			view.remove_item(x)

	def index(self, x):
		"""Get the index of a value."""
		raise ValueError()


class ListModel(Model):
	"""Model based on Python's lists."""

	def __init__(self, list):
		Model.__init__(self)
		self.list = list

	def size(self):
		return len(self.list)

	def get(self, index):
		return self.list[index]

	def append(self, x):
		self.list.append(x)
		Model.append(self, x)

	def insert(self, i, x):
		self.list.insert(i, x)
		Model.insert(self, i, x)

	def remove(self, x):
		Model.remove(self, x)
		self.list.remove(x)
		print("DEBUG: list=", self.list)

	def index(self, x):
		return self.list.index(x)


class View(Component):
	"""Vertical list of items."""

	def __init__(self, items = [], select_mode = SELECT_SINGLE, model = MODEL):
		Component.__init__(self, model)
		self.add_class("list")
		if isinstance(items, list):
			self.items = ListModel(items)
		else:
			self.items = items
		self.items.views.append(self)
		self.children = None
		self.select_mode = select_mode
		self.selection = []

	def get_items(self):
		"""Get the model of items."""
		return self.items

	def get_selection(self):
		"""Get the current selection."""
		return self.selection

	def make(self, value):
		"""Buid a component for the given value."""
		return Label(str(value))

	def select(self, i):
		"""Select the item corresponding to index i."""
		self.selection.append(i)
		self.get_children()[i].add_class("select")

	def deselect(self, i):
		"""Deselect the item of index i o all."""
		self.selection.remove(i)
		self.get_children()[i].remove_class("select")

	def deselect_all(self):
		"""Deselect the whole selection."""
		for i in self.selection:
			self.get_children()[i].remove_class("select")
		self.selection = []

	def append_item(self, x):
		self.deselect_all()
		item = self.make(x)
		self.get_children().append(item)
		if self.online():
			self.append_content("<div>%s</div>" % buffer(item.gen))

	def insert_item(self, i, x):
		self.deselect_all()
		item = self.make(x)
		self.get_children().insert(i, item)
		if self.online():
			self.insert_content("<div>%s</div>" % buffer(item.gen), i)

	def remove_item(self, x):
		self.deselect_all()
		i = self.items.index(x)
		self.remove_child(i)

	def get_children(self):
		if self.children == None:
			self.children = []
			for i in range(0, self.items.size()):
				self.children.append(self.make(self.items.get(i)))
		return self.children

	def index_of(self, id):
		for i in range(0, len(self.children)):
			if self.children[i].get_id() == id:
				return i
		return -1

	def expands_horizontal(self):
		return True

	def expands_vertical(self):
		return True

	def receive(self, msg, handler):
		if msg["action"] == "select":
			i = self.index_of(msg["item"])
			print("DEBUG: i=", i)
			if i in self.selection:
				self.deselect_all()
			else:
				self.deselect_all()
				self.select(i)

	def gen(self, out):
		out.write('<div')
		if self.select_mode != SELECT_NONE:
			out.write(' onclick="list_on_click(\'%s\', event);"' % self.get_id())
		self.gen_attrs(out)
		out.write('/>')
		for item in self.get_children():
			out.write('<div>')
			item.gen(out)
			out.write('</div>')
		out.write("</div>")
