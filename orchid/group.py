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

from orchid.base import Model, Component, ParentComponent
from orchid.util import Align, Context

GROUP_MODEL = Model(
	"group",
	style = """
.group-expand {
	flex-grow: 1;
	flex-basis: 0;
}

.group-not-expand {
	flex-shrink: 0;
}

.group-anti-expand {
	align-self: stretch;
}

.group-disabled {
	pointer-events: none;
	opacity: 0.4;
	cursor: not-allowed;
}
"""
)


class Group(ParentComponent):
	"""Groups allows to display several components together. The place
	associated to each group component depends on its weight
	(obtained by calling Component.get_weight())."""

	COMP_CLASS = "hgroup"
	EXPAND = "group-expand"
	NOT_EXPAND = "group-not-expand"
	ANTI_EXPAND = "group-anti-expand"

	ALIGNS = {
		Align.NONE: None,
		Align.TOP: "start",
		Align.BOTTOM: "end",
		Align.CENTER: "center",
		Align.JUSTIFY: "stretch"
	}

	def __init__(self, model, comps):
		ParentComponent.__init__(self, model)
		self.children = list(comps)
		self.expandh = None
		self.expandv = None
		for child in self.children:
			child.parent = self
		self.remap_children()
		self.enabled = True

	def finalize(self, page):
		Component.finalize(self, page)
		for child in self.children:
			child.finalize(page)

	def remap_children(self):
		"""Re-build the mapping of children."""
		self.expandh = False
		self.expandv = False
		for c in self.children:
			self.map_child(c)

	def map_child(self, child):
		"""Map the child in the group."""
		(hw, vw) = self.get_weight()
		if child.expands_horizontal() or hw > 0:
			self.expandh = True
		if child.expands_vertical() or vw > 0:
			self.expandv = True

	def check_remap(self):
		"""Test if remapping is needed."""
		old_expandh = self.expandh
		old_expandv = self.expandv
		self.remap_children()
		if old_expandh != self.expandh or old_expandv != self.expandv:
			self.parent.remap_child(self)

	def remap_child(self, child):
		self.check_remap()

	def remove_children(self):
		"""Remove all children of the group."""
		if self.online() and self.is_shown():
			for child in self.children:
				if child.is_shown():
					child.on_hide()
		for child in self.children:
			child.parent = None
		self.children = []
		self.remap_children()
		if self.online():
			self.clear_content()

	def replace_children(self, children):
		"""Replace all children by the new ones."""
		self.remove_children()
		self.children = children
		self.remap_children()
		for child in children:
			child.parent = self
			child.finalize(self.page)
		if self.online():
			if self.is_shown():
				for child in children():
					child.on_show()
			self.clear_content()
			self.set_content(children)

	def insert(self, child, i = -1):
		"""Add a child to the group."""
		child.parent = self
		if i < 0:
			self.children.append(child)
		else:
			self.children.insert(i, child)
		child.finalize(self.page)
		if self.online():
			if self.is_shown():
				child.on_show()
			if i < 0:
				self.append_content(child)
			else:
				self.insert_content(child, i)
		self.check_remap()

	def remove(self, i):
		"""Remove a child. i may be the index or the sub-component to remove."""
		if not isinstance(i, int):
			child = i
			i = self.children.index(child)
		else:
			child = self.children[i]
		self.remove_content(i)
		del self.children[i]
		if self.online() and self.is_shown():
			child.on_hide()
		child.parent = None
		self.check_remap()

	def get_children(self):
		return self.children

	def expands_horizontal(self):
		return self.expandh

	def expands_vertical(self):
		return self.expandv

	def get_context(self):
		"""Get the group context (one of Context enumeration value)."""
		return Context.NONE

	def on_show(self):
		ParentComponent.on_show(self)
		for child in self.children:
			if not child.is_shown():
				child.on_show()

	def on_hide(self):
		ParentComponent.on_hide(self)
		for child in self.children:
			if child.is_shown():
				child.on_hide()

	def disable(self):
		self.add_class("group-disabled")
		self.enabled = False

	def enable(self):
		self.remove_class("group-disabled")
		self.enabled = True

	def find_next_focus(self, component=None):
		if not self.enabled:
			return None
		elif component is None:
			for child in self.children:
				next = child.find_next_focus()
				if next is not None:
					return next
			return None
		else:
			i = self.children.index(component) + 1
			for child in self.children[i:]:
				next = child.find_next_focus()
				if next is not None:
					return next
			return self.parent.find_next_focus(self)

	def grab_focus(self, **args):
		child = self.find_next_focus()
		if child is not None:
			child.grab_focus(**args)


# HGroup class

HGROUP_MODEL = Model(
	"hgroup",
	parent = GROUP_MODEL,
	style = """
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
	* align: vertival alignment of model (Align enumeration value)."""

	def __init__(self, comps = None, model = HGROUP_MODEL, align = Align.LEFT):
		if comps is None:
			comps = []
		Group.__init__(self, model, comps)
		self.add_class(self.COMP_CLASS)
		align = Group.ALIGNS[align]
		if align is not None:
			self.set_style("align-items", align)

	def map_child(self, child):
		Group.map_child(self, child)
		(hw, vw) = child.get_weight()
		if hw > 0:
			child.remove_class(self.EXPAND)
			child.remove_class(self.NOT_EXPAND)
			child.set_style("flex-grow", hw)
			child.set_style("flex-basis", 0)
		elif child.expands_horizontal():
			child.remove_class(self.NOT_EXPAND)
			child.add_class(self.EXPAND)
		else:
			child.remove_class(self.EXPAND)
			child.add_class(self.NOT_EXPAND)
		if vw > 0 or child.expands_vertical():
			child.add_class(self.ANTI_EXPAND)
		else:
			child.remove_class(self.ANTI_EXPAND)

	def gen(self, out):
		out.write('<div ')
		self.gen_attrs(out)
		out.write('>\n')
		for c in self.children:
			c.gen(out)
		out.write('</div>\n')

	def show_last(self):
		if self.online():
			self.send({
				"type": "show-last",
				"id": self.get_id(),
				"dir": 0
			})

	def show_child(self, child):
		if self.online():
			self.send({
				"type": "show-child",
				"id": self.get_id(),
				"child": child.get_id(),
				"dir": 0
			})


# VGroup class

VGROUP_MODEL = Model(
	"vgroup",
	parent = GROUP_MODEL,
	style = """
.vgroup {
	display: flex;
	flex-wrap: nowrap;
	flex-direction: column;
	row-gap: 4px;
	align-self: stretch;
	overflow: hidden;
}
"""
)

class VGroup(Group):
	"""Display a group of components vertically.
	* comps: components in the group.
	* align: horizontal alignment of components (Align enumeration value)."""

	def __init__(self, comps, model = VGROUP_MODEL, align = Align.NONE):
		Group.__init__(self, model, comps)
		self.add_class("vgroup")
		align = Group.ALIGNS[align]
		if align is not None:
			self.set_style("align-items", align)

	def map_child(self, child):
		Group.map_child(self, child)
		(hw, vw) = child.get_weight()
		if vw > 0:
			child.remove_class(self.EXPAND)
			child.add_class(self.NOT_EXPAND)
			child.set_style("flex-grow", vw)
			child.set_style("flex-basis", 0)
		elif child.expands_vertical():
			child.remove_class(self.NOT_EXPAND)
			child.add_class(self.EXPAND)
		else:
			child.remove_class(self.EXPAND)
			child.add_class(self.NOT_EXPAND)
		if hw > 0 or child.expands_horizontal():
			child.add_class(self.ANTI_EXPAND)
		else:
			child.remove_class(self.ANTI_EXPAND)

	def gen(self, out):
		out.write('<div ')
		self.gen_attrs(out)
		out.write('>\n')
		for c in self.children:
			c.gen(out)
		out.write('</div>\n')


	def show_last(self):
		if self.online():
			self.send({
				"type": "show-last",
				"id": self.get_id(),
				"dir": 1
			})

	def show_child(self, child):
		if self.online():
			self.send({
				"type": "show-child",
				"id": self.get_id(),
				"child": child.get_id(),
				"dir": 1
			})


# Spring component
SPRING_MODEL = Model()

class Spring(Component):
	"""Invisible component taking as much place as possible.
	One parameter of hexpand or vexpand has to be defined else the
	component won't occupy any place."""

	def __init__(self, hexpand = False, vexpand = False, weight = 1):
		Component.__init__(self, SPRING_MODEL)
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
	overflow: auto;
}

.layered-child {
	display: flex;
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
		self.add_class("layered-parent")
		self.current = -1
		for child in self.get_children():
			self.decorate_child(child)
		if self.children != []:
			self.set_layer(0)

	def on_show(self):
		if self.current >= 0:
			self.get_children()[self.current].on_show()

	def on_hide(self):
		if self.current >= 0:
			self.get_children()[self.current].on_hide()

	def set_layer(self, num):
		"""Set the current layer."""
		if num == self.current:
			return
		if self.current >= 0:
			self.children[self.current].add_class("layered-inactive")
			self.children[self.current].remove_class("layered-active")
			self.children[self.current].on_hide()
		self.current = num
		if self.current >= 0:
			self.children[self.current].remove_class("layered-inactive")
			self.children[self.current].add_class("layered-active")
			self.children[self.current].on_show()

	def map_child(self, child):
		super().map_child(child)
		if child.expands_horizontal():
			child.remove_class(self.NOT_EXPAND)
			child.add_class(self.EXPAND)
		else:
			child.remove_class(self.EXPAND)
			child.add_class(self.NOT_EXPAND)
		if child.expands_vertical:
			child.add_class(self.ANTI_EXPAND)
		else:
			child.remove_class(self.ANTI_EXPAND)

	def decorate_child(self, child):
		child.add_class("layered-child")
		child.add_class("layered-inactive")

	def insert(self, child, i=-1):
		super().insert(child, i)
		self.decorate_child(child)

	def remove(self, i):
		Group.remove(self, i)
		if self.current >= i:
			self.current = -1

	def gen(self, out):
		out.write('<div ')
		self.gen_attrs(out)
		out.write('>\n')
		for c in self.children:
			c.gen(out)
		out.write('</div>\n')


class HSpace(Component):
	"""Passive object inserting an horizontal space."""

	MODEL = Model("hspace")

	def __init__(self, size="1em"):
		Component.__init__(self, model=HSpace.MODEL)
		if isinstance(size, int):
			size = f"{size}px"
		self.set_style("min-width", size)

	def gen(self, out):
		out.write("<span ")
		self.gen_attrs(out)
		out.write("></span>")

