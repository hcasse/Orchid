"""Button class."""

from orchid.base import *
import orchid.image as image

# AbstractButton component
class AbstractButtonModel(Model):

	def gen_script(self, out):
		out.write("""
		function button_click(id) {
			ui_send({id: id, action: "click"});
		}
""")

ABSTRACT_BUTTON_MODEL = AbstractButtonModel()

class AbstractButton(Component):

	def __init__(self, model, on_click = None, enabled = True):
		Component.__init__(self, model)
		if on_click != None:
			self.on_click = on_click
		self.enabled = enabled
		self.add_class(self.get_enabled_class())

	def gen_display(self, out):
		""""Called to generate the content of the button."""
		pass

	def get_enabled_class(self):
		"""Called to get the display class of the button."""
		return None

	def gen(self, out):
		out.write('<a')
		self.gen_attrs(out)
		out.write(' onclick="button_click(\'%s\');">' % self.get_id())
		self.gen_display(out)
		out.write('</a>')
		out.write('\n')

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

	def enable(self, enabled = True):
		"""Enable/disable the button."""
		if self.enabled != enabled:
			self.remove_class(self.get_enabled_class())
			self.enabled = enabled
			self.add_class(self.get_enabled_class())


# Button model
BUTTON_MODEL = Model(ABSTRACT_BUTTON_MODEL)

class Button(AbstractButton):

	def __init__(self, label, on_click = None, enabled = True):
		AbstractButton.__init__(self, BUTTON_MODEL, on_click, enabled)
		self.label = label

	def gen_display(self, out):
		out.write(self.label)

	def get_enabled_class(self):
		if self.enabled:
			return "button"
		else:
			return "button-disabled"


# ToolButton component
TOOL_BUTTON_MODEL = Model(ABSTRACT_BUTTON_MODEL)

class ToolButton(AbstractButton):

	def __init__(self, image, on_click = None, enabled = True):
		AbstractButton.__init__(self, TOOL_BUTTON_MODEL, on_click, enabled)
		self.image = image

	def get_add_models(self):
		return [self.image.get_model()]

	def gen_display(self, out):
		self.image.gen(out, self.parent.get_context())

	def get_enabled_class(self):
		if self.enabled:
			return "tool-button"
		else:
			return "tool-button-disabled"
