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

"""Group components."""

import orchid.base as orc
from orchid.base import Model, Component, ExpandableComponent

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
			hw = 1
		if child.expands_vertical():
			self.expandv = True
			vw = 1
		if (hw, vw) != self.weight:
			self.weight = (hw, vw)

	def remove_children(self):
		"""Remove all children of the group."""
		self.children = []
		self.remap_children()
		self.clear_content()

	def replace_children(self, children):
		"""Replace all children by the new ones."""
		if self.online():
			self.remove_children()
		self.children = children
		self.remap_children()
		for child in children:
			child.finalize(self.page)
		if self.online():
			self.clear_content()
			self.set_content(children)

	def insert(self, child, i = -1):
		"""Add a child to the group."""
		if i < 0:
			self.children.append(child)
		else:
			self.children.insert(i, child)
		self.map_child(child)
		child.finalize(self.page)
		if self.online():
			if i < 0:
				self.append_content(child)
			else:
				self.insert_content(child, i)

	def remove(self, i):
		"""Remove a child. i may be the index or the sub-component to remove."""
		if not isinstance(i, int):
			try:
				i = self.children.index(i)
			except ValueError:
				return
		self.remove_content(i)
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
		return orc.CONTEXT_NONE

	def finalize(self, page):
		Component.finalize(self, page)
		for child in self.children:
			child.finalize(page)

	def show(self):
		for child in self.children:
			child.show()

	def hide(self):
		for child in self.children:
			child.hide()


# HGroup class

HGROUP_MODEL = Model(
	"hgroup-model",
	style = """
.hgroup-item {
	flex-shrink: 0;
}
.hgroup-expand {
	align-self: stretch;
}

.hgroup {
	display: flex;
	flex-wrap: nowrap;
	column-gap: 4px;
	align-self: stretch;
	overflow: hidden;
}
""")


class HGroup(Group):
	"""Creates an horizontal group.
	* comps: components in the group.
	* align: vertival alignment of model (one of ALIGN_ constant)."""

	ALIGNS = {
		orc.ALIGN_NONE: None,
		orc.ALIGN_TOP: "start",
		orc.ALIGN_BOTTOM: "end",
		orc.ALIGN_CENTER: "center",
		orc.ALIGN_JUSTIFY: "stretch"
	}

	def __init__(self, comps = None, model = HGROUP_MODEL, align = orc.ALIGN_LEFT):
		if comps is None:
			comps = []
		Group.__init__(self, model, comps)
		self.add_class("hgroup")
		align = HGroup.ALIGNS[align]
		if align is not None:
			self.set_style("align-items", align)

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
	flex-shrink: 0;
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
}
""")
# 	white-space: nowrap;


VGROUP_MODEL = VGroupModel()

class VGroup(Group):
	"""Display a group of components vertically.
	* comps: components in the group.
	* align: horizontal alignment of components (one of ALIGN_ constant)."""

	ALIGNS = {
		orc.ALIGN_NONE: None,
		orc.ALIGN_LEFT: "start",
		orc.ALIGN_RIGHT: "end",
		orc.ALIGN_CENTER: "center",
		orc.ALIGN_JUSTIFY: "stretch"
	}

	def __init__(self, comps, model = VGROUP_MODEL, align = orc.ALIGN_NONE):
		Group.__init__(self, model, comps)
		self.add_class("vgroup")
		align = VGroup.ALIGNS[align]
		if align is not None:
			self.set_style("align-items", align)

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
		self.set_style("display", "inline-block")

	def expands_horizontal(self):
		return self.hexpand

	def expands_vertical(self):
		return self.vexpand

	def gen(self, out):
		out.write("<div")
		self.gen_attrs(out)
		out.write("></div>\n")


def hspring():
	"""Creates an horizontal spring."""
	return Spring(hexpand=True)

def vspring():
	"""Creates an horizontal spring."""
	return Spring(vexpand=True)


LAYERED_PANE_MODEL = Model(
	style = """
.layered-parent {
	display: flex;
	align-items: stretch;
}

.layered-child {
	display: block;
	flex-grow: 1;
	box-sizing: border-box;
}

.layered-inactive {
	position: absolute;
	left: -10000px;
	top: -10000px;
}

.layered-active {
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
			self.children[self.current].remove_class("layered-active")
		if self.current >= 0:
			self.children[self.current].add_class("layered-inactive")
		self.children[num].remove_class("layered-inactive")
		self.children[num].add_class("layered-active")
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
		if self.hexpand is None:
			self.hexpand = \
				any(c.expands_horizontal for c in self.children)
		return self.hexpand

	def expands_vertical(self):
		if self.vexpand is None:
			self.vexpand = \
				any(c.expands_vertical for c in self.children)
		return self.vexpand

	def gen(self, out):
		out.write('<div ')
		self.gen_attrs(out)
		out.write('>\n')
		for c in self.children:
			c.gen(out)
		out.write('</div>\n')
