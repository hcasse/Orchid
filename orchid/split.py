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

from orchid import Model
from orchid.group import Group

MODEL = Model(
	"""split-pane""",

	script="""
var split_current = null;
var split_vert = null;

function split_on_mouse_move(evt) {
	let parent = split_current.parentElement;
	let rect = parent.getBoundingClientRect();
	//console.log("moved: pinter=" + evt.clientX + "," + evt.clientY + "); parent=(" + rect.left + "," + rect.top + "," + rect.width + "," + rect.height + ")" );
	let ratio;
	if(!split_vert) {
		if(evt.clientX < rect.left)
			ratio = 0;
		else if(evt.clientX >= rect.left + rect.width)
			ratio = 100;
		else
			ratio = (evt.clientX - rect.left) * 100 / rect.width;
	}
	else {
		if(evt.clientY < rect.top)
			ratio = 0;
		else if(evt.clientY >= rect.top + rect.height)
			ratio = 100;
		else
			ratio = (evt.clientY - rect.top) * 100 / rect.height;
	}
	//console.log("DEBUG: ratio=" + ratio + ", offset=" + (evt.clientX - rect.left));
	parent.firstChild.style.flexGrow = ratio;
	parent.lastChild.style.flexGrow = 100 - ratio;
}

function split_on_mouse_up(evt) {
	//console.log("up!")
	document.onmousemove = null;
	document.onmouseup = null;
	let parent = split_current.parentElement;
	ui_send({id: parent.id, action: "move", pos: parent.firstChild.style.flexGrow });
}

function split_on_mouse_down(elt, evt, vert) {
	if(evt.button != 0)
		return;
	split_current = elt;
	split_vert = vert;
	//console.log("elt=" + elt.id);
	document.onmousemove = split_on_mouse_move;
	document.onmouseup = split_on_mouse_up;
}

""",

	style="""
.split-pane {
	display: flex;
}

.split-horz-part {
	min-width: 0;
	flex-basis: 0;
}

.split-horz-part {
	min-height: 0;
	flex-basis: 0;
}

.split-horz {
	flex-direction: row;
}

.split-vert {
	flex-direction: column;
}

.split-horz-knob {
	cursor: col-resize;
	flex-grow: 0;
	flex-shrink: 0;
	margin: 0 0 0 auto;
	wdith: 0.2rem;
}

.split-vert-knob {
	cursor: col-resize;
	flex-grow: 0;
	flex-shrink: 0;
	margin: 0 0 0 auto;
	wdith: 0.2rem;
}

"""
)

class SplitPane(Group):
	"""A double-pane group with a separator that allows to resize
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
				self.pos = h1 * 100 // (h1 + h2)
			else:
				self.pos = v1 * 100 // (v1 + v2)
		if not vert:
			self.add_class("split-horz")
			pane1.add_class("split-horz-part")
			pane2.add_class("split-horz-part")
		else:
			self.add_class("split-vert")
			pane1.add_class("split-vert-part")
			pane2.add_class("split-vert-part")
		pane1.set_style("flex-grow", self.pos)
		pane2.set_style("flex-grow", 100 - self.pos)

	def get_pane1(self):
		return self.get_children()[0]

	def get_pane2(self):
		return self.get_children()[1]

	def expands_horizontal(self):
		return not self.vert or Group.expands_horizontal(self)

	def expands_vertical(self):
		return self.vert or Group.expands_vertical(self)

	def gen(self, out):
		out.write("<div")
		self.gen_attrs(out)
		out.write(">")
		self.get_pane1().gen(out)
		out.write(f'<div id="{self.get_id()}-knob" \
			class="split-{"horz" if not self.vert else "vert"}-knob" \
			onmousedown="split_on_mouse_down(this, event, \
			{"false" if not self.vert else "true"});">&nbsp;</div>')
		self.get_pane2().gen(out)
		out.write("</div>")

	def receive(self, msg, handler):
		if msg["action"] == "move":
			self.pos = msg["pos"]
		else:
			Group.receive(self, msg, handler)

