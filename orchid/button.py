"""Button class."""

from orchid.base import *
import orchid.image as image

# AbstractButton component
class ButtonModel(Model):
	pass

BUTTON_MODEL = ButtonModel()

class Button(Component):
	"""Represents a simple button that can represented by a label
	or by an image. on_click function is called when the button is
	clicked."""

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
		self.enabled = True
		self.set_enabled(enabled)

	def get_add_models(self):
		if self.image != None:
			return [self.image.model]
		else:
			return []

	def gen(self, out):
		out.write('<button')
		self.gen_attrs(out)
		out.write(' onclick="ui_send({id: \'%s\', action: \'click\'});">' % self.get_id())
		if self.image != None:
			self.image.gen(out, self.parent.get_context())
		if self.label != None:
			out.write(self.label)
		out.write('</button>')
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

	def enable(self):
		if not self.enabled:
			self.enabled = True
			self.remove_attr("disabled")

	def disable(self):
		if self.enabled:
			self.enabled = False
			self.set_attr("disabled", True)
