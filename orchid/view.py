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

"""Module imlementing components allowing to view comple data."""

from orchid.base import Model, Component

class InteractiveViewModel(Model):

	def __init__(self, parent = None):
		Model.__init__(self, parent)

	def gen_script(self, out):
		out.write("""

function iview_reset(v) {
	v.scale = 1.;
	v.step = .1;
	v.dx = 0;
	v.dy = 0;
	v.px = 0;
	v.py = 0;
	v.pan = false;
}

function iview_new(n) {
	v = { node: n }
	iview_reset(v);
	return v;
}

function view_transform(v) {
	var t =
		`scale(${v.scale}, ${v.scale})`;
	v.node.children[0].style.transform = t;
}

function view_onmousedown(v, e) {
	if(e.button == 0) {
		v.pan = true;
		v.px = e.x;
		v.py = e.y;
	}
}

function view_onmousemove(v, e) {
	if(v.pan) {
		var dx = e.x - v.px;
		var dy = e.y - v.py;
		CFG.px = e.x;
		CFG.py = e.y;
		CFG.dx = v.dx + dx / v.scale;
		CFG.dy = v.dy + dy / v.scale;
		view_transform(v);
	}
}

function view_onmouseup(v, e) {
	if(e.button == 0)
		v.pan = false;
}

function view_onwheel(v, e) {
	if(e.wheelDelta > 0) {
		if(v.scale > v.step)
			v.scale = v.scale - v.step;
	}
	else
		v.scale = v.scale + v.step;
	view_transform(v);
}

""")

INTERACTIVE_VIEW_MODEL = InteractiveViewModel()


class InteractiveView(Component):
	"""View structured data with move/zoom actions."""

	def __init__(self,
		init = None,
		path = None,
		mime = None,
		model = INTERACTIVE_VIEW_MODEL
	):
		Component.__init__(self, model)
		self.text = None
		self.path = None
		self.mime = None
		if init is not None:
			self.text = init
		elif path is not None:
			self.path = path
		if self.mime is None:
			self.mime = mime
		self.add_class("interactive-view")
		self.url = "/interactive-view/" + self.get_id()

	def display(self, path = None, text = None, mime = None):
		"""Set the content of a view. If neither path,
		nor text is given, the view is cleared."""

		# set the state
		self.mime = mime
		if path is not None:
			self.path = path
			self.text = None
		elif text is not None:
			self.text = text
			self.path = None
			if self.mime is None:
				self.mime = "text/plain"
		else:
			self.path = None
			self.text = ""
			self.mime = None

		# show the content
		self.publish()
		self.send({
			"type": "download",
			"id": self.get_id(),
			"path": self.url
		})

	def publish(self):
		if self.text is not None:
			self.get_page().publish_text_file(self.url, self.text)
		elif self.path is not None:
			self.get_page().publish_file(self.url, self.path)

	def gen(self, out):
		out.write("<div")
		self.gen_attrs(out)
		out.write("></div>\n")
		self.publish()

	def expands_horizontal(self):
		return True

	def expands_vertical(self):
		return True
