"""Label component."""

from orchid.base import Component, Model, Displayable
from orchid.displayable import Text
from orchid.util import ProxyInterface, STANDARD_INTERFACE, Buffer

LABEL_MODEL = Model()


class Label(Component):
	"""Component displaying the given content that may be plain or an instance of Displayable."""

	def __init__(self, text):
		Component.__init__(self, LABEL_MODEL)
		self.text = None
		self.set_text(text)
		self.add_class("label")

	def finalize(self, page):
		Component.finalize(self, page)
		self.text.finalize(page)

	def gen(self, out):
		out.write('<div')
		self.gen_attrs(out)
		out.write('>')
		self.gen_content(out)
		out.write('</div>\n')

	def gen_content(self, out):
		self.text.gen(out)

	def set_text(self, text):
		if isinstance(text, Displayable):
			self.text = text
		else:
			self.text = Text.make(text)
		if self.online():
			self.text.finalize(self.get_page())
			buf = Buffer()
			self.gen_content(buf)
			self.set_content(str(buf))


BANNER_MODEL = Model()


class Banner(Component):
	"""Display an HTML text that occupies the whole avaiable width,
	like a banner."""

	def __init__(self, text):
		Component.__init__(self, BANNER_MODEL)
		self.add_class("banner")
		self.text = text

	def expands_horizontal(self):
		return True

	def gen(self, out):
		out.write('<div')
		self.gen_attrs(out)
		out.write('>')
		out.write(self.text)
		out.write('</div>\n')


class MessageLabel(Label, ProxyInterface):
	"""This label is dedicated to display user messages. It implements Interface
	and can also display errors from a list of predicates."""

	def __init__(self, preds=None, content="", interface=STANDARD_INTERFACE):
		Label.__init__(self, content)
		ProxyInterface.__init__(self, interface)
		self.add_class("message-label")
		self.last_cls = None
		if preds is None:
			self.preds = []
		else:
			self.preds = preds

	def on_show(self):
		Label.on_show(self)
		for pred in self.preds:
			pred.add_error_observer(self)

	def on_hide(self):
		Label.on_hide(self)
		for pred in self.preds:
			pred.remove_error_observer(self)

	def clear_class(self):
		if self.last_cls is not None:
			self.remove_class(self.last_cls)

	def replace_class(self, cls):
		self.clear_class()
		self.add_class(cls)
		self.last_cls = cls

	def clear_message(self):
		if self.text:
			self.clear_class()
			self.last_cls = None
			self.set_text("")

	def set_message(self, style, message):
		if self.text != message:
			self.set_text(message)
			self.replace_class(style)

	def show_error(self, message):
		self.set_message("error-text", message)

	def show_warning(self, message):
		self.set_message("warn-text", message)

	def show_info(self, message):
		self.set_message("info-text", message)
