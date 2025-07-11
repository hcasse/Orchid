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

"""Classes in charge of HTTP communication."""

from functools import partial
import http.server
import json
import mimetypes
import os.path
import re
import threading
import time
from urllib.parse import urlparse
import webbrowser

class Provider:
	"""Interface of objects providing content. Each provider is
	associated with one or zero paths on the server."""

	def __init__(self, mime = None):
		self.mime = mime

	def add_headers(self, handler):
		"""Called to let the provider to add headers on the given
		HTTPHandler."""
		if self.mime is not None:
			handler.send_header("Content-type", self.mime)

	def gen(self, out):
		"""Called to  generate the content to the given output."""
		pass


class FileProvider(Provider):
	"""Provider providing a file from the file system."""

	def __init__(self, path, mime = None):
		if mime is None:
			mime = mimetypes.guess_type(path)[0]
		Provider.__init__(self, mime)
		self.path = path

	def gen(self, out):

		# send text file
		if self.mime in TEXT_MIMES:
			with open(self.path, encoding="utf-8") as file:
				for l in file:
					out.write(bytes(l, "utf-8"))

		# send binary file
		else:
			with open(self.path, "rb") as file:
				while True:
					b = file.read(4096)
					if b == b'':
						break
					else:
						out.write(b)

		# success
		return 200


class PageProvider(Provider):
	"""Provider generating an HTML page."""

	def __init__(self, page):
		Provider.__init__(self, "text/html")
		self.page = page
		self.out = None

	def gen(self, out):
		self.out = out
		self.page.gen(self)
		self.out = None

	def write(self, text):
		self.out.write(text.encode('utf-8'))


class AppProvider(Provider):
	"""Provided for an application generating a new session and its
	index page."""

	def __init__(self, app, man):
		Provider.__init__(self, "text/html")
		self.app = app
		self.man = man
		self.out = None

	def gen(self, out):
		self.out = out
		session = self.app.new_session(self.man)
		page = session.get_index()
		session.add_page(page)
		self.man.record_page(page, PageProvider(page))
		page.gen(self)
		self.out = None

	def write(self, text):
		self.out.write(text.encode('utf-8'))


class TextProvider(Provider):
	"""Provider providing plain text message."""

	def __init__(self, text, mime = "text/plain"):
		Provider.__init__(self, mime)
		self.text = text

	def gen(self, out):
		out.write(self.text.encode('utf-8'))



GEN_RE = re.compile(r"^\s+<\?\s+(\S+)\s+\?>\s+$")

TEXT_MIMES = {
	"application/javascript",
	"text/css",
	"text/csv",
	"text/html",
	"text/javascript",
	"text/plain",
	"text/xml"
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
		self.check_thread = None
		self.is_server = config['server']
		self.super = None
		self.prefix = urlparse(config['proxy']).path

	def add_path(self, path, prov):
		"""Add a path with the given provider. May override an existing one."""
		self.paths[path] = prov

	def remove_path(self, path):
		"""Remove aprovided path."""
		del self.paths[path]

	def add_file(self, upath, rpath, mime = None):
		"""Add a provided file (at upath) served as web rpath with the passed
		MIME type."""
		prov = FileProvider(rpath, mime)
		self.paths[upath] = prov
		return prov

	def add_text_file(self, path, text, mime = "text/plain"):
		"""Server at URL path as the text as is with passed MIME."""
		prov = TextProvider(text, mime)
		self.paths[path] = prov
		return prov

	def add_provider(self, path, prov):
		"""Add a provided at the passed path."""
		self.paths[path] = prov
		return prov

	def page_path(self, page):
		"""Build the name of page as it will be served by the server."""
		return "/page/" + page.get_id()

	def record_page(self, page, prov):
		"""Record a served page with the passed provided."""
		self.pages[page.get_id()] = page
		page.manager = self
		self.paths[self.page_path(page)] = prov

	def add_page(self, page):
		"""Add a page to be served."""
		prov = PageProvider(page)
		self.record_page(page, prov)
		return prov

	def add_app(self, app):
		"""Add a an application to be served basically with its index page."""
		prov = AppProvider(app, self)
		self.paths[f"/app/{app.name}"] = prov
		return prov

	def remove_page(self, page):
		"""Remove a served page."""
		page.manager = None
		del self.pages[page.get_id()]
		del self.paths[self.page_path(page)]

	def get_page(self, id):
		"""Get the page the provided ID."""
		return self.pages[id]

	def get_dirs(self):
		"""Get the list of directories looked to find a static file."""
		return self.dirs

	def is_completed(self):
		"""Test if the server task is completed (no server option and no more
		page to serve)."""
		if self.config['server']:
			return False
		else:
			return not self.pages

	def get(self, path):
		"""Get the provider matching the page. Return None if no provider
		can be found."""
		path = os.path.normpath(path)[len(self.prefix):]
		if path == '':
			path = '/'
		try:
			return self.paths[path]
		except KeyError:
			for dir in self.dirs:
				rpath = dir + path
				if os.path.exists(rpath):
					prov = FileProvider(rpath)
					self.paths[path] = prov
					if self.config['debug']:
						print(f"DEBUG: {path} resolved to {rpath}!")
					return prov
			return None

	def add_session(self, session):
		"""Add a session to the server manager."""
		self.sessions.append(session)

	def remove_session(self, session):
		"""Remove a session from the server manager."""
		self.sessions.remove(session)
		if not self.sessions and not self.is_server:
			os._exit(0)

	def check_connections(self):
		"""Check which session connections needs to be released."""
		while True:
			time.sleep(self.check_time)
			for session in self.sessions:
				session.check()


class Handler(http.server.SimpleHTTPRequestHandler):
	"""Handler for a connection."""

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
			self.log_error(f"malformed message: {msg}")
			return
		answers = page.receive(msg["messages"], self)
		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.end_headers()
		s = json.dumps({"status": "ok", "answers": answers})
		if debug:
			print("DEBUG: answer ", s)
		self.wfile.write(s.encode("utf-8"))

	def do_GET(self):
		debug = self.server.manager.config['debug']
		prov = self.server.manager.get(self.path)
		if prov is None:
			self.log_error(f"bad path: {self.path.replace('%', '%%')}")
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

	def log_message(self, format, *args):
		debug = self.server.manager.config['debug']
		if debug:
			http.server.SimpleHTTPRequestHandler.log_message(self, format, *args)


def open_browser(host, port):
	time.sleep(.5)
	webbrowser.open(f"http://{host}:{port}")

DEFAULT_CONFIG = {
	'host': '0.0.0.0', #'localhost',
	'port': 0,
	'dirs': [],
	'browser': True,
	'server': False,
	'session_timeout': 120 * 60,
	'session_check_time': 10 * 60,
	'debug': False,
	'proxy': None
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
	* session_check_time -- time (in s) to check for end of a session,
	* proxy: when Orchid is behind a proxy, the address in the proxy.

	If behind a reverse-proxy (like generic HTTP server), the proxy address is
	used to let Javascript pass message to this address. The link inside inside
	generated HTML will be relative to this path.

	Any other application parameter can also be passed this way.
"""

	# build the configuration
	config = dict(DEFAULT_CONFIG)
	for (k, x) in args.items():
		config[k] = x
	if config["proxy"] is None:
		config["proxy"] = f"http://{config['host']}:{config['port']}"

	# build the manager
	my_assets = os.path.realpath(os.path.join(os.path.dirname(__file__), "../assets"))
	config = dict(config)
	config["dirs"] = config["dirs"] + [my_assets]
	manager = Manager(app, config)
	app.manager = manager
	app.configure(config)

	# build the server
	server = http.server.HTTPServer((config['host'], config['port']), Handler)
	server.manager = manager
	sname = server.socket.getsockname()
	if config['server']:
		print(f"Server on {sname[0]}:{sname[1]}")

	# launch browser if required
	if config['browser']:
		threading.Thread(target=partial(open_browser, sname[0], sname[1])) \
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
