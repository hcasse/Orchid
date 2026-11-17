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

import html
import os.path
from typing import Callable
import xml.etree.ElementTree as ET

from orchid.base import Model, Component, PLAIN_MODEL, Page
from orchid.control import Harness, ClickNMove
from orchid.util import Buffer, Out, escape_attr


XMLNS = "http://www.w3.org/2000/svg"

class Error(Exception):
	"""SVG error."""

	def __init__(self, msg: str):
		self.msg = msg

	def __str__(self):
		return self.msg


# standard dash arrays
DASHED = [5, 5]
DOTTED = [1, 1]

def adjust(key):
	return key.replace('_', '-')

def make_event_id(id, event):
	if isinstance(id, Shape):
		id = str(id.num)
	return f"{id}-{event}"



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
		out.write(f"scale({self.sx}, {self.sy})")
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
		out.write(f"translate({self.dx}, {self.dy})")
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
	"""Represents a shape in the canvas.
	All shapes supports a default set of attributes:
	* `stroke` -- color
	* `stroke_width` -- size
	* `stroke_opacity` -- [0, 1]
	* `stroke_linecap` -- { butt, round, square }
	* `stroke-linejoin` -- { round, bevel, miter }
	* `font-family` -- font name
    * `font-size` -- size
	* `font-style` -- { normal, italic }
    * `font-weight` -- { normal, bold, 100-900}
    * `fill` -- color
	"""

	def __init__(self, **args):
		self.parent = None
		self.num = 0
		self.attrs = {**args}
		self.trans = None

	def get_id(self):
		return f"svg-{self.parent.num}-{self.num}"

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
		return " ".join([f" {adjust(key)}='{str(val)}'"
			for (key, val) in self.attrs.items()])

	def gen(self, out):
		"""Called to generate the shape."""
		pass

	def set_attr(self, att, val):
		"""Set an attribute of the shape. If val is None, remove it."""
		if val is None:
			self.remove_attr(att)
		else:
			self.attrs[att] = val
			if self.parent.online():
				self.parent.get_page().set_direct_attr(
					self.get_id(), adjust(att), val)

	def remove_attr(self, att):
		"""Remove an attribute."""
		del self.attrs[att]
		if self.parent.online():
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

	def get_width(self):
		"""Get the width of the shape."""
		return 1

	def get_height(self):
		"""Get the height of the shape."""
		return 1


class Circle(Shape):
	"""A circle."""

	def __init__(self, x, y, r, **args):
		Shape.__init__(self, **args)
		self.x = x
		self.y = y
		self.r = r

	def gen(self, out):
		out.write(f"<circle id='{self.get_id()}' cx='{self.x}' cy='{self.y}' \
			r='{self.r}' {self.get_attrs()}/>")

	def get_width(self):
		return self.r * self.r

	def get_height(self):
		return self.r * self.r


class Text(Shape):
	"""A text."""

	def __init__(self, x, y, text, **args):
		Shape.__init__(self, **args)
		self.x = x
		self.y = y
		self.text = text

	def gen(self, out):
		out.write(f'<text x="{self.x}" y="{self.y}" {self.get_attrs()}">{html.escape(self.text)}</text>')


class Line(Shape):
	"""A line."""

	def __init__(self, x1, y1, x2, y2, **args):
		Shape.__init__(self, **args)
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

	def gen(self, out):
		out.write(f"<line id='{self.get_id()}' x1='{self.x1}' y1='{self.y1}' \
			x2='{self.x2}' y2='{self.y2}' {self.get_attrs()}/>")

	def get_width(self):
		return abs(self.x1 - self.x2)

	def get_height(self):
		return abs(self.y1 - self.y2)


class Rect(Shape):
	"""A rectangle."""

	def __init__(self, x, y, w, h, **args):
		Shape.__init__(self, **args)
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	def gen(self, out):
		out.write(f"<rect id='{self.get_id()}' x='{self.x}' y='{self.y}' \
			width='{self.w}' height='{self.h}' {self.get_attrs()}/>")

	def get_width(self):
		return self.w

	def get_height(self):
		return self.h


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
			added += f" width='{self.w}'"
		if self.h:
			added += f" height='{self.h}'"
		out.write(f"<image id='{self.get_id()}' href='{self.url}' \
			x='{self.x}' y='{self.y}' {added}/>")

	def finalize(self):
		Shape.finalize(self)
		self.url = self.parent.publish(self.path)

	def get_width(self):
		return self.w

	def get_height(self):
		return self.h


class Content(Shape):

	def __init__(self, content, width=1, height=1, **args):
		Shape.__init__(self, **args)
		self.content = content
		self.width = width
		self.height = height

	def finalize(self):
		Shape.finalize(self)
		self.content = self.content.replace("{id}", self.get_id())

	def gen(self, out):
		out.write(f"<g id='{self.get_id()}' {self.get_attrs()}>")
		out.write(self.content)
		out.write("</g>")

	def set_direct_attr(self, id, att, val):
		self.parent.get_page().set_direct_attr(id, att, val)

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height


class SVGImage(Shape):

	def __init__(self, **args):
		Shape.__init__(self, **args)
		self.content = ""
		self.width = -1
		self.height = -1

	def gen(self, out: Out) -> None:
		out.write(f"<g id='{self.get_id()}' {self.get_attrs()}>")
		out.write(self.content)
		out.write("</g>")

	def get_width(self) -> int:
		return self.width

	def get_height(self) -> int:
		return self.height

	@staticmethod
	def from_buffer(buffer: str, **args) -> "SVGImage":
		"""Build an SVGImage from a buffer."""
		image = SVGImage(**args)
		try:
			root = ET.fromstring(buffer)
		except ET.ParseError as exn:
			raise Error(f"bad content: {exn}")
		if root.tag != "{http://www.w3.org/2000/svg}svg":
			raise Error("Not SVG file")
		box = root.get("viewBox")
		image.content = buffer
		if box is not None:
			comps = box.split(" ")
			image.width = int(float(comps[2]))
			image.height = int(float(comps[3]))
		return image


class Canvas(Component, Harness):
	"""A canvas that support CFG primitives."""
	SVG_NUM = 0
	MODEL = Model(
		"svg-canvas",
		script_paths=["svg.js"]
	)

	def __init__(self):
		Component.__init__(self, self.MODEL)
		Harness.__init__(self)
		self.set_attr("xmlns", XMLNS)
		self.add_class("svg-canvas")
		self.num = Canvas.SVG_NUM
		Canvas.SVG_NUM += 1
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
			shape.finalize()
			if self.online():
				buf = Buffer()
				shape.gen(buf)
				self.call("svg_append",
					{ "id": self.get_id(), "content": str(buf) })
		return shape

	def gen(self, out):
		out.write("<svg ")
		self.gen_attrs(out)
		self.gen_harness_attrs(out)
		out.write(f'><template id="svg-{self.num}-temp"></template>')
		for shape in self.shapes:
			shape.gen(out)
		out.write("</svg>")

	def publish(self, path):
		try:
			url = self.image_map[path]
		except KeyError:
			url = f"/svg/{path}"
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
		self.finalize_harness(page)

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

	def rect(self, x, y, w, h, **args):
		"""Draw a rectangle."""
		return self.record(Rect(x, y, w, h, **args))

	def text(self, x, y, text, **args):
		"""Draw a text."""
		return self.record(Text(x, y, text, **args))

	def remove(self, shape):
		"""Remove an object."""
		if self.online():
			self.call("svg_remove", {"id": shape.get_id()})
		self.shapes.remove(shape)

	def remove_all(self):
		"""Remove all the shapes in the canvas."""
		self.shapes = []
		if self.online() and self.is_shown():
			self.call("svg_remove_all", { "id": self.get_id() })

	def image(self, path, x, y, w=None, h=None, **args):
		"""Draw an image."""
		return self.record(Image(path, x, y, w, h, **args))

	def svg_from_buffer(self, buffer: str, **args) -> Shape:
		"""Draw an SVG image from a string buffer."""
		return self.record(SVGImage.from_buffer(buffer, **args))

	def content(self, content, **args):
		"""Build an image from a straight content."""
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
		return f'svg_on_event("{self.get_id()}", "{make_event_id(id, event)}");'

	def receive(self, msg, handler):
		try:
			action = msg["action"]
			if action == "event":
				self.events[msg["event"]]()
			elif action == "size":
				width = msg["width"]
				height = msg["height"]
				for fun in self.size_funs:
					fun(width, height)
				self.size_funs = []
		except KeyError:
			Component.receive(self, msg, handler)
