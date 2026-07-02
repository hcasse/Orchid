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

"""SplitPane implementation."""

from orchid.base import Model
from orchid.group import Group


MODEL = Model(
	"""split-pane""",
	script_paths=["split.js"],
	style_paths=["split.css"]
)

class Pane(Group):
	"""A double-side group with a separator that allows to resize
	the panes. The displyed panes are pane1 and pane2. vert is False
	for horizontal pane, True for vertical.

	pos is the position of the separation (in %). If not defined, it
	is deduced from the weight of panes."""

	def __init__(self, pane1, pane2, vert=False, pos=None, model=MODEL):
		Group.__init__(self, model, [pane1, pane2])
		self.add_class("split-pane")
		self.vert = vert
		if pos is not None:
			self.pos = pos
		else:
			(h1, v1) = self.get_weight()
			(h2, v2) = self.get_weight()
			if not vert:
				if h1 + h2 == 0:
					self.pos = 50
				else:
					self.pos = h1 * 100 // (h1 + h2)
			else:
				if v1 + v2 == 0:
					self.pos = 50
				else:
					self.pos = v1 * 100 // (v1 + v2)
		if not vert:
			self.add_class("split-pane-horiz")
			pane1.add_class("split-part-horiz")
			pane2.add_class("split-part-horiz")
		else:
			self.add_class("split-pane-vert")
			pane1.add_class("split-part-vert")
			pane2.add_class("split-part-vert")

	def get_pane1(self):
		return self.get_children()[0]

	def get_pane2(self):
		return self.get_children()[1]

	def expands_horizontal(self):
		return not self.vert or Group.expands_horizontal(self)

	def expands_vertical(self):
		return self.vert or Group.expands_vertical(self)

	def gen(self, out):
		if self.vert:
			axis = "vert"
			but1 = "▲"
			but2 = "▼"
		else:
			axis = "horiz"
			but1 = "◀"
			but2 = "▶"
		out.write("<div")
		self.gen_attrs(out)
		out.write(">")
		self.get_pane1().gen(out)
		out.write(f'<div class="split-div-{axis}"><button>{but1}</button><span></span><button>{but2}</button></div>')
		self.get_pane2().gen(out)
		out.write(f"</div><script>split_init('{self.get_id()}', {self.pos}, {"true" if self.vert else "false"})</script>")

	def receive(self, msg, handler):
		if msg["action"] == "move":
			self.pos = msg["pos"]
		else:
			Group.receive(self, msg, handler)

