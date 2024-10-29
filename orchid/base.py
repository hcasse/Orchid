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

"""Orchid base classes and definitions. """

import html
import importlib
import os.path
from threading import Thread
import time
from time import sleep

from orchid import server
from orchid.mind import Action
from orchid.util import Buffer, STANDARD_INTERFACE, Subject, Context
from orchid.displayable import Displayable

CLOSE_TIMEOUT=0.250


def write_nothing(page, out):
	"""Funcion writing nothing to out."""
	pass


class Key:
	ALT = 0x01
	CONTROL = 0x02
	META = 0x04
	SHIFT = 0x08

	ENTER = "Enter"
	TAB = "Tab"
	SPACE = " "
	ARROW_DOWN = "ArrowDown"
	ARROW_LEFT = "ArrowLeft"
	ARROW_RIGHT = "ArrowRight"
	ARROW_UP = "ArrowUp"
	END = "End"
	HOME = "Home"
	PAGE_DOWN = "PageDown"
	PAGE_UP = "PageUp"
	BACK_SPACE = "BackSpace"
	CLEAR = "Clear"
	COPY = "Copy"
	CUT = "Cut"
	DELETE = "Delete"
	INSERT = "Insert"
	PASTE = "Paste"
	REDO = "Redo"
	UNDO = "Undo"
	ESCAPE = "Escape"

	F1 = "F1"
	F2 = "F2"
	F3 = "F3"
	F4 = "F4"
	F5 = "F5"
	F6 = "F6"
	F7 = "F7"
	F8 = "F8"
	F9 = "F9"
	F10 = "F10"
	F11 = "F11"
	F12 = "F12"

	def __init__(self, key, action, mask=0):
		"""Build a key combination that can trigger an action. The action
		may be a callable or mind.AbstractAction that is only called
		if it is enabled. The key is one of constant Key.XXX.

		mask must be en ORed combination of Key.ALT, Key.CONTROL, Key.META
		and Key.SHIFT."""

		self.key = key
		if callable(action):
			self.action = Action(lambda _: action())
		else:
			self.action = action
		self.mask = mask

	def trigger(self, component):
		"""Called to trigger the action associarted with the key."""
		if self.action.is_enabled():
			self.action.perform(component.get_interface())


class Model:
	"""Represents a model of component and is used to manage its
	resources. The parameters are:
	* style -- CSS code to insert in the HTML header.
	* script -- JS code to insert in the HTML header.
	* style_paths -- CSS paths to link with.
	* script_paths -- JS  paths to link with.
	* before_main -- function taking out as parameter called before main
		component generation.
	* after_main -- function taking out as parameter called before main
		component generation.

	Style and script paths are retrieved (when relative) from the `dirs` list
	passed in the configuration.
	"""

	def __init__(self,
		name = None,
		parent = None,
		style = "",
		script = "",
		style_paths = None,
		script_paths = None
	):
		if style_paths is None:
			style_paths = []
		if script_paths is None:
			script_paths = []
		self.name = name
		self.parent = parent
		self.style = style
		self.script = script
		self.style_paths = style_paths
		self.script_paths = script_paths

	def get_parent(self):
		return self.parent

	def gen_style(self, out):
		"""Called to generate the style part."""
		out.write(self.style)

	def gen_script(self, out):
		"""Called to generate the script part."""
		out.write(self.script)

	def get_style_paths(self):
		"""Return a list of style path to embed."""
		return self.style_paths

	def get_script_paths(self):
		"""Return a list of script paths to embed."""
		return self.script_paths

	def __repr__(self):
		if self.name is not None:
			return self.name
		else:
			return str(self.__class__)


class Handler:
	"""Interface providing access to the HTTP server handler."""


class AbstractComponent(Displayable, Subject):
	"""Base class allowing to generate HTML with attributes, classes
	style and content and an identifier that may be customized."""
	COMPONENT_ID = 1

	def __init__(self):
		Subject.__init__(self)
		#self.id = "x" + str(COMPONENT_ID)	# !!DEBUG!!
		self.id = f"orc{AbstractComponent.COMPONENT_ID}"
		AbstractComponent.COMPONENT_ID += 1
		self.classes = []
		self.style = {}
		self.attrs = {}
		self.parent = None
		self.page = None
		self.shown = False
		self.keys = []

	def key(self, key, action, mask=0):
		"""Add a key to the component. action may a mind.Action or a function
		taking no argument. mask is a combination Key.XXX enumeration values.
		Returns the object itself that makes usable in component construction."""
		self.keys.append(Key(key, action, mask))
		if self.online():
			self.make_keys()
		return self

	def get_page(self):
		"""Get the page containing the component."""
		return self.page

	def online(self):
		"""Test if the current page is online.
		Must be implemented by each extension class."""
		return self.page is not None and self.page.online()

	def get_interface(self):
		"""Get the interface to communicate with user."""
		return self.parent.get_interface()

	def set_interface(self, interface):
		"""Define the interface for the current component. Usually go up in theme
		component hierarchy to find a context supporting it (ultimately the page)."""
		self.parent.set_interface(interface)

	def send(self, msg):
		"""Send a message to the UI. Returns the sent message.
		Must be implemented by each extension class."""
		pass

	def receive(self, msg, handler):
		"""Called to process a message on the current component.
		Default implementation displays an error."""
		handler.log_error(f"unknown message: {msg}")

	def get_id(self):
		"""Return the identifier of the current element."""
		return self.id

	def make_attr(self, val):
		"""Prepare a string to displayed as an attribute."""
		return html.escape(str(val), quote=True)

	def gen_attr(self, out, att, val = None):
		"""Generate an attribute on the given output."""
		if val is None:
			out.write(f' {att}')
		else:
			out.write(f' {att}="{html.escape(str(val), quote=True)}"')

	def gen_attrs(self, out):
		"""Generate common attributes"""

		# generate keys
		if self.keys:
			self.make_keys()

		# generate attribute themselves
		out.write(f' id="{self.get_id()}"')

		# generate style
		if self.style:
			out.write(' style="')
			for (k, x) in self.style.items():
				out.write(f"{k}: {self.make_attr(x)}; ")
			out.write('"')

		# generate classes
		if self.classes:
			out.write(f' class="{" ".join(self.classes)}"')

		# generate attributes
		for (att, val) in self.attrs.items():
			if val is None:
				out.write(f" {att}")
			else:
				out.write(f" {att}=\"{self.make_attr(val)}\"")

	def make_keys(self):
		"""Generate the content of attribute to handle keys."""
		map = ",".join(f"{{mask: {k.mask}, key: '{k.key}', action: {i} }}" \
			for (i, k) in enumerate(self.keys))
		self.set_attr('onkeyup', f'ui_handle_key(this, event, [{map}]);')

	def make_msg(self, type, id=None, nth=None):
		"""Build a standatd message."""
		if id is None:
			id = self.get_id()
		msg = { "id": id, "type": type }
		if nth is not None:
			msg["nth"] = nth
		return msg

	def call(self, fun, args = None):
		"""Send a message to call a function."""
		if args is None:
			args = {}
		self.send({"type": "call", "fun": fun, "args": args})

	def set_style(self, attr, val):
		"""Send a message to set a style. Return component itself for
		chaining at compilation time."""
		self.style[attr] = val
		if self.online():
			self.send({
				"type": "set-style",
				"id": self.get_id(),
				"attr": attr,
				"val": val
			})
		return self

	def get_style(self, attr, default=None):
		"""Get a style. None if not set."""
		try:
			return self.style[attr]
		except KeyError:
			return default

	def set_attr(self, attr, val=None, id=None):
		"""Set the value of an attribute of the current component. If on line,
		propagate the schange to the remote page. Return component itself
		for chaining at creation time."""
		if id is None:
			id = self.get_id()
			self.attrs[attr] = val
		if self.online():
			self.send({
				"type": "set-attr",
				"id": id,
				"attr": attr,
				"val": val if val is not None else ""})
		return self

	def set_attr_async(self, attr, val = None):
		"""Set an attribute for the current component. Do not propagate
		this modificaton to the online page.

		Useful to updte the component state according to changes from
		the remote page."""
		# TODO: maybe obsolete.
		self.attrs[attr] = val

	def get_attr(self, attr, default=None):
		"""Get the value of an attribute. Return default if the attribute is
		not defined (default to None)."""
		try:
			return self.attrs[attr]
		except KeyError:
			return default

	def remove_attr(self, attr, id=None):
		"""Remove an attribute of the current component. If on line, propagate
		the modification to the remote page."""
		try:
			if id is None:
				id = self.get_id()
				del self.attrs[attr]
			if self.online():
				self.send({"type": "remove-attr", "id": id, "attr": attr})
		except KeyError:
			pass

	def remove_attr_async(self, attr):
		"""Remove an attribute of the current component. No propagation is
		performed to the remote page."""
		# TODO: maybe obsolete
		try:
			del self.attrs[attr]
			if self.online():
				self.send({"type": "remove-attr", "id": self.get_id(), "attr": attr})
		except KeyError:
			pass

	def append_content(self, content, id=None):
		"""Append content to the current element. Content may be text or
		a component (that will be generated in this case)."""
		if id is None:
			id = self.get_id()
		msg = { "type": "append", "id": self.get_id() }
		self.send(msg)
		msg['content'] = self.gen_as_text(content)

	def set_content(self, content, id=None):
		"""Change the content of an element. Content may be string or component."""
		if id is None:
			id = self.get_id()
		msg = { "type": "set-content", "id": id }
		self.send(msg)
		msg['content'] = self.gen_as_text(content)

	def insert_content(self, content, pos, id=None):
		"""Insert the given content into the current element at the
		given position. Content may be text or a component."""
		if id is None:
			id = self.get_id()
		msg = {
			"type": "insert",
			"id": id,
			"pos": pos
		}
		self.send(msg)
		msg['content'] = self.gen_as_text(content)

	def clear_content(self):
		"""Clear the content of the component."""
		self.send({ "type": "clear", "id": self.get_id()})

	def remove_content(self, pos, id=None):
		"""Remove a child at given index from the current component."""
		if id is None:
			id = self.get_id()
		self.send({
			"type": "remove",
			"id": id,
			"pos": pos
		})

	def gen_as_text(self, content):
		"""Generate the given component as a text."""
		if isinstance(content, str):
			return content
		else:
			buf = Buffer()
			if isinstance(content, list):
				for comp in content:
					comp.gen(buf)
			else:
				content.gen(buf)
		return str(buf)

	def add_class(self, cls, id=None, nth=-1):
		"""Add a class of the component. Return itself for chaining at
		creation time."""
		if id is None:
			if cls in self.classes:
				return self
			id = self.get_id()
			self.classes.append(cls)
		if self.online():
			self.send({"type": "add-class", "id": id, "nth": nth, "class": cls})
		return self

	def has_class(self, cls):
		"""Test if the class is already set."""
		return cls in self.classes

	def remove_class(self, cls, id=None, nth=-1):
		"""Remove a class of the component."""
		if id is None:
			if cls not in self.classes:
				return
			id = self.get_id()
			self.classes.remove(cls)
		if self.online():
			self.send({"type": "remove-class", "id": id, "nth": nth, "class": cls})

	def set_top_class(self, cls):
		"""Customize the component as a top component with the given class. The
		default implementation applies the style to the page."""
		self.get_page().add_class(cls)

	def get_config(self, key=None, default=None):
		"""Get the global configuration or the configuration matching the key."""
		return self.parent.get_config(key, default)

	def __str__(self):
		try:
			return f"<component {self.get_id()}:{self.__class__}>"
		except AttributeError:
			return "<page>"

	def is_enabled(self):
		"""Test if the component is enabled. Default implementation returns True."""
		return True

	def enable(self):
		"""Called to enable the component. Default implementation does nothing."""
		pass

	def disable(self):
		"""Called to disable the component. Default implementation does nothing."""
		pass

	def set_enabled(self, enabled):
		"""Enable/disable according to the enabled parameter."""
		if enabled:
			self.enable()
		else:
			self.disable()

	def grab_focus(self, **args):
		"""Grab focus on this component."""
		self.send(self.make_msg("grab-focus", **args))

	def find_next_focus(self, component=None):
		"""Lookup for focus following the passed component (if any) or for the
		current component. Returns the next component for focus or None
		(default implementation)."""
		return None

	def next_focus(self):
		"""Pass focus to the next componen (if any). Default implementation
		asks parent for next component."""
		next = self.parent.find_next_focus(self)
		if next is not None:
			next.grab_focus()


class Component(AbstractComponent):
	"""Component to build a user-interface. A component may be displayed
	but is also interactive requiring to have a link with the page."""

	def __init__(self, model):
		AbstractComponent.__init__(self)
		self.model = model
		self.weight = None
		self.shown = False

	def get_model(self):
		"""Get the model of the component."""
		return self.model

	def get_id(self):
		"""Get the unique identifier (string) of the component in the page."""
		return self.id

	def get_page(self):
		"""Get the page containing the component."""
		return self.page

	def get_context(self):
		"""Get the context of the page. One of Context.XXX enumeration value."""
		return Context.NONE

	def get_children(self):
		return []

	def send(self, msg):
		"""Send a message to the UI."""
		self.page.messages.append(msg)

	# !!CHECK!! check usage! Seems deprecated.
	def send_classes(self, classes, id = None):
		"""Set the classes of a component."""
		if id is None:
			id = self.id
		self.send({"type": "set-class", "id": id, "classes": " ".join(classes)})

	def expands_horizontal(self):
		"""Return true to support horizontal expansion."""
		return False

	def expands_vertical(self):
		"""Return true to support vertical expansion."""
		return False

	def get_weight(self):
		if self.weight is None:
			self.weight = (0, 0)
		elif isinstance(self.weight, int):
			self.weight = (self.weight, self.weight)
		return self.weight

	def set_weight(self, weight):
		"""Change the weight of the component. Only used at build time.
		Weight may be an integer or a pair (x weight, y weight).
		Return self and so can be chained."""
		self.weight = weight
		return self

	def finalize(self, page):
		"""Called to let component declare additional resources when
		added to a page."""
		page.on_add(self)

	def on_show(self):
		"""Called when the component is shown. The default implementation does nothing."""
		self.shown = True

	def on_hide(self):
		"""Called when the component is hidden."""
		self.shown = False

	def show(self):
		"""Show the current item and return itself."""
		if not self.shown:
			self.on_show()
			self.remove_class("hidden")
		return self

	def hide(self):
		"""Hide the current item and return itself."""
		if self.shown:
			self.on_hide()
			self.add_class("hidden")
		return self

	def is_shown(self):
		"""Test if the current component is shown."""
		return self.shown

	def receive(self, msg, handler):
		if msg["action"] == "key":
			self.keys[msg["idx"]].trigger(self)
		else:
			AbstractComponent.receive(self, msg, handler)


class ParentComponent(Component):
	"""Interface implemented by any component containing other
	components. All components are contained in a parent
	component."""

	def __init__(self, model):
		Component.__init__(self, model)

	def remap_child(self, child):
		"""Function to call to signal that mapping properties of a child
		changed. Default implementation does nothing."""
		pass

	def show_last(self):
		"""If the current element is a container, show its last item.
		Default implementation does nothing."""
		pass

	def show_child(self, child):
		"""If the current element is a container, ensure that the child is visible.
		Default implementation does nothing."""
		pass


class PageObserver:
	"""Observer of events of a page."""

	def on_open(self, page):
		"""Called when the page is opened."""
		pass

	def on_receive(self, page, msg):
		"""Called when the page receive a message.
		Return True to stop propagation."""
		pass

	def on_close(self, page):
		"""Called when the page is closed."""
		pass


class Page(AbstractComponent):
	"""Implements a page ready to be displayed."""

	def __init__(self, main = None, parent = None,
	app = None, title = None, style = "default.css", theme = "basic", interface=STANDARD_INTERFACE):
		AbstractComponent.__init__(self)
		self.messages = []
		self.is_online = False
		self.parent = parent
		self.app = app
		self.title = title
		self.session = None
		self.main = None
		self.base_style = style
		self.timeout_thread = None
		self.hidden = []
		self.interface = interface
		self.manager = None
		self.style_paths = []
		self.focus_id = None
		self.set_attr("onbeforeunload", "ui_close();")
		self.set_attr("onload", 'ui_hi();')
		self.set_attr("onfocusin", "ui_on_focus(event);")

		# prepare the theme
		if isinstance(theme, str):
			m = importlib.import_module(f"orchid.themes.{theme}")
			theme = m.get()
		self.theme = theme

		# install main component
		if main is not None:
			self.set_main(main)
		else:
			self.models = {}
			self.components = {}
		self.add_model(theme)

	def get_focus(self):
		"""Get the element that gets the focus. None if no one has the focus."""
		if self.focus_id is None:
			return None
		try:
			return self.components[self.focus_id]
		except KeyError:
			try:
				i = self.focus_id.index('-')
				self.focus_id = self.focus_id[:i]
				return self.components[self.focus_id]
			except (ValueError, KeyError):
				return None

	def find_next_focus(self, component=None):
		return self.main.find_next_focus()

	def next_focus(self):
		"""Pass focus to next element."""
		current = self.get_focus()
		if current is None:
			self.main.next_focus()
		else:
			current.next_focus()

	def get_theme(self):
		"""Get the current theme of the page."""
		return self.theme

	def get_interface(self):
		return self.interface

	def set_interface(self, interface):
		self.interface = interface

	def online(self):
		"""Test if the current page is online.
		Must be implemented by each extension class."""
		return self.is_online

	def get_session(self):
		"""Get the current session."""
		return self.session

	def get_application(self):
		"""Get the application containing the page."""
		return self.session.get_application()

	def get_config(self, key=None, default=None):
		"""Get the global configuration as passed to the run()
		server command or an item from the global configuration."""
		return self.app.get_config(key, default)

	def add_style_path(self, path):
		"""Add a style path to the generated model."""
		self.style_paths.append(path)

	def add_model(self, model):
		"""Add a model to the page."""
		m = model
		while m is not None:
			try:
				self.models[m] += 1
				m = None
			except KeyError:
				self.models[m] = 1
				if self.online():
					self.download_model(model)
				m = m.get_parent()

	def download_model(self, model):
		"""Update a remote page with the model of a new added component."""
		script = Buffer()
		model.gen_script(script)
		style = Buffer()
		model.gen_style(style)
		self.send({
			"type": "model",
			"script": str(script),
			"style": str(style),
			"script_paths": model.get_script_paths(),
			"style_paths": model.get_style_paths()
		})

	def on_add(self, comp):
		"""Called each time a component is added."""
		comp.page = self
		self.components[comp.get_id()] = comp
		self.add_model(comp.get_model())

	def add_hidden(self, comp):
		"""Add an hidden component (typically dialog or popup)."""
		self.hidden.append(comp)
		comp.parent = self
		comp.finalize(self)
		if self.online():
			self.append_content(comp)

	def set_main(self, main):
		"""Set the main component."""
		self.main = main
		main.parent = self
		self.components = {}
		self.models = {}
		main.finalize(self)
		main.set_style("flex", "1")
		main.set_top_class("top-content")

	def get_context(self):
		return Context.MAIN

	def on_remove(self, comp):
		"""Called each time a component is removed."""
		m = comp.get_model()
		self.models[m] -= 1
		if self.models[m] == 0:
			del self.models[m]

	def gen_style(self, out):
		"""Generate the style part."""
		for m in self.models:
			m.gen_style(out)

	def gen_script(self, out):
		"""Generate the script part."""
		out.write(f"var ui_page=\"{self.get_id()}\";\n")
		for m in self.models:
			m.gen_script(out)

	def gen_content(self, out):
		"""Generate the content."""
		self.main.gen(out)
		for comp in self.hidden:
			comp.gen(out)
		self.is_online = True

	def receive(self, msg, handler):
		"""Called to receive messages and answer. The answer is a
		possibly list of back messages."""

		# manage session
		if self.session is not None:
			self.session.update()

		# manage messages
		for m in msg:
			id = m["id"]
			if id == "0":
				self.manage(m, handler)
			else:
				try:
					comp = self.components[id]
				except KeyError:
					handler.log_error(f"unknown component in {m}")
					comp = None
				if comp is not None:
					comp.receive(m, handler)

		# manage answers
		res = self.messages
		self.messages = []
		return res

	def close(self):
		"""Called to close the page."""
		self.send({"type": "quit"})
		self.timeout_thread = Thread(target=self.close_timeout)
		self.timeout_thread.start()

	def close_timeout(self):
		"""Manage timeout in case the browser does not answer the quit command."""
		sleep(CLOSE_TIMEOUT)
		print("Close timeout!")
		if self.timeout_thread is not None:
			self.on_close()

	def on_close(self):
		"""Called when a closure message is received from the client."""
		self.timeout_thread = None
		for obs in self.filter_observers(PageObserver):
			obs.on_close(self)
		self.session.remove_page(self)
		if self.parent is not None:
			self.parent.on_close()

	def on_hide(self):
		self.main.on_hide()

	def on_show(self):
		self.main.on_show()

	def manage(self, msg, handler):
		"""Manage window messages."""

		# observers turn
		for obs in self.filter_observers(PageObserver):
			if obs.on_receive(self, msg):
				return

		# default actions
		a = msg["action"]
		if a == "close":
			self.on_close()
		elif a == "hi":
			pass
		elif a == "focus":
			self.focus_id = msg["target"]
		else:
			handler.log_error(f"unknown action: {a}")

	def gen_script_paths(self, out):
		"""Called to generate linked scripts."""
		ss = ["orchid.js"]
		for m in self.models:
			for s in m.get_script_paths():
				if s not in ss:
					ss.append(s)
		for s in ss:
			out.write(f'<script src="{s}"></script>\n')

	def gen_style_paths(self, out):
		"""Called to generate linked CSS."""
		ss = [self.base_style]
		for m in self.models:
			for s in m.get_style_paths():
				if s not in ss:
					ss.append(s)
		if self.app is not None:
			ss = ss + self.app.style_paths
		for s in ss:
			out.write(f'<link rel="stylesheet" href="{s}"/>\n')

	def open(self, page):
		"""Change page to the given page."""
		self.manager.add_page(page)
		self.page.messages.append({
			"type": "call",
			"fun": "ui_open",
			"args": f"/_/{page.get_id()}"
		})

	def gen_title(self, out):
		if self.title is not None:
			text = self.title
		elif self.app is not None:
			text = self.app.name
		else:
			text = "No Title"
		out.write(text)

	def send(self, msg):
		"""Send a message to the UI."""
		self.messages.append(msg)

	def gen(self, out):
		for obs in self.filter_observers(PageObserver):
			obs.on_open(self)
		self.main.on_show()
		out.write("""
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8"/>
	<title>""")
		self.gen_title(out)
		out.write("</title>\n")
		self.gen_style_paths(out)
		out.write("\t<style>\n")
		self.gen_style(out)
		out.write("\t</style>\n")
		self.gen_script_paths(out)
		out.write("\t<script>\n")
		self.gen_script(out)
		out.write("\t</script>\n")
		out.write("</head>\n")
		out.write('<body ')
		self.gen_attrs(out)
		out.write(">\n")
		self.gen_content(out)
		#out.write('<script>console.log("end of body!");</script>')
		out.write('</body>')
		out.write('</html>')

	def publish_text_file(self, url, text, mime = None):
		"""Publish an URL returning the given text
		(for big GET operation)."""
		self.get_application().add_text_file(url, text, mime)

	def publish_file(self, url, path, mime = None):
		"""Publish an URL returning the content of the file
		corresponding to the path. If url is None, one is built
		and returned."""
		return self.get_application().publish_file(url, path, mime)

	def publish(self, url, provider):
		"""Publish an URL with a custom provider."""
		self.get_application().add_provider(url, provider)

	def set_direct_attr(self, id, att, val):
		"""Set the attribute of an element identified with id.
		Works only online."""
		if self.online():
			self.send({
				"type": "set-attr",
				"id": id,
				"attr": att,
				"val": val})

	def remove_direct_attr(self, id, att):
		"""Remove an attribute of an arbitrary object."""
		if self.online():
			self.send({
				"type": "remove-attr",
				"id": id,
				"attr": att
			})

	def open_url(self, url, target="_self"):
		"""Open the URL in the given target. Target may be classic target in
		HTML <a> tags."""
		if self.online():
			self.send({ "type": "open", "url": url, "target": target })


class Session:
	"""Represent a sessuib to a specific client. It allows to
	detect when a connection is completed and its resources have to
	be released. It may be used by application page to store
	sesison information. Accessible by Page.get_session() function."""

	COUNT = 0
	FREE = []

	def __init__(self, app, man):
		self.app = app
		self.man = man
		self.pages = []
		self.creation = time.time()
		self.last = self.creation
		self.timeout = man.config['session_timeout']
		man.add_session(self)
		if Session.FREE:
			self.number = Session.FREE.pop()
		else:
			self.number = Session.COUNT
			Session.COUNT += 1

	def get_number(self):
		"""Get the session number."""
		return self.number

	def get_creation_time(self):
		"""Get the creation of session (in s from the OS)."""
		return self.creation

	def get_last_access(self):
		"""Get the last access date (in s from the OS)."""
		return self.last

	def add_page(self, page):
		"""Record a page to belong to the session."""
		self.pages.append(page)
		page.session = self

	def remove_page(self, page):
		"""Remove a page from the session. If there is no more page in the session, it is cleaned."""
		self.man.remove_page(page)
		self.pages.remove(page)
		if not self.pages:
			self.release()

	def update(self):
		"""Called each time there is an access to a page of the session."""
		self.last = time.time()

	def check(self):
		"""Called to check if the session is expired."""
		t = time.time()
		if t - self.last > self.timeout:
			self.release()

	def release(self):
		"""Called to relase the resources of the session
		(basically pages)."""
		if self.number == Session.COUNT - 1:
			Session.COUNT -= 1
		else:
			Session.FREE.append(self.number)
		for page in self.pages:
			self.man.remove_page(page)
		self.man.remove_session(self)

	def get_application(self):
		"""Get the application owning the session."""
		return self.app

	def get_index(self):
		"""Get the index page for this session."""
		return self.app.first()

	def publish_text_file(self, url, text, mime = None):
		"""Publish an URL returning the given text
		(for big GET operation)."""
		self.app.add_text_file(url, text, mime)

	def publish_file(self, url, path, mime = None):
		"""Publish an URL returning the content of the file
		corresponding to the path. If url is None, one is built
		and returned."""
		return self.app.add_file(url, path, mime)

	def publish(self, url, provider):
		"""Publish an URL with a custom provider."""
		self.app.add_provider(url, provider)


class Application:
	"""Class representing the application and specially provides the initial page."""

	def __init__(self, name,
		version = None,
		authors = None,
		license = None,
		copyright = None,
		description = None,
		website = None,
		icon = None,
		style_paths = None,
		theme = "basic",
		first = lambda _: None,
		session = None
	):
		"""Build an applications. Parameters encompasses:
		* version (as a string)
		* authors (as a string)
		* licence (as a string)
		* description (as a string)
		* website (URL)
		* icon (path to icon file)
		* style_paths (list of paths to find .css files)
		* theme (theme to use for the applications pages)
		* first (function called with application as paramter to
			build the first page, typically class of main page)
		* session (constructor of session taking application, manager as parameter)
		"""

		if authors is None:
			authors = []
		if style_paths is None:
			style_paths = []
		self.name = name
		self.version = version
		self.license = license
		self.copyright = copyright
		self.description = description
		self.website = website
		self.icon = icon
		self.style_paths = style_paths
		self.theme = theme
		self.config = {}
		self.first_class = first
		if session is None:
			session = Session
		self.session_cons = session
		self.manager = None
		self.file_map = {}

	def run(self, **args):
		"""Run the server for the application.
		Parameters are passed as is to the server."""
		server.run(self, **args)

	def get_theme(self):
		"""Get the theme of the application."""
		return self.theme

	def configure(self, config):
		"""Function called to configure the application."""
		self.config = config

	def first(self):
		"""Get the first page."""
		return self.first_class(self)

	def new_session(self, man):
		"""Called to create a new session for the application.
		Default return the base class Session. This function can be
		overloaded to customize the session object."""
		return self.session_cons(self, man)

	def get_config(self, key=None, default=None):
		"""Get the configuration of the application."""
		if key is None:
			return self.config
		else:
			try:
				return self.config[key]
			except KeyError:
				return default

	def make_url(self, path):
		"""Build a unique URL for the file at the passed path."""
		path = os.path.abspath(path)
		try:
			return self.file_map[path]
		except KeyError:
			base = os.path.basename(path)
			root, ext = os.path.splitext(base)[1]
			url = f"/file/{root}-{len(self.file_map)}{ext}"
			self.file_map[path] = url
			return url

	def publish_text_file(self, url, text, mime = None):
		"""Publish an URL returning the given text
		(for big GET operation)."""
		self.manager.add_text_file(url, text, mime)

	def publish_file(self, url, path, mime = None):
		"""Publish an URL returning the content of the file
		corresponding to the path. An url as None requires
		a valid URL to be built."""
		if url is None:
			url = self.make_url(path)
		self.manager.add_file(url, path, mime)

	def publish(self, url, provider):
		"""Publish an URL with a custom provider."""
		self.manager.add_provider(url, provider)


TIMER_MODEL = Model("timer")

class Timer(Component):
	"""A timer that is able to call the trigger() function according to a time
	basis. IT may be oneshot or periodic if a periond in ms is given.
	It may also be started at application start-time if started is True."""

	def __init__(self, page, trigger, period=0, started=False):
		Component.__init__(self, TIMER_MODEL)
		self.trigger = trigger
		self.period = period
		self.started = started
		page.add_hidden(self)

	def gen(self, out):
		if self.started and self.period != 0:
			out.write(f'<script>ui_timer_start({{id: "{self.get_id}", \
						time: {self.period}, periodic: true}});</script>')

	def start(self, time = None):
		"""Start the timer to trigger at given time or after period.
		Argument time is in ms. If not given, the period time applies."""
		if time is not None:
			periodic = False
		else:
			time = self.period
			periodic = True
		self.started = True
		self.call("ui_timer_start", {
			"id": self.get_id(),
			"time": time,
			"periodic": periodic
		})

	def stop(self):
		"""Stop the timer."""
		self.call("ui_timer_stop", {"id": self.get_id()})
		self.started = False

	def receive(self, msg, handler):
		if msg["action"] == "trigger":
			if self.period == 0:
				self.started = False
			self.trigger()
		else:
			Component.receive(self, msg, handler)


PLAIN_MODEL = Model("plain")

class Plain(Component):
	"""A component displaying plain HTML. The HTML can be embedded
	in a parent tag if needed (supporting class and attribute setting)."""

	def __init__(self, text, in_tag=None):
		Component.__init__(self, PLAIN_MODEL)
		self.text = text.replace("\n", "<br>")
		self.in_tag = in_tag

	def gen(self, out):
		if self.in_tag is not None:
			out.write(f"<{self.in_tag}")
			self.gen_attrs(out)
			out.write(">")
		out.write(self.text)
		if self.in_tag is not None:
			out.write(f"</{self.in_tag}>")


class Theme(Model):
	"""A theme represented a set of assorted resource to display the UI."""

	def __init__(self,
		name = None,
		parent = None,
		style = "",
		script = "",
		style_paths = None,
		script_paths = None
	):
		Model.__init__(self, name, parent, style, script, style_paths, script_paths)

	def get_name(self):
		"""Get the name of the theme."""
		return self.name

	def get_icon(self, type, color = None):
		"""Get an icon by type. Possibly with a color if the icon is monochrom."""
		return None

	def get_dialog_icon(self, type, size=32):
		"""Get the icon for a dialog. type must be one of MessageType
		enumeration value. May return None if the type is not supported."""
		return None
