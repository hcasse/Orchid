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

from orchid.util import buffer
from orchid.base import Component, Model
from orchid.models import ListVar, ListObserver
from orchid.displayable import Text

SELECT_NONE = 0
SELECT_SINGLE = 1
SELECT_MUTLI = 2

MODEL = Model(
	script_paths = [ "list.js" ],
	style = """
.list {
	cursor: default;
}
"""
)


class ListView(Component, ListObserver):
	"""Vertical list of items."""

	def __init__(self,
		items = None,
		selection = None,
		select_mode = SELECT_SINGLE,
		context_menu = None,
		model = MODEL
	):
		Component.__init__(self, model)
		ListObserver.__init__(self)
		if items is None:
			items = []
		if selection is None:
			selection = []
		self.add_class("list")
		if isinstance(items, list):
			self.items = ListVar(items)
		else:
			self.items = items
		self.children = None
		self.select_mode = select_mode
		if isinstance(selection, ListVar):
			self.selection = selection
		else:
			self.selection = ListVar(selection)
		self.context_menu = context_menu
		if select_mode != SELECT_NONE:
			self.set_attr('onclick',
				 f"list_on_click('{self.get_id()}', event);")
		if context_menu is not None:
			self.set_attr("oncontextmenu",
				f"list_on_context_menu('{self.get_id()}', event);")

	def finalize(self, page):
		Component.finalize(self, page)
		if self.context_menu is not None:
			self.context_menu.finalize(page)
			page.add_hidden(self.context_menu)

	def on_show(self):
		Component.on_show(self)
		self.items.add_observer(self)

	def on_hide(self):
		Component.on_hide(self)
		self.items.remove_observer(self)

	def get_items(self):
		"""Get the model of items of class orchid.models.ListModel ."""
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
			items = ListVar(items)
		self.selection.clear()
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
			self.append_content(f"<div>{buffer(item.gen)}</div>")

	def on_insert(self, i, x):
		self.deselect_all()
		item = self.make(x)
		self.get_children().insert(i, item)
		if self.online():
			self.insert_content(f"<div>{buffer(item.gen)}</div>", i)

	def on_remove(self, i):
		self.deselect_all()
		j = self.items.index(i)
		if self.online():
			self.remove_content(j)

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
			})

	def on_clear(self):
		if self.online():
			self.call("list_clear", {"id": self.get_id()})

	def get_children(self):
		if self.children is None:
			self.children = []
			for i in range(0, self.items.size()):
				self.children.append(self.make(self.items.get_index(i)))
		return self.children

	def index_of(self, id):
		for (i, x) in enumerate(self.children):
			if x.get_id() == id:
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

