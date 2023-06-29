"""This module manage popups: menus and dialons."""

from orchid import *
from orchid import group
import orchid.image

BELOW = 0
RIGHT = 1
ABOVE = 2
LEFT = 3

class MenuModel(group.VGroupModel):
	pass

MENU_MODEL = MenuModel()

class Menu(VGroup):
	"""Menu made of a list of components verticaly placed."""

	def __init__(self, items):
		VGroup.__init__(self, items, model=MENU_MODEL)
		self.add_class("modal-content")

	def display(self, comp, pos = BELOW):
		"""Display the popup menu at the given position relatively to
		the given component."""
		pass

	def get_context(self):
		return CONTEXT_MENU


class MenuButton(Button):
	"""Button that is able to display a menu."""

	def __init__(self, menu, label = None, image = None, enabled = True):
		if image == None:
			image = orchid.image.Icon(orchid.image.ICON_MENU)
		Button.__init__(self,
			label=label,
			image=image,
			enabled=enabled,
			on_click=self.show_menu)
		self.menu = menu

	def finalize(self, page):
		page.add_popup(self.menu)

	def show_menu(self):
		"""Show the current menu."""
		self.call("popup_show", {"id": self.menu.get_id()})

	def hide_menu(self):
		"""Hide the menu."""
		self.call("popup_hide", {})

