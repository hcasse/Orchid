"""Classes in charge of HTTP communication."""

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
from orchid.base import Page

class Provider:
	"""Interface of objects providing content."""

	def add_headers(self, handler):
		"""Get MIME type for the content.
		None if there is no content."""
		return None

	def gen(self, out):
		"""Generate the content on the given output."""
		pass


class FileProvider(Provider):

	def __init__(self, path, mime = None):
		self.path = path
		if mime == None:
			self.mime = mimetypes.guess_type(path)[0]
		else:
			self.mime = mime

	def add_headers(self, handler):
		if self.mime != None:
			handler.send_header("Content-type", self.mime)

	def gen(self, out):

		# send text file
		if self.mime in TEXT_MIMES:
			file = open(self.path, encoding="utf-8")
			for l in file:
				out.write(bytes(l, "utf-8"))
			file.close()

		# send binary file
		else:
			file = open(self.path, "rb")
			while True:
				b = file.read(4096)
				if b == b'':
					break
				else:
					out.write(b)
			file.close()

		# success
		return 200


class PageProvider(Provider):

	def __init__(self, page):
		self.page = page
	
	def add_headers(self, handler):
		handler.send_header("Content-type", "text/html")

	def gen(self, out):
		self.out = out
		self.page.gen(self)

	def write(self, text):
		self.out.write(text.encode('utf-8'))


class TextProvider(Provider):

	def __init__(self, text, mime = None):
		self.text = text
		if mime == None:
			self.mime = "text/plain"
		else:
			self.mime = mime

	def add_headers(self, handler):
		handler.send_header("Content-type", self.mime)

	def gen(self, out):
		out.write(self.text.encodre('utf-8'))

	

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
		self.urls = {}
		self.first = self.app.first()
		self.add_page(self.first)
		self.urls["/"] = PageProvider(self.first)

	def add_prefix(self, pref, prov):
		self.urls[pref] = prov

	def remove_prefix(self, pref):
		del self.urls[pref]

	def add_file(self, prefix, path, mime = None):
		self.urls[prefix] = FileProvider(path, mime)

	def add_page(self, page):
		self.pages[page.get_id()] = page
		page.manager = self
		self.urls["/page/" + page.get_id()] = PageProvider(page)

	def remove_page(self, page):
		page.manager = None
		del self.pages[page.get_id()]
		del self.urls["/page/" + page.get_id()]

	def gen_page(self, page, out):
		page.gen(out)

	def get_page(self, id):
		return self.pages[id]

	def get_dirs(self):
		return self.dirs

	def is_completed(self):
		return self.pages == {}

	def get(self, path):
		path = os.path.normpath(path)
		try:
			return self.urls[path]
		except KeyError:
			for dir in self.dirs:
				rpath = dir + path
				if os.path.exists(rpath):
					return FileProvider(rpath)
			return None

def check_quit(manager):
	time.sleep(.25)
	if manager.is_completed():
		os._exit(0)

class Handler(http.server.SimpleHTTPRequestHandler):

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
			threading.Thread(target=partial(check_quit, self.server.manager)).start()

	def do_GET(self):
		prov = self.server.manager.get(self.path)
		if prov == None:
			self.log_error("bad path: %s" % path)
			self.send_response(404)
			self.end_headers()
		else:
			self.send_response(200)
			prov.add_headers(self)
			self.end_headers()
			prov.gen(self.wfile)


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
	server = http.server.HTTPServer(("localhost", port), Handler)
	server.manager = manager
	if browser:
		threading.Thread(target=partial(open_browser, port)).start()
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	server.server_close()



