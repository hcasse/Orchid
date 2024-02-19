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
	"""Interface of objects providing content. Each provider is
	associated with one or zero paths on the server."""

	def __init__(self, mime = None):
		self.mime = mime

	def add_headers(self, handler):
		"""Called to let the provider to add headers on the given
		HTTPHandler."""
		if self.mime != None:
			handler.send_header("Content-type", self.mime)

	def gen(self, out):
		"""Called to  generate the content to the given output."""
		pass


class FileProvider(Provider):
	"""Provider provding a file from the file system."""

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
	"""Provider generating an HTML page."""

	def __init__(self, page):
		Provider.__init__(self, "text/html")
		self.page = page
	
	def gen(self, out):
		self.out = out
		self.page.gen(self)

	def write(self, text):
		self.out.write(text.encode('utf-8'))


class AppProvider(Provider):
	"""Provided for an application generating a new session and its
	index page."""

	def __init__(self, app, man):
		Provider.__init__(self, "text/html")
		self.app = app
		self.man = man

	def gen(self, out):
		self.out = out
		session = self.app.new_session(self.man)
		page = session.get_index()
		session.add_page(page)
		self.man.record_page(page, PageProvider(page))
		page.gen(self)

	def write(self, text):
		self.out.write(text.encode('utf-8'))
	

class TextProvider(Provider):
	"""Provider providing plain text message."""

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
	"""Orchid server manager."""

	def __init__(self, app, config):
		self.app = app
		self.config = config
		self.dirs = config['dirs']
		self.pages = {}
		self.paths = {}
		self.paths["/"] = self.add_app(app)
		self.sessions = []
		self.check_time = self.config['session_check_time']

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

	def record_page(self, page, prov):
		self.pages[page.get_id()] = page
		page.manager = self
		self.paths[self.page_path(page)] = prov

	def add_page(self, page):
		prov = PageProvider(page)
		self.record_page(page, prov)
		return prov

	def add_app(self, app):
		prov = AppProvider(app, self)
		self.paths["/app/%s" % app.name] = prov
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
		if self.config['server']:
			return False
		else:
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

	def check_connections(self):
		while True:
			time.sleep(self.check_time)
			for session in self.sessions:
				sessions.check()

def check_quit(manager):
	time.sleep(.25)
	if manager.is_completed():
		os._exit(0)

class Handler(http.server.SimpleHTTPRequestHandler):

	def write(self, text):
		self.wfile.write(bytes(text, "utf-8"))

	def do_POST(self):
		debug = self.server.manager.config['debug']
		length = int(self.headers['content-length'])
		data = self.rfile.read(length)
		msg = json.loads(data)
		if debug:
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
		if debug:
			print("DEBUG: answer ", s)
		self.wfile.write(s.encode("utf-8"))
		if self.server.manager.is_completed():
			threading.Thread(target=partial(check_quit, self.server.manager)).start()

	def do_GET(self):
		debug = self.server.manager.config['debug']
		prov = self.server.manager.get(self.path)
		if prov == None:
			self.log_error("bad path: %s" % self.path)
			self.send_response(404)
			self.end_headers()
			if debug:
				print("DEBUG: request processed!")
		else:
			self.send_response(200)
			prov.add_headers(self)
			self.end_headers()
			prov.gen(self.wfile)
			if debug:
				print("DEBUG: request processed!")


def open_browser(host, port):
	time.sleep(.5)
	webbrowser.open("http://%s:%d" % (host, port))

DEFAULT_CONFIG = {
	'host': 'localhost',
	'port': 4444,
	'dirs': [],
	'browser': True,
	'server': False,
	'session_timeout': 120 * 60,
	'session_check_time': 10 * 60,
	'debug': False
}

def run(app, **args):
	"""Run the UI with the following configuration items:
	* debug -- run in debugging mode,
	* host -- name of the host,
	* port -- port to use,
	* dirs -- list of directories to get files,
	* browser -- if true, open the index page in a browser,
	* server -- if true, run as a server (no stop on last page close),
	* session_timeout -- time-out (in s) of a session,
	* session_check_time -- time (in s) to check for end of a session.

	Any other application parameter can also be passed this way.
"""

	# build the configuration
	config = dict(DEFAULT_CONFIG)
	for k in args:
		config[k] = args[k]

	# build the manager
	my_assets = os.path.realpath(os.path.join(os.path.dirname(__file__), "../assets"))
	config = dict(config)
	config["dirs"] = config["dirs"] + [my_assets]
	manager = Manager(app, config)
	app.configure(config)

	# build the server
	server = http.server.HTTPServer((config['host'], config['port']), Handler)
	server.manager = manager
	print("Server on %s:%d" % (config['host'], config['port']))

	# launch browser if required
	if config['browser']:
		threading.Thread(target=
			partial(open_browser, config['host'], config['port'])) \
			.start()

	# launch supervisor
	if config['server']:
		manager.super = threading.Thread(
			target=manager.check_connections,
			name = "supervisor",
			daemon = True)
		manager.super.start()

	# launch the server
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	server.server_close()
