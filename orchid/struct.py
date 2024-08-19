"""Component for a structured view."""

from orchid.base import Model
from orchid.util import Context, MessageType, Align
from orchid.label import Label
from orchid.group import HGroup, Spring, HGROUP_MODEL, VGroup, Group

BACKS = {
	MessageType.ERROR: "error-back",
	MessageType.WARN: "warn-back",
	MessageType.INFO: "info-back"
}


# Header component
HEADER_MODEL = Model("header-model", parent=HGROUP_MODEL)

class Header(HGroup):

	def __init__(self, title, tools = None, model = HEADER_MODEL):
		if tools is None:
			tools = []
		self.label  = Label(title)
		HGroup.__init__(self,
			comps = [self.label, Spring(hexpand = True)] + tools,
			model = HEADER_MODEL)
		self.label.add_class("header-label")
		self.add_class("header")

	def get_context(self):
		return Context.HEADERBAR


class ToolBar(HGroup):
	"""Represent window-level toolbar."""

	def __init__(self, tools = None):
		if tools is None:
			tools = []
		HGroup.__init__(self, tools)
		self.add_class("toolbar")

	def get_context(self):
		return Context.TOOLBAR


class ButtonBar(HGroup):
	"""Represents window division toolbar."""

	def __init__(self, tools = None):
		if tools is None:
			tools = []
		HGroup.__init__(self, tools)
		self.add_class("buttonbar")

	def get_context(self):
		return Context.BUTTONBAR


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
		self.msg_comp.set_style("row-gap", "0")

	def set_top_class(self, cls):
		self.content.add_class(cls)

	def clear(self):
		"""Hide the message."""
		self.msg_comp.remove_children()

	def hide_message(self, id):
		"""Hide a displayed message."""
		self.msg_comp.remove(id)

	def show_message(self, msg, type=None):
		"""Show the message. type may be one of MessageType enumeration
		constant. """
		comps = []
		icon = self.get_page().get_theme().get_dialog_icon(type, 16)
		if icon is not None:
			comps.append(Label(icon))
		comps.append(Label(msg))
		group = HGroup(comps, align=Align.CENTER)
		try:
			group.add_class(BACKS[type])
		except KeyError:
			pass
		group.add_class("message")
		self.msg_comp.insert(group)
		return group

	def error(self, msg):
		"""Show an error and return display identifier."""
		return self.show_message(msg, MessageType.ERROR)

	def warn(self, msg):
		"""Show a warning and return display identifier."""
		return self.show_message(msg, MessageType.WARN)

	def info(self, msg):
		"""Show an information and return display identifier.."""
		return self.show_message(msg, MessageType.INFO)


class StatusBar(HGroup):

	MODEL = Model(
		"status-bar",
		parent = HGROUP_MODEL
	)

	def __init__(self, content, model=None):
		if model is None:
			model = self.MODEL
		HGroup.__init__(self, content, model=model)

	def get_context(self):
		return Context.STATUSBAR

	def expands_horizontal(self):
		return True
