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

"""Module providing dialogs to Orchid."""

# https://css-tricks.com/some-hands-on-with-the-html-dialog-element/

from orchid.base import Component, Model

MODEL = Model(
	name = "orchid.dialog.Base",
	script = """
function dialog_show(args) {
	const dialog = window.document.getElementById(args.id);
	dialog.showModal();
}

function dialog_hide(args) {
	const dialog = window.document.getElementById(args.id);
	dialog.close();
}
"""
)

class Base(Component):

	def __init__(self, page, main, model = MODEL):
		Component.__init__(self, model)
		self.main = main
		main.parent = self
		page.add_hidden(self)

	def finalize(self, page):
		Component.finalize(self, page)
		self.main.finalize(page)

	def gen(self, out):
		out.write('<dialog')
		self.gen_attrs(out)
		out.write('>')
		self.main.gen(out)
		out.write('</dialog>')

	def show(self):
		self.call("dialog_show", {"id": self.get_id()})

	def hide(self):
		self.call("dialog_hide", {"id": self.get_id()})
