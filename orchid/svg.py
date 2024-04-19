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

"""This module mainly provides an SVG canvas. It provides also
useful constants.

* for stroke-dash-array: DASHED, DOTTED.
"""

import os.path

from orchid import *
from orchid.util import *

MODEL = Model(
	"svg-canvas",
	script_paths=["svg.js"]
)

XMLNS = "http://www.w3.org/2000/svg"

SVG_NUM = 0

# standard dash arrays
DASHED = [5, 5]
DOTTED = [1, 1]

class Canvas(Component):
	"""A canvas that support CFG primitives."""

	def __init__(self):
		global SVG_NUM
		Component.__init__(self, MODEL)
		self.set_attr("xmlns", XMLNS)
		self.add_class("svg-canvas")
		self.num = SVG_NUM
		SVG_NUM = SVG_NUM + 1;
		self.child_num = 0
		self.image_map = {}
		
		self.stroke = None
		self.stroke_width = None
		self.stroke_linecap = None
		self.stroke_linejoin = None
		self.fill = None
		self.stroke_dasharray = None
		self.lookup = None

	def gen(self, out):
		out.write("<svg ")
		self.gen_attrs(out)
		out.write('><template id="svg-%d-temp"></template></svg>' % self.num)

	def expands_horizontal(self):
		return True

	def expands_vertical(self):
		return True

	def get_lookup(self):
		if self.lookup is None:
			buf = Buffer()
			if self.stroke:
				buf.write(' stroke="%s"' % self.stroke)
			if self.stroke_width:
				buf.write(' stroke-width="%s"' % self.stroke_width)
			if self.stroke_linecap:
				buf.write(' stroke-linecap="%s"' % self.stroke_linecap)
			if self.stroke_linejoin:
				buf.write(' stroke-linejoin="%s"' % self.stroke_linejoin)
			if self.fill:
				buf.write(' fill="%s"' % self.fill)
			if self.stroke_dasharray:
				buf.write(' stroke-dasharray="%s"' % ",".join(self.stroke_dasharray))
			self.lookup = str(buf)
		return self.lookup

	def next_num(self):
		num = self.child_num
		self.child_num = self.child_num + 1
		return num

	def set_stroke(self, stroke):
		"""Change stroke (draw color)."""
		self.stroke = stroke
		self.lookup = None

	def set_stroke_width(self, width):
		"""Change the stroke width."""
		self.stroke_width = width
		self.lookup = None

	def set_fill(self, fill):
		"""Set the fill color."""
		self.fill = fill
		self.lookup = None

	def circle(self, cx, cy, r):
		"""Draw a circle at point(cx, cy) of ray r."""
		num = self.next_num()
		self.call("svg_append",
			{
				"id": self.get_id(),
				"content": '<circle id="svg-%d-%d" cx="%d" cy="%d" r="%d" %s/>' % (self.num, num, cx, cy, r, self.get_lookup())
			}
		)
		return num

	def line(self, x1, y1, x2, y2):
		"""Draw a line."""
		num = self.next_num()
		self.call("svg_append",
			{
				"id": self.get_id(),
				"content": '<line id="svg-%d-%d" x1="%d" y1="%d" x2="%d" y2="%d" %s/>' % (self.num, num, x1, y1, x2, y2, self.get_lookup())
			}
		)
		return num

	def remove(self, num):
		"""Remove an object."""
		self.call("svg_remove", {"id": "svg-%d-%d" % (self.num, num)})

	def draw_image(self, path, x, y, w=None, h=None):
		"""Draw an image."""
		path = os.path.normpath(path)
		try:
			url = self.image_map[path]
		except KeyError:
			url = "/svg/%s" % path
			if os.path.splitext(path) in [".svg"]:
				self.get_page().publish_text_file(url, path)
			else:
				self.get_page().publish_file(url, path)
		added = ""
		if w:
			added += " width='%d'" % w
		if h:
			added += " height='%d'" % h
		num = self.next_num()
		self.call("svg_append",
			{
				"id": self.get_id(),
				"content": "<image id='svg-%d-%d' href='%s' x='%d' y='%d' %s/>" % (self.num, num, url, x, y, added)
			}
		)
		return num

	def inject(self, content, replace_id=False):
		"""Inject raw SVG in the image. If replace_id is True, replace any instance of "{id}
		by a unique id for the container of this object."""
		num = self.next_num()
		id = self.get_object_id(num)
		if replace_id:
			content = content.replace("{id}", id)
		self.call("svg_append",
			{
				"id": self.get_id(),
				"content": "<g  id='%s'>%s</g>" % (id, content)
			}
		)
		return num

	def get_object_id(self, num, suffix = ""):
		"""Get the identifier for the given object number. Add the suffix if provided."""
		return "svg-%d-%d%s" % (self.num, num, suffix)
