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

"""Field components."""

import re
from orchid.base import Component, Model, ALIGN_JUSTIFY
from orchid.util import Buffer
from orchid.group import VGroup, Group
from orchid.label import Label
from orchid.mind import Var, EnumType


class LabelledField:
	"""A field with separated label and input."""

	def gen_field(self, out, with_label=True):
		"""Generate the field itself with or without label."""
		pass

	def gen_label(self, out):
		"""Generate the label only."""
		pass


FIELD_MODEL = Model(
	"abstract-field-model",
	script = """
function field_change(id, value) {
	ui_send({id: id, action: "change", value: value});
}
"""
)


class Field(Component, LabelledField):
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
		init = None,
		size = None,
		validate = lambda x: x,
		weight = None,
		place_holder = None,
		read_only = False,
		help = None,
		convert = lambda x: x,
		enabled = True,
		model = FIELD_MODEL,
		var = None
	):
		Component.__init__(self, model)

		# var construction
		if isinstance(label, Var):
			self.var = label
		elif var is None:
			self.var = self.make_var(init,
				label=label,
				help=help)
		else:
			self.var = var

		# other attributes
		self.size = size
		self.convert = convert
		self.validate = validate
		self.place_holder = place_holder
		if weight is None:
			if size is not None:
				weight = (size, 0)
			else:
				weight = (1, 0)
		self.weight = weight
		self.read_only = read_only

		# internal state
		self.valid = None
		self.add_class("field")
		self.check(self.var.get())
		self.enabled = None
		self.set_enabled(enabled)
		self.updating = False

	def make_var(self, init, **args):
		"""Build a variable for the current field."""
		if init is None:
			return Var("", **args)
		else:
			return Var(init)

	def get_var(self):
		"""Get the variable containing the value of the field."""
		return self.var

	def enable(self):
		"""Enable the field."""
		self.enabled = True
		self.remove_attr("disabled")

	def disable(self):
		"""Disable the field."""
		self.enabled = False
		self.set_attr("disabled")

	def get_value(self):
		"""Get the content of the field."""
		if self.valid:
			return self.var.get()
		else:
			return None

	def record_var(self, value):
		self.updating = True
		self.var.set(value)
		self.updating = False

	def set_value(self, val):
		"""Set the current value."""
		self.record_var(val)
		self.update_remote()
		self.set_validity(self.validate(str(val)) is not None)

	def on_show(self):
		self.var.add_observer(self)
		self.updating = False

	def on_hide(self):
		self.var.remove_observer(self)

	def update_remote(self):
		if self.online():
			self.get_page().set_direct_attr(f"{self.get_id()}-field", "value", str(~self.var))

	def update(self, subject):
		if not self.updating:
			self.update_remote()
			self.set_validity(self.validate(str(~self.var)) is not None)

	def gen_custom(self, out):
		"""Called to generate custom attributes (used for specialization).
		Default implementation selects text type."""
		self.gen_attr(out, "type", "text")

	def gen_custom_content(self, out):
		"""Called to generate custom content (just after input).
		Default implementation does nothing."""
		pass

	def gen_input_attrs(self, out):
		"""Generate attributes that goes inside <input> tag."""
		if self.size is not None:
			self.gen_attr(out, "size", self.size)
		if self.place_holder is not None:
			self.gen_attr(out, "placeholder", self.place_holder)
		if self.read_only:
			self.gen_attr(out, "readonly")
		if self.var.help is not None:
			self.gen_attr(out, "title", self.var.help)
		self.gen_custom(out)
		val = self.get_value()
		if val is not None:
			self.gen_attr(out, "value", val)
		self.gen_attr(out, "oninput", f'field_change("{self.get_id()}", this.value);')

	def gen_label(self, out):
		"""Generate label for the field."""
		if self.var.label is not None:
			out.write(f'<label for="{self.get_id()}-field">{self.var.label}</label>')

	def gen_input(self, out):
		"""Generate the <input> tag."""
		out.write(f'<input id="{self.get_id()}-field"')
		self.gen_input_attrs(out)
		out.write('>')
		self.gen_custom_content(out)
		out.write('</input>')

	def gen_field(self, out, with_label=True):
		out.write("<div ")
		self.gen_attrs(out)
		out.write(">")
		if with_label:
			self.gen_label(out)
		self.gen_input(out)
		out.write("</div>")

	def gen(self, out):
		self.gen_field(out)

	def set_validity(self, valid):
		"""Mark the field as valid or invalid."""
		if self.valid != valid:
			self.valid = valid
			if valid:
				self.remove_class("invalid")
				self.add_class("valid")
			else:
				self.remove_class("valid")
				self.add_class("invalid")

	def is_valid(self):
		"""Test if the field is valid or invalid."""
		return self.valid

	def check(self, content):
		"""Check the current value."""
		if content is None:
			self.set_validity(True)
			return
		content = self.validate(content)
		if content is None:
			self.set_validity(False)
		else:
			if self.var.get() != content:
				self.record_var(content)
			self.set_validity(True)

	def receive(self, msg, handler):
		if msg["action"] == "change":
			content = msg["value"]
			self.check(content)
		else:
			Component.receive(self, msg, handler)


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
		self.min = min
		self.max = max
		Field.__init__(self, validate=as_natural, **args)

	def make_var(self, init, **args):
		if init is None:
			return Var(None, type=int, **args)
		else:
			return Var(init, **args)

	def gen_custom(self, out):
		self.gen_attr(out, "type", "range")
		self.gen_attr(out, "min", self.min)
		self.gen_attr(out, "max", self.max)


SELECT_MODEL = Model(
		"select-model",
		script = """
function select_choose(m) {
	let comp = document.getElementById(m.idx);
	comp.selectedIndex = m.id;
}

function select_on_choose(elt) {
	ui_send({id: elt.id, action: "choose", idx: elt.selectedIndex });
}
"""
	)

class Select(Component, LabelledField):
	"""Field to select from a list."""

	def __init__(self, choices, choice=0, label=None, enabled=True, size=None, help=None, var=None):
		Component.__init__(self, SELECT_MODEL)
		if var is not None:
			assert isinstance(var.type, EnumType)
			assert 0 <= choice < len(var.type.values)
			self.var = var
		else:
			assert 0 <= choice < len(choices)
			self.var = Var(choice, EnumType(choices),
				label=label,
				help=help
			)
		self.choices = self.var.get_type().get_values()
		self.enabled = None
		self.set_enabled(enabled)
		self.size = size
		self.set_attr("onchange", 'select_on_choose(this);')
		self.updating = False

	def on_show(self):
		self.var.add_observer(self)
		self.updating = False

	def on_hide(self):
		self.var.remove_observer(self)

	def set_enabled(self, enabled=True):
		"""Set the enabled state."""
		if enabled != self.enabled:
			if enabled:
				self.enable()
			else:
				self.disable()

	def enable(self):
		"""Enable the selector."""
		self.remove_attr("disabled")
		self.enabled = True

	def disable(self):
		"""Disable the selector."""
		self.set_attr("disabled")
		self.enabled = True

	def record_var(self, value):
		self.updating = True
		self.var.set(value)
		self.updating = False

	def update_remote(self):
		self.call("select_choose", {"id": self.get_id(), "idx": self.get_choice()})

	def get_choice(self):
		"""Get the current choice number."""
		return ~self.var

	def set_choice(self, choice):
		"""Set the current choice."""
		if ~self.var != choice:
			self.record_var(choice)
			self.update_remote()

	def receive(self, msg, handler):
		if msg["action"] == "choose":
			self.record_var(msg["idx"])
		else:
			Component.receive(self, msg, handler)

	def update(self, subject):
		if not self.updating:
			self.update_remote()

	def gen_label(self, out):
		if self.var.label is not None:
			out.write(f'<label for="{self.get_id()}">{self.var.label}</label>')

	def gen_field(self, out, with_label=True):
		out.write("<div>")
		if with_label:
			self.gen_label(out)
		out.write('<select')
		self.gen_attrs(out)
		out.write(f' name="{self.get_id()}"')
		if self.var.help is not None:
			self.gen_attr(out, "title", self.var.help)
		out.write('>')
		self.gen_options(out)
		out.write('</select>')
		out.write("</div>")

	def gen(self, out):
		self.gen_field(out)

	def gen_option(self, i, out):
		out.write(f'<option value="{i}" \
			{" selected" if i == ~self.var else ""}>{self.choices[i]}</option>')

	def gen_options(self, out):
		for i in range(0, len(self.choices)):
			self.gen_option(i, out)

	def set_choices(self, choices):
		"""Change the set of choices."""
		self.choices = choices
		self.var.set(0)
		if self.online():
			buf = Buffer()
			self.gen_options(buf)
			self.set_content(str(buf))

	def add_choice(self, choice):
		"""Add a choice to the list of choices."""
		self.choices.append(choice)
		if self.online():
			buf = Buffer()
			self.gen_option(len(self.choices)-1, buf)
			self.append_content(str(buf))

	def remove_choice(self, i):
		"""Remove the choice matching the given number."""
		del self.choices[i]
		if self.online():
			self.remove_content(i)


PROPOSAL_MODEL = Model(
	"field.proposal-model",
	parent = FIELD_MODEL,

	style = """
.proposal-field {
	display: inline-block;
}

.proposal-field div {
	display: inline-block;
}

.proposal-selected {
	background-color: var(--myyellow);
}

.proposal-popup {
	display: none;
	position: absolute;
	z-index: 1;
	width: max-content;
}
""",

	script = """
var proposal_id = null;
var proposal_pos = null;
var proposal_props = null;
var proposal_input = null;

function proposal_hide() {
	if(proposal_pos != null) {
		proposal_pos.classList.remove("proposal-selected");
		proposal_pos = null;
	}
	if(proposal_props != null) {
		proposal_props.style.display = "none";
		proposal_props = null;
	}
}

function proposal_show(m) {
	proposal_id = m.input;
	proposal_props = document.getElementById(m.props);
	proposal_props.style.display = "flex";
	proposal_input = document.getElementById(`${proposal_id}-field`);
	proposal_pos = null;
}

function proposal_on_key_down(evt) {
	//console.log("Key = " + evt.key);
	if(evt.key == "ArrowDown") {
		if(proposal_pos != null) {
			proposal_pos.classList.remove("proposal-selected");
			proposal_pos = proposal_pos.nextElementSibling;
		}
		if(proposal_pos == null)
			proposal_pos = proposal_props.firstElementChild;
		proposal_pos.classList.add("proposal-selected");
		event.stopPropagation();
		event.preventDefault();
	}
	else if(evt.key == "ArrowUp") {
		if(proposal_pos != null) {
			proposal_pos.classList.remove("proposal-selected");
			proposal_pos = proposal_pos.previousElementSibling;
		}
		if(proposal_pos == null)
			proposal_pos = proposal_props.lastElementChild;
		proposal_pos.classList.add("proposal-selected");
		event.stopPropagation();
		event.preventDefault();
	}
	else if(evt.key == "Enter" && proposal_pos != null) {
		let value = proposal_pos.innerHTML;
		proposal_input.value = value;
		proposal_hide();
		ui_send({id: proposal_id, action: "select", value: value});
	}
	else if(evt.key == "Escape") {
		proposal_hide();
		event.stopPropagation();
		event.preventDefault();
	}
}
"""
)

class ProposalField(Field):
	"""Like a field but also with the possibility to provides, with a menu,
	proposals to the user to shorten the typing effort. The propose function
	takes as input the current content of the field and returns a list of
	proposals as a list of strings."""

	def __init__(self, propose = lambda x: [], **args):
		Field.__init__(self, model=PROPOSAL_MODEL, **args)
		self.propose = propose
		self.prev = []
		self.group = VGroup([], align=ALIGN_JUSTIFY)
		self.group.add_class("proposal-popup")
		self.group.set_style("display", "none")
		self.add_class("proposal-field")

	def gen_field(self, out, with_label=True):
		out.write("<div ")
		self.gen_attrs(out)
		out.write(">")
		if with_label:
			self.gen_label(out)
		out.write("<div>")
		self.gen_input(out)
		self.group.gen(out)
		out.write("</div></div>")

	def gen_input_attrs(self, out):
		Field.gen_input_attrs(self, out)
		out.write(' onfocusout="proposal_hide();"')

	def finalize(self, page):
		Field.finalize(self, page)
		self.group.finalize(page)
		self.set_attr("onkeydown", 'proposal_on_key_down(event);')

	def show_props(self):
		self.call("proposal_show",
			{"props": self.group.get_id(), "input": self.get_id()})

	def hide_props(self):
		self.call("proposal_hide")

	def receive(self, msg, handler):
		if msg["action"] == "change":
			value = msg["value"]
			if value == "":
				self.hide_props()
				self.prev = []
			else:
				props = self.propose(value)
				if props != self.prev:
					self.prev = props
					if props == [] or (len(props) == 1 and props[0] == value):
						self.hide_props()
					else:
						labs = [Label(prop) for prop in props]
						self.group.replace_children(labs)
						self.show_props()
		elif msg["action"] == "select":
			self.prev = []
			self.check(msg["value"])
		else:
			Field.receive(self, msg, handler)


def as_natural(x):
	"""Test if the string is numeric."""
	try:
		return int(x)
	except ValueError:
		return None

def as_re(r):
	"""Generate a function to test if the content match RE."""
	cre = re.compile(r)
	def check(x):
		return x if cre.fullmatch(x) is not None else None
	return check


FORM_MODEL = Model(
	"form",
	style = """
table.form tr td:first-child {
	text-align: right;
	padding-right: 1em;
	vertical-align: top;
}
"""
)

class Form(Group):
	"""A form is a list of fields with labels aligned for good looking.
	Its component extends LabelledField."""

	def __init__(self, fields):
		Group.__init__(self, FORM_MODEL, fields)
		self.add_class("form")

	def gen(self, out):
		out.write("<table")
		self.gen_attrs(out)
		out.write(">")
		for field in self.get_children():
			out.write("<tr><td>")
			field.gen_label(out)
			out.write("</td><td>")
			field.gen_field(out, False)
			out.write("</td></tr>")
		out.write("</table>")
