"""Orchid base classes and definitions. """

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


class Component(Subject):
	"""Component to build a user-interface."""

	def __init__(self, model):
		Subject.__init__(self)
		self.model = model
		self.page = None

	def get_id(self):
		return str(id(self))

	def get_model(self):
		return self.model

	def get_page(self):
		return page

	def get_children(self):
		return []

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

	def set_class(self, cls):
		"""Change the class of the component."""
		self.send({"type": "class", "id": self.get_id(), "class": cls})

	def add_class(self, cls):
		"""Add a class of the component."""
		self.send({"type": "add-class", "id": self.get_id(), "class": cls})

	def remove_class(self, cls):
		"""Add a class of the component."""
		self.send({"type": "remove-class", "id": self.get_id(), "class": cls})

	def gen_resize(self):
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


class Page:
	"""Implements a page ready to be displayed."""

	def __init__(self, main = None, template = None):
		self.messages = []
		self.main = None
		self.template = template
		if main != None:
			self.set_main(main)
		else:
			self.models = {}
			self.components = {}

	def get_id(self):
		return str(id(self))

	def get_template(self):
		return self.template

	def on_add(self, comp):
		"""Called each time a component is added."""
		comp.page = self
		self.components[comp.get_id()] = comp
		m = comp.get_model()
		while m != None:
			try:
				self.models[m] += 1
				m = None
			except KeyError:
				self.models[m] = 1
				m = m.get_parent()

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

	def gen_content(self, out):
		"""Generate the content."""
		self.main.gen(out)

	def receive(self, messages, handler):
		"""Called to receive messages and answer. The answer is a
		possibly list of back messages."""

		# manage messages
		for m in messages:
			try:
				comp = self.components[m["id"]]
				comp.receive(m, handler)
			except KeyError:
				handler.log_error("unknown component in ", m)

		# manage answers
		res = self.messages
		self.messages = []
		return res

