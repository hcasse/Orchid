"""Field components."""

from orchid.base import *

class FieldModel(Model):

	def gen_script(self, out):
		out.write("""
		function field_change(id, value) {
			ui_send({id: id, action: "change", value: value});
		}
""")		

FIELD_MODEL = FieldModel()

class Field(Component):

	def __init__(self,
		label = None,
		init = "",
		size = None,
		is_valid = lambda x: True,
		weight = None
	):
		Component.__init__(self, FIELD_MODEL)
		self.content = str(init)
		self.label = label
		self.size = size
		self.valid = True
		self.is_valid = is_valid
		if weight == None:
			if size != None:
				weight = (size, 0)
			else:
				weight = (1, 0)
		self.weight = weight
		self.set_style("display", "flex")

	def get_content(self):
		return self.content

	def gen(self, out):
		if self.label != None:
			out.write('<label for="%s-field" class="field">%s</label>' % (self.get_id(), self.label))
		out.write('<input id="%s-field" class="field" type="text"' % self.get_id())
		out.write(' value="%s"' % self.content)
		out.write(' oninput="field_change(\'%s\', this.value)"' % self.get_id())
		if self.size != None:
			out.write(' size="%d"' % self.size)
		self.gen_attrs(out)
		out.write('/>')

	def check_validity(self):
		valid = self.is_valid(self.content)
		if valid != self.valid:
			self.valid = valid
			if valid:
				self.send_classes(["field", "valid"], "%s-field" % self.get_id())
			else:
				self.send_classes(["field", "invalid"], "%s-field" % self.get_id())
			self.update_observers(self)

	def receive(self, m, h):
		if m["action"] == "change":
			content = m["value"]
			if self.content != content:
				print("content = %s" % self.content)
				self.content = content
				self.update_observers(self)
				self.check_validity()
		else:
			Component.receive(self, m, h)


def is_valid_number(x):
	"""Test if the string is numeric."""
	return x.isnumeric()
