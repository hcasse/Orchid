"""Orchid base classes and definitions. """

PAGE_ID = 1
COMPONENT_ID = 1

# type of context
CONTEXT_NONE = 0
CONTEXT_TOOLBAR = 1
CONTEXT_HEADERBAR = 2
CONTEXT_BUTTONBAR = 3

# type of icons
ICON_ERASE = "erase"
ICON_FORWARD = "forward"
ICON_BACKWARD = "backward"
ICON_MENU = "menu"

class Observer:
	"""Observer for subject-observer pattern."""

	def update(self, subject):
		pass

class Subject:
	"""Observer for subject-observer pattern."""

	def __init__(self):
		self.observers = []

	def add_observer(self, observer):
		self.observers.append(observer)

	def remove_observer(self, observer):
		self.observers.remove(observer)

	def update_observers(self, subject):
		for observer in self.observers:
			observer.update(subject)


class Model:
	"""Represents a model of component and is used to manage its
	resources."""

	def __init__(self, parent = None):
		self.parent = parent

	def get_parent(self):
		return self.parent

	def gen_style(self, out):
		"""Called to generate the style part."""
		pass

	def gen_script(self, out):
		"""Called to generate the script part."""
		pass

	def get_style_paths(self):
		"""Return a list of style path to embed."""
		return []

	def get_script_paths(self):
		"""Return a list of script paths to embed."""
		return []


class Component(Subject):
	"""Component to build a user-interface."""

	def __init__(self, model):
		global COMPONENT_ID
		Subject.__init__(self)
		self.page = None
		self.model = model
		self.id = str(COMPONENT_ID)
		COMPONENT_ID += 1
		self.classes = []

	def get_model(self):
		return self.model

	def get_id(self):
		return self.id

	def get_page(self):
		return page

	def get_children(self):
		return []

	def gen_attrs(self, out):
		"""Generate common attributes"""
		out.write(' id="%s"' % self.get_id())
		if self.classes != []:
			out.write(' class="%s"' % " ".join(self.classes))

	def gen(self, out):
		"""Called to generate the component itself."""
		pass

	def receive(self, msg, handler):
		"""Called to process a message."""
		handler.log_error("%s: unknown message: %s" % (self.model, msg))

	def send(self, msg):
		"""Send a message to the UI."""
		self.page.messages.append(msg)

	def call(self, fun, args):
		"""Send a message to call a function."""
		self.send({"type": "call", "fun": fun, "args": args})

	def set_style(self, attr, val):
		"""Send a message to set a style."""
		self.send({"type": "set", "id": self.get_id(), "attr": attr, "val": val})

	def set_attr(self, attr, val = None):
		"""Send a message to set an attribute."""
		self.send({"type": "set-attr", "id": self.get_id(), "attr": attr, "val": val})

	def remove_attr(self, attr):
		"""Send a message to remove an attribute."""
		self.send({"type": "remove-attr", "id": self.get_id(), "attr": attr})

	def add_class(self, cls):
		"""Add a class of the component."""
		if cls not in self.classes:
			self.classes.append(cls)
			if self.page != None and self.page.online:
				self.send_classes(self.classes)

	def remove_class(self, cls):
		"""Remove a class of the component."""
		if cls in self.classes:
			self.classes.remove(cls)
			if self.page != None and self.page.online:
				self.send_classes(self.classes)

	def send_classes(self, classes, id = None):
		"""Set the classes of a component."""
		if id == None:
			id = self.id
		self.send({"type": "set-class", "id": id, "classes": " ".join(classes)})

	def gen_resize(self, out):
		"""Called to generate the content of resize. The code is generated
		in hierarchical order, from root to leaf components."""
		pass

	def expands_horizontal(self):
		"""Return true to support horizontal expansion."""
		return False

	def expands_vertical(self):
		"""Return true to support vertical expansion."""
		return False

	def get_weight(self):
		try:
			return self.weight
		except AttributeError:
			return 1

	def get_add_models(self):
		"""Called to get additional used modles."""
		return []


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
# console.log("resize " + e.id + ": " + w + " x " + h);
# ui_show_size(e);


class Page:
	"""Implements a page ready to be displayed."""

	def __init__(self, main = None, template = None, parent = None):
		global PAGE_ID
		self.messages = []
		self.main = None
		self.template = template
		if main != None:
			self.set_main(main)
		else:
			self.models = {}
			self.components = {}
		self.id = str(PAGE_ID)
		PAGE_ID += 1
		self.online = False
		self.parent = parent

	def get_id(self):
		return self.id

	def get_template(self):
		return self.template

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
		for m in comp.get_add_models():
			self.add_model(m)

	def set_main(self, main):
		"""Set the main component."""
		self.main = main
		self.components = {}
		self.models = {}
		todo = [main]
		while todo != []:
			c = todo.pop()
			self.on_add(c)
			for cc in c.get_children():
				todo.append(cc)

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
		self.gen_resize(out)

	def gen_content(self, out):
		"""Generate the content."""
		self.main.gen(out)
		self.online = True

	def receive(self, messages, handler):
		"""Called to receive messages and answer. The answer is a
		possibly list of back messages."""

		# manage messages
		for m in messages:
			try:
				id = m["id"]
				if id != "0":
					self.components[id].receive(m, handler)
				else:
					self.manage(m, handler)
			except KeyError:
				handler.log_error("unknown component in %s" % m)

		# manage answers
		res = self.messages
		self.messages = []
		return res

	def on_close(self):
		self.manager.remove_page(self)
		if self.parent != None:
			self.parent.on_close()

	def manage(self, msg, handler):
		"""Manage window messages."""
		#print("DEBUG: closing!")
		a = msg["action"]
		if a == "close":
			self.on_close()
		else:
			handler.log_error("unknown action: %s" % a)

	def gen_resize(self, out):
		"""Called to generate the resize code."""
		if self.main == None:
			out.write("""
		function ui_resize() {
		}
""")
		else:
			self.main.gen_resize(out)
			out.write("""
		function ui_resize() {
			p = document.getElementById("content");
			/*console.log("total: " + ui_content_width(p) + " x " + ui_content_height(p));*/
			resize_%s(ui_content_width(p), ui_content_height(p));
		}
""" % self.main.get_id())

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
		ss = ["basic.css"]
		for m in self.models:
			for s in m.get_style_paths():
				if s not in ss:
					ss.append(s)
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

	def gen_body_attrs(self, out):
		"""Generate body attributes."""
		out.write("""
			onresize="ui_resize()"
			onload="ui_resize()"
			onbeforeunload="ui_close()"
""")


class Application:
	"""Class representing the application and specially provides the initial page."""

	def __init__(self, name,
		version = None,
		authors = [],
		license = None,
		copyright = None,
		description = None,
		website = None
	):
		self.name = name
		self.version = version
		self.license = license
		self.copyright = copyright
		self.description = description
		self.website = website

	def first(self):
		"""Function called to get the first page."""
		return None

