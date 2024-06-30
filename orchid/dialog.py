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

from orchid.base import Model, Component, Plain, ALIGN_CENTER
from orchid.button import Button
from orchid.label import Label
from orchid.group import VGroup, HGroup, Spring
from orchid.image import AssetImage

MODEL = Model(
	name = "orchid.dialog.Base",
	script = """
var dialog_display = null;
function dialog_show(args) {
	const dialog = window.document.getElementById(args.id);
	dialog.showModal();
	dialog_display = dialog.style.display;
	dialog.style.display = "flex";
}

function dialog_hide(args) {
	const dialog = window.document.getElementById(args.id);
	dialog.style.display = dialog_display;
	dialog.close();
}
""",
	style = """
dialog {
	justify-content: stretch;
}
.dialog-flex {
	flex-grow: 1;
}
"""
)

class Base(Component):

	def __init__(self, page, main, title=None, no_pad=False, model=MODEL):
		Component.__init__(self, model)
		if not no_pad:
			main.add_class("dialog-content")
		if title is not None:
			main = VGroup([
				self.make_title(title),
				main
			])
		self.main = main
		main.parent = self
		main.add_class("dialog-flex")
		self.interface = None
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
		self.main.on_show()

	def hide(self):
		self.main.hide()
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

	def get_interface(self):
		if self.interface is None:
			return self.parent.get_interface()
		else:
			return self.interface

	def set_interface(self, interface):
		self.interface = interface


def default_answer(dialog, answer):
	pass


ANSWER_MODEL = Model(
	"dialog-answer-model",
	parent = MODEL,
	script = """
function dialog_answer_choose(id, n) {
	ui_send({ id: id, action: "choose", n: n });
}
"""
)


class Answer(Base):
	"""Answer dialog: provides information to the user and wait
	for its answer."""

	def __init__(self, page, message, buttons = None, title = None, on_close = default_answer):
		"""Build the dialog displaying the given message optionally with a title.
		It displays the given list of button (may be Orchid button or simple strings).
		The on_close is function is called when the dialog is close and takes as
		parameter (dialog, answer) with answer the index of the clicked answer button (starting from 0).

		If you want to provide a custom button, use the dialog on_click() function to close the dialog."""
		if buttons is None:
			buttons = ["Okay"]
		content = []

		# add message
		if not isinstance(message, Component):
			message = Label(message)
		message.add_class("dialog-text")
		content.append(message)
		self.message = message

		# prepare buttons
		buts = [Spring(hexpand=True)]
		n = 0
		self.buttons = []
		for but in buttons:
			if not isinstance(but, Component):
				but = Button(label = but)
			self.buttons.append(but)
			buts.append(but)
			buts.append(Spring(hexpand=True))
			n = n + 1
		self.button_bar = HGroup(buts)
		self.button_bar.add_class("dialog-buttons")
		content.append(self.button_bar)

		# initialize the parent
		Base.__init__(self, page, VGroup(content), title=title, model=ANSWER_MODEL)
		self.on_close = on_close
		self.add_class("dialog-answer")

		# capture button click
		for (n, button) in enumerate(self.buttons):
			button.set_attr('onclick', f'dialog_answer_choose("{self.get_id()}", {n});')

	def select(self, n):
		"""Called when a button number n is choosed/"""
		self.hide()
		self.on_close(self, n)
		self.buttons[n].click()

	def receive(self, msg, handler):
		if msg['action'] == 'choose':
			self.select(msg['n'])
		else:
			Base.receive(self, msg, handler)


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
		message = self.make_message(message)
		message.add_class("dialog-message-text")
		icon = page.get_theme().get_dialog_icon(type)
		if icon is not None:
			icon = Label(icon)
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
		Base.__init__(self, page, VGroup(content), title=title)
		if type is not None and type in MESSAGES:
			self.add_class(type)
		self.on_close = on_close
		self.add_class("dialog-message")

	def close(self):
		self.hide()
		self.on_close()


class About(Base):
	"""Dialog displaying information about the application."""

	def __init__(self, page):
		app = page.app
		all = []

		# prepare the icon if any
		if app.icon is not None:
			label = Label(AssetImage(app.icon, width=96))
			label.add_class("dialog-about-icon")
			all.append(label)

		# prepare the text
		text = []
		title = app.name
		if app.version is not None:
			title = f"{title} V{app.version}"
		if app.description is not None:
			text.append(Plain(app.description, in_tag="p"))
		if app.website is not None:
			text.append(Plain(f'<a href="{app.website}">{app.website}</a>', in_tag="p"))
		if app.license is not None:
			text.append(Plain(f"<b>License:</b> {app.license}", in_tag="p"))
		if app.copyright is not None:
			text.append(Plain(f"<i>{app.copyright}</i>", in_tag="center"))
		text = VGroup(text)
		text.add_class("dialog-text")
		all.append(text)

		# prepare buttons
		buttons = HGroup([
			Spring(hexpand=True),
			Button("Ok", on_click=self.hide)
		], align=ALIGN_CENTER)
		buttons.add_class("dialog-buttons")
		all.append(buttons)

		# build the dialog
		Base.__init__(self, page, VGroup(all), title=title)
		self.add_class("dialog-about")


