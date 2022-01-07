"""Data/Process-oriented user interface."""

import http.server
import json
import mimetypes
import os.path
import re
import socketserver

from orchid.base import *
from orchid.button import Button
from orchid.label import Label
from orchid.field import Field, is_valid_number
from orchid.group import HGroup, VGroup
from orchid.updater import *
from orchid.editor import Editor
from orchid.console import Console

GEN_RE = re.compile("^\s+<\?\s+(\S+)\s+\?>\s+$")

class Manager:

	def __init__(self, page, template, dirs):
		self.index = page
		self.template = template
		self.dirs = dirs
		self.pages = {}

	def add_page(self, page):
		print(page)
		self.pages[page.get_id()] = page

	def remove_page(self, page):
		del self.pages[page.get_id()]

	def gen_page(self, page, out):
		path = page.get_template()
		if path == None:
			path = self.template
		template = open(path, encoding="utf-8")
		for l in template:
			m = GEN_RE.match(l)
			if m == None:
				out.write(l)
			else:
				cmd = m.group(1)
				if cmd == "content":
					page.gen_content(out)
				elif cmd == "style":
					page.gen_style(out)
				elif cmd == "script":
					page.gen_script(out)
				elif cmd == "resize":
					page.gen_resize(out)
				else:
					error("bad command in %s: %s" % (path, cmd))
		template.close()

	def get_page(self, id):
		return self.pages[id]

	def make_index(self):
		return self.index()

	def get_template(self):
		return self.template

	def get_dirs(self):
		return self.dirs


class Server(http.server.SimpleHTTPRequestHandler):

	def write(self, text):
		self.wfile.write(bytes(text, "utf-8"))

	def do_POST(self):
		length = int(self.headers['content-length'])
		data = self.rfile.read(length)
		msg = json.loads(data)
		print("DEBUG: receive ", msg)
		try:
			page = self.server.manager.get_page(msg["page"])
		except KeyError:
			self.log_error("malformed message: %s" % msg)
			return
		answers = page.receive(msg["messages"], self)
		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.end_headers()
		s = json.dumps({"status": "ok", "answers": answers})
		print("DEBUG: answer ", s)
		self.wfile.write(s.encode("utf-8"))

	def do_GET(self):

		# manage the top-level
		if self.path == "/":
			page = self.server.manager.make_index()
			self.server.manager.add_page(page)
			self.send_response(200)
			self.end_headers()
			self.server.manager.gen_page(page, self)
			return

		# manage other files
		else:
			path = os.path.normpath(self.path)
			if path.startswith("/.."):
				error("out of sandbox access: assets/%s" % path)
				self.send_response(404)
				self.end_headers()
				return
			for dir in self.server.manager.get_dirs():
				rpath = dir + path
				print(rpath)
				if os.path.exists(rpath):
					self.send_response(200)
					(type, _) = mimetypes.guess_type(rpath)
					if type != None:
						self.send_header("Content-type", type)
					else:
						self.warn("no MIME for %s" % rpath)
					self.end_headers()
					file = open(rpath, encoding="utf-8")
					for l in file:
						self.wfile.write(bytes(l, "utf-8"))
					file.close()
					return

		# file not found				
		self.log_error("invalid file: %s" % path)
		self.send_response(404)
		self.end_headers()


def run(page, port=4444, dirs=[]):
	"""Run the UI on the given port."""

	# build the manager
	my_assets = os.path.join(os.path.dirname(__file__), "../assets")
	template = os.path.join(my_assets, "template.html")
	dirs = dirs + [my_assets]
	manager = Manager(page, template, dirs)

	# launch the server
	server = http.server.HTTPServer(("localhost", port), Server)
	server.manager = manager
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	server.server_close()
