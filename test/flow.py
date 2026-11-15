#!/usr/bin/python3

"""Flow component test."""

import html
from collections.abc import Iterable

import orchid as orc
from orchid.util import Buffer
from orchid.button import Button

MODEL = orc.Model(
	script="""

""",
	style="""
.flow span {
	margin: 2px;
}
"""
)

class Base:
	"""Base class for Token and Par. Supports CSS classes and attributes."""

	def __init__(self, classes=None, attrs=None):
		if classes is None:
			self.classes = set()
		elif isinstance(classes, str):
			self.classes = set([str])
		else:
			self.classes = set(classes)
		if attrs is None:
			self.attrs = {}
		else:
			self.attrs = dict(attrs)

	def gen_attrs(self, out):
		"""Generate attributes."""

		out.write(" style=\"")
		for (name, val) in self.attrs.items():
			out.write(f"{name}:{html.escape(val)};")
		out.write("\"")

		if self.classes:
			out.write(f" class=\"{' '.join(self.classes)}\"")


class Token(Base):
	"""A token in the flow."""

	def __init__(self, text, classes=None, attrs=None):
		Base.__init__(self, classes, attrs)
		self.text = text

	def gen(self, out):
		"""Generate the word in HTML."""
		out.write("<span")
		self.gen_attrs(out)
		out.write(f">{html.escape(self.text)}</span>")


class Par(Base):
	"""A paragraph in the flow, made of several tokens."""

	def __init__(self, tokens=None, classes=None, attrs=None):
		Base.__init__(self, classes, attrs)
		if tokens is None:
			self.content = []
		elif isinstance(tokens, str):
			self.content = [Token(tokens)]
		elif isinstance(tokens, Iterable):
			self.content = []
			for token in tokens:
				self.content.append(Par.make_token(token))
		else:
			self.content = [Par.make_token(tokens)]
		self.id = None
		self.parent = None

	@staticmethod
	def make_token(obj):
		"""Build a token from the object."""
		if isinstance(obj, Token):
			return obj
		else:
			return Token(str(obj))

	def add(self, token, at=None, before=False):
		"""Add a token to the paragraph.
		Relatively to token at, before if true, after else."""
		token = Par.make_token(token)
		if at is None:
			if before:
				self.content.append(token)
			else:
				self.content.insert(0, token)
		else:
			i = self.content.index(at)
			if before:
				self.content.insert(i, token)
			else:
				self.content.insert(i+1, token)

	def remove(self, token):
		"""Remove a token from the paragraph."""
		self.content.remove(token)

	def gen(self, out):
		"""Generate the paragraph."""
		out.write("<div")
		self.gen_attrs(out)
		out.write(">")
		for token in self.content:
			token.gen(out)
		out.write("</div>")


class Component(orc.Component):
	"""Component showing a text whioch some parts can be edited. The text is
	made of paragraphs (class Par) that, in turn, are made of tokens (class Token).

	A style expressed in CSS can be attached to the flow component and used with
	different paragraph and component. The flow itself has for class "flow"
	and paragraphs are put in "<div>" and tokens in "<span>"."""
	styles = set()

	def __init__(self, pars=None, flow_style=None):
		orc.Component.__init__(self, MODEL)
		if pars is None:
			self.content = []
		elif isinstance(pars, str):
			self.content = [Par(pars)]
		elif isinstance(pars, Iterable):
			self.content = []
			for par in pars:
				self.content.append(Component.make_par(par))
		else:
			self.content = [Component.make_par(par)]
		self.content = pars
		self.add_class("flow")
		self.id_count = 0
		self.flow_style = flow_style

	def finalize(self, page):
		if self.flow_style is not None and self.flow_style not in Component.styles:
			Component.styles.add(self.flow_style)
			page.add_model(orc.Model(style=self.flow_style))
		orc.Component.finalize(self, page)

	@staticmethod
	def make_par(obj):
		"""Build a paragraph from the object."""
		if isinstance(obj, Par):
			return obj
		else:
			return Par(obj)

	def add(self, par, at=None, before=False):
		"""Add a paragraph to the flow.
		Relatively to the paragraph at.
		Before if true, after else."""
		par = Component.make_par(par)
		par.id = f"{self.get_id()}-{self.id_count}"
		self.id_count += 1
		par.parent = self
		if at is None:
			if before:
				pos = 0
			else:
				pos = len(self.content)
		else:
			i = self.content.index(at)
			if before:
				pos = i
			else:
				pos = i + 1
		self.content.insert(pos, par)
		if self.is_shown():
			buf = Buffer()
			par.gen(buf)
			self.insert_content(str(buf), pos)

	def remove(self, par):
		"""Remove a paragraph."""
		i = self.content.index(par)
		del self.content[i]
		self.remove_content(i)

	def on_token_add(self, par, token, pos):
		"""Callback from paragraph when token is added."""
		pass

	def on_token_remove(self, par, pos):
		"""Callback from paragraph when toke is remove."""

	def gen(self, out):
		out.write('<div');
		self.gen_attrs(out);
		out.write('>')
		for par in self.content:
			par.gen(out)
		out.write('</div>')

	def expands_horizontal(self):
		return True

	def expands_vertical(self):
		return True


class MyPage(orc.Page):

	def __init__(self, app):
		self.flow = Component([
			Par(["First", "paragraph"]),
			Par(["Second","paragraph"]),
		])
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.Label("Flow Test"),
				self.flow,
				orc.HGroup([
					orc.Button("Add par", on_click=self.add_par)
				])
			]),
			app = app
		)

	def add_par(self):
		self.flow.add("Added par!")

orc.Application("Flow Test", first=MyPage).run()

