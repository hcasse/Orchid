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

from functools import partial
from orchid import *

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

	def make_title(self, title):
		"""Generate the title from a component or from a string title."""
		if not isinstance(title, Component):
			title = Label(title)
		title.add_class("dialog-title")
		return title

	def make_message(self, message):
		"""Transform message to be displayed in dialog."""
		return Label(message.replace("\n", "<br>"))


def default_answer(dialog, answer):
	pass


class Answer(Base):
	"""Answer dialog: provides information to the user and wait
	for its answer."""

	def __init__(self, page, message, buttons = ["Okay"], title = None, on_close = default_answer):
		"""Build the dialog displaying the given message optionally with a title.
		It displays the given list of button (may be Orchid button or simple strings).
		The on_close is function is called when the dialog is close and takes as
		parameter (dialog, answer) with answer the index of the clicked answer button (starting from 0)."""
		content = []

		# process title
		if title != None:
			self.title = self.make_title(title)
			content.append(self.title)

		# add message
		if not isinstance(message, Component):
			message = Label(message)
		message.add_class("dialog-text")
		content.append(message)
		self.message = message

		# prepare buttons
		buts = [Spring(hexpand=True)]
		n = 0
		for but in buttons:
			if not isinstance(but, Component):
				but = Button(label = but)
			but.old_on_click = but.on_click
			but.on_click = partial(self.select, but, n)
			buts.append(but)
			buts.append(Spring(hexpand=True))
			n = n + 1
		self.buttons = HGroup(buts)
		self.buttons.add_class("dialog-buttons")
		content.append(self.buttons)

		# initialize the parent
		Base.__init__(self, page, VGroup(content))
		self.on_close = on_close
		self.add_class("dialog-answer")

	def select(self, but, i):
		self.hide()
		but.old_on_click()
		self.on_close(self, i)

MESSAGES = {
	"warning": "basic/warning.svg",
	"error": "basic/error.svg",
	"info": "basic/info.svg"
}

class Message(Base):
	"""Display a dialog with a message. Dialog display can
	be customized with a type.

	The type may "warning", "error", "info".

	In addition, the callback on_close is called when the dialog is closed."""

	def __init__(self, page, message, title=None, type=None, on_close=lambda: None):
		content = []
		if title != None:
			content.append(self.make_title(title))
		message = self.make_message(message)
		message.add_class("dialog-text")
		if type != None and type in MESSAGES:
			icon = Label(AssetImage(MESSAGES[type], width=32))
			icon.add_class("dialog-icon")
			content.append(HGroup([
				icon,
				message
			]))
		else:
			content.append(message)
		buttons = HGroup([
			Spring(hexpand=True),
			Button("Ok", on_click=self.close)
		])
		buttons.add_class("dialog-buttons")
		content.append(buttons)
		Base.__init__(self, page, VGroup(content))
		if type != None and type in MESSAGES:
			self.add_class(type)
		self.on_close = on_close
		self.add_class("dialog-message")

	def close(self):
		self.hide()
		self.on_close()




