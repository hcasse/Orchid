"""Field components."""

import re
from orchid.base import *

FIELD_MODEL = Model(
	"abstract-field-model",
	script = """
function field_change(id, value) {
	ui_send({id: id, action: "change", value: value});
}
"""
)


class Field(Component):
	"""Represents a field where a user can enter a value. The field can then
	be obtained by the application. The following parameters are available
	for the construction:
	* label - to be displayed in front of field.
	* init - initial value.
	* size - field size in characters.
	* validate - validate the raw string content and return the value. Return None else.
	* weight - weight of the field in the horizontal display.
	* place_holder - palce holder text.
	* read_only - field read-only (mainly used to display information).
	* help - help message displayed as tooltip.

	Convenient validating functions: is_valid_natural(), is_valid_re()."""

	def __init__(self,
		label = None,
		init = "",
		size = None,
		validate = lambda x: x,
		weight = None,
		place_holder = None,
		read_only = False,
		help = None,
		convert = lambda x: x
	):
		Component.__init__(self, FIELD_MODEL)
		self.label = label
		self.size = size
		self.valid = True
		self.validate = validate
		self.place_holder = place_holder
		if weight == None:
			if size != None:
				weight = (size, 0)
			else:
				weight = (1, 0)
		self.weight = weight
		self.read_only = read_only
		self.add_class("field")
		self.help = help
		self.convert = convert
		self.content = None
		self.valid = None
		self.check(init)

	def get_content(self):
		"""Get the content of the field."""
		if self.valid:
			return self.content
		else:
			return None

	def gen_custom(self, out):
		self.gen_attr(out, "type", "text")

	def gen(self, out):
		out.write("<div ")
		self.gen_attrs(out)
		out.write(">")
		if self.label != None:
			out.write('<label for="%s-field">%s</label>' % (self.get_id(), self.label))
		out.write('<input id="%s-field"' % self.get_id())
		self.gen_attr(out, "value", self.content)
		self.gen_attr(out, "oninput", 'field_change("%s", this.value);' % self.get_id())
		if self.size != None:
			self.gen_attr(out, "size", self.size)
		if self.place_holder is not None:
			self.gen_attr(out, "placeholder", self.place_holder)
		if self.read_only:
			self.gen_attr(out, "readonly")
		if self.help is not None:
			self.gen_attr(out, "title", self.help)
		self.gen_custom(out)
		self.gen_attrs(out)
		out.write('/>')
		out.write("</div>")

	def set_validity(self, valid):
		if self.valid != valid:
			self.valid = valid
			if valid:
				self.remove_class("invalid")
				self.add_class("valid")
			else:
				self.remove_class("valid")
				self.add_class("invalid")

	def check(self, content):
		content = self.validate(content)
		if content == None:
			self.set_validity(False)
		else:
			if self.content != content:
				print("DEBUG: content =", content)
				self.content = content
				self.update_observers()
			self.set_validity(True)

	def receive(self, m, h):
		if m["action"] == "change":
			content = m["value"]
			self.check(content)
		else:
			Component.receive(self, m, h)


class ColorField(Field):
	"""Field to edit color."""

	def __init__(self, init="#ff0000", **args):
		Field.__init__(self, init=init, **args)

	def gen_custom(self, out):
		self.gen_attr(out, "type", "color")


class DateField(Field):
	"""Field to edit a date."""

	def __init__(self, **args):
		Field.__init__(self, **args)

	def gen_custom(self, out):
		self.gen_attr(out, "type", "date")


class TimeField(Field):
	"""Field to edit time."""

	def __init__(self, **args):
		Field.__init__(self, **args)

	def gen_custom(self, out):
		self.gen_attr(out, "type", "time")


class DateTimeField(Field):
	"""Field to edit a date and time."""

	def __init__(self, **args):
		Field.__init__(self, **args)

	def gen_custom(self, out):
		self.gen_attr(out, "type", "datetime-local")


class PasswordField(Field):
	"""Field to edit a password."""

	def __init__(self, **args):
		Field.__init__(self, **args)

	def gen_custom(self, out):
		self.gen_attr(out, "type", "password")


class EmailField(Field):
	"""Field to edit an email."""

	def __init__(self, **args):
		Field.__init__(self, **args)

	def gen_custom(self, out):
		self.gen_attr(out, "type", "email")


class RangeField(Field):
	"""Field to edit an email."""

	def __init__(self, min, max, **args):
		Field.__init__(self, **args)
		self.min = min
		self.max = max

	def gen_custom(self, out):
		self.gen_attr(out, "type", "range")
		self.gen_attr(out, "min", self.min)
		self.gen_attr(out, "max", self.max)


def as_natural(x):
	"""Test if the string is numeric."""
	return x if x.isnumeric() else None

def as_re(r):
	"""Generate a function to test if the content match RE."""
	cre = re.compile(r)
	def check(x):
		return x if cre.fullmatch(x) != None else None
	return check
