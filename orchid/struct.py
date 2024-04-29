"""Component for a structured view."""

from orchid.base import Model, CONTEXT_HEADERBAR, CONTEXT_TOOLBAR
from orchid.label import Label
from orchid.group import HGroup, Spring, HGROUP_MODEL

# Header component
HEADER_MODEL = Model("hgroupo-model", parent=HGROUP_MODEL)

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
