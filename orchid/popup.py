"""This module manage popups: menus and dialons."""

from orchid import *
from orchid import group
import orchid.image

BELOW = 0
RIGHT = 1
ABOVE = 2
LEFT = 3

MENU_MODEL = Model(
	script_paths = [ 'popup_menu.js']
)

class Menu(VGroup):
	"""Menu made of a list of components verticaly placed."""

	def __init__(self, items):
		VGroup.__init__(self, items, model=MENU_MODEL)
		self.add_class("dropdown-content")
		self.add_class("menu")
		self.set_style('display', 'none')

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
			on_click=self.on_click)
		self.menu = menu
		self.shown = False

	def finalize(self, page):
		Button.finalize(self, page)
		self.menu.finalize(page)

	def gen(self, out):
		out.write("<div class='dropdown'>")
		Button.gen(self, out)
		self.menu.gen(out)
		out.write("</div>")

	def on_click(self):
		if not self.shown:
			self.show_menu()

	def show_menu(self):
		"""Show the current menu."""
		self.call("popup_menu_show", {
			"id": self.menu.get_id(),
			"ref": self.get_id()
		})
		self.page.enable_modal(self)
		self.shown = True

	def on_modal_disable(self):
		self.call("popup_menu_hide", {"id": self.menu.get_id()})
		self.shown = False
