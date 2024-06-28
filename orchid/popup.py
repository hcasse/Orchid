#
#	This file is part of Orchid.
#
#    Orchid is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Lesser General Public License as
#	published by the Free Software Foundation, either version 3 of the
#	License, or (at your option) any later version.
#
#	Orchid is distributed in the hope that it will be useful, but
#	WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#	GNU Lesser General Public License for more details.
#
#	You should have received a copy of the GNU Lesser General Public
#	License along with Orchid. If not, see <https://www.gnu.org/licenses/>.
#

"""This module manage popups: menus."""

from orchid.base import ICON_MENU, Model, CONTEXT_MENU, ALIGN_LEFT
from orchid.group import VGroup
from orchid.button import Button
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

	def __init__(self, items, align=ALIGN_LEFT):
		"""Build the menu with the items (that are usually buttons).
		align can be set to one of orchid.base.ALIGN_XXX constant
		(default ALIGN_LEFT)."""
		VGroup.__init__(self, items, align=align, model=MENU_MODEL)
		self.add_class("dropdown-content")
		self.add_class("menu")
		self.set_style('display', 'none')
		self.shown = False

	def is_shown(self):
		"""Test if the menu is shown."""
		return self.shown

	def display(self, comp, pos = BELOW):
		"""Display the popup menu at the given position relatively to
		the given component."""
		pass

	def get_context(self):
		return CONTEXT_MENU

	def receive(self, msg, handler):
		if msg['action'] == 'hide':
			self.hide_menu()
		else:
			VGroup.receive(self, msg, handler)

	def get_onclick(self):
		"""Get the on-click code."""
		return f"popup_menu_top_click('{self.get_id()}');"

	def show(self):
		pass

	def hide(self):
		pass

	def show_menu(self, ref, index = None):
		"""Show the menu."""
		if self.shown:
			return
		VGroup.show(self)
		code = self.get_onclick()
		onclick = self.page.get_attr("onclick", "")
		if code not in onclick:
			self.page.set_attr("onclick", code + onclick)
		if index is None:
			self.call("popup_menu_show", {
				"id": self.get_id(),
				"ref": ref.get_id()
			})
		else:
			self.call("popup_menu_show_child", {
				"id": self.get_id(),
				"ref": ref.get_id(),
				"index": index
			})
		self.shown = True

	def hide_menu(self):
		"""Hide the menu."""
		if not self.shown:
			return
		code = self.get_onclick()
		onclick = self.page.get_attr("onclick")
		try:
			p = onclick.index(code)
			self.page.set_attr("onclick", onclick[:p] + onclick[p+len(code):])
		except ValueError:
			pass
		self.call("popup_menu_hide", {"id": self.get_id()})
		VGroup.hide(self)
		self.shown = False


class MenuButton(Button):
	"""Button that is able to display a menu."""

	def __init__(self, menu, label = None, image = None, enabled = True):
		if image is None:
			image = orchid.image.Icon(ICON_MENU)
		Button.__init__(self,
			label=label,
			image=image,
			enabled=enabled,
			on_click=self.on_click)
		self.menu = menu

	def finalize(self, page):
		Button.finalize(self, page)
		self.menu.finalize(page)

	def gen(self, out):
		out.write("<div class='dropdown'>")
		Button.gen(self, out)
		self.menu.gen(out)
		out.write("</div>")

	def on_click(self):
		if not self.menu.is_shown():
			self.show_menu()

	def show_menu(self):
		"""Show the current menu."""
		self.menu.show_menu(self)

	def hide_menu(self):
		self.menu.hide_menu()
