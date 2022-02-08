"""Button class."""

from orchid.base import *
import orchid.image as image

# AbstractButton component
class ButtonModel(Model):

	def gen_script(self, out):
		out.write("""
		function button_click(id) {
			ui_send({id: id, action: "click"});
		}
""")

BUTTON_MODEL = ButtonModel()

class Button(Component):

	def __init__(self,
		label = None,
		image = None,
		on_click = None,
		enabled = True
	):
		Component.__init__(self, BUTTON_MODEL)
		self.label = label
		self.image = image
		if on_click != None:
			self.on_click = on_click
		self.enabled = enabled
		self.add_class(self.get_enabled_class())

	def gen(self, out):
		out.write('<a')
		self.gen_attrs(out)
		out.write(' onclick="button_click(\'%s\');">' % self.get_id())
		if self.image != None:
			self.image.gen(out, self.parent.get_context())
		if self.label != None:
			out.write(self.label)
		out.write('</a>')
		out.write('\n')

	def receive(self, m, h):
		if m["action"] == "click":
			if self.enabled:
				#h.log_message("click!")
				self.on_click()
		else:
			Component.receive(self, m, h)

	def on_click(self):
		"""Called when a click is performed."""
		pass

	def get_enabled_class(self):
		if self.label != None:
			if self.enabled:
				return "button"
			else:
				return "button-disabled"
		else:
			if self.enabled:
				return "tool-button"
			else:
				return "tool-button-disabled"

	def enable(self, enabled = True):
		"""Enable/disable the button."""
		if self.enabled != enabled:
			self.remove_class(self.get_enabled_class())
			self.enabled = enabled
			self.add_class(self.get_enabled_class())
