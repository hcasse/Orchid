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

	def __init__(self, mime = None):
		self.mime = mime

	def add_headers(self, handler):
		"""Get MIME type for the content.
		None if there is no content."""
		if self.mime != None:
			handler.send_header("Content-type", self.mime)

	def gen(self, out):
		"""Generate the content on the given output."""
		pass


class FileProvider(Provider):

	def __init__(self, path, mime = None):
		if mime == None:
			mime = mimetypes.guess_type(path)[0]
		Provider.__init__(self, mime)
		self.path = path

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
		Provider.__init__(self, "text/html")
		self.page = page
	
	def gen(self, out):
		self.out = out
		self.page.gen(self)

	def write(self, text):
		self.out.write(text.encode('utf-8'))


class TextProvider(Provider):

	def __init__(self, text, mime = "text/plain"):
		Provider.__init__(self, mime)
		self.text = text

	def gen(self, out):
		out.write(self.text.encode('utf-8'))

	

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
		self.first = self.app.first()
		self.paths = {}
		self.paths["/"] = self.add_page(self.first)

	def add_path(self, path, prov):
		self.paths[path] = prov

	def remove_path(self, path):
		del self.paths[path]

	def add_file(self, upath, rpath, mime = None):
		prov = FileProvider(rpath, mime)
		self.paths[upath] = prov
		return prov

	def add_text(self, path, text, mime = "text/plain"):
		prov = TextProvider(text, mime)
		self.paths[path] = prov
		return prov

	def page_path(self, page):
		return "/page/" + page.get_id()

	def add_page(self, page):
		self.pages[page.get_id()] = page
		page.manager = self
		prov = PageProvider(page)
		self.paths[self.page_path(page)] = prov
		return prov

	def remove_page(self, page):
		page.manager = None
		del self.pages[page.get_id()]
		del self.paths[self.page_path(page)]

	def get_page(self, id):
		return self.pages[id]

	def get_dirs(self):
		return self.dirs

	def is_completed(self):
		return self.pages == {}

	def get(self, path):
		path = os.path.normpath(path)
		try:
			return self.paths[path]
		except KeyError:
			for dir in self.dirs:
				rpath = dir + path
				if os.path.exists(rpath):
					prov = FileProvider(rpath)
					self.paths[path] = prov
					return prov
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
			self.log_error("bad path: %s" % self.path)
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



