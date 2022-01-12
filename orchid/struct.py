"""Component for a structured view."""

from orchid.base import Model
from orchid.label import Label
from orchid.group import HGroup, Spring, HGROUP_MODEL

# Header component
HEADER_MODEL = Model(HGROUP_MODEL)

class Header(HGroup):

	def __init__(self, title, tools = [], model = HEADER_MODEL):
		self.label  = Label(title)
		HGroup.__init__(self,
			comps = [self.label, Spring(hexpand = True)] + tools,
			model = HEADER_MODEL)
		self.label.add_class("header-label")
		self.add_class("header")
