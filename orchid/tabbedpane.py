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

"""Provide TabbedPane component.q"""

from orchid.base import Model
import orchid
from orchid.group import VGroup, HGroup, VGROUP_MODEL, LayeredPane

MODEL = Model(
		parent = VGROUP_MODEL,
		name = "orchid-tabbed-pane",
		style = """
.tabbed-label {
}
.tabbed-current {	
}
.tabbed-labelbar {
	flex-wrap: wrap-reverse;
	align-items: flex-end;
}
.tabbed-body {
}
"""
	)

class Tab:
	"""Interface to a tab."""

	def get_label(self):
		"""Get he label of the tab."""
		return None

	def get_component(self):
		"""Get the component of the tab."""
		return None

	def on_show(self):
		"""Called when the tab is shown."""
		pass

	def on_hide(self):
		"""Called when a tab is hidden."""

	def on_release(self):
		"""Called when a tab is released."""
		pass


class TabbedPane(VGroup):
	"""Implements tabbed pane i.e. a list of layered pane accesible
	from a list of labels displayed at top. The tabs parameters must
	be a list of Tab objects."""

	def __init__(self, tabs, model=MODEL):
		self.tabs = tabs
		labs = []
		for tab in tabs:
			labs.append(self.make_label(tab))
		self.labs = HGroup(labs)
		self.labs.add_class("tabbed-labelbar")
		self.panes = LayeredPane([tab.get_component() for tab in tabs])
		self.panes.add_class("tabbed-body")
		self.current = -1
		if tabs:
			self.select(0)
		VGroup.__init__(self, [self.labs, self.panes], model)
		self.add_class("tabbed")

	def get_tabs(self):
		"""Get the list of tabs."""
		return self.tabs

	def make_label(self, tab):
		but = orchid.Button(
			tab.get_label(),
			on_click=lambda: self.select(tab))
		but.add_class("tabbed-label")
		return but

	def get_index(self, tab):
		"""Get the index of the given tab. If the tab is not in this
		pane, return None."""
		try:
			return self.tabs.index(tab)
		except ValueError:
			return None

	def select(self, i):
		"""Select the current shown tab. i may be the index of the tab
		or the tab itself."""
		if isinstance(i, Tab):
			i = self.get_index(i)
		if i == self.current:
			return
		if self.current >= 0:
			self.labs.get_children()[self.current].remove_class("tabbed-current")
			self.get_tab(self.current).on_hide()
		self.current = i
		if i >= 0:
			self.labs.get_children()[self.current].add_class("tabbed-current")
			self.panes.set_layer(i)
			self.get_tab(self.current).on_show()

	def get_tab(self, i):
		"""Get the tab which number is i."""
		return self.tabs[i]

	def expands_horizontal(self):
		return True

	def expands_vertical(self):
		expand = False
		for child in self.panes.get_children():
			if child.expands_vertical():
				expand = True
				break
		return expand

	def insert(self, child, i = -1):
		if i < 0:
			self.append(child)
		else:
			self.tabs.insert(i, child)
			self.complete_tab(i, child)

	def append(self, tab):
		self.tabs.append(tab)
		self.complete_tab(len(self.tabs)-1, tab)

	def complete_tab(self, i, tab):
		self.labs.insert(self.make_label(tab), i)
		self.panes.insert(tab.get_component(), i)
		if len(self.tabs) == 1:
			self.select(0)

	def remove(self, i):
		"""Remove a tab. i may be the tab number or the tab to remove."""
		if isinstance(i, Tab):
			tab = i
			i = self.tabs.index(i)
		else:
			tab = self.get_tab(i)
		if i == self.current:
			l = len(self.tabs)
			if l < 2:
				self.select(-1)
			else:
				if self.current + 1 >= l:
					self.select(0)
				else:
					self.select(self.current + 1)
		del self.tabs[i]
		self.labs.remove(i)
		self.panes.remove(i)
		tab.on_release()

	def gen(self, out):
		out.write('<div ')
		self.gen_attrs(out)
		out.write('>\n')
		for c in self.children:
			c.gen(out)
		out.write('</div>\n')
