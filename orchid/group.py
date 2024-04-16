"""Group components."""

import orchid
from orchid.base import *

class Group(Component):
	"""Groups allows to display several components together. The place
	associated to each group component depends on its weight
	(obtained by calling Component.get_weight())."""

	def __init__(self, model, comps):
		Component.__init__(self, model)
		self.children = list(comps)
		self.expandh = False
		self.expandv = False
		self.remap_children()

	def remap_children(self):
		"""Re-build the mapping of children."""
		self.weight = (0, 0)
		for c in self.children:
			self.map_child(c)	

	def map_child(self, child):
		"""Map the child in the group."""
		(hw, vw) = self.weight
		child.parent = self
		if child.expands_horizontal():
			self.expandh = True
			hw = 1;
		if child.expands_vertical():
			self.expandv = True
			vw = 1;
		if (hw, vw) != self.weight:
			self.weight = (hw, vw)

	def insert(self, child, i = -1):
		"""Add a child to the group."""
		if i < 0:
			self.children.append(child)
		else:
			self.children.insert(i, child)
		self.map_child(child)
		child.finalize(self.page)
		if self.online():
			buf = orchid.Buffer()
			child.gen(buf)
			if i < 0:
				self.append_child(str(buf))
			else:
				self.insert_child(str(buf), i)

	def remove(self, i):
		"""Remove a child."""
		self.remove_child(i)
		del self.children[i]
		self.remap_children()

	def get_children(self):
		return self.children

	def expands_horizontal(self):
		return self.expandh

	def expands_vertical(self):
		return self.expandv

	def get_context(self):
		"""Get the group context (one of CONTEXT_* constants)."""
		return CONTEXT_NONE

	def finalize(self, page):
		Component.finalize(self, page)
		for child in self.children:
			child.finalize(page)

# HGroup class
class HGroupModel(Model):
	"""Represents a group of component horizontally arranged."""

	def __init__(self):
		Model.__init__(self)

	def gen_style(self, out):
		out.write("""
.hgroup-item {
}
.hgroup-expand {
	align-self: stretch;
}

.hgroup {
	display: flex;
	vertical-align: middle;
	flex-wrap: nowrap;
	column-gap: 4px;
	align-self: stretch;
	overflow: hidden;
	align-items: center;
}
""")

HGROUP_MODEL = HGroupModel()

class HGroup(Group):

	def __init__(self, comps = [], model = HGROUP_MODEL, align = None):
		Group.__init__(self, model, comps)
		self.align = align
		self.add_class("hgroup")

	def map_child(self, child):
		Group.map_child(self, child)
		child.add_class("hgroup-item")
		w  = child.get_weight()[0]
		if w == 0 and child.expands_horizontal():
			w = 1
		if w != 0:
			child.set_style("flex", str(w))
		if child.expands_vertical():
			child.add_class("hgroup-expand")

	def gen(self, out):
		out.write('<div ')
		self.gen_attrs(out)
		out.write('>\n')
		for c in self.children:
			c.gen(out)
		out.write('</div>\n')	


# VGroup class
class VGroupModel(Model):
	"""Represents a group of component vertically arranged."""

	def __init__(self):
		Model.__init__(self)

	def gen_style(self, out):
		out.write("""
.vgroup-item {
	align-self: center;
}
.vgroup-expand {
	align-self: stretch;
}

.vgroup {
	display: flex;
	flex-wrap: nowrap;
	flex-direction: column;
	row-gap: 4px;
	align-self: stretch;
	overflow: hidden;
	align-items: center;
}
""")
# 	white-space: nowrap;


VGROUP_MODEL = VGroupModel()

class VGroup(Group):

	def __init__(self, comps, model = VGROUP_MODEL, align = None):
		Group.__init__(self, model, comps)
		self.align = align
		self.add_class("vgroup")

	def map_child(self, child):
		Group.map_child(self, child)
		child.add_class("vgroup-item")
		w = child.get_weight()[1]
		if w == 0 and child.expands_vertical():
			w = 1
		if w != 0:
			child.set_style("flex", str(w))
		if child.expands_horizontal():
			child.add_class("vgroup-expand")

	def gen(self, out):
		out.write('<div ')
		self.gen_attrs(out)
		out.write('>\n')
		for c in self.children:
			c.gen(out)
		out.write('</div>\n')


# Spring component
SPRING_MODEL = Model()

class Spring(ExpandableComponent):
	"""Invisible component taking as much place as possible.
	One parameter of hexpand or vexpand has to be defined else the
	component won't occupy any place."""

	def __init__(self, hexpand = False, vexpand = False, weight = 1):
		ExpandableComponent.__init__(self, SPRING_MODEL)
		self.hexpand = hexpand
		hw = weight if hexpand else 0
		self.vexpand = vexpand
		vw = weight if vexpand else 0
		self.weight = (hw, vw)

	def expands_horizontal(self):
		return self.hexpand

	def expands_vertical(self):
		return self.vexpand

	def gen(self, out):
		out.write("<div")
		self.gen_attrs(out)
		out.write("></div>\n")
		self.set_style("display", "inline-block")


LAYERED_PANE_MODEL = Model(
	style = """
.layered-parent {
}

.layered-child {
	width: 100%;
	height: 100%;
	box-sizing: border-box;
}

.layered-inactive {
	display: none;
}

.layered-active {
	display: block;
}
"""
)

class LayeredPane(Group):
	"""A group made of overlapping layer with only one visible at a time."""

	def __init__(self, comps, model = LAYERED_PANE_MODEL):
		Group.__init__(self, model, comps)
		self.hexpand = None
		self.vexpand = None
		self.add_class("layered-parent")
		self.current = -1
		if self.children != []:
			self.set_layer(0)

	def set_layer(self, num):
		if num == self.current:
			return
		if self.current >= 0:
			self.children[self.current].add_class("layered-inactive")
			self.children[self.current].remove_class("layered-active")
		self.children[num].add_class("layered-active")
		self.children[num].remove_class("layered-inactive")
		self.current = num

	def map_child(self, child):
		Group.map_child(self, child)
		child.add_class("layered-child")
		child.add_class("layered-inactive")

	def remove(self, i):
		Group.remove(self, i)
		if self.current == i:
			self.current = -1

	def expands_horizontal(self):
		if self.hexpand == None:
			self.hexpand = \
				any([c.expands_horizontal for c in self.children])
		return self.hexpand

	def expands_vertical(self):
		if self.vexpand == None:
			self.vexpand = \
				any([c.expands_vertical for c in self.children])
		return self.vexpand
	
	def gen(self, out):
		out.write('<div ')
		self.gen_attrs(out)
		out.write('>\n')
		for c in self.children:
			c.gen(out)
		out.write('</div>\n')



TABBED_PANE_MODEL = Model(
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

	def __init__(self, tabs, model=TABBED_PANE_MODEL):
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

	def insert(self, tab, i = -1):
		if i < 0:
			self.tabs.append(tab)
		else:
			self.tabs.insert(tab, i)
		self.labs.insert(self.make_label(tab), i)
		self.panes.insert(tab.get_component(), i)
		if len(self.tabs) == 1:
			self.select(0)

	def remove(self, i):
		if i == self.current:
			l = len(self.tabs) 
			if l < 2:
				self.select(-1)
			else:
				if self.current + 1 >= l:
					self.select(0)
				else:
					self.select(self.current + 1)
		tab = self.get_tab(i)
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
