"""Button class."""

from orchid.base import *
import orchid.image
from orchid.mind import AbstractAction, EnableObserver
from orchid.label import Label


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
		return self.action.is_enabled()


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
		if action is not None:
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
		Component.finalize(self, page)
		if self.action.icon != None:
			self.action.icon.finalize(page)
		if self.label is not None:
			self.label.finalize(page)

	def gen(self, out):
		out.write('<button')
		self.gen_attrs(out)
		#if not self.is_enabled():
		#	out.write(" disabled")
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

class CheckBox(AbstractButton):
	"""Implements a check box representing a boolean value."""

	def __init__(self, label, value=False, enabled=True, help=None, on_change=lambda x: None):
		AbstractButton.__init__(self, CHECK_BOX_MODEL, enabled=enabled, help=help)
		self.label = label
		self.value = value
		self.value = False
		self.set_value(value)
		self.set_attr("onchange",
			"check_box_on_change('%s', event);" % self.get_id())
		self.on_change = on_change

	def set_value(self, value):
		"""Change the value of the checkbox."""
		if value != self.value:
			self.value = value
			self.call("check_box_set",
				{"id": self.get_id(), "checked": value})

	def get_value(self):
		"""Get the value of the checkbox."""
		return self.value

	def gen(self, out):
		out.write('<div class="checkbox"><input type="checkbox" name="%s"' % self.get_id())
		self.gen_attrs(out)
		out.write('><label for="%s">' % self.get_id())
		out.write(self.label)
		out.write('</label></div>')

	def receive(self, msg, handler):
		action = msg['action']
		if action == 'check':
			self.value = True
			self.on_change(self.value)
		elif action == 'uncheck':
			self.value = False
			self.on_change(self.value)
		else:
			AbstractButton.receive(self, msg, handler)


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

class RadioButton(Component):
	"""List of exclusive buttons."""

	def __init__(self, options, choice=0, help=None, on_change=lambda n: None, horizontal=False):
		Component.__init__(self, RADIO_BUTTON_MODEL)
		self.options = options
		self.choice = choice
		self.help = help
		self.on_change = on_change
		self.horizontal = horizontal

	def get_option_id(self, n):
		return "%s-%d" % (self.get_id(), n)

	def set_choice(self, n):
		"""Set the current choice with n in [0, number of options-1]."""
		if self.choice != n:
			self.choice = n
			self.call("radio_button_set", {"id": self.get_option_id(n)})

	def get_choice(self):
		"""Get the current choosen option. Return is in [0, number of options-1]."""
		return self.choice

	def gen(self, out):
		out.write('<div onchange="radio_button_on_change(\'%s\', event);">' % self.get_id())
		for i in range(0, len(self.options)):
			if i != 0 and not self.horizontal:
				out.write('<br/>')
			id = self.get_option_id(i)
			out.write('<input type="radio" id="%s" name="%s" value="%d"' % (id, self.get_id(), i))
			if i == self.choice:
				out.write(' checked')
			out.write('>')
			out.write('<label for="%s">%s</label>' % (id, self.options[i]))
		out.write("</div>")

	def receive(self, msg, handler):
		action = msg['action']
		if action == 'choose':
			self.choice = int(msg['choice'])
			self.on_change(self.choice)
		else:
			Component.receive(self, msg, handler)
