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
from orchid.button import Button
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

	def __init__(self, label, component):
		self.label = label
		self.component = component

	def get_label(self):
		"""Get he label of the tab."""
		return self.label

	def get_component(self):
		"""Get the component of the tab."""
		return self.component


class TabbedPane(VGroup):
	"""Implements tabbed pane i.e. a list of layered pane accessible
	from a list of labels displayed at top. The tabs parameters must
	be a list of Tab objects. Tabs is a list of (string label, component)
	or of Tab."""

	def __init__(self, tabs = None, model=MODEL):
		if tabs is None:
			tabs = []
		self.tabs = []
		labs = []
		for tab in tabs:
			if not isinstance(tab, Tab):
				tab = Tab(tab[0], tab[1])
			self.tabs.append(tab)
			labs.append(self.make_label(tab))
		self.labs = HGroup(labs)
		self.labs.add_class("tabbed-labelbar")
		self.panes = LayeredPane([tab.get_component() for tab in self.tabs])
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
		but = Button(
			tab.get_label(),
			on_click=lambda: self.select(tab))
		but.add_class("tabbed-label")
		return but

	def get_index(self, tab):
		"""Get the index of the given tab or component. If the tab is not in this
		pane, return None."""
		if isinstance(tab, Tab):
			try:
				return self.tabs.index(tab)
			except ValueError:
				return None
		else:
			for (i, t) in enumerate(self.tabs):
				if tab.get_component() is t:
					return i
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
			self.get_tab(self.current).get_component().on_hide()
		self.current = i
		if i >= 0:
			self.labs.get_children()[self.current].add_class("tabbed-current")
			self.panes.set_layer(i)
			self.get_tab(self.current).get_component().on_show()

	def get_tab(self, i):
		"""Get the tab which number is i."""
		return self.tabs[i]

	def expands_horizontal(self):
		return True

	def insert_tab(self, tab, label=None, i=-1):
		"""Insert a tab or a component at position i. If the tab is a component,
		the label must also be given."""
		if not isinstance(tab, Tab):
			tab = Tab(label, tab)
		if i < 0:
			self.append_tab(tab)
		else:
			self.tabs.insert(i, tab)
			self.complete_tab(i, tab)

	def append_tab(self, tab, label=None):
		"""Append a tab to the list of tabs. tab may be a Tab or a component and
		in this case, a label must be given."""
		self.tabs.append(tab)
		self.complete_tab(len(self.tabs)-1, tab)

	def complete_tab(self, i, tab):
		""""After adding a new tab, finalize the setup."""
		self.labs.insert(self.make_label(tab), i)
		self.panes.insert(tab.get_component(), i)
		if len(self.tabs) == 1:
			self.select(0)

	def remove_tab(self, tab):
		"""Remove a tab. tab may be a tab, the number of a tab or the component."""
		if isinstance(tab, int):
			i = tab
		else:
			i = self.tabs.index(tab)
		fix = False
		if i == self.current:
			l = len(self.tabs)
			if l == 1:
				self.select(-1)
			elif self.current == l-1:
				self.select(self.current - 1)
			else:
				self.select(self.current + 1)
				fix = True
		del self.tabs[i]
		self.labs.remove(i)
		self.panes.remove(i)
		if fix:
			self.current -= 1
