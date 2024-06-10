"""Component for a structured view."""

from orchid.base import Model, CONTEXT_HEADERBAR, CONTEXT_TOOLBAR
from orchid.label import Label
from orchid.group import HGroup, Spring, HGROUP_MODEL, VGroup, Group

# Header component
HEADER_MODEL = Model("header-model", parent=HGROUP_MODEL)

class Header(HGroup):

	def __init__(self, title, tools = [], model = HEADER_MODEL):
		self.label  = Label(title)
		HGroup.__init__(self,
			comps = [self.label, Spring(hexpand = True)] + tools,
			model = HEADER_MODEL)
		self.label.add_class("header-label")
		self.add_class("header")

	def get_context(self):
		return CONTEXT_HEADERBAR


class ToolBar(HGroup):

	def __init__(self, tools = []):
		HGroup.__init__(self, tools)
		self.add_class("toolbar")

	def get_context(self):
		return CONTEXT_TOOLBAR

class MessageContainer(VGroup):
	"""A message container add a banner at the top or at the bottom of another
	content that is displayed when required to inform the user about an error
	or for other reasons. The displayed requires less action to the user than
	an error dialog."""

	def __init__(self, content, down=False):
		self.msg_comp = VGroup([])
		self.clear()
		if not isinstance(content, Group):
			content = VGroup([content])
		self.content = content
		if down:
			comps = [content, self.msg_comp]
		else:
			comps = [self.msg_comp, content]
		VGroup.__init__(self, comps)
		#self.msg_comp.add_class("message")
		self.msg_comp.set_style("row-gap", "0")

	def set_top_class(self, cls):
		self.content.add_class(cls)

	def clear(self):
		"""Hide the message."""
		self.msg_comp.remove_children()

	def hide(self, id):
		"""Hide a displayed message."""
		self.msg_comp.remove(id)

	def show(self, msg, cls):
		"""Show the message colored with class cls."""
		label = Label(msg)
		label.add_class(cls)
		label.add_class("message")
		self.msg_comp.insert(label)
		return label

	def error(self, msg):
		"""Show an error and return display identifier."""
		return self.show(msg, "error-back")

	def warn(self, msg):
		"""Show a warning and return display identifier."""
		return self.show(msg, "warn-back")

	def info(self, msg):
		"""Show an information and return display identifier.."""
		return self.show(msg, "info-back")
