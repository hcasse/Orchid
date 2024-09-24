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

"""ShiftSelector allows to place horizontally several components and to
navigate using buttons when the components are too wide."""

from orchid import HGroup, Button, Model, Icon, IconType

class ShiftSelector(HGroup):

	MODEL = Model("shift-selector",
		script = """
function shift_selector_check(msg) {
	let top = document.getElementById(msg.id);
	let left = top.children[0]
	let right = top.children[1]
	let content = top.children[2]
	if(content.clientWidth < content.scrollWidth) {
		left.style.display = "flex";
		right.style.display = "flex";
	}
	else {
		left.style.display = "none";
		right.style.display = "none";
	}
}

function shift_selector_right(msg) {
	let top = document.getElementById(msg.id);
	let content = top.children[2]
	let width = content.getBoundingClientRect().width;
	for(var i = 0; i < content.children.length; i++) {
		let cur = content.children[i];
		let rect = cur.getBoundingClientRect();
		if(rect.left >= width) {
			cur.scrollIntoView();
			return;
		}
	}
}

function shift_selector_left(msg) {
	let top = document.getElementById(msg.id);
	let content = top.children[2]
	let left = content.getBoundingClientRect().left;
	var prev = null;
	for(var i = 0; i < content.children.length; i++) {
		let cur = content.children[i];
		let rect = cur.getBoundingClientRect();
		if(rect.left >= left) {
			if(prev != null)
				prev.scrollIntoView();
			return;
		}
		prev = cur;
	}
}
""",
		style = """
.ss_content {
	overflow-x: auto !important;
	flex-shrink: 1 !important;
}
.ss_content button {
	white-space: nowrap;
}
"""
	)

	def __init__(self, content = None):
		if content is None:
			content = []
		self.left_but = Button(
			Icon(IconType.ARROW_LEFT),
			on_click=self.move_left)
		self.right_but = Button(
			Icon(IconType.ARROW_RIGHT),
			on_click=self.move_right)
		self.content = HGroup(content)
		self.content.add_class("ss_content")
		HGroup.__init__(self, [self.left_but, self.right_but, self.content],
			model=self.MODEL)

	def update_arrows(self):
		self.call("shift_selector_check", {
			"id": self.get_id(),
			"gid": self.content.get_id()
		})

	def gen(self, out):
		HGroup.gen(self, out)
		self.update_arrows()
		if self.get_children():
			self.content.show_last()

	def insert(self, child, i=-1):
		self.content.insert(child, i)
		self.update_arrows()
		self.content.show_child(child)

	def remove(self, i):
		self.content.remove(i)
		self.update_arrows()

	def remove_children(self):
		self.content.remove_children()
		self.update_arrows()

	def get_children(self):
		return self.content.get_children()

	def replace_children(self, children):
		self.content.replace_children(children)
		self.update_arrows()

	def expands_horizontal(self):
		return True

	def move_left(self):
		self.call("shift_selector_left", { "id": self.get_id() })

	def move_right(self):
		self.call("shift_selector_right", { "id": self.get_id() })





