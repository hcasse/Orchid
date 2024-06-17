"""Button class."""

from orchid.base import *
import orchid.image
from orchid.mind import AbstractAction, EnableObserver, Var, BOOL_TYPE, EnumType
from orchid.label import Label
from orchid.field import LabelledField


class ButtonAction(AbstractAction):
	"""Default action built from button configuration."""

	def __init__(self, enabled, on_click, **args):
		AbstractAction.__init__(self, **args)
		self.enabled = enabled
		self.on_click = on_click

	def is_enabled(self):
		return self.enabled

	def perform(self, console):
		if self.on_click is not None:
			self.on_click()


class AbstractButton(Component, EnableObserver):
	"""Abstract class for buttons supporting tooltip, enabling/disablong,
	etc."""

	def __init__(self, model, enabled=True, help=None, action=None):
		Component.__init__(self, model)
		if action is not None:
			self.action = action
		else:
			self.action = ButtonAction(
				enabled,
				None,
				help=help
			)

	def finalize(self, page):
		Component.finalize(self, page)
		self.action.set_context(self)

	def show(self):
		self.action.add_observer(self)
		if not self.action.is_enabled():
			self.set_attr("disabled", None)

	def hide(self):
		self.action.remove_observer(self)

	def enable(self):
		self.remove_attr("disabled")

	def disable(self):
		self.set_attr("disabled", None)

	def is_enabled(self):
		return self.action.is_enabled(self)


BUTTON_MODEL = Model("button-model")

class Button(AbstractButton):
	"""Represents a simple button that can represented by a label
	or by an image. on_click function is called when the button is
	clicked."""

	def __init__(self,
		label = None,
		image = None,
		on_click = None,
		enabled = True,
		help = None,
		action = None,
		model = BUTTON_MODEL
	):
		"""The parameters are the following:
		* label - text displayed on the button,
		* image - displayed on the button,
		* on_click - function called when the button is clicked (no parameter).
		* enabled - enable/disable the button,
		* action - orchid.mind action to use,
		* help - plain text displayed to get help from the button (usually )"""
		if isinstance(label, AbstractAction):
			AbstractButton.__init__(self, model, action=label)
		elif action is not None:
			AbstractButton.__init__(self, model, action=action)
		else:
			AbstractButton.__init__(self, model, action=ButtonAction(
				enabled,
				on_click,
				label=label,
				icon=image,
				help=help
			))
		if self.action.label is None:
			self.label = None
		else:
			self.label = Label(self.action.label)
		if self.action.help is not None:
			self.set_attr("title", self.action.help)

	def finalize(self, page):
		AbstractButton.finalize(self, page)
		if self.action.icon != None:
			self.action.icon.finalize(page)
		if self.label is not None:
			self.label.finalize(page)

	def gen(self, out):
		out.write('<button')
		self.gen_attrs(out)
		out.write(' onclick="ui_onclick(\'%s\');">' % self.get_id())
		if self.action.icon is not None:
			self.action.icon.gen(out, self.parent.get_context())
		if self.label is not None:
			self.label.gen(out)
		out.write('</button>')
		out.write('\n')

	def receive(self, m, h):
		if m["action"] == "click":
			if self.action.is_enabled():
				self.action.perform(None)
		else:
			Component.receive(self, m, h)

	def on_click(self):
		"""Called when a click is performed."""
		pass


CHECK_BOX_MODEL = Model("check-box",
	script=
"""
function check_box_on_change(id, event) {
	const comp = document.getElementById(id);
	if(comp.checked)
		ui_send({id: id, action: 'check'});
	else
		ui_send({id: id, action: 'uncheck'});
}

function check_box_set(args) {
	const comp = document.getElementById(args.id);
	comp.checked = args.checked;
}
"""
)

class CheckBox(Component, LabelledField):
	"""Implements a check box representing a boolean value."""

	def __init__(self, label="", value=False, enabled=True, help=None, var=None):
		Component.__init__(self, CHECK_BOX_MODEL)
		if var is not None:
			self.var = var
			assert var.get_type() == BOOL_TYPE
		else:
			self.var = Var(value, label=label, help=help)
		self.set_value(value)
		self.set_attr("onchange",
			"check_box_on_change('%s', event);" % self.get_id())
		self.enabled = True
		self.set_enabled(enabled)

	def show(self):
		self.var.add_observer(self)
		self.updating = True

	def hide(self):
		self.varr.remove_observer(self)

	def update_remote(self):
		self.call("check_box_set",
			{"id": self.get_id(), "checked": value})

	def record_var(self, value):
		self.updating = True
		self.var.set(value)
		self.updating = False

	def set_value(self, value):
		"""Change the value of the checkbox."""
		if value != ~self.var:
			self.record_var(value)
			self.update_remote()

	def get_value(self):
		"""Get the value of the checkbox."""
		return ~self.var

	def update(self, subject):
		if not self.updating:
			self.update_remote()

	def gen_label(self, out):
		if self.var.label is not None:
			out.write('<label for="%s">' % self.get_id())
			out.write(self.var.label)
			out.write('</label>')

	def gen_field(self, out, with_label=True):
		out.write('<div class="checkbox"><input type="checkbox" name="%s"' % self.get_id())
		self.gen_attrs(out)
		out.write('>')
		if with_label:
			self.gen_label(out)
		out.write('</div>')

	def gen(self, out):
		self.gen_field(out)

	def receive(self, msg, handler):
		action = msg['action']
		if action == 'check':
			self.record_var(True)
		elif action == 'uncheck':
			self.record_var(False)
		else:
			AbstractButton.receive(self, msg, handler)

	def enable(self):
		self.remove_attr("disabled")

	def disable(self):
		self.set_attr("disabled", None)

	def is_enabled(self):
		return self.enabled

	def set_enabled(self, enabled):
		if self.enabled != enabled:
			self.enabled = enabled
			if enabled:
				self.enable()
			else:
				self.disable()


RADIO_BUTTON_MODEL = Model("radio-button",
	script =
"""
function radio_button_on_change(id, event) {
	ui_send({id: id, action: "choose", choice: event.target.value});
}

function radio_button_set(args) {
	const comp = document.getElementById(args.id);
	comp.checked = true;
}
"""
)

class RadioButton(Component, LabelledField):
	"""List of exclusive buttons."""

	def __init__(self, options, choice=0, label=None, help=None, horizontal=False, var=None):
		Component.__init__(self, RADIO_BUTTON_MODEL)
		if var is not None:
			assert isinstance(var.get_type(), EnumType)
			self.var = var
		else:
			t = EnumType(options)
			self.var = Var(choice, t,
				  label=label,
				  help=help)
		self.options = self.var.get_type().get_values()
		assert 0 <= choice and choice < len(self.options)
		self.horizontal = horizontal

	def get_option_id(self, n):
		return "%s-%d" % (self.get_id(), n)

	def show(self):
		self.var.add_observer(self)
		self.updating = False

	def hide(self):
		self.var.remove_observer(self)

	def record_var(self, value):
		assert 0 <= n and n < (self.options)
		self.updating = True
		self.var.set(n)
		self.updating = False

	def set_choice(self, n):
		"""Set the current choice with n in [0, number of options-1]."""
		if ~self.var != n:
			self.record_var(n)

	def get_choice(self):
		"""Get the current choosen option. Return is in [0, number of options-1]."""
		return ~self.var

	def update_remote(self):
		self.call("radio_button_set", {"id": self.get_option_id(self.get_choice())})

	def gen_label(self, out):
		if self.var.label is not None:
			out.write('<label>')
			out.write(self.var.label)
			out.write('</label>')

	def gen_field(self, out, with_label=True):
		out.write('<div onchange="radio_button_on_change(\'%s\', event);">' % self.get_id())
		for i in range(0, len(self.options)):
			if i != 0 and not self.horizontal:
				out.write('<br/>')
			id = self.get_option_id(i)
			out.write('<input type="radio" id="%s" name="%s" value="%d"' % (id, self.get_id(), i))
			if i == ~self.var:
				out.write(' checked')
			out.write('>')
			out.write('<label for="%s">%s</label>' % (id,  self.options[i]))
		out.write("</div>")

	def gen(self, out):
		self.gen_field(out)

	def receive(self, msg, handler):
		action = msg['action']
		if action == 'choose':
			self.record_var(int(msg['choice']))
		else:
			Component.receive(self, msg, handler)

	def update(self):
		if not self.updating:
			self.update_remote()
