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


"""Module definint Displayable interface and basic text display with style."""

import html
import re

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
	"""Test just containing a string."""

	MARKDOWN_RES = [
		(re.compile(r'<'), r'&lt;'),
		(re.compile(r'>'), r'&gt;'),
		(re.compile(r'&'), r'&amp;'),
		(re.compile(r'"'), r'&quot;'),
		(re.compile(r'\*\*(.*)\*\*'), r'<b>\1</b>'),
		(re.compile('__(.*)__'), r'<b>\1</b>'),
		(re.compile(r'\*(.*)\*'), r'<i>\1</i>'),
		(re.compile(r'_(.*)_'), r'<i>\1</i>'),
		(re.compile(r'\n\n'), '<br>')
	]

	@staticmethod
	def wiki_to_html(text, res):
		for (re, pat) in res:
			text = re.sub(re, pat)
		return text

	@staticmethod
	def html(text):
		return Text(text)

	@staticmethod
	def markdown(text):
		return Text(Text.wiki_to_html(text, Text.MARKDOWN_RES))

	@staticmethod
	def plain(text):
		return Text(html.escape(str(text).replace("\n", "<br>")))

	@staticmethod
	def make(content):
		if content.startswith("@html:"):
			return Text.html(content[6:])
		elif content.startswith("@markdown:"):
			return Text.markdown(content[10:])
		else:
			return Text.plain(content)

	def __init__(self, text, clazz=None):
		if clazz is None:
			self.text = text
		else:
			self.text = f'<span class="{clazz}">{text}</span>'

	def gen(self, out):
		out.write(self.text)
