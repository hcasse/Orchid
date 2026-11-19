"""Component for a structured view."""

from orchid.base import Model, Component, Page
from orchid.util import Context, MessageType, Align, Out
from orchid.label import Label
from orchid.group import HGroup, Spring, HGROUP_MODEL, VGroup, Group

BACKS = {
	MessageType.ERROR: "error-back",
	MessageType.WARN: "warn-back",
	MessageType.INFO: "info-back"
}


# Header component

class Header(HGroup):
	MODEL = Model("header-model", parent = HGROUP_MODEL)

	def __init__(self, title: str, tools: list[Component] = [], model = MODEL):
		self.label  = Label(title)
		HGroup.__init__(self,
			comps = [self.label, Spring(hexpand = True)] + tools,
			model = HEADER_MODEL)
		self.label.add_class("header-label")
		self.add_class("header")

	def get_context(self) -> Context:
		return Context.HEADERBAR


class ToolBar(HGroup):
	"""Represent window-level toolbar."""

	def __init__(self, tools: list[Component] = []):
		HGroup.__init__(self, list(tools))
		self.add_class("toolbar")

	def get_context(self) -> Context:
		return Context.TOOLBAR


class ButtonBar(HGroup):
	"""Represents window division toolbar."""

	def __init__(self, tools: list[Component] = []):
		HGroup.__init__(self, list(tools))
		self.add_class("buttonbar")

	def get_context(self) -> Context:
		return Context.BUTTONBAR


class MessageContainer(VGroup):
	"""A message container add a banner at the top or at the bottom of another
	content that is displayed when required to inform the user about an error
	or for other reasons. The displayed requires less action to the user than
	an error dialog."""

	def __init__(self, content: Component, down: bool = False):
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

	def set_top_class(self, cls: str) -> None:
		self.content.add_class(cls)

	def clear(self) -> None:
		"""Hide the message."""
		self.msg_comp.remove_children()

	def hide_message(self, id: str) -> None:
		"""Hide a displayed message."""
		self.msg_comp.remove(id)

	def show_message(self, msg: str, type: MessageType = MessageType.ERROR) -> Component:
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

	def error(self, msg: str) -> Component:
		"""Show an error and return display identifier."""
		return self.show_message(msg, MessageType.ERROR)

	def warn(self, msg: str) -> Component:
		"""Show a warning and return display identifier."""
		return self.show_message(msg, MessageType.WARN)

	def info(self, msg: str) -> Component:
		"""Show an information and return display identifier.."""
		return self.show_message(msg, MessageType.INFO)


class StatusBar(HGroup):
	"""Horizontal group to show a status bar."""

	MODEL = Model(
		"status-bar",
		parent = HGROUP_MODEL
	)

	def __init__(self, content: list[Component], model: Model = MODEL):
		if model is None:
			model = self.MODEL
		HGroup.__init__(self, content, model=model)
		self.add_class("status-bar")

	def get_context(self) -> Context:
		return Context.STATUSBAR

	def expands_horizontal(self) -> bool:
		return True


class Center(Component):
	"""Component displaying its content centered (occupying all space)."""
	MODEL = Model("center-model",
			style = """
.struct-center {
    display: flex;
    justify-content: center;
    align-items: center;
}
			""")

	def __init__(self, content: Component, model: Model = MODEL):
		Component.__init__(self, model)
		self.content = content
		self.add_class("struct-center")

	def expands_horizontal(self) -> bool:
		return True

	def expands_vertical(self) -> bool:
		return True

	def finalize(self, page: Page) -> None:
		Component.finalize(self, page)
		self.content.finalize(page)

	def gen(self, out: Out) -> None:
		out.write("<div ")
		self.gen_attrs(out)
		out.write(">")
		self.content.gen(out)
		out.write("</div>")

HEADER_MODEL = Header.MODEL

