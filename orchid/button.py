"""Button class."""

from orchid.base import *
import orchid.image


class AbstractButton(Component):
	"""Abstract class for buttons supporting tooltip, enabling/disablong,
	etc."""

	def __init__(self, model, enabled = True, help = None):
		Component.__init__(self, model)
		self.enabled = True
		self.set_enabled(enabled)
		self.help = help
		if help != None:
			self.set_attr("title", help)

	def enable(self):
		if not self.enabled:
			self.enabled = True
			self.remove_attr("disabled")

	def disable(self):
		if self.enabled:
			self.enabled = False
			self.set_attr("disabled", None)

		

BUTTON_MODEL = Model("button")

class Button(AbstractButton):
	"""Represents a simple button that can represented by a label
	or by an image. on_click function is called when the button is
	clicked."""

	def __init__(self,
		label = None,
		image = None,
		on_click = None,
		enabled = True,
		help = None
	):
		"""The parameters are the following:
		* label - text displayed on the button,
		* image - displayed on the button,
		* on_click - function called when the button is clicked (no parameter).
		* enabled - enable/disable the button,
		* help - plain text displayed to get help from the button (usually )"""
		AbstractButton.__init__(self, BUTTON_MODEL, enabled=enabled, help=help)
		self.label = label
		self.image = image
		if image == None and isinstance(label, orchid.image.Image):
			self.label = None
			self.image = label
		if on_click != None:
			self.on_click = on_click

	def finalize(self, page):
		Component.finalize(self, page)
		if self.image != None:
			self.image.finalize(page)

	def gen(self, out):
		out.write('<button')
		self.gen_attrs(out)
		out.write(' onclick="ui_onclick(\'%s\');">' % self.get_id())
		if self.image != None:
			self.image.gen(out, self.parent.get_context())
		if self.label != None:
			out.write(self.label)
		out.write('</button>')
		out.write('\n')

	def receive(self, m, h):
		if m["action"] == "click":
			if self.enabled:
				self.on_click()
		else:
			Component.receive(self, m, h)

	def on_click(self):
		"""Called when a click is performed."""
		pass


CHECK_BUTTON_MODEL = Model("check-button",
	script=
"""
function check_button_on_change(id, event) {
	const comp = document.getElementById(id);
	console.log("DEBUG: change " + id + " -> " + comp.checked);
	if(comp.checked)
		ui_send({id: id, action: 'check'});
	else
		ui_send({id: id, action: 'uncheck'});
}
"""
)

class CheckButton(AbstractButton):
	"""Implements a check button representing a boolean value."""

	def __init__(self, label, value=False, enabled=True, help=None, on_change=lambda x: None):
		AbstractButton.__init__(self, CHECK_BUTTON_MODEL, enabled=enabled, help=help)
		self.label = label
		self.value = value
		self.value = False
		self.set_value(value)
		self.set_attr("onchange",
			"check_button_on_change('%s', event);" % self.get_id())
		self.on_change = on_change

	def set_value(self, value):
		if value != self.value:
			if value:
				self.set_attr("checked")
			else:
				self.remove_attr("checked")
			self.value = value

	def gen(self, out):
		out.write('<div><input type="checkbox" name="%s"' % self.get_id())
		self.gen_attrs(out)
		out.write('><label for="%s">' % self.get_id())
		out.write(self.label)
		out.write('</label></div>')

	def receive(self, msg, handler):
		action = msg['action']
		if action == 'check':
			self.value = True
			self.on_change(self.value)
		elif action == 'uncheck':
			self.value = False
			self.on_change(self.value)
		else:
			AbstractButton.receive(self, msg, handler)
