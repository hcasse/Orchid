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
		self.add_class("dropdown-content")
		self.add_class("menu")
		self.set_style('display', 'none')
		#self.set_attr("onshow", "popup_onresize(this);")

	def display(self, comp, pos = BELOW):
		"""Display the popup menu at the given position relatively to
		the given component."""
		pass

	def get_context(self):
		return CONTEXT_MENU

	def show(self):
		"""Show the menu."""
		self.get_page().show_popup(self, "flex")

	def hide(self):
		"""Hide the menu."""
		self.get_page().hide_popup()

	def isShown(self):
		"""Test if the menu is shown or not."""
		return self.get_page().current_popup == self


class MenuButton(Button):
	"""Button that is able to display a menu."""

	def __init__(self, menu, label = None, image = None, enabled = True, pos = DIR_SOUTH_WEST):
		if image == None:
			image = orchid.image.Icon(orchid.image.ICON_MENU)
		Button.__init__(self,
			label=label,
			image=image,
			enabled=enabled,
			on_click=self.on_click)
		self.menu = menu
		self.pos = pos

	def finalize(self, page):
		page.collect_rec(self.menu)

	def gen(self, out):
		out.write("<div class='dropdown'>")
		Button.gen(self, out)
		self.menu.gen(out)
		out.write("</div>")

	def on_click(self):
		if self.menu.isShown():
			self.hide_menu()
		else:
			self.show_menu()

	def show_menu(self):
		"""Show the current menu."""
		self.menu.show()

	def hide_menu(self):
		"""Hide the menu."""
		self.menu.hide()
