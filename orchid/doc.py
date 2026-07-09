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

"""Module proposing a pane to display and navigate in the documentation
of an application."""

from urllib.parse import urlparse

import orchid as orc
from orchid import base
from orchid import group
from orchid import models
from orchid import listview

class Body(base.Component):
	"""Display for the documentation."""

	MODEL = base.Model("orchid.docs.body")

	def __init__(self):
		base.Component.__init__(self, self.MODEL)
		self.add_class("docs-body")
		self.content = ""

	def show(self, url):
		"""Display the URL in the component."""
		pass

	def expands_horizontal(self):
		return True

	def expands_vertical(self):
		return True

	def gen(self, out):
		out.write('<div ')
		self.gen_attrs(out)
		out.write('>')
		out.write(self.content)
		out.write('</div>')

COUNTER = 0


class Pane(group.Row, models.ListObserver):
	"""Display a document made of a collection of HTML documents."""

	MODEL = base.Model("orchid.docs", parent=group.Row.MODEL)

	def __init__(self, docs):
		"""Build a documentation. docs is a list of pairs (title, URL)."""
		assert docs
		self.titles = listview.ListView([doc[0] for doc in docs]).set_weight(1)
		self.title = orc.Label(docs[0][0]).add_class("docs-title")
		self.body = Body().set_weight(4)
		group.Row.__init__(self,
			[self.titles, group.Column([self.title, self.body]).set_weight(4)],
			model=self.MODEL)
		self.docs = docs
		self.map = {}
		global COUNTER
		self.index = COUNTER
		COUNTER += 1

	def finalize(self, page):
		group.Row.finalize(self, page)

	def on_show(self):
		group.Row.on_show(self)
		self.titles.get_selection().add_observer(self)

	def on_hide(self):
		self.titles.get_selection.remove_observer(self)
		group.Row.on_hide(self)

	def gen(self, out):
		self.body.content = self.gen_doc(0)
		group.Row.gen(self, out)

	def make_local_url(self, url):
		return f"/doc-{self.index}/{url}"

	def gen_doc(self, index):
		"""Generate documentation content as a string."""
		(title, url) = self.docs[index]
		if title not in self.map:
			if urlparse(url).scheme == "":
				path = url
				url = self.make_local_url(url)
				self.get_page().publish_file(url, path, mime="text/html")
			self.map[title] = url
		return f'<iframe src="{self.map[title]}" width="100%" height="100%" style="border: none;"></iframe>'

	def on_append(self, i):
		self.title.set_text(self.docs[i][0])
		self.body.set_content(self.gen_doc(i))
