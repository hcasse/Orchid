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

import time

COMPONENT_ID = 1

# type of context
CONTEXT_NONE = 0
CONTEXT_TOOLBAR = 1
CONTEXT_HEADERBAR = 2
CONTEXT_BUTTONBAR = 3
CONTEXT_MENU = 4
CONTEXT_MAIN = 5

# type of icons
ICON_ERASE = "erase"
ICON_FORWARD = "forward"
ICON_BACKWARD = "backward"
ICON_MENU = "menu"

def write_nothing(page, out):
	"""Funcion writing nothing to out."""
	pass

class Observer:
	"""Observer for subject-observer pattern."""

	def update(self, subject):
		pass

class Subject:
	"""Observer for subject-observer pattern."""

	def __init__(self):
		self.observers = []

	def get_observers(self):
		"""Get the list of observers."""
		return self.observers

	def filter_observers(self, cls):
		"""Filter observers with the given class."""
		for obs in self.observers:
			if isinstance(obs, cls):
				yield obs

	def add_observer(self, observer):
		"""Add an observer to the subject."""
		self.observers.append(observer)

	def remove_observer(self, observer):
		"""Remove an observer from the subject."""
		self.observers.remove(observer)

	def update_observers(self):
		"""Call the update function of the observers."""
		for observer in self.observers:
			observer.update(self)

class Model:
	"""Represents a model of component and is used to manage its
	resources. The parameters are:
	* style -- CSS code to insert in the HTML header.
	* script -- JS code to insert in the HTML header.
	* style_paths -- CSS paths to link with.
	* script_paths -- JS  paths to link with.
	* before_main -- function taking out as parameter called before main component generation.
	* after_main -- function taking out as parameter called before main component generation.

	Style and script paths are retrieved (when relative) from the `dirs` list passed in the configuration.
	"""

	def __init__(self,
		name = None,
		parent = None,
		style = "",
		script = "",
		style_paths = [],
		script_paths = []
	):
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

	

class Displayable:
	"""Defines an object that may be displayed in the UI but is not
	interactive. It may be finalized and generated."""

	def finalize(self, page):
		"""Called before the generation in order to link with the page
		and possibly ask for resources."""
		pass

	def gen(self, out):
		"""Called  to generate the HTML content corresponding to the
		displayable on the given output (supporting only write() method).
		The default implementation does nothing."""
		pass

DISPLAY_NONE = Displayable()
"""Displayable that displays nothing."""

class Text(Displayable):
	"""A simple displayable showing a text."""

	def __init__(self, text, style = None):
		self.text = text
		self.style = style

	def gen(self, out):
		out.write("<span")
		if self.style is not None:
			out.write(' class="text-%s"' % self.style)
		out.write('>')
		out.write(self.text)
		out.write('</span>')


class AbstractComponent(Displayable, Subject):
	"""Base class allowing to generate HTML with attributes, classes
	style and content and an identifier that may be customized."""

	def __init__(self):
		global COMPONENT_ID
		Subject.__init__(self)
		self.id = str(COMPONENT_ID)
		COMPONENT_ID += 1
		self.classes = []
		self.style = {}
		self.attrs = {}

	def online(self):
		"""Test if the current page is online.
		Must be implemented by each extension class."""
		return None

	def send(self, msg):
		"""Send a message to the UI.
		Must be implemented by each extension class."""
		pass

	def receive(self, msg, handler):
		"""Called to process a message on the current component.
		Default implementation displays an error."""
		handler.log_error("%s: unknown message: %s" % (self.model, msg))

	def get_id(self):
		"""Return the identifier of the current element."""
		return self.id

	def gen_attrs(self, out):
		"""Generate common attributes"""

		# generate attribute themselves
		out.write(' id="%s"' % self.get_id())

		# generate style
		if self.style != {}:
			out.write(' style="')
			for k in self.style:
				out.write("%s: %s; " % (k, self.style[k]))
			out.write('"')

		# generate classes
		if self.classes != []:
			out.write(' class="%s"' % " ".join(self.classes))

		# generate attributes
		for att in self.attrs:
			val = self.attrs[att]
			if val == None:
				out.write(" %s" % att)
			else:
				out.write(" %s=\"%s\"" % (att, val))

	def call(self, fun, args = {}):
		"""Send a message to call a function."""
		self.send({"type": "call", "fun": fun, "args": args})

	def set_style(self, attr, val):
		"""Send a message to set a style."""
		self.style[attr] = val
		if self.online():
			self.send({"type": "set", "id": self.get_id(), "attr": attr, "val": val})

	def set_content(self, content):
		"""Change the content of an element."""
		if self.online():
			self.send({"type": "set-content", "id": self.get_id(), "content": content})

	def set_attr(self, attr, val = None):
		"""Send a message to set an attribute.
		Notice that, if you have to use a quote in the value, use the simple
		quote."""
		self.attrs[attr] = val
		if self.online():
			self.send({
				"type": "set-attr",
				"id": self.get_id(),
				"attr": attr,
				"val": val if val != None else ""})

	def get_attr(self, attr):
		"""Get the value of an attribute. Return None if the attribute is not defined."""
		try:
			return self.attrs[attr]
		except KeyError:
			return None

	def append_content(self, content):
		"""Append content to the current element."""
		if self.online():
			self.send({
				"type": "append",
				"id": self.get_id(),
				"content": content})

	def insert_content(self, content, pos):
		"""Insert the given content into the current element at the
		given position."""
		if self.online():
			self.send({
				"type": "insert",
				"id": self.get_id(),
				"pos": pos,
				"content": content})

	def clear_content(self):
		"""Clear the content of the component."""
		if self.online():
			self.send({
				"type": "clear",
				"id": self.get_id()})

	def remove_child(self, index):
		"""Remove a child at given index from the current component."""
		if self.online():
			self.send({
				"type": "remove",
				"id": self.get_id(),
				"child": index});

	def show_last(self):
		"""If the current element is a container, show its last item."""
		if self.online():
			self.send({
				"type": "show-last",
				"id": self.get_id()})
	
	def remove_attr(self, attr):
		"""Send a message to remove an attribute."""
		try:
			del self.attrs[attr]
			if self.online():
				self.send({"type": "remove-attr", "id": self.get_id(), "attr": attr})
		except KeyError:
			pass

	def add_class(self, cls):
		"""Add a class of the component."""
		if cls not in self.classes:
			self.classes.append(cls)
			if self.online():
				self.send_classes(self.classes)

	def remove_class(self, cls):
		"""Remove a class of the component."""
		if cls in self.classes:
			self.classes.remove(cls)
			if self.online():
				self.send_classes(self.classes)


class Component(AbstractComponent):
	"""Component to build a user-interface. A component may be displayed
	but is also interactive requiring to have a link with the page."""

	def __init__(self, model):
		global COMPONENT_ID
		AbstractComponent.__init__(self)
		self.page = None
		self.model = model
		self.id = str(COMPONENT_ID)
		COMPONENT_ID += 1

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
		"""Get the context of the page. One of CONTEXT_XXX constant."""
		return CONTEXT_NONE

	def get_children(self):
		return []

	def online(self):
		"""Test if the current page is online."""
		return self.page != None and self.page.online

	def send(self, msg):
		"""Send a message to the UI."""
		self.page.messages.append(msg)

	# !!CHECK!! check usage! Seems deprecated.
	def send_classes(self, classes, id = None):
		"""Set the classes of a component."""
		if id == None:
			id = self.id
		self.send({"type": "set-class", "id": id, "classes": " ".join(classes)})

	def expands_horizontal(self):
		"""Return true to support horizontal expansion."""
		return False

	def expands_vertical(self):
		"""Return true to support vertical expansion."""
		return False

	def get_weight(self):
		try:
			if isinstance(self.weight, tuple):
				return self.weight
			else:
				return (self.weight, self.weight)
		except AttributeError:
			return (0, 0)

	def set_enabled(self, enabled = True):
		"""Enable/disable a component."""
		if enabled:
			self.enable()
		else:
			self.disable()

	def enable(self):
		"""Enable the component."""
		pass

	def disable(self):
		"""Disable the component."""
		pass

	def finalize(self, page):
		"""Called to let component declare additional resources when
		added to a page."""
		page.on_add(self)


class ExpandableComponent(Component):

	def __init__(self, model):
		Component.__init__(self, model)

	def gen_resize(self, out):
		out.write("""
			function resize_%s(w, h) {
				e = document.getElementById("%s");
				ui_set_width(e, w);
				ui_set_height(e, h);
			}
""" % (self.get_id(), self.get_id()))


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
	app = None, title = None, style = "default.css"):
		AbstractComponent.__init__(self)
		self.messages = []
		self.is_online = False
		self.parent = parent
		self.app = app
		self.title = title
		self.session = None
		self.main = None
		if main != None:
			self.set_main(main)
		else:
			self.models = {}
			self.components = {}
		self.base_style = style
		self.hidden = []
		self.set_attr("onbeforeunload", "ui_close();")
		self.set_attr("onclick", "ui_complete();")

	def online(self):
		"""Test if the current page is online.
		Must be implemented by each extension class."""
		return self.is_online

	def get_session(self):
		"""Get the current session."""
		return self.session

	def get_config(self):
		"""Get the global configuration as passed to the run()
		server command."""
		return self.manager.config

	def add_style_path(self, path):
		"""Add a style path to the generated model."""
		self.style_paths.append(path)

	def add_model(self, model):
		"""Add a model to the page."""
		m = model
		while m != None:
			try:
				self.models[m] += 1
				m = None
			except KeyError:
				self.models[m] = 1
				m = m.get_parent()

	def on_add(self, comp):
		"""Called each time a component is added."""
		comp.page = self
		self.components[comp.get_id()] = comp
		self.add_model(comp.get_model())

	def add_hidden(self, comp):
		"""Add an hidden component (typically dialog or popup)."""
		self.hidden.append(comp)
		comp.finalize(self)

	def set_main(self, main):
		"""Set the main component."""
		self.main = main
		main.parent = self
		self.components = {}
		self.models = {}
		main.finalize(self)
		main.set_style("flex", "1")

	def get_context(self):
		return CONTEXT_MAIN

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
		out.write("var ui_page=\"%s\";\n" % self.get_id())
		for m in self.models:
			m.gen_script(out)

	def gen_content(self, out):
		"""Generate the content."""
		self.main.gen(out)
		for comp in self.hidden:
			comp.gen(out)
		self.is_online = True

	def receive(self, messages, handler):
		"""Called to receive messages and answer. The answer is a
		possibly list of back messages."""

		# manage session
		if self.session != None:
			self.session.update()

		# manage messages
		for m in messages:
			id = m["id"]
			if id == "0":
				self.manage(m, handler)
			else:
				try:
					comp = self.components[id]
					comp.receive(m, handler)
				except KeyError:
					handler.log_error("unknown component in %s" % m)

		# manage answers
		res = self.messages
		self.messages = []
		return res

	def on_close(self):
		"""Called when a closure message is received from the client."""
		for obs in self.filter_observers(PageObserver):
			obs.on_close(self)
		self.session.remove_page(self)
		if self.parent != None:
			self.parent.on_close()

	def close(self):
		"""Called to close the page."""
		self.send({"type": "quit"})

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
		else:
			handler.log_error("unknown action: %s" % a)

	def gen_script_paths(self, out):
		"""Called to generate linked scripts."""
		ss = ["orchid.js"]
		for m in self.models:
			for s in m.get_script_paths():
				if s not in ss:
					ss.append(s)
		for s in ss:
			out.write('<script src="%s"></script>\n' % s)

	def gen_style_paths(self, out):
		"""Called to generate linked CSS."""
		ss = ["basic.css", self.base_style]
		for m in self.models:
			for s in m.get_style_paths():
				if s not in ss:
					ss.append(s)
		if self.app != None:
			ss = ss + self.app.style_paths
		for s in ss:
			out.write('<link rel="stylesheet" href="%s"/>\n' % s)

	def open(self, page):
		"""Change page to the given page."""
		self.manager.add_page(page)
		self.page.messages.append({
			"type": "call",
			"fun": "ui_open",
			"args": "/_/%s" % page.get_id()
		})

	def gen_title(self, out):
		if self.title != None:
			text = self.title
		elif self.app != None:
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
		out.write('</body>')
		out.write('</html>')

	def publish_text(self, url, text, mime = None):
		"""Publish an URL returning the given text
		(for big GET operation)."""
		self.manager.add_text(url, text, mime)

	def publish_file(self, url, path, mime = None):
		"""Publish an URL returning the content of the file
		corresponding to the path."""
		self.manager.add_file(url, path, mime)


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
		man.sessions.append(self)
		if Session.FREE != []:
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
		if self.pages == []:
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
		self.man.sessions.remove(self)

	def get_application(self):
		"""Get the application owning the session."""
		return self.app

	def get_index(self):
		"""Get the index page for this session."""
		return self.app.first()


class Application:
	"""Class representing the application and specially provides the initial page."""

	def __init__(self, name,
		version = None,
		authors = [],
		license = None,
		copyright = None,
		description = None,
		website = None,
		style_paths = []
	):
		self.name = name
		self.version = version
		self.license = license
		self.copyright = copyright
		self.description = description
		self.website = website
		self.style_paths = style_paths

	def first(self):
		"""Function called to get the first page."""
		return None

	def configure(self, config):
		"""Function called to configure the application."""
		self.config = config

	def new_session(self, man):
		"""Called to create a new session for the application.
		Default return the base class Session. This function can be
		overloaded to customize the session object."""
		return Session(self, man)
