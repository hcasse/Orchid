"""Label component."""

from orchid.base import *

LABEL_MODEL = Model()

class Label(Component):
	"""Component displaying the given content that may be plain or an instance of Displayable."""

	def __init__(self, content):
		Component.__init__(self, LABEL_MODEL)
		self.content = content
		self.add_class("label")

	def finalize(self, page):
		Component.finalize(self, page)
		if isinstance(self.content, Displayable):
			self.content.finalize(page)

	def gen(self, out):
		out.write('<div')
		self.gen_attrs(out)
		out.write('>')
		self.gen_content(out)
		out.write('</div>\n')

	def gen_content(self, out):
		if isinstance(self.content, Displayable):
			self.content.gen(out)
		else:
			out.write(self.content)

	def set_text(self, content):
		self.content = content
		if self.online():
			buf = Buffer()
			self.gen_content(buf)
			self.set_content(str(buf))

BANNER_MODEL = Model()

class Banner(ExpandableComponent):
	"""Display an HTML text that occupies the whole avaiable width,
	like a banner."""
	
	def __init__(self, text):
		ExpandableComponent.__init__(self, BANNER_MODEL)
		self.add_class("banner")
		self.text = text

	def expands_horizontal(self):
		return True

	def gen(self, out):
		out.write('<div')
		self.gen_attrs(out)
		out.write('>')
		out.write(self.text)
		out.write('</div>\n')

		
