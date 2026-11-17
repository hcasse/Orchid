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

"""Classes for control and harness for finer interaction in the HTML page."""

from typing import Callable

from orchid.base import Model, Component, PLAIN_MODEL, Receiver, Message, \
	Page, Handler
from orchid.util import escape_attr, Out

class Control(Receiver):
	"""Base class of special controls that may be a added to a component."""
	CONTROL_CNT = 0

	def __init__(self):
		self.id = f"ctrl{self.CONTROL_CNT}"
		Control.CONTROL_CNT += 1

	def get_id(self) -> str:
		return self.id

	def get_model(self) -> Model:
		"""Get the model for the harness."""
		return PLAIN_MODEL

	def get_event_map(self, comp: Component) -> dict[str, str]:
		"""Called to generate code for the different events.
		Return a dictionrary matching event name (as in HTML element attribute)
		with JS code to execute."""
		return {}


class Harness:
	"""Harness is put on component to handle controls. It contains a collection
	if controls.

	Do not extend a component from this class as it may override some functions
	from Component class.

	Current implementation does not support adding control during online."""

	def __init__(self):
		self.controls = []

	def finalize_harness(self, page: Page) -> None:
		"""Should be call to let control decalre their models."""
		for control in self.controls:
			model = control.get_model()
			if model != PLAIN_MODEL:
				page.add_model(model)
			page.register_receiver(control)

	def add_control(self, control: Control) -> None:
		"""Add a control to the harness."""
		self.controls.append(control)

	def gen_harness_attrs(self, out: Out) -> None:
		"""Generate the attribute for the harness."""

		# prepare the map
		map: dict[str, str] = {}
		for control in self.controls:
			new_map = control.get_event_map(self)
			for (event, code) in new_map.items():
				if event in map:
					code = f"{map[event]} {code}"
				map[event] = code

		# generate the code
		for (event, code) in map.items():
			out.write(f' {event}={escape_attr(code)}')


class ClickNMove(Control, Receiver):
	"""Control that capture a mouse click, move and then release."""
	MODEL = Model("clicknmove-control-model", script_paths=["cnm.js"])

	def __init__(self,
		on_move: Callable[[int, int], None]
	):
		Control.__init__(self)
		self.on_move = on_move

	def get_model(self) -> Model:
		return self.MODEL

	def get_event_map(self, comp: Component) -> dict[str, str]:
		return {
			"onpointerdown": "orc_cnm_push(this, event);",
			"onpointermove": f"orc_cnm_move(this, event, '{self.get_id()}');",
			"onpointerup": "orc_cnm_release(this, event);",
			"onpointercancel": "orc_nm_cancel(this, event);",
		}

	def receive(self, msg: Message, handler: Handler) -> None:
		if msg["action"] == "move":
			self.on_move(msg["dx"], msg["dy"])


class MouseWheel(Control, Receiver):
	"""Control that capture wheel move."""
	MODEL = Model("mousewheel-control-model", script="""
function orc_mw_change(event, id) {
	event.preventDefault();
	//console.log("DEBUG: wheel: " + event.deltaX + ", " + event.deltaY);
	ui_send({id: id, action: "change", delta: event.deltaY});
}
	""")

	def __init__(self,
		on_change: Callable[[int], None]
	):
		Control.__init__(self)
		self.on_change = on_change

	def get_model(self) -> Model:
		return self.MODEL

	def get_event_map(self, comp: Component) -> dict[str, str]:
		return {
			"onwheel": f"orc_mw_change(event, '{self.get_id()}');",
		}

	def receive(self, msg: Message, handler: Handler) -> None:
		if msg["action"] == "change":
			self.on_change(msg["delta"])
