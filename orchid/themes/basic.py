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

"""Definition of basic theme."""

from orchid.base import Model, CONTEXT_HEADERBAR, CONTEXT_TOOLBAR, Theme, \
	CONTEXT_NONE
from orchid.image import AssetImage, Image

MESSAGES = {
	"warning": "basic/warning.svg",
	"error": "basic/error.svg",
	"info": "basic/info.svg"
}

BOOTSTRAP_ICONS = {

	# actions
	"about": "info-lg", #!
	"add": "plug-lg",
	"align-left": "text-left",
	"align-right": "text-right",
	"center": "text-center",
	"chat": "chat-dots",
	"check": "check",
	"check-all": "check-all",
	"configure": "tools",
	"context-menu": "three-dots-vertical",
	"cut": "scissors",
	"debug": "bug-fill",
	"download": "cloud-download",
	"eject": "eject-fill",
	"enter": "box-arrow-in-right",
	"erase": "eraser-fill",
	"fast-forward": "fast-forward-fill",
	"go-back": "back",
	"go-forward": "forward-fill",
	"go-front": "front",
	"go-home": "house-fill",
	"indent": "text-indentleft",
	"justify": "justify",
	"leave": "box-arrow-right",
	"menu": "list",
	"paint": "brush-fill",
	"pause": "pause-fill",
	"pick": "eyedropper",
	"pin": "pin-angle-fill",
	"play": "play-fill",
	"print": "printer-fill",
	"process": "gear",
	"protect": "shield-fill-check",
	"quit": "power",
	"record": "record-fill",
	"remove": "x-lg",
	"repeat": "repeat",
	"reply": "reply-fill",
	"reset": "bootstrap-reboot",	#!
	"rewind": "rewind-fill",
	"search": "search",
	"send": "send",
	"show": "eye",
	"shuffle": "shuffle",
	"skip-backward": "skip-backward-fill",
	"skip-end": "skip-end-fill",
	"skip-forward": "skip-forward-fill",
	"skip-start": "skip-start-fill",
	"sort-alpha-down": "sort-alpha-down",
	"sort-alpha-up": "sort-alpha-up",
	"stop": "stop-fill",
	"unindent": "text-indent-right",
	"uplodad": "cloud-upload",
	"work": "hammer",
	"zoom-in": "zoom-in",
	"zoom-out": "zoom-out",

	# decorators
	"add-decorator": "plus-circle-fill",
	"remove-decorator": "x-circle-fill",

	# symbols
	"angry": "emoji-angry",
	"female": "geneder-female",	#!
	"happy": "emoji-smile",
	"help": "life-preserver",
	"info": "info-circle-fill",
	"layers": "layers",		# !
	"male": "gender-male",		# !
	"neutral": "emoji-neutral",
	"question": "question-circle-fill",
	"quote": "quote",
	"warning": "exclamation-triangle-fill",

	# keys
	"arrow-down": "caret-down-fill",
	"arrow-left": "caret-left-fill",
	"arrow-right": "caret-right-fill",
	"arrow-up": "caret-up-fill",
	"backspace": "backspace-fill",
	"braces": "braces",
	"shift": "shift-fill",

	# objects
	"alarm": "bell-fill",
	"bookmark": "bookmark-fill",
	"bookmarks": "bookmarks-fill",
	"box": "box2-fill",
	"calendar": "calendar",
	"camera": "camera-reels-fill",
	"clock": "clock",
	"doc": "book-fill",
	"drop": "droplet-fill",
	"event": "calendar-event",
	"fire": "fire",				# !
	"flag": "flag-fill",
	"flower": "flower1",		# !
	"fullscreen": "fullscreen",
	"graph": "diagram-3-fill",
	"hourglass": "hourglass-split",	# !
	"idea": "lighbulb",
	"image": "image",
	"key": "key",
	"lock": "lock-fill",
	"magic": "magic",	#!
	"map": "map",
	"message": "envelope",
	"money": "cash-coin",
	"music": "music-note-beamed",
	"people": "people-fill",
	"palette": "palette",	 	#!
	"paperclip": "paperclip",	#!
	"pencil": "pencil", #!
	"person": "person-fill",
	"piece": "puzzle",
	"plug": "plug",		#!
	"point": "geo-alt-fill",
	"stack": "stack",	#!
	"star-empty": "star",
	"star-full": "star-fill",
	"stats": "bar_char_line-fill",
	"stopwatch": "stopwatch",
	"tag": "tag",
	"target": "bullseye",	#++
	"thrashcan": "thrash",
	"todo": "clipboard-check",
	"wall": "bricks",
	"virus": "virus",	#!

	# technology
	"code": "code",		#!
	"cpu": "cpu",		#!
	"database": "database",
	"desktop": "pc-display",	#!
	"ethernet": "ethernet",
	"file": "file-earmark",
	"folder": "folder",
	"harddisk": "device-hdd",
	"headphones": "headphones",
	"keyboard": "keyboard",
	"laptop": "laptop",	#!
	"link": "link", #!
	"micro": "mic",
	"mouse": "mouse-fill",
	"printer": "printer-fill",
	"screen": "display",
	"terminal": "terminal",
	"usbkey": "device-ssd",
	"wifi": "wifi",
	"window": "window"
}

ICONS = BOOTSTRAP_ICONS

ICON_MODEL = Model("basic.icon-model")

class Icon(Image):
	"""An image using standard icons as defined in the documentation.
	If the icon name starts with "!", the named is looked in the
	current icon collection (https://icons.getbootstrap.com/)."""

	CONTEXT = {
		CONTEXT_HEADERBAR: " headerbar-icon",
		CONTEXT_TOOLBAR: " toolbar-icon",
	}

	def __init__(self, name, color = None):
		Image.__init__(self, ICON_MODEL)
		self.name = name
		self.color = color

	def gen(self, out):
		self.gen_in_context(out, CONTEXT_NONE)

	def gen_in_context(self, out, context):
		if self.name.startswith("!"):
			icon = self.name[1:]
		else:
			try:
				icon = ICONS[self.name]
			except KeyError:
				icon = ICONS["image"]
		out.write(f'<i class="bi bi-{icon}')
		try:
			out.write(Icon.CONTEXT[context])
		except KeyError:
			pass
		out.write('"')
		if self.color is not None:
			out.write(f' style="color: {self.color}"')
		out.write('"></i>')


class BasicTheme(Theme):

	def __init__(self):
		Theme.__init__(self, "basic", style_paths=[
			"basic.css",
			"bootstrap-icons/bootstrap-icons.css"
		])

	def get_icon(self, name, color=None):
		return Icon(name, color)

	def get_dialog_icon(self, type, size=32):
		if type in MESSAGES:
			return AssetImage(MESSAGES[type], width=size)
		else:
			return None


def get():
	"""Get an instance of this theme."""
	return BasicTheme()
