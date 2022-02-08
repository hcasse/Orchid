"""Data/Process-oriented user interface."""

from functools import partial
import http.server
import json
import mimetypes
import os.path
import re
import socketserver
import sys
import threading
import time
import webbrowser

from orchid.base import *
from orchid.button import Button
from orchid.label import Label
from orchid.label import Banner
from orchid.field import Field, is_valid_number
from orchid.group import HGroup, VGroup
from orchid.group import Spring
from orchid.updater import *
from orchid.editor import Editor
from orchid.console import Console
from orchid.struct import Header
from orchid.image import Icon, Image

GEN_RE = re.compile("^\s+<\?\s+(\S+)\s+\?>\s+$")

TEXT_MIMES = {
	"application/javascript",
	"text/css",
	"text/csv",
	"text/html",
	"text/javascript",
	"text/plain",
	"text/xml"
}

CMD_MAP = {
	"body-attrs":	Page.gen_body_attrs,
	"content":		Page.gen_content,
	"style": 		Page.gen_style,
	"script": 		Page.gen_script,
	"script-paths": Page.gen_script_paths,
	"style-paths": 	Page.gen_style_paths,
	"title":		Page.gen_title
}

class Manager:

	def __init__(self, app, dirs):
		self.app = app
		self.dirs = dirs
		self.pages = {}

	def add_page(self, page):
		self.pages[page.get_id()] = page
		page.manager = self

	def remove_page(self, page):
		page.manager = None
		del self.pages[page.get_id()]

	def gen_page(self, page, out):
		page.gen(out)

	def get_page(self, id):
		return self.pages[id]

	def make_index(self):
		page = self.app.first()
		self.add_page(page)
		return page

	def get_dirs(self):
		return self.dirs

	def is_completed(self):
		return self.pages == {}


class Server(http.server.SimpleHTTPRequestHandler):

	def write(self, text):
		self.wfile.write(bytes(text, "utf-8"))

	def do_POST(self):
		length = int(self.headers['content-length'])
		data = self.rfile.read(length)
		msg = json.loads(data)
		#print("DEBUG: receive ", msg)
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
		#print("DEBUG: answer ", s)
		self.wfile.write(s.encode("utf-8"))
		if self.server.manager.is_completed():
			#print("DEBUG: closing server")
			self.close_connection = True
			sys.exit(0)

	def do_GET(self):

		# manage the top-level
		if self.path == "/":
			page = self.server.manager.make_index()
			self.send_response(200)
			self.end_headers()
			self.server.manager.gen_page(page, self)
			return

		# manage other files
		else:
			path = os.path.normpath(self.path)
			#print("DEBUG: looking for ", path)
			if path.startswith("/.."):
				self.log_error("out of sandbox access: assets/%s" % path)
				self.send_response(404)
				self.end_headers()
				return
			for dir in self.server.manager.get_dirs():
				rpath = dir + path
				#print("DEBUG: testing ", rpath)
				if os.path.exists(rpath):
					#self.path = rpath
					#print("DEBUG: serving ", self.path)
					#http.server.SimpleHTTPRequestHandler.do_GET(self)
					self.answer_file(rpath)
					return

		# file not found				
		self.log_error("invalid file: %s" % path)
		self.send_response(404)
		self.end_headers()

	def answer_file(self, path):

		# build the header
		self.send_response(200)
		(type, _) = mimetypes.guess_type(path)
		#print(type, path)
		if type == None:
			self.log_error("no MIME for %s" % path)
		else:
			self.send_header("Content-type", type)
		self.end_headers()

		# send text file
		if type in TEXT_MIMES:
			file = open(path, encoding="utf-8")
			for l in file:
				self.wfile.write(bytes(l, "utf-8"))
			file.close()

		# send binary file
		else:
			file = open(path, "rb")
			while True:
				b = file.read(4096)
				#print(b)
				if b == b'':
					break
				else:
					self.wfile.write(b)
			file.close()


def open_browser(port):
	time.sleep(.5)
	webbrowser.open("http://localhost:%d" % port)


def run(app, port=4444, dirs=[], browser = True):
	"""Run the UI on the given port."""

	# build the manager
	my_assets = os.path.realpath(os.path.join(os.path.dirname(__file__), "../assets"))
	dirs = dirs + [my_assets]
	manager = Manager(app, dirs)

	# launch the server
	server = http.server.HTTPServer(("localhost", port), Server)
	server.manager = manager
	if browser:
		threading.Thread(target=partial(open_browser, port)).start()
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	server.server_close()
