"""Button class."""

from orchid.base import Component, Model
from orchid.mind import AbstractAction, EnableObserver, Var, BOOL_TYPE, EnumType
from orchid.label import Label
from orchid.field import LabelledField
from orchid.image import Image


class ButtonAction(AbstractAction):
	"""Default action built from button configuration."""

	def __init__(self, enabled, on_click, **args):
		AbstractAction.__init__(self, **args)
		self.enabled = enabled
		self.on_click = on_click

	def is_enabled(self):
		return self.enabled

	def perform(self, interface):
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

	def on_show(self):
		self.action.add_enable_observer(self)
		if not self.action.is_enabled():
			self.set_attr("disabled", None)

	def on_hide(self):
		self.action.remove_enable_observer(self)

	def enable(self):
		self.remove_attr("disabled")

	def disable(self):
		self.set_attr("disabled", None)

	def is_enabled(self):
		return self.action.is_enabled(self)

	def get_action(self):
		"""Get the action of the button."""
		return self.action

	def test_enabled(self):
		if not self.action.is_enabled():
			self.set_attr("disabled", None)
		else:
			self.remove_attr("disabled")

	def set_action(self, action):
		"""Change the action of the button."""
		if self.online():
			self.action.remove_enable_observer()
		self.action = action
		if self.online():
			self.action.add_enable_observer(self)
			self.test_enabled()


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
			if isinstance(label, Image):
				image = label
				label = None
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
		self.set_attr("onclick", f'ui_onclick("{self.get_id()}");')


	def finalize(self, page):
		AbstractButton.finalize(self, page)
		if self.action.icon is not None:
			self.action.icon.finalize(page)
		if self.label is not None:
			self.label.finalize(page)

	def gen(self, out):
		out.write('<button')
		self.gen_attrs(out)
		out.write('>')
		context = self.parent.get_context()
		if self.action.icon is not None:
			self.action.icon.gen_in_context(out, context)
		if self.label is not None:
			self.label.gen(out)
		out.write('</button>')
		out.write('\n')

	def click(self):
		"""Called when the button is clicked."""
		if self.action.is_enabled():
			self.action.perform(None)

	def receive(self, msg, handler):
		if msg["action"] == "click":
			self.click()
		else:
			Component.receive(self, msg, handler)

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
			f"check_box_on_change('{self.get_id()}', event);")
		self.enabled = True
		self.set_enabled(enabled)
		self.updating = False

	def on_show(self):
		self.var.add_observer(self)
		self.updating = True

	def on_hide(self):
		self.var.remove_observer(self)

	def update_remote(self):
		self.call("check_box_set",
			{"id": self.get_id(), "checked": ~self.var})

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
			out.write(f'<label for="{self.get_id()}">')
			out.write(self.var.label)
			out.write('</label>')

	def gen_field(self, out, with_label=True):
		out.write(f'<div class="checkbox"><input type="checkbox" name="{self.get_id()}"')
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

	def set_enabled(self, enabled = True):
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

function radio_button_set(msg) {
	const comp = document.getElementById(msg.id);
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
		assert 0 <= choice < len(self.options)
		self.horizontal = horizontal
		self.updating = False

	def get_option_id(self, n):
		return f"{self.get_id()}-{n}"

	def on_show(self):
		self.var.add_observer(self)
		self.updating = False

	def on_hide(self):
		self.var.remove_observer(self)

	def record_var(self, n):
		assert 0 <= n < len(self.options)
		self.updating = True
		self.var.set(n)
		self.updating = False

	def set_choice(self, n):
		"""Set the current choice with n in [0, number of options-1]."""
		if ~self.var != n:
			self.var.set(n)
			self.update_remote()

	def get_choice(self):
		"""Get the current choosen option. Return is in [0, number of options-1]."""
		return ~self.var

	def update_remote(self):
		if self.online():
			self.call("radio_button_set", {"id": self.get_option_id(self.get_choice())})

	def gen_label(self, out):
		if self.var.label is not None:
			out.write('<label>')
			out.write(self.var.label)
			out.write('</label>')

	def gen_field(self, out, with_label=True):
		out.write(f'<form onchange="radio_button_on_change(\'{self.get_id()}\', event);">')
		for i, _ in enumerate(self.options):
			if i != 0 and not self.horizontal:
				out.write('<br/>')
			id = self.get_option_id(i)
			out.write(f'<input type="radio" id="{id}" \
				name="{self.get_id()}-radio" value="{i}"')
			if i == ~self.var:
				out.write(' checked')
			out.write('>')
			out.write(f'<label for="{id}">{self.options[i]}</label>')
		out.write("</form>")

	def gen(self, out):
		self.gen_field(out)

	def receive(self, msg, handler):
		action = msg['action']
		if action == 'choose':
			new = int(msg['choice'])
			self.record_var(new)
			#if self.online():
			#	self.remove_attr('checked', id=self.get_option_id(old))
			#	self.set_attr('checked', id=self.get_option_id(new))
		else:
			Component.receive(self, msg, handler)

	def update(self, subject):
		if not self.updating:
			self.update_remote()
