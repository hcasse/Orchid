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

def adjust(key):
	return key.replace('_', '-')

def make_event_id(id, event):
	if isinstance(id, Shape):
		id = str(id.num)
	return "%s-%s" % (id, event)

class Transform:
	"""A transformation in SVG."""

	def __init__(self):
		self.parent = None
		self.next = None

	def gen(self, out):
		"""Generate the text for the transformation."""
		if self.next is not None:
			self.next.gen(out)


class Scale(Transform):
	"""Scale transformation."""

	def __init__(self, sx, sy = None):
		Transform.__init__(self)
		self.sx = sx
		self.sy = sy if sy is not None else sx

	def gen(self, out):
		out.write("scale(%f, %f)" % (self.sx, self.sy))
		Transform.gen(self, out)

	def set(self, sx, sy = None):
		self.sx = sx
		self.sy = sy if sy is not None else sx
		self.parent.update_transform()

class Translate(Transform):
	"""Translation."""

	def __init__(self, dx, dy):
		Transform.__init__(self)
		self.dx = dx
		self.dy = dy

	def gen(self, out):
		out.write("translate(%f, %f)" % (self.dx, self.dy))
		Transform.gen(self, out)

	def move(self, dx, dy):
		self.dx += dx
		self.dy += dy
		self.parent.update_transform()

	def moveAt(self, dx, dy):
		self.dx = dx
		self.dy = dy
		self.parent.update_transform()
	

class Shape:
	"""Represents a shape in the canvas."""

	def __init__(self, **args):
		self.parent = None
		self.num = None
		self.attrs = dict(**args)
		self.trans = None

	def get_id(self):
		return "svg-%d-%d" % (self.parent.num, self.num)

	def finalize(self):
		pass

	def make_transform(self):
		buf = Buffer()
		self.trans.gen(buf)
		self.attrs["transform"] = str(buf)
	
	def update_transform(self):
		self.make_transform()
		if self.parent is not None and self.parent.online():
			self.parent.get_page().set_direct_attr(
				self.get_id(), "transform", self.attrs["transform"])

	def get_attrs(self):
		return " ".join([" %s='%s'" % (adjust(key), str(val))
			for (key, val) in self.attrs.items()])
			
	def gen(self, id, out):
		"""Called to generate the shape."""
		pass

	def set_attr(self, att, val):
		"""Set an attribute of the shape. If val is None, remove it."""
		if val == None:
			self.remove_attr(att)
		else:
			self.attrs[att] = val
			if self.parent.online():
				self.parent.get_page().set_direct_attr(
					self.get_id(), adjust(att), val)

	def remove_attr(self, att):
		"""Remove an attribute."""
		del self.attrs[att]
		if self.online():
			self.parent.get_page().remove_direct_attr(
				self.get_id(), adjust(att))

	def add_event(self, event, fun):
		"""Add an event on the current shape. event is any usual HTML event.
		fun is the function to call when the event is triggered."""
		self.parent.add_event(self, event, fun)

	def remove_event(self, event):
		"""Remove the gien event on the current shape."""
		self.parent.remove_event(self, event)

	def add_transformation(self, t):
		"""Add a transformation."""
		t.next = self.trans
		self.trans = t
		self.update_transform()
		return t

	def scale(self, sx, sy = None):
		"""Scale the shape."""
		return self.add_transformation(Scale(sx, sy))

	def translate(self, dx, dy):
		"""Scale the shape."""
		return self.add_transformation(Translate(dx, dy))


class Circle(Shape):
	"""A circle."""

	def __init__(self, x, y, r, **args):
		Shape.__init__(self, **args)
		self.x = x
		self.y = y
		self.r = r

	def gen(self, out):
		out.write("<circle id='%s' cx='%d' cy='%d' r='%d' %s/>" %
			(self.get_id(), self.x, self.y, self.r, self.get_attrs()))


class Line(Shape):
	"""A line."""

	def __init__(self, x1, y1, x2, y2, **args):
		Shape.__init__(self, **args)
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

	def gen(self, out):
		out.write("<line id='%s' x1='%d' y1='%d' x2='%d' y2='%d' %s/>" % (self.get_id(), self.x1, self.y1, self.x2, self.y2, self.get_attrs()))


class Image(Shape):

	def __init__(self, path, x, y, w=None, h=None, **args):
		Shape.__init__(self, **args)
		self.path = os.path.normpath(path)
		self.url = None
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	def gen(self, out):
		added = ""
		if self.w:
			added += " width='%d'" % self.w
		if self.h:
			added += " height='%d'" % self.h
		out.write("<image id='%s' href='%s' x='%d' y='%d' %s/>" %
			(self.get_id(), self.url, self.x, self.y, added))

	def finalize(self):
		Shape.finalize(self)
		self.url = parent.publish(self.path)


class Content(Shape):

	def __init__(self, content, **args):
		Shape.__init__(self, **args)
		self.content = content

	def finalize(self):
		Shape.finalize(self)
		self.content = self.content.replace("{id}", self.get_id())

	def gen(self, out):
		out.write("<g id='%s' %s>" % (self.get_id(), self.get_attrs()))
		out.write(self.content)
		out.write("</g>")

	def set_direct_attr(self, id, att, val):
		self.parent.get_page().set_direct_attr(id, att, val)


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
		self.shapes = []
		self.events = {}
		
	def record(self, shape):
		shape.parent = self
		shape.num = self.child_num
		self.child_num += 1
		self.shapes.append(shape)
		if self.get_page() is not None:
			shape.finalize(self)
			if self.online():
				buf = Buffer()
				shape.gen(buf)
				self.call("svg_append",
					{ "id": self.get_id(), "content": str(buf) })
		return shape

	def gen(self, out):
		out.write("<svg ")
		self.gen_attrs(out)
		out.write('><template id="svg-%d-temp"></template>' % self.num)
		for shape in self.shapes:
			shape.gen(out)
		out.write("</svg>")

	def publish(self, path):
		try:
			url = self.image_map[path]
		except KeyError:
			url = "/svg/%s" % path
			self.image_map[path] = url
			if self.online():
				self.publish_server(path, url)
		return url

	def publish_server(self, path, url):
		if os.path.splitext(path) in [".svg"]:
			self.get_page().publish_text_file(url, path)
		else:
			self.get_page().publish_file(url, path)

	def finalize(self, page):
		Component.finalize(self, page)
		for shape in self.shapes:
			shape.finalize()

	def expands_horizontal(self):
		return True

	def expands_vertical(self):
		return True

	def circle(self, x, y, r, **args):
		"""Draw a circle at point(x, y) of ray r."""
		return self.record(Circle(x, y, r, **args))

	def line(self, x1, y1, x2, y2, **args):
		"""Draw a line."""
		return self.record(Line(x1, y1, x2, y2, **args))

	def remove(self, shape):
		"""Remove an object."""
		if self.online():
			self.call("svg_remove", {"id": shape.get_id()})
		self.shapes.remove(shape)

	def image(self, path, x, y, w=None, h=None, **args):
		"""Draw an image."""
		return self.record(Image(path, x, y, w, h, **args))

	def content(self, content, **args):
		return self.record(Content(content, **args))

	def add_event(self, id, event, fun):
		"""Add an event handler on SVG shapes. id may be a string or a shape."""
		self.events[make_event_id(id, event)] = fun
		if isinstance(id, Shape):
			id.set_attr(event, self.gen_event_call(id, event))

	def remove_event(self, id, event):
		"""Remove an event handler. id may be a string or a shape."""
		del self.events[make_event_id(id, event)]
		if isinstance(id, Shape):
			id.remove_attr(event, self.gen_event_call(id, event))

	def gen_event_call(self, id, event):
		"""Generate code to invoke event. id may be a shape or any string."""
		return 'svg_on_event("%s", "%s");' % (self.get_id(), make_event_id(id, event))

	def receive(self, m, h):
		try:
			self.events[m["event"]]()
		except KeyError:
			Component.receive(self, m, h)
