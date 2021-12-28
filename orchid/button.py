"""Button class."""

from orchid.base import *

class ButtonModel(Model):

	def gen_script(self, out):
		out.write("""
		function button_click(id) {
			ui_send({id: id, action: "click"});
		}
""")

BUTTON_MODEL = ButtonModel()

class Button(Component):

	def __init__(self, label, on_click = None, enabled = True):
		Component.__init__(self, BUTTON_MODEL)
		self.label = label
		if on_click != None:
			self.on_click = on_click
		self.enabled = enabled

	def gen(self, out):
		out.write('<a class="%s"' % self.get_class())
		out.write(' onclick="button_click(\'%s\');">' % self.get_id())
		out.write(self.label)
		out.write('</a>\n')

	def receive(self, m, h):
		if m["action"] == "click":
			if self.enabled:
				h.log_message("click!")
				self.on_click()
		else:
			Component.receive(self, m, h)

	def on_click(self):
		"""Called when a click is performed."""
		pass

	def get_class(self):
		if self.enabled:
			return "button"
		else:
			return "button-disabled"

	def enable(self, enabled = True):
		"""Enable/disable the button."""
		if self.enabled != enabled:
			self.enabled = enabled
			self.set_class(self.get_class())
