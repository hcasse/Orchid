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

"""Defines a transparent group that is able to capture keyboard events."""

from orchid.base import ParentComponent, Model
from orchid.mind import AbstractAction

class Key:
	ALT = 0x01
	CONTROL = 0x02
	META = 0x04
	SHIFT = 0x08

	ENTER = "Enter"
	TAB = "Tab"
	SPACE = " "
	ARROW_DOWN = "ArrowDown"
	ARROW_LEFT = "ArrowLeft"
	ARROW_RIGHT = "ArrowRight"
	ARROW_UP = "ArrowUp"
	END = "End"
	HOME = "Home"
	PAGE_DOWN = "PageDown"
	PAGE_UP = "PageUp"
	BACK_SPACE = "BackSpace"
	CLEAR = "Clear"
	COPY = "Copy"
	CUT = "Cut"
	DELETE = "Delete"
	INSERT = "Insert"
	PASTE = "Paste"
	REDO = "Redo"
	UNDO = "Undo"

	F1 = "F1"
	F2 = "F2"
	F3 = "F3"
	F4 = "F4"
	F5 = "F5"
	F6 = "F6"
	F7 = "F7"
	F8 = "F8"
	F9 = "F9"
	F10 = "F10"
	F11 = "F11"
	F12 = "F12"

	def __init__(self, key, action, mask=0):
		"""Build a key combination that can trigger an action. The action
		may be a callable or mind.AbstractAction that is only called
		if it is enabled. The key is one of constant Key.XXX.

		mask must be en ORed combination of Key.ALT, Key.CONTROL, Key.META
		and Key.SHIFT."""

		self.key = key
		self.action = action
		self.mask = mask

	def trigger(self, component):
		"""Called to trigger the action associarted with the key."""
		if callable(self.action):
			self.action()
		elif self.action.is_enabled():
			self.action.perform(component.get_interface)



class KeyGroup(ParentComponent):
	"""A component that is capable of handling events."""

	MODEL = Model(
		"key-group",
		script="""
function keygroup_handle(element, event, keys) {

	// prepare mask
	let mask = 0;
	if(event.altKey)
		mask |= 0x01;
	if(event.ctrlKey)
		mask |= 0x02;
	if(event.metaKey)
		mask |= 0x04;
	if(event.shiftKey)
		mask |= 0x08;

	// look for matching
	for(const key of keys)
		if(event.key == key.key && mask == key.mask)
			ui_send({id: element.id, action: key.action});
}
"""
	)

	def __init__(self, content, keys):
		"""Build a key group where content is a sub-component where to apply
		the key detection and keys is a sequence of Key objects, the keys to
		handle."""
		ParentComponent.__init__(self, KeyGroup.MODEL)
		self.content = content
		content.parent = self
		self.keys = list(keys)
		map = ",".join(f"{{mask: {k.mask}, key: '{k.key}', action: {i} }}" \
			for (i, k) in enumerate(self.keys))
		self.set_attr("onkeypress", f"keygroup_handle(this, event, [{map}]);")

	def finalize(self, page):
		ParentComponent.finalize(self, page)
		self.content.finalize(page)

	def on_show(self):
		self.content.on_show()

	def on_hide(self):
		self.content.on_hide()

	def gen(self, out):
		out.write("<div ")
		self.gen_attrs(out)
		out.write(">")
		self.content.gen(out)
		out.write("</div>")

	def receive(self, msg, handler):
		action = msg["action"]
		if isinstance(action, int):
			self.keys[action].trigger(self)
		else:
			ParentComponent.receive(self, msg, handler)






