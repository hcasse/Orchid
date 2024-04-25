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

"""Module providing support for list component."""

from orchid import buffer
from orchid.base import *

SELECT_NONE = 0
SELECT_SINGLE = 1
SELECT_MUTLI = 2

MODEL = Model(
	script_paths = [ "list.js" ],
)

class Observer:
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


class Model(Subject):
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

	def index(self, x):
		return self.list.index(x)

	def set(self, i, x):
		self.list[i] = x
		Model.set(self, i, x)


class View(Component, Observer):
	"""Vertical list of items."""

	def __init__(self,
		items = [],
		selection = [],
		select_mode = SELECT_SINGLE,
		model = MODEL,
		context_menu = None
	):
		Component.__init__(self, model)
		self.add_class("list")
		if isinstance(items, list):
			self.items = ListModel(items)
		else:
			self.items = items
		self.items.add_observer(self)
		self.children = None
		self.select_mode = select_mode
		self.selection = selection
		self.context_menu = context_menu
		if select_mode != SELECT_NONE:
			self.set_attr('onclick',
				"list_on_click('%s', event);" % self.get_id())
		if context_menu != None:
			self.set_attr("oncontextmenu",
				"list_on_context_menu('%s', event);" % self.get_id())

	def finalize(self, page):
		Component.finalize(self, page)
		if self.context_menu != None:
			self.context_menu.finalize(page)
			page.add_hidden(self.context_menu)

	def get_items(self):
		"""Get the model of items."""
		return self.items

	def get_selection(self):
		"""Get the current selection."""
		return self.selection

	def make(self, value):
		"""Buid a component for the given value."""
		return Text(str(value))

	def select(self, i):
		"""Select the item corresponding to index i."""
		self.selection.append(i)
		self.call("list_select", { "id": self.get_id(), "index": i })

	def deselect(self, i):
		"""Deselect the item of index i o all."""
		self.selection.remove(i)
		self.call("list_deselect", { "id": self.get_id(), "index": i })

	def deselect_all(self):
		"""Deselect the whole selection."""
		for i in self.selection:
			self.call("list_deselect", { "id": self.get_id(), "index": i })
		self.selection.clear()

	def set_items(self, items):
		"""Chane the items displayed."""
		if isinstance(items, list):
			items = ListModel(items)
		self.selection.clear();
		self.items.remove_observer(self)
		self.items = items
		self.items.add_observer(self)
		self.children = None
		if self.online():
			self.set_content(buffer(self.gen_content))

	def on_append(self, x):
		self.deselect_all()
		item = self.make(x)
		self.get_children().append(item)
		if self.online():
			self.append_content("<div>%s</div>" % buffer(item.gen))

	def on_insert(self, i, x):
		self.deselect_all()
		item = self.make(x)
		self.get_children().insert(i, item)
		if self.online():
			self.insert_content("<div>%s</div>" % buffer(item.gen), i)

	def on_remove(self, x):
		self.deselect_all()
		i = self.items.index(x)
		if self.online():
			self.remove_child(i)

	def on_set(self, i, x):
		children = self.get_children()
		item = self.make(x)
		children[i] = item
		item.finalize(self.page)
		if self.online():
			self.call("list_set", {
				"id": self.get_id(),
				"index": i,
				"content": buffer(item.gen)
			});

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
		action = msg["action"]
		if action == "select":
			i = msg["item"]
			if i in self.selection:
				self.deselect_all()
			else:
				self.deselect_all()
				self.select(i)
		elif action == "menu":
			i = msg["item"]
			if self.selection != [msg["item"]]:
				self.deselect_all()
				self.select(i)
			self.context_menu.show(self, i)
		else:
			Component.receive(self, msg, handler)

	def gen(self, out):
		out.write('<div')
		self.gen_attrs(out)
		out.write('/>')
		self.gen_content(out)
		out.write("</div>")

	def gen_content(self, out):
		"""Generate the content of the view."""
		for item in self.get_children():
			out.write("<div>")
			item.gen(out)
			out.write("</div>")

